#imports
# import tiktoken
from pydantic import BaseModel
from openai import OpenAI
from promptHelper import getTweets, getUsernames
import re
# from dotenv import load_dotenv
import os

clearLens = "sk-svcacct-bO-fs6SsL0-EU60RuZEqYdL9BJg9xRPGnvloKqkZZZveZRszo_lUP_YAMeFW348ST3BlbkFJPNSfpXQqhk8ckK4vre9qy0kAinj2DcDbkBH3xSv09EIKgLqmYBTTg7lD6_QcFW4A"
client = OpenAI(api_key=clearLens)

#model definitions
MODEL_NAME = "gpt-4o-mini"
ENCODING_NAME = "o200k_base"

#define sizes
TWEETS_SIZE=60
USERS_SIZE=20

#out file
tweetSaveFile="tweets_response.txt"
userSaveFile="users_response.txt"

#check token count
# encoding = tiktoken.encoding_for_model("gpt-4o-mini")
# def num_tokens_from_string(string: str, encoding_name: str) -> int:
#     """Returns the number of tokens in a text string."""
#     encoding = tiktoken.get_encoding(encoding_name)
#     num_tokens = len(encoding.encode(string))
#     return num_tokens

#example dataset
# Your dataset of tweets (replace this with your actual tweets dataset)
# tweets_dataset = """
# 1: "Char talks about himself, completely unrelated to the matter at hand. He has zero reason to lie here. For the first time this movie, he is being real. And what does he say? \"Lalah was a woman who could've been like a mother to me\"."
# 2: "until the topic of Quess comes up, and how Char manipulated her by using Quess's belief that Char could be a father figure to her. This triggers Char's last words; not a defence of himself or his actions, not a realization that what he's done was wrong, or a display of contrition"
# 3: "Cover art reveal today or monday?"
# 4: "Lalah was the one person to view Char without expectation. He was not the Red Comet, the ace pilot, or Casval Rem Deikun, the saviour of the spacenoids. He was someone she loved, unconditionally. That's all Char wanted; unconditional love, the reassurance of a mother figure."
# 5: "oh my god who is this dickhead on espn2 complaining about the refs reviewing a temple player getting hit in the face to declare a flagrant foul is ruining the sport"
# """

def getResponse(theMessages, model_name=MODEL_NAME, out_response_format="text"):
    response = client.chat.completions.create(
    model=model_name,
    messages=theMessages,
    response_format={
        "type": out_response_format
    },
    temperature=1,
    max_completion_tokens=16384,
    presence_penalty=2.0
    )
    return response

def save_results_to_file(generatedResults, file):
    # generatedResults = results.choices[0].message.content
    with open(file, "a") as f:
        f.write(generatedResults)
    # print(f"Content saved to {file}")


def generateTweets(tweet_sample_size=TWEETS_SIZE):
    tweets_dataset=getTweets(tweet_sample_size)

    # Prompt to generate new tweets
    tweet_prompt = f"""
    Generate tweets in a similar format to the following dataset.:
    {tweets_dataset}
    """
    # print(prompt)
    # print("Total tokens used by tweet prompt: %s"%num_tokens_from_string(tweet_prompt, ENCODING_NAME))

    tweet_message=messages=[
            {"role": "system", "content": "You are a creative assistant that generates realistic tweets. No links, use \"https://t.co/twitter_link\" instead. No mentions, use \"@mention\" instead."},
            {"role": "user", "content": tweet_prompt}
        ]

    tweets_response = getResponse(tweet_message)
    tweets_response_content=tweets_response.choices[0].message.content
    # save_results_to_file(tweets_response_content,tweetSaveFile)

    def parse_tweets(line):
        # Regular expression to capture the content inside quotes
        match = re.search(r': "(.*?)"', line)
        if match:
            return match.group(1)  # Extract the text inside quotes
        else:
            return None

    # Read the file and parse each line
    parsed_tweets = []
    for tweet in tweets_response_content.split('\n'):
        text = parse_tweets(tweet)
        if text:
            parsed_tweets.append(text)
    
    return parsed_tweets


def generateUsers(user_sample_size=USERS_SIZE):
    users_dataset=getUsernames(user_sample_size)
    # print(users_dataset)
    # Prompt to generate new users
    user_prompt = f"""
    Generate user metadata in a similar format to the following dataset.:
    {users_dataset}
    """
    # print(prompt)
    # print("Total tokens used by user prompt: %s"%num_tokens_from_string(user_prompt, ENCODING_NAME))

    user_messages=[
        {"role": "system", "content": "You are a creative assistant that generates realistic twitter user metadata."},
        {"role": "user", "content": user_prompt}
    ]

    users_response = getResponse(user_messages, out_response_format="text")
    users_response_content=users_response.choices[0].message.content
    # save_results_to_file(users_response_content,userSaveFile)

    # Function to parse a single line of user metadata
    def parse_user_metadata(line):
        # Define a regular expression to capture the name, username, and description
        match = re.search(r'Name - "(.*?)" username - "(.*?)" description - "(.*?)" location - "(.*?)"', line)
        if match:
            name = match.group(1)  # Extract Name
            username = match.group(2)  # Extract Username
            description = match.group(3)  # Extract Description
            location = match.group(4)  # Extract Location
            return name, username, description, location
        else:
            return None, None, None, None

    parsed_users = []
    for each_user in users_response_content.split('\n'):
        name, username, description, location = parse_user_metadata(each_user)
        if name and username and description and location:
            parsed_users.append({"name": name, "username": username, "description": description, "location": location})
    return parsed_users

# print(generateUsers())

# Print the parsed data
# for user in parsed_users:
#     print(f"Name: {user['name']}")
#     print(f"Username: {user['username']}")
#     print(f"Description: {user['description']}")
#     print("-" * 40)