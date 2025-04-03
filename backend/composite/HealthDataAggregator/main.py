import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

load_dotenv()

def monthly_report():
    message = Mail(from_email = 'ecosmart.diet@gmail.com',
                to_emails = 'zephanchin123@gmail.com',
                subject = 'Monthly Report Stats',
                plain_text_content = 'Ran for 30 mins and burnt 120 calories',
                html_content = '<strong>Ran for 30 mins and burnt 120 calories</strong>')
    try:
        sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(f"Email sent with status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == '__main__':
    # Start Scheduler
    scheduler = BackgroundScheduler(timezone=timezone("Asia/Singapore"))
    # trigger = CronTrigger(day=28, hour=0, minute=0)
    trigger = CronTrigger(second='*/10')  
    scheduler.add_job(monthly_report, trigger)
    print("Scheduler started...")
    scheduler.start()

    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
