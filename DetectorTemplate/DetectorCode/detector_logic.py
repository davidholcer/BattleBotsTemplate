from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/calculateDetections', methods=['POST'])
def calculateDetections():
    sessionData = request.json
    # todo logic
    value = {
        'users': [
            {
                'userId': sessionData['users'][0]['id'],
                'confidence': 50
            }
        ]
    }


    return json.dumps(value)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)