import requests
import json
import os
import signal


DETECTOR_SERVICE_URL = os.getenv("DETECTOR_SERVICE_URL", "http://detector:5001")
# API endpoint URL
baseUrl = os.getenv('BASE_URL', 'http://localhost:3000')

def handler(signum, frame):
    raise Exception("Timeout")

authenticationToken_for_detector = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWFtSWQiOiI0IiwidGVhbU5hbWUiOiJFbWlsaWUgRGV0ZWN0b3IiLCJpYXQiOjE3MjMyNTYyNzEsImV4cCI6MTcyMzM0MjY3MX0.ROeQWowIDS3rSubdemnfoQDaRuT4hkcxdObbGcvX8G0'

headers = {'Authorization': 'bearer ' + authenticationToken_for_detector, 'Content-Type': 'application/json' }

sessionId = 4

try:

    # ask for Session Info
    sessionResponse = requests.get(baseUrl + '/api/detector/session/' + str(sessionId), headers=headers) 
    
    sessionResponse.raise_for_status()

    print("Response status code:", sessionResponse.status_code)
    # print("Response content:", sessionResponse.json())

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(3601)
    try:
        detections_response = requests.post(f"{DETECTOR_SERVICE_URL}/calculateDetections", json=sessionResponse.json())
        detections = detections_response.json()
    except Exception as exc:
        print(exc)
        print("Timeout: The code took more than one more hour to run. Continue with an empty submission.")
        detections = {"users": []}

    signal.alarm(0)

    detection = requests.post(baseUrl + '/api/detector/session/' + str(sessionId), headers=headers, data=json.dumps(detections)) 

    
    # Check if the request was successful
    detection.raise_for_status()
    
    # Print the response
    print("Response status code:", detection.status_code)
    # print("Response content:", detection.json())

except requests.exceptions.RequestException as e:
    print("An error occurred:", e)