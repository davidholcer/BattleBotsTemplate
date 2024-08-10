import requests
import json
import os
import signal

BOT_SERVICE_URL = os.getenv("BOT_SERVICE_URL", "http://bot:5001")

def handler(signum, frame):
    raise Exception("Timeout")

def main():
    session_id = 4
    # API endpoint URL
    baseUrl = os.getenv('BASE_URL', 'http://localhost:3000')
    # Authentication token to know which team we are dealing with and make the requests
    authenticationToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWFtSWQiOiIzIiwidGVhbU5hbWUiOiJFbWlsaWUgQm90IiwiaWF0IjoxNzIzMjY3NjE4LCJleHAiOjE3MjMzNTQwMTh9.N0OBLvwi87qXUKP5dyXqECDU7pv9ejBZt8giZMyuAP8'
    header = {'Authorization': 'bearer ' + authenticationToken, 'Content-Type': 'application/json'}
    sub_sessions_id = []

    try:
        # Get session info for the present session
        sessionInfo_response = requests.get(baseUrl + '/api/bot/session/' + str(session_id) + '/info', headers=header)
        # Verify if response was successful for sessionInfo_response
        sessionInfo_response.raise_for_status()
        # Print the response output
        print("sessionInfo response status code:", sessionInfo_response.status_code)
        #print(f"sessionInfo output: {sessionInfo_response.json()}\n- - - - -")

        # Get the sub-session id from the get info.
        sub_sessions_id = [1, 2, 3, 4]
        # Give the session info to the bot teams and the id of the present sub_session and receive from there createUser
        # function the amount of users they want
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(300)
        try:
            team_user_response = requests.post(f"{BOT_SERVICE_URL}/createUser", json=sessionInfo_response.json())
            num_of_users = team_user_response.json()
        except Exception as exc:
            print(exc)
            print(f"Timeout occurred for createUser. Continuing with default 1 user.")
            num_of_users = 1
        
        signal.alarm(0)
        #team_user_response.raise_for_status()
        #print(f"{team_user_response}\n- - - - -") # T

        # Create the users for the team according to their response, the default value should be 1
        createUser_response = requests.post(baseUrl + '/api/bot/session/' + str(session_id) + '/createuser', headers=header, data=json.dumps({"num_of_users": num_of_users}))
        # Verify if response was successful for createUser_response
        createUser_response.raise_for_status()
        # Print the response output
        print("createUser response status code:", createUser_response.status_code)
        #print(f"createUser output: {createUser_response.json()}\n- - - - -")

        for sub_session in sub_sessions_id:
            # Get the team sub-session posts dataset and users dataset
            getSubSession_response = requests.get(baseUrl + '/api/bot/session/' + str(session_id) + '/' + str(sub_session), headers=header)
            # Verify if response was successful for getSubSession_response
            getSubSession_response.raise_for_status()
            # Print the response output
            print("getSubSession response status code:", getSubSession_response.status_code)
            #print(f"getSubSession output:{getSubSession_response.json()}\n- - - - -")

            # Give the datasets and the list of users id to the team and make them start the run of their code and timeout if too long
            # Run subSessionInjection
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(1801) # Set the timeout to 30 minutes + 1 second
            try:
                team_injection_response = requests.post(f"{BOT_SERVICE_URL}/subSessionInjection", json={"sub_session_id": sub_session, "datasets_json": getSubSession_response.json(), "users_id": createUser_response.json()})
                team_injection_response.raise_for_status()
                team_injection_data = team_injection_response.json()
            
            except Exception as exc:
                print(exc)
                print(f"Timeout occurred for sub-session {sub_session}. Continuing with an empty response.")
                team_injection_data = {"posts": [], "users": []}
            
            signal.alarm(0)
            
            # Inject the new posts and users in the session dataset
            injectSubSession_response = requests.post(baseUrl + '/api/bot/session/' + str(session_id) + '/' + str(sub_session), headers=header, data=json.dumps(team_injection_data))
            print("injectSubSession response status code:", injectSubSession_response.status_code)
            # Verify if response was successful for injectSubSession_response
            injectSubSession_response.raise_for_status()
            # Print the response output
            print("injectSubSession response status code:", injectSubSession_response.status_code)
            #print(f"injectSubSession output: {injectSubSession_response.json()}\n- - - - -")
        # Maybe add time stamp for analysis.

    except requests.exceptions.RequestException as err:
        print("An error occurred:", err)

if __name__ == "__main__":
    main()

# To be automated: 
# - the sub-sessions id list creation
# - getting the authentication token 
# - getting the session id

# To maybe modify:
# - the timeout might not work on other computer system so we might have to look for an alternative
# - some minor change might be done here depending on which metadata we give
# - any other analysis information that could be useful like the time it took for each sub-session or others
