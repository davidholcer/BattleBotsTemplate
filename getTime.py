import random
from datetime import datetime, timedelta

def select_random_time(sub_sessions,sub_ses_n,num_times=1):
    random_times_formatted=[]
    # Select a random sub-session
    try:
        selected_sub_session = [s for s in sub_sessions if s['sub_session_id'] == sub_ses_n][0]
    except IndexError:
        selected_sub_session = random.choice(sub_sessions)
    
    # Parse start and end times
    start_time = datetime.fromisoformat(selected_sub_session['start_time'].replace('Z', '+00:00'))
    end_time = datetime.fromisoformat(selected_sub_session['end_time'].replace('Z', '+00:00'))
    
    # Calculate the time difference between start and end times
    time_diff = end_time - start_time
    
    for i in range(num_times):
        # Select a random time delta within this range
        random_delta = timedelta(seconds=random.randint(0, int(time_diff.total_seconds())))
        # Compute the random time by adding the random delta to the start time
        random_time = start_time + random_delta
        # Format the random time in the desired ISO 8601 format with 'Z'
        random_time_formatted = random_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        # add the time to the list of times
        random_times_formatted.append(random_time_formatted)

    return (random_times_formatted)

# Example usage
# sub_sessions = [
#     {'sub_session_id': 1, 'start_time': '2024-03-27T00:06:30.000Z', 'end_time': '2025-03-27T00:06:30.000Z'},
#     {'sub_session_id': 2, 'start_time': '2024-03-27T00:06:30.000Z', 'end_time': '2025-03-27T00:06:30.000Z'},
#     {'sub_session_id': 3, 'start_time': '2024-03-27T00:06:30.000Z', 'end_time': '2025-03-27T00:06:30.000Z'}
# ]

# random_sub_session_id, random_time = select_random_time(sub_sessions)
# print(f"Random Subsession ID: {random_sub_session_id}, Random Time: {random_time}")
