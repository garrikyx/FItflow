# notif.py sends health-related notifications (monthly summaries and calorie updates) to RabbitMQ and schedules tasks.
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Report')))

import monthly_report
from flask import Flask, request, jsonify
import pika
import json
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone


app = Flask(__name__)

# AMQP Connection Setup
def get_rabbitmq_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='notifications')
    return channel

# Function to publish messages
def publish_message(message):
    channel = get_rabbitmq_channel()
    channel.basic_publish(exchange='', routing_key='notifications', body=json.dumps(message))
    print(f"Sent: {message}")

# Scheduled Task: Send Monthly Summary
def send_monthly_summary():
        today = datetime.datetime.today()
    # if today.day == 28:  # Assuming 28th to be safe for all months
    ### FOR LOOP HERE for all the users in the database and connect to db for email?
        content = monthly_report.get_monthly_data()
        message = {
            "type": "monthly_summary",
            "content": content,
            "timestamp": today.isoformat(),
        }
        publish_message(message)

# Start Scheduler
scheduler = BackgroundScheduler(timezone=timezone("Asia/Singapore"))
# scheduler.add_job(send_monthly_summary, 'cron', day=28, hour=0, minute=0)
scheduler.add_job(send_monthly_summary, 'interval', seconds=5)
scheduler.start()

# API Endpoint: Notify Friends on Calorie Update
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
    })

    return jsonify({"status": "Notification sent"}), 200

if __name__ == '__main__':
    app.run(debug=True)
