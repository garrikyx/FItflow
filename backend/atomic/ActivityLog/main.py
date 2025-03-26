from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)

CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = (
     environ.get("dbURL") or "mysql+mysqlconnector://root:root@localhost:3306/activitylog"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)


class ActivityLog(db.Model):
    __tablename__ = "activitylog"

    

    def __init__(self,):
        return

    def json(self):
        return {
        }





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
