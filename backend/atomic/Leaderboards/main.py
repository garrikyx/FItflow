from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import logging
import requests

from database import app, db, Leaderboards, add_activity
from cache import LeaderboardCache

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/leaderboards")
def get_all_activities():
    """Retrieve all activities from the database."""
    try:
        leaderboards = db.session.scalars(db.select(Leaderboards)).all()
        
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
    """Record a user's fitness activity and update weekly leaderboard."""
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
        
        # Add to SQL database (persistent storage)
        activity = add_activity(
            user_id=user_id, 
            calories_burned=calories_burned, 
            activity_type=activity_type, 
            timestamp=timestamp
        )
        
        # Update Redis weekly leaderboard only
        LeaderboardCache.update_leaderboards(user_id, calories_burned, timestamp)
        
        # Update friends leaderboard
        LeaderboardCache.update_friends_leaderboard(user_id, calories_burned)
        
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

@app.route("/leaderboard/clean", methods=["POST"])
def clean_redis_data():
    """Clean up Redis data, keeping only current weekly leaderboards."""
    try:
        deleted_count = LeaderboardCache.clear_old_data()
        
        return jsonify({
            "code": 200,
            "message": f"Cleaned up Redis data, removed {deleted_count} old keys",
        })
    except Exception as e:
        logger.error(f"Error cleaning Redis data: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"Error cleaning Redis data: {str(e)}"
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
        db.session.execute(db.select(Leaderboards).limit(1))
        
        # Check Redis connection
        redis = LeaderboardCache.get_redis()
        redis.ping()
        redis.close()
        
        return jsonify({"status": "healthy", "code": 200})
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "status": "unhealthy", 
            "code": 500,
            "message": str(e)
        }), 500

@app.route("/leaderboard/friends/<user_id>")
def get_friends_leaderboard(user_id):
    """Get leaderboard for a user and their friends."""
    try:
        # Get limit parameter
        limit = int(request.args.get("limit", 10))
        
        # First, ensure the user's friends leaderboard is built
        LeaderboardCache.build_friends_leaderboard(user_id)
        
        # Get friends leaderboard key
        friends_key = LeaderboardCache.get_friends_leaderboard_key(user_id)
        
        # Get leaderboard data
        leaderboard_data, total_users = LeaderboardCache.get_leaderboard(friends_key, limit, 0)
        
        entries = []
        for rank, (friend_id, calories) in enumerate(leaderboard_data, start=1):
            # Get user info
            user_info = LeaderboardCache.get_user_from_composite(friend_id)
            
            entries.append({
                "user_id": friend_id,
                "username": user_info.get('username', f"User-{friend_id[:6]}"),
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

@app.route("/leaderboard/user/<user_id>")
def get_user_leaderboard_info(user_id):
    """Get a user's rank and position in the weekly leaderboard."""
    try:
        # Get weekly key
        weekly_key = LeaderboardCache.get_weekly_leaderboard_key()
        
        # Get user's rank in weekly leaderboard
        weekly_calories, weekly_rank, weekly_total = LeaderboardCache.get_user_rank(user_id, weekly_key)
        
        # Also check if they have a friends leaderboard
        friends_key = LeaderboardCache.get_friends_leaderboard_key(user_id)
        friends_calories, friends_rank, friends_total = LeaderboardCache.get_user_rank(user_id, friends_key)
        
        # Get user info
        user_info = LeaderboardCache.get_user_from_composite(user_id)
        
        return jsonify({
            "code": 200,
            "data": {
                "user_id": user_id,
                "username": user_info.get('username', f"User-{user_id[:6]}"),
                "weekly": {
                    "calories_burned": float(weekly_calories) if weekly_calories else 0,
                    "rank": weekly_rank if weekly_rank else "Not ranked",
                    "total_users": weekly_total
                },
                "friends": {
                    "calories_burned": float(friends_calories) if friends_calories else 0,
                    "rank": friends_rank if friends_rank else "Not ranked",
                    "total_users": friends_total
                }
            }
        })
    except Exception as e:
        logger.error(f"Error getting user leaderboard info: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"Error getting user leaderboard info: {str(e)}"
        }), 500

@app.route("/sync/weekly-leaderboard", methods=["POST"])
def sync_weekly_leaderboard():
    """Sync weekly leaderboard from database to Redis."""
    try:
        # Clear existing weekly leaderboard in Redis
        redis = LeaderboardCache.get_redis()
        weekly_key = LeaderboardCache.get_weekly_leaderboard_key()
        redis.delete(weekly_key)
        
        # Get week start date
        today = datetime.now()
        # Calculate the start of the week (Monday)
        start_of_week = today.replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        days_since_monday = today.weekday()
        start_of_week = start_of_week - timedelta(days=days_since_monday)
        
        # Query database for this week's activities
        query = db.select(Leaderboards).where(Leaderboards.timestamp >= start_of_week)
        activities = db.session.scalars(query).all()
        
        # Group activities by user_id
        user_calories = {}
        for activity in activities:
            if activity.user_id not in user_calories:
                user_calories[activity.user_id] = 0
            user_calories[activity.user_id] += activity.calories_burned
        
        # Update Redis weekly leaderboard
        for user_id, calories in user_calories.items():
            redis.zadd(weekly_key, {user_id: calories})
        
        redis.expire(weekly_key, 60 * 60 * 24 * 21)  # 3 weeks
        redis.close()
        
        return jsonify({
            "code": 200,
            "message": f"Synced {len(user_calories)} users to weekly leaderboard",
            "data": {
                "users_synced": len(user_calories),
                "activities_processed": len(activities)
            }
        })
    except Exception as e:
        logger.error(f"Error syncing weekly leaderboard: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"Error syncing weekly leaderboard: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)