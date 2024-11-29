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

        # "user_distribution_across_time": [
        #     {
        #         "start_at": "2024-03-27T00:00:00Z",
        #         "end_at": "2024-03-27T02:00:00Z",
        #         "percentage_of_users": 50.7,
        #         "percentage_of_posts": 6.5
        #     },
        #     {
        #         "start_at": "2024-03-27T02:00:00Z",
        #         "end_at": "2024-03-27T04:00:00Z",
        #         "percentage_of_users": 43.7,
        #         "percentage_of_posts": 5.7
        #     },
        #     {
        #         "start_at": "2024-03-27T04:00:00Z",
        #         "end_at": "2024-03-27T06:00:00Z",
        #         "percentage_of_users": 27.1,
        #         "percentage_of_posts": 2
        #     },
        #     {
        #         "start_at": "2024-03-27T06:00:00Z",
        #         "end_at": "2024-03-27T08:00:00Z",
        #         "percentage_of_users": 13.7,
        #         "percentage_of_posts": 1.1
        #     },
        #     {
        #         "start_at": "2024-03-27T08:00:00Z",
        #         "end_at": "2024-03-27T10:00:00Z",
        #         "percentage_of_users": 13.7,
        #         "percentage_of_posts": 0.9
        #     },
        #     {
        #         "start_at": "2024-03-27T10:00:00Z",
        #         "end_at": "2024-03-27T12:00:00Z",
        #         "percentage_of_users": 15.3,
        #         "percentage_of_posts": 1.1
        #     },
        #     {
        #         "start_at": "2024-03-27T12:00:00Z",
        #         "end_at": "2024-03-27T14:00:00Z",
        #         "percentage_of_users": 30,
        #         "percentage_of_posts": 2.3
        #     },
        #     {
        #         "start_at": "2024-03-27T14:00:00Z",
        #         "end_at": "2024-03-27T16:00:00Z",
        #         "percentage_of_users": 41.6,
        #         "percentage_of_posts": 3.3
        #     },
        #     {
        #         "start_at": "2024-03-27T16:00:00Z",
        #         "end_at": "2024-03-27T18:00:00Z",
        #         "percentage_of_users": 44.2,
        #         "percentage_of_posts": 4.3
        #     },
        #     {
        #         "start_at": "2024-03-27T18:00:00Z",
        #         "end_at": "2024-03-27T20:00:00Z",
        #         "percentage_of_users": 49.3,
        #         "percentage_of_posts": 4.6
        #     },
        #     {
        #         "start_at": "2024-03-27T20:00:00Z",
        #         "end_at": "2024-03-27T22:00:00Z",
        #         "percentage_of_users": 47.2,
        #         "percentage_of_posts": 3.8
        #     },
        #     {
        #         "start_at": "2024-03-27T22:00:00Z",
        #         "end_at": "2024-03-28T00:00:00Z",
        #         "percentage_of_users": 54.2,
        #         "percentage_of_posts": 5.1
        #     },
        #     {
        #         "start_at": "2024-03-28T00:00:00Z",
        #         "end_at": "2024-03-28T02:00:00Z",
        #         "percentage_of_users": 48.3,
        #         "percentage_of_posts": 5.6
        #     },
        #     {
        #         "start_at": "2024-03-28T02:00:00Z",
        #         "end_at": "2024-03-28T04:00:00Z",
        #         "percentage_of_users": 38.1,
        #         "percentage_of_posts": 4.4
        #     },
        #     {
        #         "start_at": "2024-03-28T04:00:00Z",
        #         "end_at": "2024-03-28T06:00:00Z",
        #         "percentage_of_users": 29,
        #         "percentage_of_posts": 2.5
        #     },
        #     {
        #         "start_at": "2024-03-28T06:00:00Z",
        #         "end_at": "2024-03-28T08:00:00Z",
        #         "percentage_of_users": 15.3,
        #         "percentage_of_posts": 1.2
        #     },
        #     {
        #         "start_at": "2024-03-28T08:00:00Z",
        #         "end_at": "2024-03-28T10:00:00Z",
        #         "percentage_of_users": 11.8,
        #         "percentage_of_posts": 1
        #     },
        #     {
        #         "start_at": "2024-03-28T10:00:00Z",
        #         "end_at": "2024-03-28T12:00:00Z",
        #         "percentage_of_users": 24.1,
        #         "percentage_of_posts": 2.5
        #     },
        #     {
        #         "start_at": "2024-03-28T12:00:00Z",
        #         "end_at": "2024-03-28T14:00:00Z",
        #         "percentage_of_users": 33.5,
        #         "percentage_of_posts": 3.4
        #     },
        #     {
        #         "start_at": "2024-03-28T14:00:00Z",
        #         "end_at": "2024-03-28T16:00:00Z",
        #         "percentage_of_users": 45,
        #         "percentage_of_posts": 5
        #     },
        #     {
        #         "start_at": "2024-03-28T16:00:00Z",
        #         "end_at": "2024-03-28T18:00:00Z",
        #         "percentage_of_users": 52,
        #         "percentage_of_posts": 5.4
        #     },
        #     {
        #         "start_at": "2024-03-28T18:00:00Z",
        #         "end_at": "2024-03-28T20:00:00Z",
        #         "percentage_of_users": 59,
        #         "percentage_of_posts": 7.4
        #     },
        #     {
        #         "start_at": "2024-03-28T20:00:00Z",
        #         "end_at": "2024-03-28T22:00:00Z",
        #         "percentage_of_users": 61.4,
        #         "percentage_of_posts": 8.4
        #     },
        #     {
        #         "start_at": "2024-03-28T22:00:00Z",
        #         "end_at": "2024-03-29T00:00:00Z",
        #         "percentage_of_users": 80.2,
        #         "percentage_of_posts": 12.4
        #     }
        # ],