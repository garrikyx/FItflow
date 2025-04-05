from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
import requests
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Service URLs - can be overridden with environment variables
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:5000")
ACTIVITY_LOG_SERVICE_URL = os.getenv("ACTIVITY_LOG_SERVICE_URL", "http://activitylog-service:5030")
LEADERBOARDS_SERVICE_URL = os.getenv("LEADERBOARDS_SERVICE_URL", "http://leaderboards-service:5005")
SOCIAL_SERVICE_URL = os.getenv("SOCIAL_SERVICE_URL", "https://personal-ywco1luc.outsystemscloud.com/SocialsService")

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "ActivityCoordination",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route("/activity", methods=["POST"])
def coordinate_activity():
    """
    Coordinate activity logging across multiple services.
    1. Get user profile from user service
    2. Log activity in activity log service
    3. Get friends from social service
    4. Update leaderboards for user and friends
    """
    try:
        # Get request data
        data = request.get_json()
        logger.debug(f"Received activity data: {data}")
        
        # Validate required fields
        required_fields = ["userId", "duration", "activityType"]
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "code": 400,
                    "message": f"Missing required field: {field}"
                }), 400
        
        user_id = data.get("userId")
        duration = data.get("duration")
        activity_type = data.get("activityType")
        
        # 1. Get user profile from user service
        logger.debug(f"Fetching user profile for user ID: {user_id}")
        user_response = requests.get(f"{USER_SERVICE_URL}/user/{user_id}")
        
        if user_response.status_code != 200:
            logger.error(f"Failed to get user profile: {user_response.text}")
            return jsonify({
                "code": user_response.status_code,
                "message": f"Failed to get user profile: {user_response.text}"
            }), user_response.status_code
        
        user_data = user_response.json().get("data", {})
        logger.debug(f"Retrieved user data: {user_data}")
        
        # Calculate calories burned based on weight, activity type, and duration
        weight = user_data.get("weight", 70)  # Default to 70kg if not provided
        calories_burned = calculate_calories_burned(weight, activity_type, duration)
        
        # Calculate intensity based on duration and activity type
        intensity = calculate_intensity(duration, activity_type)
        
        # 2. Log activity in activity log service
        logger.debug("Logging activity to activity log service")
        activity_log_data = {
            "userId": user_id,
            "exerciseType": activity_type,
            "duration": duration,
            "intensity": intensity,
            "caloriesBurned": calories_burned
        }
        
        activity_response = requests.post(
            f"{ACTIVITY_LOG_SERVICE_URL}/activity",
            json=activity_log_data
        )
        
        if activity_response.status_code not in [200, 201]:
            logger.error(f"Failed to log activity: {activity_response.text}")
            return jsonify({
                "code": activity_response.status_code,
                "message": f"Failed to log activity: {activity_response.text}"
            }), activity_response.status_code
        
        logger.debug(f"Activity logged successfully: {activity_response.json()}")
        
        # 3. Get friends from social service
        logger.debug(f"Fetching friends for user ID: {user_id}")
        friends_response = requests.get(f"{SOCIAL_SERVICE_URL}/rest/FriendAPI/Friends/{user_id}")
        
        if friends_response.status_code != 200:
            logger.warning(f"Failed to get friends: {friends_response.text}")
            friends = []
        else:
            friends_data = friends_response.json()
            friends = [friend.get("Id") for friend in friends_data]
            logger.debug(f"Retrieved {len(friends)} friends: {friends}")
        
        # 4. Update leaderboards for user and friends
        logger.debug("Updating leaderboards")
        leaderboard_data = {
            "user_id": user_id,
            "calories_burned": calories_burned,
            "activity_type": activity_type,
            "timestamp": datetime.now().isoformat()
        }
        
        leaderboard_response = requests.post(
            f"{LEADERBOARDS_SERVICE_URL}/leaderboard",
            json=leaderboard_data
        )
        
        if leaderboard_response.status_code not in [200, 201]:
            logger.error(f"Failed to update leaderboards: {leaderboard_response.text}")
            return jsonify({
                "code": leaderboard_response.status_code,
                "message": f"Failed to update leaderboards: {leaderboard_response.text}"
            }), leaderboard_response.status_code
        
        logger.debug(f"Leaderboards updated successfully: {leaderboard_response.json()}")
        
        # Return combined response
        return jsonify({
            "code": 200,
            "message": "Activity successfully coordinated",
            "data": {
                "user": user_data,
                "activity": activity_response.json(),
                "friends": friends,
                "leaderboard": leaderboard_response.json().get("data", {})
            }
        }), 200
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"Service communication error: {str(e)}"
        }), 500
    except Exception as e:
        logger.error(f"Error coordinating activity: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"Error coordinating activity: {str(e)}"
        }), 500

def calculate_calories_burned(weight, activity_type, duration):
    """
    Calculate calories burned based on weight, activity type, and duration.
    This is a simplified calculation and can be improved with more detailed algorithms.
    
    Args:
        weight (float): User's weight in kg
        activity_type (str): Type of activity (e.g., running, walking, cycling)
        duration (int): Duration of activity in minutes
        
    Returns:
        int: Estimated calories burned
    """
    # MET (Metabolic Equivalent of Task) values for different activities
    met_values = {
        "running": 9.8,
        "walking": 3.5,
        "cycling": 7.5,
        "swimming": 8.3,
        "hiking": 5.3,
        "yoga": 2.5,
        "weightlifting": 3.5,
        "dancing": 4.8,
        "basketball": 6.5,
        "soccer": 7.0,
        "tennis": 7.3
    }
    
    # Default to moderate activity if not recognized
    met = met_values.get(activity_type.lower(), 5.0)
    
    # Formula: calories = MET * weight (kg) * duration (hours)
    # Convert duration from minutes to hours
    duration_hours = duration / 60.0
    
    calories = met * weight * duration_hours
    
    return int(calories)

def calculate_intensity(duration, activity_type):
    """
    Calculate intensity based on duration and activity type.
    
    Args:
        duration (int): Duration of activity in minutes
        activity_type (str): Type of activity
        
    Returns:
        str: Intensity level (low, medium, high)
    """
    # High-intensity activities
    high_intensity = ["running", "swimming", "basketball", "soccer", "tennis"]
    
    # Medium-intensity activities
    medium_intensity = ["cycling", "hiking", "dancing", "weightlifting"]
    
    # Low-intensity activities
    low_intensity = ["walking", "yoga"]
    
    activity_type_lower = activity_type.lower()
    
    # Base intensity on activity type first
    if activity_type_lower in high_intensity:
        base_intensity = "high"
    elif activity_type_lower in medium_intensity:
        base_intensity = "medium"
    elif activity_type_lower in low_intensity:
        base_intensity = "low"
    else:
        base_intensity = "medium"  # Default
    
    # Adjust based on duration
    if duration < 15:
        intensity_adjustment = -1  # Lower intensity for short durations
    elif duration > 45:
        intensity_adjustment = 1  # Higher intensity for long durations
    else:
        intensity_adjustment = 0  # No adjustment for medium durations
    
    # Map base intensity to numeric value
    intensity_map = {"low": 1, "medium": 2, "high": 3}
    numeric_intensity = intensity_map[base_intensity] + intensity_adjustment
    
    # Convert back to string intensity, ensuring it's within bounds
    numeric_intensity = max(1, min(3, numeric_intensity))
    reverse_map = {1: "low", 2: "medium", 3: "high"}
    
    return reverse_map[numeric_intensity]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5051, debug=True)
