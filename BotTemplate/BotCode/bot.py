from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/createUser', methods=['POST'])
def createUser():
    session_info = request.json
    # Implement logic here and replace the return value with the number of users you want to create.
    # Example:
    number_user = 2
    return jsonify(number_user)

@app.route('/subSessionInjection', methods=['POST'])
def subSessionInjection():
    data = request.json
    sub_session_id = data['sub_session_id']
    datasets_json = data['datasets_json']
    users_id = data['users_id']
    # Implement your code to process the datasets here.
    # It needs to return json with the users and their description and the posts to be inserted.
    # Example:
    users = []
    posts = []
    for user_id in users_id['users']:
        posts.append({"id": "123", "text": "Hello I'm a bot", "author_id": user_id['id'], "created_at": "8 am", "lang": "en"})
        users.append({"id": user_id['id'], "tweet_count": 1, "z_score": 0, "username": "Em88", "name": "Emilie", "description": "test", "location": "SF"})
    submission_file = {"posts": posts, "users": users}
    return json.dumps(submission_file)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)