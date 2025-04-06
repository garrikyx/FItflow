from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime
import os
import time
from sqlalchemy.exc import SQLAlchemyError
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "activitylog-db")
DB_NAME = os.getenv("DB_NAME", "activitylog")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True  

db = SQLAlchemy(app)


class ActivityLog(db.Model):
    __tablename__ = "activitylog"

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(50), nullable=False)
    exerciseType = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    intensity = db.Column(db.String(50), nullable=False)
    caloriesBurned = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def json(self):
        return {
            "id": self.id,
            "userId": self.userId,
            "exerciseType": self.exerciseType,
            "duration": self.duration,
            "intensity": self.intensity,
            "caloriesBurned": self.caloriesBurned,
            "timestamp": self.timestamp.isoformat()
        }

@app.route("/health", methods=["GET"])
def health_check():
    try:
        db.session.query(ActivityLog).first()
        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }), 500


@app.route("/activity", methods=["GET"])
def get_all_activities():
    try:
        activities = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).all()
        if not activities:
            return jsonify({"message": "No activity records found"}), 404
        return jsonify([a.json() for a in activities]), 200
    except SQLAlchemyError:
        return jsonify({"error": "Database error occurred"}), 500

@app.route("/activity", methods=["POST"])
def log_activity():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ["userId", "exerciseType", "duration", "intensity", "caloriesBurned"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        activity = ActivityLog(
            userId=data["userId"],
            exerciseType=data["exerciseType"],
            duration=data["duration"],
            intensity=data["intensity"],
            caloriesBurned=data["caloriesBurned"]
        )

        db.session.add(activity)
        db.session.commit()
        return jsonify(activity.json()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred"}), 500

@app.route("/activity/<userId>", methods=["GET"])
def get_activities(userId):
    try:
        activities = ActivityLog.query.filter_by(userId=userId).order_by(ActivityLog.timestamp.desc()).all()
        if not activities:
            return jsonify({"message": f"No activity records found for user {userId}"}), 404
        return jsonify([a.json() for a in activities]), 200
    except SQLAlchemyError:
        return jsonify({"error": "Database error occurred"}), 500

if __name__ == "__main__":
    max_retries = 5
    retry_count = 0
    while retry_count < max_retries:
        try:
            with app.app_context():
                db.create_all()
            break
        except SQLAlchemyError:
            retry_count += 1
            if retry_count == max_retries:
                print("Failed to connect to database after multiple attempts")
                exit(1)
            time.sleep(2)
    
    app.run(host="0.0.0.0", port=5030, debug=True)
