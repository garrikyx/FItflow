from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime
import os

app = Flask(__name__)
CORS(app)

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "activitylog")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class ActivityLog(db.Model):
    __tablename__ = "activitylog"

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(50), nullable=False)
    exerciseType = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    intensity = db.Column(db.String(50), nullable=False)
    caloriesBurned = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

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


@app.route("/activity", methods=["POST"])
def log_activity():
    data = request.get_json()
    required_fields = ["userId", "exerciseType", "duration", "intensity", "caloriesBurned"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields"}), 400

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


@app.route("/activity/<userId>", methods=["GET"])
def get_activities(userId):
    activities = ActivityLog.query.filter_by(userId=userId).order_by(ActivityLog.timestamp.desc()).all()
    return jsonify([a.json() for a in activities]), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # create table if it doesn't exist
    app.run(host="0.0.0.0", port=5030, debug=True)
