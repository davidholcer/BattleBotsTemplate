import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
import json
from DetectorTemplate.DetectorCode.detector import Detector
import logging
import signal
from constants import detector_session_id, detect_bot_max_time
from pydantic import ValidationError
from teams_classes import DetectionMark
from api_requests import DetectorRequests

logging.basicConfig(
    filename='DetectorTemplate/run.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TimeoutError(Exception):
    """Custom exception for timeout errors."""
    pass

# API endpoint URL
#base_url = "http://localhost:3000"

#authentication_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWFtSWQiOiI0IiwidGVhbU5hbWUiOiJFbWlsaWUgRGV0ZWN0b3IiLCJpYXQiOjE3MjQwMjAzNDMsImV4cCI6MTcyNDEwNjc0M30.kBwhxS5Xr_mjt4fZNIDPUUin-cAWdFVNmOTyYS0L3Jg'

#headers = {'Authorization': 'bearer ' + authentication_token, 'Content-Type': 'application/json' }

def handler(signum, frame):
    raise TimeoutError("Timeout Error:")

logging.info(f"START SESSION {detector_session_id}")
try:
    detector = Detector()
    # ask for Session Info
    #session_dataset = requests.get(base_url + '/api/detector/session/' + str(detector_session_id), headers=headers) 
    session_dataset = DetectorRequests.get_session_data()
    
    session_dataset.raise_for_status()

    logging.info(f"Get Session response status code: {session_dataset.status_code}")
    print("Get Session response status code:", session_dataset.status_code)
    #print("Get Session response content:", session_dataset.json())

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(detect_bot_max_time)
    try:
        marked_account = detector.detect_bot(session_dataset.json())
        if len(marked_account) == 0: # Empty submission
            detections_submission = []  
        elif not isinstance(marked_account[0], DetectionMark): #If the teams don't return a list of DetectionMark instance/object???.
            raise TypeError("The elements of the list should be DetectionMark instance. Make sure to return a list[DetectionMark].")
        else:
            detections_submission = [user.to_dict() for user in marked_account]
    except TimeoutError as exc:
        logging.error(f"{exc} The code took more than one hour to run. Continue with an empty submission.")
        print(f"{exc} The code took more than one hour to run. Continue with an empty submission.")
        detections_submission = []

    signal.alarm(0)

    #submission_confirmation = requests.post(base_url + '/api/detector/session/' + str(detector_session_id), headers=headers, data=json.dumps({"users": detections_submission}))
    submission_confirmation = DetectorRequests.submit_detection(detections_submission) 
    
    # Check if the request was successful
    submission_confirmation.raise_for_status()
    
    # Print the response
    logging.info(f"Detection Submission repsonse status code: {submission_confirmation.status_code}")
    print("Detection Submission repsonse status code:", submission_confirmation.status_code)
    print("Detection Submission response content:", json.dumps(submission_confirmation.json(), indent=4))

    logging.info(f"END SESSION {detector_session_id}")

except (requests.exceptions.RequestException, ValidationError, TypeError) as exc:
    if isinstance(exc, requests.exceptions.RequestException):
        logging.error(f"An error occurred: {exc}")
        print("An error occurred:", exc)
    elif isinstance(exc, ValidationError):
        if exc.errors()[0]['type'] == 'int_from_float':
            logging.error(f"DetectionMark Object Error: The confidence should be an int between 0 (definitely not a bot) and 100 (definitely a bot). Error Description {exc.errors()}.")
            print(f"DetectionMark Object Error: The confidence should be an int between 0 (definitely not a bot) and 100 (definitely a bot). Error Description {exc.errors()}.")
        else:
            logging.error(f"DetectionMark Object Error: Error Description {exc.errors()}. Make sure you create your instance correctly.")
            print(f"DetectionMark Object Error: Error Description {exc.errors()}. Make sure you create your instance correctly.")
    elif isinstance(exc, TypeError):
        logging.error(exc)
        print(exc)