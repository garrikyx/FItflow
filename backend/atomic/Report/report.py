from flask import Flask, request, jsonify
import pika
import json
import datetime
# from notif import publish_message

def get_monthly_data():
    # report = create_workout_report(user_data)

    # publish_message(report)  # Publish the message for RabbitMQ to consume and send the email
    
    body = "You ran 5km, spent 1 hour exercising, burnt 100 calories"
    return body