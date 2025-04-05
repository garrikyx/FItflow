import pika
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

RABBITMQ_HOST = "rabbitmq"

# AMQP Connection Setup
def get_rabbitmq_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    # Declare both queues
    channel.queue_declare(queue='notifications', durable=True)
    channel.queue_declare(queue='reports', durable=True)
    return channel

# Generic publisher
def publish_message(message, queue):
    channel = get_rabbitmq_channel()
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)  
    )
    print(f"[x] Sent to {queue}: {message}")

# Endpoint: Notify Friends on Calorie Update
@app.route('/notify_calories', methods=['POST'])
def notify_calories():
    data = request.json
    if not all(key in data for key in ("friends_emails", "message", "timestamp")):
        return jsonify({"error": "Missing data fields"}), 400

    publish_message({
        "type": "calorie_update",
        "friends_emails": data["friends_emails"],
        "message": data["message"],
        "timestamp": data["timestamp"]
    }, queue="notifications")

    return jsonify({"status": "Notification sent to friends"}), 200

# Endpoint: Monthly Report 
@app.route('/enqueue_report', methods=['POST'])
def enqueue_report():
    data = request.json
    if not all(k in data for k in ("email", "name", "userId", "duration", "calories")):
        return jsonify({"error": "Missing data fields"}), 400

    publish_message({
        "type": "monthly_report",
        "email": data["email"],
        "name": data["name"],
        "userId": data["userId"],
        "duration": data["duration"],
        "calories": data["calories"]
    }, queue="reports")

    return jsonify({"status": "Monthly report enqueued"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
