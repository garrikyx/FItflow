from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
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

try:
    cred = credentials.Certificate("./serviceAccountKey.json")
    initialize_app(cred)
    db = firestore.client()
except Exception as e:
    app.logger.error(f"Firebase initialization error: {str(e)}")
    # Continue running the app even if Firebase fails to initialize
    # This allows us to see the error in logs

# GET ALL USERS
@app.route("/user")
def get_all():
    try:
        users_ref = db.collection('users')
        users = users_ref.stream()
        users_list = []
        for user in users:
            user_data = user.to_dict()
            user_data['userId'] = user.id
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
        user_ref = db.collection('users').document(userId)
        user = user_ref.get()
        
        if user.exists:
            user_data = user.to_dict()
            user_data['userId'] = user.id
            return jsonify({"code": 200, "data": user_data})
        return jsonify({"code": 404, "message": "User not found."}), 404
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)}), 500

# CREATE NEW USER
@app.route("/user/<string:userId>", methods=["POST"])
def create_user(userId):
    try:
        data = request.json
        user_ref = db.collection('users').document(userId)
        
        # Store user data
        user_ref.set({
            'email': data.get('email'),
            'name': data.get('name'),
            'weight': data.get('weight'),
            'password': data.get('password'),  # In production, hash this!
            'goal': data.get('goal')
        })

        return jsonify({
            "code": 201,
            "message": "User created successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"An error occurred: {str(e)}"
        }), 500

# UPDATE USER DETAILS
@app.route("/user/<string:userId>", methods=["PUT"])
def update_user(userId):
    try:
        user_ref = db.collection('users').document(userId)
        if not user_ref.get().exists:
            return jsonify({
                "code": 404,
                "data": {"userId": userId},
                "message": "User not found."
            }), 404

        data = request.get_json()
        
        # Hash new password if provided
        if 'password' in data:
            data['password'] = generate_password_hash(data['password'])

        # Update user in Firebase
        user_ref.update(data)
        
        # Get updated user data
        updated_user = user_ref.get().to_dict()
        updated_user.pop('password', None)  # Remove password from response
        updated_user['userId'] = userId

        return jsonify({
            "code": 200,
            "data": updated_user,
            "message": "User updated successfully."
        })

    except Exception as e:
        return jsonify({
            "code": 500,
            "data": {"userId": userId},
            "message": str(e)
        }), 500

# DELETE USER
@app.route("/user/<string:userId>", methods=["DELETE"])
def delete_user(userId):
    try:
        user_ref = db.collection('users').document(userId)
        if not user_ref.get().exists:
            return jsonify({
                "code": 404,
                "data": {"userId": userId},
                "message": "User not found."
            }), 404

        # Delete user from Firebase
        user_ref.delete()

        return jsonify({
            "code": 200,
            "data": {"userId": userId},
            "message": "User deleted successfully."
        })

    except Exception as e:
        return jsonify({
            "code": 500,
            "data": {"userId": userId},
            "message": str(e)
        }), 500

# Add this new endpoint
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        print("Received login request data:", data)  # Debug print
        
        userId = data.get('userId')
        password = data.get('password')

        print(f"Looking for user with ID: {userId}")  # Debug print

        # Try getting the user document directly
        user_ref = db.collection('users').document(userId)
        user = user_ref.get()

        if not user.exists:
            # Debug: List all users to see what's actually in the database
            all_users = db.collection('users').stream()
            print("All users in database:")
            for u in all_users:
                print(f"User ID: {u.id}")
                print(f"User data: {u.to_dict()}")
            
            return jsonify({
                "code": 404,
                "message": "User not found"
            }), 404

        user_data = user.to_dict()
        print(f"Found user data: {user_data}")  # Debug print

        # Check password
        if user_data.get('password') == password:  # For now, direct comparison
            return jsonify({
                "code": 200,
                "message": "Login successful",
                "data": {
                    "userId": userId,
                    "weight": user_data.get('weight'),
                    "goal": user_data.get('goal')
                }
            })
        else:
            return jsonify({
                "code": 401,
                "message": "Invalid password"
            }), 401

    except Exception as e:
        print("Login error:", str(e))
        return jsonify({
            "code": 500,
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
