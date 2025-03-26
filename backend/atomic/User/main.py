from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)

CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = (
     environ.get("dbURL") or "mysql+mysqlconnector://root:root@localhost:3306/user"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"

    userId = db.Column(db.String(13), primary_key=True)
    name = db.Column(db.String(13))
    weight = db.Column(db.Float(precision=1), nullable=False)
    preferences = db.Column(db.String(64))



    def __init__(self, userId, name, weight, preferences):
        self.userId = userId
        self,name = name
        self.weight = weight
        self.preferences = preferences


    def json(self):
        return {
            "userId": self.userId,
            "name": self.name,
            "weight": self.weight,
            "preferences": self.preferences,
            
        }

# GET ALL USERS
@app.route("/user")
def get_all():
    users = db.session.scalars(db.select(User)).all()

    if len(users):
        return jsonify(
            {
                "code": 200,
                "data": {"users": [user.json() for user in users]},
            }
        )
    return jsonify({"code": 404, "message": "There are no users."}), 404

#GET USER BY USERID
@app.route("/user/<string:userId>")
def search_by_userid(userId):
    user = db.session.scalar(db.select(User).filter_by(userId=userId))

    if user:
        return jsonify({"code": 200, "data": user.json()})
    return jsonify({"code": 404, "message": "User not found."}), 404


#CREATE NEW USER
@app.route("/user/<string:userId>", methods=["POST"])
def create_user(userId):
    if db.session.scalar(db.select(User).filter_by(userId=userId)):
        return (
            jsonify(
                {
                    "code": 400,
                    "data": {"userId": userId},
                    "message": "User already exists.",
                }
            ),
            400,
        )

    data = request.get_json()
    user = User(userId, **data)

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print("Exception:{}".format(str(e)))
        return (
            jsonify(
                {
                    "code": 500,
                    "data": {"userId": userId},
                    "message": "An error occurred creating the book.",
                }
            ),
            500,
        )

    return jsonify({"code": 201, "data": user.json()}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
