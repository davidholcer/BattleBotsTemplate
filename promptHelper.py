import json
import re
import random

# List of filenames to read
FILENAMES = ["session_3_results.json", "session_4_results.json", "session_5_results.json"]

# Function to clean and load JSON data
def load_and_clean_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        raw_data = f.read()
    # Clean improperly escaped emojis
    cleaned_data = re.sub(r'\\([^n"\\\s])\\?', r'\1', raw_data)
    # Validate and return the JSON data
    try:
        return json.loads(cleaned_data)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError in {filename}: {e}")
        return {"posts": []}  # Return empty structure if there's an error

# Combine all posts from multiple files
all_posts = []
all_users=[]
for filename in FILENAMES:
    data = load_and_clean_json(filename)
    all_posts.extend(data.get('posts', []))
    all_users.extend(data.get('users', []))

# print(all_users[0])

# Separate posts by bots (alphanumeric) vs real accounts (numeric)
bot_posts = []
real_posts = []

# Function to check if author_id is bot (alphanumeric) or real (numeric)
def is_bot(author_id):
    return any(char.isalpha() for char in author_id)

for post in all_posts:
    if is_bot(post['author_id']):
        bot_posts.append(post)
    else:
        real_posts.append(post)

random.shuffle(real_posts)

# Generate a random prompt from the real posts
def getTweets(n=50):
    prompt = ""
    selected_posts = random.sample(real_posts, min(n, len(real_posts)))  # Avoid IndexError if n > len(real_posts)
    for i, post in enumerate(selected_posts, 1):
        prompt += f"{i}: \"{post['text']}\"\n"
    return prompt

real_users=[]
for user in all_users:
    if not user['is_bot']:
        real_users.append(user)

random.shuffle(real_users)
# print(real_users[0])

def getUsernames(n=50):
    prompt = ""
    selected_users = random.sample(real_users, min(n, len(real_users)))  # Avoid IndexError if n > len(real_posts)
    for i, user in enumerate(selected_users, 1):
        prompt += f"{i}: Name - \"{user['name']}\" username - \"{user['username']}\" description - \"{user['description']}\" location - \"{user['location']}\"\n"
    return prompt

# print(getUsernames(50))