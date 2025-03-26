import os
import logging
from datetime import datetime
from redis import Redis
from typing import List, Dict, Optional, Tuple
import requests

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_redis():
    """Get Redis connection instance with configuration from environment variables."""
    redis_host = os.environ.get("REDIS_HOST", "localhost")
    redis_port = int(os.environ.get("REDIS_PORT", 6379))
    redis_password = os.environ.get("REDIS_PASSWORD", "")
    
    return Redis(
        host=redis_host,
        port=redis_port,
        password=redis_password,
        decode_responses=True
    )

class LeaderboardCache:
    """Redis-based cache for leaderboard operations using sorted sets."""
    
    @staticmethod
    def get_weekly_leaderboard_key():
        """Generate the Redis key for the current week's leaderboard."""
        today = datetime.now()
        week_number = today.isocalendar()[1]
        year = today.year
        return f"leaderboard:weekly:{year}:{week_number}"

    @staticmethod
    def get_monthly_leaderboard_key():
        """Generate the Redis key for the current month's leaderboard."""
        today = datetime.now()
        return f"leaderboard:monthly:{today.year}:{today.month}"

    @staticmethod
    def get_friends_leaderboard_key(user_id: str):
        """Generate the Redis key for a user's friends leaderboard."""
        today = datetime.now()
        week_number = today.isocalendar()[1]
        year = today.year
        return f"leaderboard:friends:{user_id}:{year}:{week_number}"

    @staticmethod
    def update_leaderboards(user_id: str, calories_burned: float, timestamp: Optional[datetime] = None):
        """Update weekly and monthly leaderboards with new activity data."""
        redis = get_redis()
        try:
            if not timestamp:
                timestamp = datetime.now()
            
            # Update weekly leaderboard
            weekly_key = LeaderboardCache.get_weekly_leaderboard_key()
            redis.zincrby(weekly_key, calories_burned, user_id)
            redis.expire(weekly_key, 60 * 60 * 24 * 21)  # 3 weeks
            
            # Update monthly leaderboard
            monthly_key = LeaderboardCache.get_monthly_leaderboard_key()
            redis.zincrby(monthly_key, calories_burned, user_id)
            redis.expire(monthly_key, 60 * 60 * 24 * 90)  # 90 days
            
            # Store activity in activity log
            activity_id = f"activity:{user_id}:{int(timestamp.timestamp())}"
            return activity_id
        except Exception as e:
            logger.error(f"Error updating leaderboards: {str(e)}")
            raise
        finally:
            redis.close()

    @staticmethod
    def get_user_from_composite(user_id: str) -> Dict:
        """Get user information from composite service."""
        composite_url = os.environ.get("COMPOSITE_SERVICE_URL", "http://composite-service:8000")
        try:
            response = requests.get(f"{composite_url}/users/{user_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching user data from composite service: {str(e)}")
            # Return basic info if service is unavailable
            return {"user_id": user_id, "username": f"User-{user_id[:6]}"}

    @staticmethod
    def get_friends_from_composite(user_id: str) -> List[str]:
        """Get user's friends from composite service."""
        composite_url = os.environ.get("COMPOSITE_SERVICE_URL", "http://composite-service:8000")
        try:
            response = requests.get(f"{composite_url}/users/{user_id}/friends")
            response.raise_for_status()
            return response.json().get("friends", [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching friends from composite service: {str(e)}")
            return []

    @staticmethod
    def build_friends_leaderboard(user_id: str) -> bool:
        """Build the initial friends leaderboard for a user."""
        redis = get_redis()
        try:
            # Get friends list from composite service
            friends_ids = LeaderboardCache.get_friends_from_composite(user_id)
            
            # Include the user themself
            friends_ids.append(user_id)
            
            # Get weekly leaderboard key
            weekly_key = LeaderboardCache.get_weekly_leaderboard_key()
            friends_key = LeaderboardCache.get_friends_leaderboard_key(user_id)
            
            # Add each friend to the leaderboard with their current calories
            for friend_id in friends_ids:
                calories = redis.zscore(weekly_key, friend_id) or 0
                redis.zadd(friends_key, {friend_id: calories})
            
            # Set expiration (currently 2 weeks)
            redis.expire(friends_key, 60 * 60 * 24 * 14)  
            
            return True
        except Exception as e:
            logger.error(f"Error building friends leaderboard: {str(e)}")
            return False
        finally:
            redis.close()

    @staticmethod
    def update_friends_leaderboard(user_id: str, calories_burned: float):
        """Update the friends leaderboard for this user and their friends"""
        redis = get_redis()
        try:
            # Get the user's friends from composite service
            friends = LeaderboardCache.get_friends_from_composite(user_id)
            
            # Update the user's own friends leaderboard
            user_friends_key = LeaderboardCache.get_friends_leaderboard_key(user_id)
            redis.zincrby(user_friends_key, calories_burned, user_id)
            
            # Also add/update all friends in this leaderboard
            for friend_id in friends:
                # Get friend's current calories from weekly leaderboard
                weekly_key = LeaderboardCache.get_weekly_leaderboard_key()
                friend_calories = redis.zscore(weekly_key, friend_id) or 0
                
                # Update or add friend to this user's friends leaderboard
                redis.zadd(user_friends_key, {friend_id: friend_calories})
            
            # Set expiration
            redis.expire(user_friends_key, 60 * 60 * 24 * 14)  # 2 weeks
            
            # Now update this user in all friends' leaderboards
            for friend_id in friends:
                friend_leaderboard_key = LeaderboardCache.get_friends_leaderboard_key(friend_id)
                
                # Get user's total calories from weekly leaderboard
                user_total_calories = redis.zscore(weekly_key, user_id) or 0
                
                # Update this user in friend's leaderboard
                redis.zadd(friend_leaderboard_key, {user_id: user_total_calories})
                redis.expire(friend_leaderboard_key, 60 * 60 * 24 * 14)  # 2 weeks
        
        except Exception as e:
            logger.error(f"Error updating friends leaderboard: {str(e)}")
        finally:
            redis.close()

    @staticmethod
    def get_leaderboard(leaderboard_key: str, limit: int, offset: int) -> Tuple[List[Tuple[str, float]], int]:
        """Get leaderboard entries with pagination."""
        redis = get_redis()
        try:
            # Get total users in leaderboard
            total_users = redis.zcard(leaderboard_key)
            
            # Get top users with scores
            leaderboard_data = redis.zrevrange(
                leaderboard_key, 
                offset, 
                offset + limit - 1, 
                withscores=True
            )
            
            return leaderboard_data, total_users
        except Exception as e:
            logger.error(f"Error getting leaderboard data: {str(e)}")
            raise
        finally:
            redis.close()

    @staticmethod
    def get_user_rank(user_id: str, leaderboard_key: str) -> Tuple[Optional[float], Optional[int], int]:
        """Get a user's rank, score and total users in a specific leaderboard."""
        redis = get_redis()
        try:
            # Get user's calories
            calories = redis.zscore(leaderboard_key, user_id)
            
            # Get user's rank (0-based, so add 1 later)
            rank = redis.zrevrank(leaderboard_key, user_id)
            if rank is not None:
                rank += 1  # Convert to 1-based ranking
            
            # Get total users
            total_users = redis.zcard(leaderboard_key)
            
            return calories, rank, total_users
        except Exception as e:
            logger.error(f"Error getting user rank: {str(e)}")
            raise
        finally:
            redis.close()