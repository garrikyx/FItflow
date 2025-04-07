from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+mysqlconnector://root:root@user-mysql:3306/user')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Enable SQL query logging

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    goal = db.Column(db.String(20), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# GET ALL USERS
@app.route("/user")
def get_all():
    try:
        users = User.query.all()
        users_list = []
        for user in users:
            user_data = {
                'userId': user.user_id,
                'email': user.email,
                'name': user.name,
                'weight': user.weight,
                'goal': user.goal
            }
            users_list.append(user_data)

        if users_list:
            return jsonify({
                "code": 200,
                "data": {"users": users_list}
            })
        return jsonify({"code": 404, "message": "There are no users."}), 404
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)}), 500

# GET USER BY USERID
@app.route("/user/<string:userId>")
def search_by_userid(userId):
    try:
        user = User.query.get(userId)
        if user:
            user_data = {
                'userId': user.user_id,
                'email': user.email,
                'name': user.name,
                'weight': user.weight,
                'goal': user.goal
            }
            return jsonify({"code": 200, "data": user_data})
        return jsonify({"code": 404, "message": "User not found."}), 404
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)}), 500

# CREATE NEW USER
@app.route("/user/<string:userId>", methods=["POST"])
def create_user(userId):
    try:
        data = request.json
        
        # Check if user already exists
        if User.query.get(userId):
            return jsonify({
                "code": 400,
                "message": "User ID already exists"
            }), 400

        # Check if email already exists
        if User.query.filter_by(email=data.get('email')).first():
            return jsonify({
                "code": 400,
                "message": "Email already registered"
            }), 400

        # Create new user
        new_user = User(
            user_id=userId,
            email=data.get('email'),
            name=data.get('name'),
            password=generate_password_hash(data.get('password')),
            weight=data.get('weight'),
            goal=data.get('goal')
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "code": 201,
            "message": "User created successfully"
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "message": f"An error occurred: {str(e)}"
        }), 500

# UPDATE USER DETAILS
@app.route("/user/<string:userId>", methods=["PUT"])
def update_user(userId):
    try:
        user = User.query.get(userId)
        if not user:
            return jsonify({
                "code": 404,
                "data": {"userId": userId},
                "message": "User not found."
            }), 404

        data = request.get_json()
        
        # Update user fields
        if 'email' in data:
            user.email = data['email']
        if 'name' in data:
            user.name = data['name']
        if 'password' in data:
            user.password = generate_password_hash(data['password'])
        if 'weight' in data:
            user.weight = data['weight']
        if 'goal' in data:
            user.goal = data['goal']

        db.session.commit()

        updated_data = {
            'userId': user.user_id,
            'email': user.email,
            'name': user.name,
            'weight': user.weight,
            'goal': user.goal
        }

        return jsonify({
            "code": 200,
            "data": updated_data,
            "message": "User updated successfully."
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "data": {"userId": userId},
            "message": str(e)
        }), 500

# DELETE USER
@app.route("/user/<string:userId>", methods=["DELETE"])
def delete_user(userId):
    try:
        user = User.query.get(userId)
        if not user:
            return jsonify({
                "code": 404,
                "data": {"userId": userId},
                "message": "User not found."
            }), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({
            "code": 200,
            "data": {"userId": userId},
            "message": "User deleted successfully."
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "data": {"userId": userId},
            "message": str(e)
        }), 500

# LOGIN
@app.route("/login", methods=["POST"])
def login():
    app.logger.debug("Login endpoint called")
    try:
        data = request.get_json()
        app.logger.info(f"Parsed JSON data: {data}")
        
        if not data:
            app.logger.error("No JSON data received")
            return jsonify({
                "code": 400,
                "message": "No data received"
            }), 400

        userId = data.get('userId')
        password = data.get('password')
        
        app.logger.debug(f"Login attempt for user: {userId}")

        # Add more detailed logging
        app.logger.debug("Querying SQL database for user...")
        user = User.query.get(userId)
        app.logger.debug(f"SQL query result: {user is not None}")

        if not user:
            app.logger.warning(f"User not found in SQL database: {userId}")
            return jsonify({
                "code": 404,
                "message": "User not found"
            }), 404

        # Log the actual SQL user data
        app.logger.debug(f"Found user in SQL: {user.user_id}, {user.email}")

        if check_password_hash(user.password, password):
            app.logger.info(f"Successful login for user: {userId}")
            return jsonify({
                "code": 200,
                "message": "Login successful",
                "data": {
                    "userId": userId,
                    "weight": user.weight,
                    "goal": user.goal
                }
            })
        else:
            app.logger.warning(f"Invalid password for user: {userId}")
            return jsonify({
                "code": 401,
                "message": "Invalid password"
            }), 401

    except Exception as e:
        app.logger.error(f"Login error: {str(e)}", exc_info=True)
        return jsonify({
            "code": 500,
            "message": f"Server error: {str(e)}"
        }), 500

# Add this new route to check database connection and contents
@app.route("/debug/users")
def debug_users():
    try:
        
        # Get all users from SQL table
        users = User.query.all()
        users_list = [{
            'user_id': user.user_id,
            'email': user.email,
            'name': user.name,
            'weight': user.weight,
            'goal': user.goal
        } for user in users]
        
        return jsonify({
            "code": 200,
            "message": "Database connected",
            "user_count": len(users_list),
            "users": users_list
        })
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"Database error: {str(e)}"
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
