import os
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
import datetime
from flask import Flask
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:5000/user")
ACTIVITYLOG_SERVICE_URL = os.getenv("ACTIVITY_SERVICE_URL", "http://activitylog:5030/activity")

def monthly_report():
    try:
        # Step 1: Get all users
        users_resp = requests.get(USER_SERVICE_URL)
        users_data = users_resp.json().get("data", {}).get("users", [])

        for user in users_data:
            user_id = user["userId"]
            name = user["name"]
            email = user["email"]

            # Step 2: Get activity log for user
            activity_resp = requests.get(f"{ACTIVITYLOG_SERVICE_URL}/{user_id}")
            if activity_resp.status_code != 200:
                print(f"No activity data for user: {user_id}")
                continue

            activities = activity_resp.json()
            
            # filter activities from the past month
            now = datetime.datetime.now()
            one_month_ago = now - datetime.timedelta(days=30)
            recent_activities = [
                a for a in activities
                if datetime.datetime.fromisoformat(a["timestamp"]) > one_month_ago
            ]

            total_calories = sum(a["caloriesBurned"] for a in recent_activities)
            total_duration = sum(a["duration"] for a in recent_activities)

            # Step 3: Send email
    #         html_content = f"""
    #             <strong>Hello {name},</strong><br><br>
    #             Here's your activity report for the past month:<br>
    #             Total Duration: <b>{total_duration} minutes</b><br>
    #             Total Calories Burned: <b>{total_calories} kcal</b><br><br>
    #             Keep it up! 💪
    #         """
    #         message = Mail(
    #             from_email='ecosmart.diet@gmail.com',
    #             to_emails=email,
    #             subject='Your Monthly Activity Report 💡',
    #             plain_text_content=f"{name}, you exercised for {total_duration} minutes and burned {total_calories} calories this month!",
    #             html_content=html_content
    #         )

    #         sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
    #         response = sg.send(message)
    #         print(f"Email sent to {email} with status: {response.status_code}")

    # except Exception as e:
    #     print(f"Error in monthly report: {e}")


        # FOR TESTING OF 1 USER
        # Add a new user 
        # Step 1: Get test user details
        user_resp = requests.get(f"{USER_SERVICE_URL}/10")
        if user_resp.status_code != 200:
            print(f"Test user '5' not found.")
            return

        user = user_resp.json().get("data", {})
        name = user["name"]
        email = user["email"]

        # Step 2: Get activity log for test user
        activity_resp = requests.get(f"{ACTIVITYLOG_SERVICE_URL}/10")
        if activity_resp.status_code != 200:
            print(f"No activity data for user: 5")
            return

        activities = activity_resp.json()

        # Optional: filter for the last 30 days
        now = datetime.datetime.now()
        one_month_ago = now - datetime.timedelta(days=30)
        recent_activities = [
            a for a in activities
            if datetime.datetime.fromisoformat(a["timestamp"]) > one_month_ago
        ]

        total_calories = sum(a["caloriesBurned"] for a in recent_activities)
        total_duration = sum(a["duration"] for a in recent_activities)

        # Step 3: Send email
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .container {{
                    background-color: white;
                    border-radius: 10px;
                    padding: 30px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                .header {{
                    background-color: #2c3e50;
                    color: white;
                    text-align: center;
                    padding: 15px;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    margin-top: 20px;
                }}
                .stats {{
                    background-color: #ecf0f1;
                    border-radius: 8px;
                    padding: 20px;
                    text-align: center;
                    margin: 20px 0;
                }}
                .stats h2 {{
                    color: #2c3e50;
                    margin-bottom: 15px;
                }}
                .stats p {{
                    font-size: 18px;
                    color: #34495e;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    color: #7f8c8d;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Your Monthly Activity Report</h1>
                </div>
                
                <div class="content">
                    <p>Hello {name},</p>
                    
                    <div class="stats">
                        <h2>🏋️ Your Progress This Month 📊</h2>
                        <p>Total Workout Duration: <strong>{total_duration} minutes</strong></p>
                        <p>Calories Burned: <strong>{total_calories} kcal</strong></p>
                    </div>
                    
                    <p>You're making great strides towards your fitness goals! Every minute counts, and you should be proud of your consistency and effort.</p>
                </div>
                
                <div class="footer">
                    <p>Keep pushing forward! 💪 Your FitFlow Team</p>
                </div>
            </div>
        </body>
        </html>
        """
        message = Mail(
            from_email='ecosmart.diet@gmail.com',
            to_emails=email,
            subject='Your Monthly Activity Report 💡',
            plain_text_content=f"{name}, you worked out for {total_duration} minutes and burned {total_calories} calories!",
            html_content=html_content
        )

        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f"✅ Email sent to {email} with status: {response.status_code}")

    except Exception as e:
        print(f"❌ Error in monthly report: {e}")

@app.route('/test-report')
def test_report():
    monthly_report()
    return "Monthly report triggered!", 200
    
@app.route("/test-email")
def test_email():
    try:
        now = datetime.datetime.now()

        message = Mail(
            from_email='ecosmart.diet@gmail.com',
            to_emails='garrisonkoh.2023@scis.smu.edu.sg',
            subject='Test Email',
            plain_text_content=f"This is a test email, timestamp:{now}",
            html_content='<strong>This is a test email</strong>'
        )
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f"✅ Test email sent with status: {response.status_code}")
        return "Test email sent", 200
    except Exception as e:
        print(f"❌ Error sending test email: {e}")
        return f"Error: {e}", 500

@app.route('/health')
def health():
    return {"status": "healthy", "service": "HealthDataAggregator"}, 200

if __name__ == '__main__':
    scheduler = BackgroundScheduler(timezone=timezone("Asia/Singapore"))
    trigger = CronTrigger(day=1, hour=0, minute=0)  # Real monthly trigger
    # trigger = CronTrigger(minute='*/10')  # For testing every 10 minutes
    scheduler.add_job(monthly_report, trigger)
    print("Scheduler started...")
    scheduler.start()
    # try:
    #     while True:
    #         datetime.time.sleep(1)  
    # except (KeyboardInterrupt, SystemExit):
    #     scheduler.shutdown()
    
    app.run(host='0.0.0.0', port=5052)
