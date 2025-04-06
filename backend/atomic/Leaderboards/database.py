from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import environ
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    environ.get("dbURL") or "mysql+mysqlconnector://root:root@leaderboards-mysql:3306/leaderboards"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class Leaderboards(db.Model):
    __tablename__ = 'leaderboards'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String, nullable=False, index=True)
    calories_burned = db.Column(db.Float, nullable=False)
    activity_type = db.Column(db.String, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, calories_burned, activity_type=None, timestamp=None):
        self.user_id = user_id
        self.calories_burned = calories_burned
        self.activity_type = activity_type
        self.timestamp = timestamp or datetime.now()

    def json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "calories_burned": self.calories_burned,
            "activity_type": self.activity_type,
            "timestamp": self.timestamp.isoformat()
        }

# Create database tables
with app.app_context():
    db.create_all()

def add_activity(user_id, calories_burned, activity_type=None, timestamp=None):
    """
    Add a new activity record to the database
    
    Args:
        user_id (str): ID of the user
        calories_burned (float): Calories burned in the activity
        activity_type (str, optional): Type of activity
        timestamp (datetime, optional): Timestamp of the activity
    
    Returns:
        Activity: The created activity record
    """
    try:
        leaderboards = Leaderboards(
            user_id=user_id,
            calories_burned=calories_burned,
            activity_type=activity_type,
            timestamp=timestamp
        )
        
        db.session.add(leaderboards)
        db.session.commit()
        
        return leaderboards
    except Exception as e:
        db.session.rollback()
        raise