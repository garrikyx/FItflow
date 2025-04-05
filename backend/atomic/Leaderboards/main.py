from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import logging

from database import app, db, Leaderboards, add_activity
from cache import LeaderboardCache

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/leaderboard", methods=["POST"])
def record_activity():
    """Record a user's fitness activity and update leaderboards."""
    try:
        activity_data = request.get_json()
        
        user_id = activity_data.get("user_id")
        calories_burned = float(activity_data.get("calories_burned",0.00))
        activity_type = activity_data.get("activity_type", "run")
        friends = activity_data.get("friends", [])  
        
        # Use provided timestamp or current time
        if "timestamp" in activity_data and activity_data["timestamp"]:
            timestamp = datetime.fromisoformat(activity_data["timestamp"])
        else:
            timestamp = datetime.now()
        
        activity = add_activity(
            user_id=user_id, 
            calories_burned=calories_burned, 
            activity_type=activity_type, 
            timestamp=timestamp
        )
        
        # Update Redis weekly leaderboard
        LeaderboardCache.update_leaderboards(user_id, calories_burned, timestamp)
        
        # Update friends leaderboards with provided friends list
        LeaderboardCache.update_friends_leaderboard(user_id, friends)
        
        # Clean up any old data
        LeaderboardCache.clear_old_data()
        
        return jsonify({
            "code": 201,
            "message": "Activity recorded successfully",
            "data": activity.json()
        }), 201
    except Exception as e:
        logger.error(f"Error recording activity: {str(e)}")
        return jsonify({
            "code": 400,
            "message": f"Error recording activity: {str(e)}"
        }), 400

@app.route("/leaderboard/weekly")
def get_weekly_leaderboard():
    """Get the current week's leaderboard."""
    try:
        limit = int(request.args.get("limit", 10))
        offset = int(request.args.get("offset", 0))
        
        weekly_key = LeaderboardCache.get_weekly_leaderboard_key()
        leaderboard_data, total_users = LeaderboardCache.get_leaderboard(weekly_key, limit, offset)
        
        entries = []
        for rank, (user_id, calories) in enumerate(leaderboard_data, start=offset + 1):
            entries.append({
                "user_id": user_id,
                "calories_burned": float(calories),
                "rank": rank
            })
        
        today = datetime.now()
        week_number = today.isocalendar()[1]
        time_period = f"Week {week_number}, {today.year}"
        
        return jsonify({
            "code": 200,
            "data": {
                "entries": entries,
                "total_users": total_users,
                "time_period": time_period
            }
        })
    except Exception as e:
        logger.error(f"Error getting weekly leaderboard: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"Error getting weekly leaderboard: {str(e)}"
        }), 500

@app.route("/leaderboard/friends/<user_id>")
def get_friends_leaderboard(user_id):
    """Get leaderboard for a user and their friends."""
    try:
        limit = int(request.args.get("limit", 10))
        
        friends_key = LeaderboardCache.get_friends_leaderboard_key(user_id)
        leaderboard_data, total_users = LeaderboardCache.get_leaderboard(friends_key, limit, 0)
        
        entries = []
        for rank, (friend_id, calories) in enumerate(leaderboard_data, start=1):
            entries.append({
                "user_id": friend_id,
                "calories_burned": float(calories),
                "rank": rank
            })
        
        return jsonify({
            "code": 200,
            "data": {
                "entries": entries,
                "total_users": total_users
            }
        })
    except Exception as e:
        logger.error(f"Error getting friends leaderboard: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"Error getting friends leaderboard: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)