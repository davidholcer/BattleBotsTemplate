from abc_classes import ABot
from teams_classes import NewUser, NewPost
from getTime import select_random_time
from div_array import divide_into_random_subarrays
import os

class Bot(ABot):
    def create_user(self, session_info):
        # todo logic
        # Example:
        self.session_info = session_info
        new_users = [
            NewUser(username="aaronjayjack", name="Aaron Jayjack", description="Storm Chaser. YouTube, Videographer, Photographer, Livestreamer. Experiencing & documenting extreme weather is my passion. CHASE Your PASSION."),
            NewUser(username="davidholcer", name="David Holcer", description="Creating & Coding: Generative Art, Graphic Design, Digital Music #nftartist  McGill ‘23\uD83C\uDDE6\uD83C\uDDF7 \uD83C\uDDE8\uD83C\uDDE6 \uD83C\uDDFA\uD83C\uDDF8"),
            NewUser(username="bethanybo", name="Bethany Bo", description="I hate fossil fuels. Enought is enough!!!",location="Montreal, QC"),
            NewUser(username="mrmarkov", name="Markov Chainer", description="Predicting the future one word at a time :)",location="Moscow, RS")
        ]

        self.users_post_info = {}
        # Populate the dictionary with data from each user's file
        for user in new_users:
            file_path = f"{user.username}.txt"
            try:
                with open(file_path, 'r') as file:
                    # Read each line, strip any extra whitespace, and store in the dictionary as a list
                    # self.users_post_info[user.username] = [line.strip() for line in file.readlines()]
                    tweets = [line.strip() for line in file.readlines()]
            except FileNotFoundError:
                # print(f"File {user.username}.txt not found.")
                pass
            except Exception as e:
                # print(f"An error occurred while reading {user.username}.txt: {e}")
                pass
            totSessions=len(self.session_info.sub_sessions_info)
            # print(self.session_info)
            self.users_post_info[user.username] = divide_into_random_subarrays(tweets,totSessions)

        # print(self.users_post_info)

        return new_users

    def generate_content(self, datasets_json, users_list):
        # todo logic
        # It needs to return json with the users and their description and the posts to be inserted.
        # Example:
        sessionNum=datasets_json.sub_session_id
        # print("SESSION:",sessionNum,"\n")
        # print(self.session_info.sub_sessions_info)

        posts = []
        for j in range(len(users_list)):
            username=users_list[j].username
            curUser=users_list[j]
            userId=users_list[j].user_id
            subsesh_tweets_by_user=self.users_post_info[username][sessionNum-1]
            totTweets=len(subsesh_tweets_by_user)
            allTimes=select_random_time(self.session_info.sub_sessions_info,sessionNum,totTweets)
            # print("TIMES",allTimes,"\n")

            for i in range(totTweets):
                posts.append(NewPost(text=subsesh_tweets_by_user[i], author_id=userId, created_at=allTimes[i],user=curUser))
            # posts.append(NewPost(text="Pandas are amazing!", author_id=users_list[j].user_id, created_at='2024-08-18T00:20:30.000Z',user=users_list[j]))

        return posts
        
        
        