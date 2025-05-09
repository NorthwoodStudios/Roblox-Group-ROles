from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)

# Replace with your Roblox group ID
GROUP_ID = 123456789  # Example Group ID

# Check server is running with a simple ping
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "Server is running!"}), 200

def get_rank_id_from_roblox(user_id):
    # The Roblox API to get the user's group roles
    url = f"https://groups.roblox.com/v1/users/{user_id}/groups/roles"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Check the group roles
        for group in data['data']:
            if group['group']['id'] == GROUP_ID:
                return group['role']['id']  # Return the long rank ID
    return None  # Return None if the group isn't found or the rank doesn't exist

@app.route('/get_rank', methods=['GET'])
def get_user_rank():
    user_id = request.args.get('user_id')
    if user_id:
        rank_id = get_rank_id_from_roblox(user_id)
        if rank_id:
            return jsonify({"rank_id": rank_id}), 200
        else:
            return jsonify({"error": "User not in group or rank not found"}), 400
    return jsonify({"error": "No user_id provided"}), 400

@app.route('/check_rank', methods=['POST'])
def check_user_rank():
    data = request.get_json()
    user_id = data.get('user_id')
    required_rank_id = data.get('required_rank_id')
    
    if user_id and required_rank_id:
        rank_id = get_rank_id_from_roblox(user_id)
        if rank_id:
            # Compare the rank ID with the required rank ID
            if rank_id >= int(required_rank_id):  # You can adjust the comparison based on your needs
                return jsonify({"access_granted": True}), 200
            else:
                return jsonify({"access_granted": False}), 403
        else:
            return jsonify({"error": "User not in group or rank not found"}), 400
    return jsonify({"error": "Missing user_id or required_rank_id"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
