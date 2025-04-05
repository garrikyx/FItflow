import os
import logging
from datetime import datetime
from redis import Redis
from typing import List, Dict, Optional, Tuple

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
    def get_friends_leaderboard_key(user_id: str):
        """Generate the Redis key for a user's friends leaderboard."""
        today = datetime.now()
        week_number = today.isocalendar()[1]
        year = today.year
        return f"leaderboard:friends:{user_id}:{year}:{week_number}"

    @staticmethod
    def update_leaderboards(user_id: str, calories_burned: float, timestamp: Optional[datetime] = None):
        """Update weekly leaderboard with new activity data."""
        redis = get_redis()
        try:
            if not timestamp:
                timestamp = datetime.now()
            
            weekly_key = LeaderboardCache.get_weekly_leaderboard_key()
            redis.zincrby(weekly_key, calories_burned, user_id)
            redis.expire(weekly_key, 60 * 60 * 24 * 21)  # 3 weeks
            
            logger.info(f"Updated weekly leaderboard for user {user_id}")
            return f"activity:{user_id}:{int(timestamp.timestamp())}"
        except Exception as e:
            logger.error(f"Error updating leaderboard: {str(e)}")
            raise
        finally:
            redis.close()

    @staticmethod
    def update_friends_leaderboard(user_id: str, friends: List[Dict]):
        """Update friends leaderboards using provided friends list."""
        redis = get_redis()
        weekly_key = LeaderboardCache.get_weekly_leaderboard_key()
        
        try:
            # Get user's current total from weekly leaderboard
            user_total = redis.zscore(weekly_key, user_id) or 0
            
            # Update user's own friends leaderboard
            user_friends_key = LeaderboardCache.get_friends_leaderboard_key(user_id)
            
            # Add user to their own leaderboard
            redis.zadd(user_friends_key, {user_id: user_total})
            
            # Add each friend to user's leaderboard with their current total
            for friend in friends:
                friend_id = str(friend["Id"])
                friend_total = redis.zscore(weekly_key, friend_id) or 0
                redis.zadd(user_friends_key, {friend_id: friend_total})
            
            # Set expiration for user's friends leaderboard
            redis.expire(user_friends_key, 60 * 60 * 24 * 14)
            
            # Update each friend's leaderboard to include the user
            for friend in friends:
                friend_id = str(friend["Id"])
                friend_leaderboard_key = LeaderboardCache.get_friends_leaderboard_key(friend_id)
                redis.zadd(friend_leaderboard_key, {user_id: user_total})
                redis.expire(friend_leaderboard_key, 60 * 60 * 24 * 14)
            
        except Exception as e:
            logger.error(f"Error updating friends leaderboard: {str(e)}")
            raise
        finally:
            redis.close()

    @staticmethod
    def get_leaderboard(leaderboard_key: str, limit: int, offset: int) -> Tuple[List[Tuple[str, float]], int]:
        """Get leaderboard entries with pagination."""
        redis = get_redis()
        try:
            total_users = redis.zcard(leaderboard_key)
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
            calories = redis.zscore(leaderboard_key, user_id)
            rank = redis.zrevrank(leaderboard_key, user_id)
            if rank is not None:
                rank += 1  # Convert to 1-based ranking
            total_users = redis.zcard(leaderboard_key)
            return calories, rank, total_users
        except Exception as e:
            logger.error(f"Error getting user rank: {str(e)}")
            raise
        finally:
            redis.close()

    @staticmethod
    def clear_old_data():
        """Clear any data in Redis that's not the current week's leaderboard."""
        redis = get_redis()
        try:
            current_weekly_key = LeaderboardCache.get_weekly_leaderboard_key()
            all_leaderboard_keys = redis.keys("leaderboard:*")
            
            keys_to_delete = []
            for key in all_leaderboard_keys:
                if key != current_weekly_key and not key.startswith("leaderboard:friends:"):
                    keys_to_delete.append(key)
            
            if keys_to_delete:
                redis.delete(*keys_to_delete)
                logger.info(f"Cleared {len(keys_to_delete)} old leaderboard keys")
            
            return len(keys_to_delete)
        except Exception as e:
            logger.error(f"Error clearing old data: {str(e)}")
            return 0
        finally:
            redis.close()