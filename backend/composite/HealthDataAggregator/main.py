from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Define the endpoint for your user-service
USER_SERVICE_URL = "http://user-service:5001/user/"

@app.route('/get-username/<string:userId>', methods=['GET'])
def get_username(userId):
    try:
        # Call the user service to fetch user data
        response = requests.get(f"{USER_SERVICE_URL}{userId}")

        if response.status_code == 200:
            user_data = response.json().get("data", {})
            username = user_data.get("name")
            if username:
                return jsonify({"userId": userId, "name": username})
            else:
                return jsonify({"error": "Username not found"}), 404
        elif response.status_code == 404:
            return jsonify({"error": "User not found"}), 404
        else:
            return jsonify({"error": "Failed to retrieve user data", "details": response.text}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
