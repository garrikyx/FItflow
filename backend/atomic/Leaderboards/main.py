from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import logging
import requests

from database import app, db, Activity, add_activity
from cache import LeaderboardCache

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/leaderboards")
def get_all_activities():
    """Retrieve all activities."""
    try:
        leaderboards = db.session.scalars(db.select(leaderboards)).all()
        
        if leaderboards:
            return jsonify({
                "code": 200,
                "data": {"leaderboards": [board.json() for board in leaderboards]}
            })
        
        return jsonify({
            "code": 404,
            "message": "No activities found."
        }), 404
    except Exception as e:
        logger.error(f"Error retrieving activities: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"Error retrieving activities: {str(e)}"
        }), 500

@app.route("/leaderboard", methods=["POST"])
def record_activity():
    """Record a user's fitness activity and update leaderboards."""
    try:
        activity_data = request.get_json()
        
        user_id = activity_data.get("user_id")
        calories_burned = float(activity_data.get("calories_burned"))
        activity_type = activity_data.get("activity_type", "unknown")
        
        # Use provided timestamp or current time
        if "timestamp" in activity_data and activity_data["timestamp"]:
            timestamp = datetime.fromisoformat(activity_data["timestamp"])
        else:
            timestamp = datetime.now()
        
        # Add to database
        activity = add_activity(
            user_id=user_id, 
            calories_burned=calories_burned, 
            activity_type=activity_type, 
            timestamp=timestamp
        )
        
        # Update Redis leaderboards
        LeaderboardCache.update_leaderboards(user_id, calories_burned, timestamp)
        
        # Update friends leaderboard in background
        LeaderboardCache.update_friends_leaderboard(user_id, calories_burned)
        
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


@app.route("/activity/<int:activity_id>")
def find_activity_by_id(activity_id):
    """Find a specific activity by its ID."""
    try:
        activity = db.session.scalar(db.select(Activity).filter_by(id=activity_id))
        
        if activity:
            return jsonify({
                "code": 200,
                "data": activity.json()
            })
        
        return jsonify({
            "code": 404,
            "message": "Activity not found."
        }), 404
    except Exception as e:
        logger.error(f"Error finding activity: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"Error finding activity: {str(e)}"
        }), 500

@app.route("/leaderboard/weekly")
def get_weekly_leaderboard():
    """Get the current week's leaderboard."""
    try:
        # Get query parameters with defaults
        limit = int(request.args.get("limit", 10))
        offset = int(request.args.get("offset", 0))
        
        # Get weekly leaderboard key
        weekly_key = LeaderboardCache.get_weekly_leaderboard_key()
        
        # Fetch leaderboard data
        leaderboard_data, total_users = LeaderboardCache.get_leaderboard(weekly_key, limit, offset)
        
        # Format the response
        entries = []
        for rank, (user_id, calories) in enumerate(leaderboard_data, start=offset + 1):
            # Get user from composite service
            user_info = LeaderboardCache.get_user_from_composite(user_id)
            
            entries.append({
                "user_id": user_id,
                "username": user_info.get('username', f"User-{user_id[:6]}"),
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

@app.route("/health")
def health_check():
    """Health check endpoint."""
    try:
        # Check database connection
        db.session.execute(db.select(Activity).limit(1))
        
        # Check Redis connection
        LeaderboardCache.get_weekly_leaderboard_key()
        
        
        return jsonify({"status": "healthy", "code": 200})
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "status": "unhealthy", 
            "code": 500,
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)