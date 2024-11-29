import random
from datetime import datetime, timedelta
import json


def sample_time(distribution, session_start, session_end):
    """
    Sample a random time from the distribution using the percentage_of_posts as weights.
    Ensures the sampled time falls within the session bounds.
    """
    # Parse session start and end times into datetime objects
    session_start_dt = datetime.fromisoformat(session_start.replace("Z", "+00:00"))
    session_end_dt = datetime.fromisoformat(session_end.replace("Z", "+00:00"))

    # Extract weights and intervals from the distribution
    weights = [entry["percentage_of_posts"] for entry in distribution]
    intervals = [(entry["start_at"], entry["end_at"]) for entry in distribution]

    # Sample an interval based on percentage_of_posts
    sampled_interval = random.choices(intervals, weights=weights, k=1)[0]

    # Parse the start and end times of the sampled interval
    interval_start_dt = datetime.fromisoformat(sampled_interval[0].replace("Z", "+00:00"))
    interval_end_dt = datetime.fromisoformat(sampled_interval[1].replace("Z", "+00:00"))

    # Ensure the interval is clamped within the session bounds
    clamped_start = max(interval_start_dt, session_start_dt)
    clamped_end = min(interval_end_dt, session_end_dt)

    # If the interval is invalid (start >= end), use the session bounds
    if clamped_start >= clamped_end:
        return session_start if clamped_start == session_start_dt else session_end

    # Sample a random time within the clamped interval
    random_seconds = random.randint(0, int((clamped_end - clamped_start).total_seconds()))
    sampled_time = clamped_start + timedelta(seconds=random_seconds)

    # Return the sampled time in the required string format
    return sampled_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")


# Example usage
if __name__ == "__main__":
    # Load the user distribution across time (replace with your JSON loading method if needed)
    user_distribution = [
            {
                "start_at": "2024-03-27T00:00:00Z",
                "end_at": "2024-03-27T02:00:00Z",
                "percentage_of_users": 50.7,
                "percentage_of_posts": 6.5
            },
            {
                "start_at": "2024-03-27T02:00:00Z",
                "end_at": "2024-03-27T04:00:00Z",
                "percentage_of_users": 43.7,
                "percentage_of_posts": 5.7
            },
            {
                "start_at": "2024-03-27T04:00:00Z",
                "end_at": "2024-03-27T06:00:00Z",
                "percentage_of_users": 27.1,
                "percentage_of_posts": 2
            },
            {
                "start_at": "2024-03-27T06:00:00Z",
                "end_at": "2024-03-27T08:00:00Z",
                "percentage_of_users": 13.7,
                "percentage_of_posts": 1.1
            },
            {
                "start_at": "2024-03-27T08:00:00Z",
                "end_at": "2024-03-27T10:00:00Z",
                "percentage_of_users": 13.7,
                "percentage_of_posts": 0.9
            },
            {
                "start_at": "2024-03-27T10:00:00Z",
                "end_at": "2024-03-27T12:00:00Z",
                "percentage_of_users": 15.3,
                "percentage_of_posts": 1.1
            },
            {
                "start_at": "2024-03-27T12:00:00Z",
                "end_at": "2024-03-27T14:00:00Z",
                "percentage_of_users": 30,
                "percentage_of_posts": 2.3
            },
            {
                "start_at": "2024-03-27T14:00:00Z",
                "end_at": "2024-03-27T16:00:00Z",
                "percentage_of_users": 41.6,
                "percentage_of_posts": 3.3
            },
            {
                "start_at": "2024-03-27T16:00:00Z",
                "end_at": "2024-03-27T18:00:00Z",
                "percentage_of_users": 44.2,
                "percentage_of_posts": 4.3
            },
            {
                "start_at": "2024-03-27T18:00:00Z",
                "end_at": "2024-03-27T20:00:00Z",
                "percentage_of_users": 49.3,
                "percentage_of_posts": 4.6
            },
            {
                "start_at": "2024-03-27T20:00:00Z",
                "end_at": "2024-03-27T22:00:00Z",
                "percentage_of_users": 47.2,
                "percentage_of_posts": 3.8
            },
            {
                "start_at": "2024-03-27T22:00:00Z",
                "end_at": "2024-03-28T00:00:00Z",
                "percentage_of_users": 54.2,
                "percentage_of_posts": 5.1
            },
            {
                "start_at": "2024-03-28T00:00:00Z",
                "end_at": "2024-03-28T02:00:00Z",
                "percentage_of_users": 48.3,
                "percentage_of_posts": 5.6
            },
            {
                "start_at": "2024-03-28T02:00:00Z",
                "end_at": "2024-03-28T04:00:00Z",
                "percentage_of_users": 38.1,
                "percentage_of_posts": 4.4
            },
            {
                "start_at": "2024-03-28T04:00:00Z",
                "end_at": "2024-03-28T06:00:00Z",
                "percentage_of_users": 29,
                "percentage_of_posts": 2.5
            },
            {
                "start_at": "2024-03-28T06:00:00Z",
                "end_at": "2024-03-28T08:00:00Z",
                "percentage_of_users": 15.3,
                "percentage_of_posts": 1.2
            },
            {
                "start_at": "2024-03-28T08:00:00Z",
                "end_at": "2024-03-28T10:00:00Z",
                "percentage_of_users": 11.8,
                "percentage_of_posts": 1
            },
            {
                "start_at": "2024-03-28T10:00:00Z",
                "end_at": "2024-03-28T12:00:00Z",
                "percentage_of_users": 24.1,
                "percentage_of_posts": 2.5
            },
            {
                "start_at": "2024-03-28T12:00:00Z",
                "end_at": "2024-03-28T14:00:00Z",
                "percentage_of_users": 33.5,
                "percentage_of_posts": 3.4
            },
            {
                "start_at": "2024-03-28T14:00:00Z",
                "end_at": "2024-03-28T16:00:00Z",
                "percentage_of_users": 45,
                "percentage_of_posts": 5
            },
            {
                "start_at": "2024-03-28T16:00:00Z",
                "end_at": "2024-03-28T18:00:00Z",
                "percentage_of_users": 52,
                "percentage_of_posts": 5.4
            },
            {
                "start_at": "2024-03-28T18:00:00Z",
                "end_at": "2024-03-28T20:00:00Z",
                "percentage_of_users": 59,
                "percentage_of_posts": 7.4
            },
            {
                "start_at": "2024-03-28T20:00:00Z",
                "end_at": "2024-03-28T22:00:00Z",
                "percentage_of_users": 61.4,
                "percentage_of_posts": 8.4
            },
            {
                "start_at": "2024-03-28T22:00:00Z",
                "end_at": "2024-03-29T00:00:00Z",
                "percentage_of_users": 80.2,
                "percentage_of_posts": 12.4
            }
        ]

    # Define the session start and end times
    session_start_time = "2024-03-27T01:00:00Z"
    session_end_time = "2025-03-27T23:00:00Z"

    # Get a sampled time
    sampled_time = sample_time(user_distribution, session_start_time, session_end_time)

    # Print the sampled time
    print("Sampled Time:", sampled_time)