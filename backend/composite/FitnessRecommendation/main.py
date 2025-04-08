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

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:5000/user")
ACTIVITY_LOG_URL = os.getenv("ACTIVITY_LOG_URL", "http://activitylog-service:5030/activity")


def compute_average_intensity(activities):
    intensity_scale = {"low": 1, "medium": 2, "high": 3}
    total = sum(intensity_scale.get(a.get("intensity", "").lower(), 1) for a in activities)
    return round(total / len(activities), 2) if activities else 0


def fetch_user_data(user_id):
    try:
        user_resp = requests.get(f"{USER_SERVICE_URL}/{user_id}")
        user_resp.raise_for_status()
        result = user_resp.json()
        user_info = result.get("data", {})  # ✅ get only the "data" dict

        return user_info  # ✅ this contains userId, name, goal, etc.
    except requests.exceptions.RequestException as e:
        # Fallback to hardcoded user if service is not available
        app.logger.warning(f"Failed to fetch user data: {str(e)}. Using fallback data.")
        return {
            "userId": user_id,
            "name": "Jane Doe",
            "goal": "lose",
            "weight": 70.0
        }


def fetch_activity_logs(user_id):
    try:
        activity_resp = requests.get(f"{ACTIVITY_LOG_URL}/{user_id}")
        activity_resp.raise_for_status()
        return activity_resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch activity log: {str(e)}")
        raise Exception(f"Failed to fetch activity log: {str(e)}")


def filter_recent_activities(activity_log, time_str=None):
    if time_str:
        try:
            target_time = datetime.fromisoformat(time_str)
        except ValueError:
            raise ValueError("Invalid time format. Use ISO format (e.g., 2023-04-15T14:30:00)")
        
        # Filter activities based on the provided time
        return [
            a for a in activity_log
            if abs((datetime.fromisoformat(a['timestamp']) - target_time).total_seconds()) < 86400  # Within 24 hours
        ]
    else:
        # Use default 7-day window
        one_week_ago = datetime.now() - timedelta(days=7)
        return [
            a for a in activity_log
            if datetime.fromisoformat(a['timestamp']) > one_week_ago
        ]


def calculate_summary_stats(activities):
    if activities:
        return {
            "total_sessions": len(activities),
            "total_minutes": sum(a['duration'] for a in activities),
            "avg_intensity": compute_average_intensity(activities)
        }
    else:
        return {
            "total_sessions": 0,
            "total_minutes": 0,
            "avg_intensity": 0
        }


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


@app.route('/recommendation', methods=['GET'])
def recommend():
    # Get parameters from request
    user_id = request.args.get('userId')
    location = request.args.get('location', 'Singapore')
    time_str = request.args.get('time')  # Optional time parameter
    
    if not user_id:
        return jsonify({"error": "userId is required"}), 400

    try:
        # 1. Fetch user data from user microservice
        user_data = fetch_user_data(user_id)


        # 2. Fetch weather data based on location
        weather = get_weather_data(location)
        if not weather:
            return jsonify({"error": f"Failed to fetch weather data for {location}"}), 500

        # 3. Fetch activity log data based on user id
        activity_log = fetch_activity_logs(user_id)
        
        # 4. Filter recent activities
        try:
            recent_activities = filter_recent_activities(activity_log, time_str)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        
        # 5. Calculate summary statistics
        summary_stats = calculate_summary_stats(recent_activities)
       
        # 6. Generate recommendation using Groq via openai_client
        advice = get_recommendation(user_data, activity_log, weather, summary_stats)

        # 7. Return the recommendation and weather data
        return jsonify({
            "user": user_data,
            "recommendation": advice,
            "weather": weather,
            "activitySummary": summary_stats
        })
    
    except Exception as e:
        app.logger.error(f"Error generating recommendation: {str(e)}")
        return jsonify({"error": f"Failed to generate recommendation: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050) 