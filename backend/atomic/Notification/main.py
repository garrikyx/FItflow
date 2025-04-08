import pika
import json
from flask import Flask, request, jsonify, Response, stream_with_context
import threading
import queue
import logging
import signal
import sys
from datetime import datetime
import time
import os

app = Flask(__name__)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")

# In-memory store of connected clients and lock for thread safety
clients = []
clients_lock = threading.Lock()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# RabbitMQ Connection Setup
def get_rabbitmq_channel():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                heartbeat=600,
                blocked_connection_timeout=300
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue='notifications', durable=True)
        channel.queue_declare(queue='reports', durable=True)
        return channel
    except Exception as e:
        logger.error(f"Failed to connect to RabbitMQ: {str(e)}")
        raise

# Publish message to a specific queue
def publish_message(message, queue):
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            channel = get_rabbitmq_channel()
            channel.basic_publish(
                exchange='',
                routing_key=queue,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2)  
            )
            logger.info(f"[x] Sent to {queue}: {message}")
            return
        except Exception as e:
            logger.error(f"Failed to publish message (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise

# Health check
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "NotificationService"
    }), 200

# Notify Friends on Calorie Update
@app.route('/notification/notify_calories', methods=['POST'])
def notify_calories():
    data = request.json
    if not all(key in data for key in ("friends_user_ids", "message", "timestamp", "userId", "name")):
        return jsonify({"error": "Missing data fields"}), 400

    publish_message({
        "type": "calorie_update",
        "friends_user_ids": data["friends_user_ids"],
        "message": data["message"],
        "timestamp": data["timestamp"],
        "userId": data["userId"],
        "name": data["name"]
    }, queue="notifications")

    return jsonify({"status": "Notification sent to friends"}), 200

# Notify on Leaderboard Pass
@app.route('/notification/notify_leaderboard', methods=['POST'])
def notify_leaderboard():
    data = request.json
    if not all(key in data for key in ("friends_user_ids", "userId", "name", "message", "timestamp")):
        return jsonify({"error": "Missing data fields"}), 400

    publish_message({
        "type": "leaderboard_pass",
        "friends_user_ids": data["friends_user_ids"],
        "userId": data["userId"],
        "name": data["name"],
        "message": data["message"],
        "timestamp": data["timestamp"]
    }, queue="notifications")

    return jsonify({"status": "Leaderboard pass notification sent"}), 200

# SSE Endpoint for Real-Time Notifications
@app.route('/notification/events')
def sse_stream():
    q = queue.Queue()
    
    # Ensure thread-safe access to clients list
    with clients_lock:
        clients.append(q)

    def event_stream():
        try:
            while True:
                data = q.get()
                yield f"data: {json.dumps(data)}\n\n"
        except GeneratorExit:
            # Handle client disconnection
            with clients_lock:
                clients.remove(q)

    return Response(stream_with_context(event_stream()), mimetype='text/event-stream')

# RabbitMQ Consumer in background thread
def rabbitmq_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue='notifications', durable=True)

    def callback(ch, method, properties, body):
        message = json.loads(body)
        logger.info(f"Received message: {message}")
        
        # Send message to all clients
        with clients_lock:
            for client in clients:
                client.put(message)
        
        # Acknowledge message (if auto_ack is False)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='notifications', on_message_callback=callback, auto_ack=False)
    channel.start_consuming()

# Start RabbitMQ listener in background
def start_consumer_thread():
    threading.Thread(target=rabbitmq_consumer, daemon=True).start()

# Gracefully shutdown the app
def graceful_shutdown(signum, frame):
    logger.info("Gracefully shutting down...")
    sys.exit(0)

# Set up signal handler for graceful shutdown
signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)

if __name__ == "__main__":
    # Start the RabbitMQ consumer thread
    start_consumer_thread()
    
    # Run Flask app
    app.run(host="0.0.0.0", port=5010, threaded=True)
