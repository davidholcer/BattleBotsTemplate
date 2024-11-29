#imports
from abc_classes import ABot
from teams_classes import NewUser, NewPost
from chat_gpt import generateTweets, generateUsers
from getTime import sample_time
from div_array import divide_into_random_subarrays
from generateTypos import augmentTweets
import os
import random

#defines
NUM_USERS=5

class Bot(ABot):
    def get_normal_subset(self, ap, sd_ap, minsize, totTweets, tweets):
        # Generate a normal sample
        n = int(random.gauss(ap, sd_ap))
        
        # Ensure n is within bounds
        n = max(minsize, min(n, totTweets))
        
        # Get a random subset of size n
        subset = random.sample(tweets, n)
        
        return subset

    def create_user(self, session_info):
        # todo logic
        # Example:
        self.session_info = session_info
        # session_info

        #to model normal dist
        self.aP=session_info.metadata['users_average_amount_posts']
        self.sd_aP=self.aP/4

        #get user info
        users=generateUsers()

        # add user info
        new_users=[]
        for i in range(min(len(users),NUM_USERS)):
            new_users.append(NewUser(username=users[i]['username'],name=users[i]['name'],description=users[i]['description'],location=users[i]['location']   ))

        self.users_post_info = {}
        # Populate the dictionary with data from each user's file
        for user in new_users:
            tweets=generateTweets()
            tweets=augmentTweets(tweets)
            totSessions=len(self.session_info.sub_sessions_info)
            # print(self.session_info)
            totTweets=len(tweets)
            desiredTweets=self.get_normal_subset(self.aP, self.sd_aP, 10, totTweets, tweets)
            # print(len(desiredTweets))
            # print(desiredTweets)

            self.users_post_info[user.username] = divide_into_random_subarrays(desiredTweets,totSessions)
        # print(self.users_post_info)

        return new_users

    def generate_content(self, datasets_json, users_list):
        # todo logic
        # It needs to return json with the users and their description and the posts to be inserted.
        # Example:
        sessionNum=datasets_json.sub_session_id
        # print("SESSION:",sessionNum,"\n")
        # print(self.session_info.sub_sessions_info)
        
        sessionStartTime=self.session_info.sub_sessions_info[sessionNum-1]["start_time"]
        sessionEndTime=self.session_info.sub_sessions_info[sessionNum-1]["end_time"]

        posts = []

        for j in range(len(users_list)):
            username=users_list[j].username
            curUser=users_list[j]
            userId=users_list[j].user_id

            try:
                subsesh_tweets_by_user=self.users_post_info[username][sessionNum-1]
            except IndexError:
                subsesh_tweets_by_user=[]

        
            totTweets=len(subsesh_tweets_by_user)

            # allTimes=select_random_time(self.session_info.sub_sessions_info,sessionNum,totTweets)
            # allTimes=getProbTime(self.timeDistribution)
            # print("TIMES",allTimes,"\n")

            for i in range(totTweets):
                tweetTime=sample_time(self.session_info.metadata["user_distribution_across_time"], sessionStartTime, sessionEndTime)
                posts.append(NewPost(text=subsesh_tweets_by_user[i], author_id=userId, created_at=tweetTime, user=curUser))
            # posts.append(NewPost(text="Pandas are amazing!", author_id=users_list[j].user_id, created_at='2024-08-18T00:20:30.000Z',user=users_list[j]))

        return posts
        
        
        