from flask import Flask, request, jsonify
import requests
from weather_client import get_weather_data
from openai_client import get_recommendation  
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

#USER_SERVICE_URL = "http://user:5004/user"
#ACTIVITY_LOG_URL = "http://activitylog:5001/activity"

USER_SERVICE_URL = "http://localhost:5004/user"
ACTIVITY_LOG_URL = "http://localhost:5001/activity"

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

    # --- Hard coded Activity Log lol ---
    activity_log = [
        {"exerciseType": "yoga", "duration": 30, "intensity": "low", "caloriesBurned": 120},
        {"exerciseType": "walk", "duration": 20, "intensity": "low", "caloriesBurned": 90}
    ]

    # 1. Fetch weather
    weather = get_weather_data(location)

    # 2. Fetch user profile
   # user_resp = requests.get(f"{USER_SERVICE_URL}/{user_id}")
    #user_data = user_resp.json()

    # 3. Fetch activity log
    #activity_resp = requests.get(f"{ACTIVITY_LOG_URL}/{user_id}")
    #activity_log = activity_resp.json()
   

    # 4. Generate recommendation using Groq via openai_client
    advice = get_recommendation(user_data, activity_log, weather)

    return jsonify({
        "recommendation": advice,
        "weather": weather
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
