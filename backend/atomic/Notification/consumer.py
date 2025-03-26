import pika
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail SMTP configuration
GMAIL_SMTP_SERVER = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587
GMAIL_USER = "ecosmart.diet@gmail.com"  # Replace with your Gmail address
GMAIL_PASSWORD = "hyhv ytts xosm fsij"   # Replace with your Gmail app password

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='notifications')

def send_email_via_gmail(subject, body, recipient_email):
    """Function to send email using Gmail's SMTP server"""
    # Setup the MIME
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Send email via Gmail SMTP server
    try:
        with smtplib.SMTP(GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(GMAIL_USER, GMAIL_PASSWORD)  # Login to your Gmail account
            server.sendmail(GMAIL_USER, recipient_email, msg.as_string())  # Send email
            print(f"Email sent to {recipient_email} via Gmail")
    except Exception as e:
        print(f"Error sending email to {recipient_email}: {e}")

def callback(ch, method, properties, body):
    """Callback function to process messages from RabbitMQ"""
    message = json.loads(body)
    print(f"Received Message: {message}")

    # Handle Monthly Summary Message
    if message["type"] == "monthly_summary":
        print(f"Sending Monthly Summary Email: {message['content']}")
        # Send email to user (mocked with a hardcoded email for demo)
        subject = "Monthly Health Summary"
        body = message['content']
        recipient_email = "shihua.kwok.2023@scis.smu.edu.sg"  # Replace with actual user email
        send_email_via_gmail(subject, body, recipient_email)  # Send using Gmail

    # Handle Calorie Update Message
    elif message["type"] == "calorie_update":
        print(f"Notifying Friends: {message['friends_emails']}")
        print(f"Message: {message['message']}")
        # Send email to each friend (mocked with example email)
        subject = "Calorie Update Notification"
        body = message['message']
        for email in message["friends_emails"]:
            send_email_via_gmail(subject, body, email)  # Send using Gmail

# Start consuming messages from RabbitMQ
channel.basic_consume(queue='notifications', on_message_callback=callback, auto_ack=True)
print("Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
