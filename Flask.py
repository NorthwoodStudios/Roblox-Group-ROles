from flask import Flask, jsonify, request
import requests
import json
import os

app = Flask(__name__)

GROUP_ID = 11617706  # Replace this with your actual group ID

def get_user_groups(user_id):
    url = f"https://groups.roblox.com/v1/users/{user_id}/groups/roles"
    response = requests.get(url)
    
    if response.status_code == 200:
        groups_data = response.json()
        accessible_groups = []
        
        for group in groups_data['data']:
            if group['group']['id'] == GROUP_ID:
                accessible_groups.append({
                    'name': group['role']['name'],
                    'rank': group['role']['rank']
                })
        
        return accessible_groups
    else:
        return {"error": "Failed to fetch groups"}

@app.route('/get_user_groups', methods=['POST'])
def get_user_groups_route():
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    
    groups = get_user_groups(user_id)
    
    if "error" in groups:
        return jsonify(groups), 500
    
    return jsonify({"groups": groups})

# Keep-alive endpoint to ensure the server stays active
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
