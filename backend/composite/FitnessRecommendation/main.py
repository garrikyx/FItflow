from flask import Flask, request, jsonify
import requests
from weather_client import get_weather_data
from openai_client import get_recommendation  
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

USER_SERVICE_URL = "http://user-service:5000/user"
ACTIVITY_LOG_URL = "http://activitylog-service:5030/activity"


def compute_average_intensity(activities):
    intensity_scale = {"low": 1, "medium": 2, "high": 3}
    total = sum(intensity_scale.get(a.get("intensity", "").lower(), 1) for a in activities)
    return round(total / len(activities), 2) if activities else 0
@app.route('/recommendation', methods=['GET'])

def recommend():
    user_id = request.args.get('userId')
    location = request.args.get('location', 'Singapore')

    # --- hardcoded User LOL---
    user_data = {
        "id": user_id,
        "name": "Jane Doe",
        "preferences": ["Lose Weight"]
    }


    # 1. Fetch weather
    weather = get_weather_data(location)

    # 2. Fetch user profile
   # user_resp = requests.get(f"{USER_SERVICE_URL}/{user_id}")
    #user_data = user_resp.json()

    # 3. Fetch activity log
    #activity_resp = requests.get(f"{ACTIVITY_LOG_URL}/{user_id}")
    #activity_log = activity_resp.json()
    try:
        activity_resp = requests.get(f"{ACTIVITY_LOG_URL}/{user_id}")
        activity_resp.raise_for_status()
        activity_log = activity_resp.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch activity log: {str(e)}"}), 500
    
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    recent_activities = [
        a for a in activity_log
        if datetime.fromisoformat(a['timestamp']) > one_week_ago
    ]

    summary_stats = {
        "total_sessions": len(recent_activities),
        "total_minutes": sum(a['duration'] for a in recent_activities),
        "avg_intensity": compute_average_intensity(recent_activities)
    }
   

    # 4. Generate recommendation using Groq via openai_client
    advice = get_recommendation(user_data, activity_log, weather,summary_stats)

    return jsonify({
        "recommendation": advice,
        "weather": weather
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
