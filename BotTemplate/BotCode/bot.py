from abc_classes import ABot
from teams_classes import NewUser, NewPost
import json
import openai
import os
import random
from datetime import datetime, timedelta

# client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#CHANGE TO THIS FOR COMPETITION
client = openai.OpenAI(api_key=os.getenv('ENV_VAR1'))

keywords = []
times = []

class Bot(ABot):
    @staticmethod

    #This method returns a random time between the given start and end date
    def random_time(start_date: str, end_date: str) -> str:
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        output_format = "%Y-%m-%dT%H:%M:%S.000Z"  # Force milliseconds to .000Z
        
        start = datetime.strptime(start_date, date_format)
        end = datetime.strptime(end_date, date_format)

        random_seconds = random.randint(0, int((end - start).total_seconds()))
        random_datetime = start + timedelta(seconds=random_seconds)

        return random_datetime.strftime(output_format)  # Use correct format


    def create_user(self, session_info):
        output = session_info.__dict__.get('metadata', None)
        topics = output['topics']

        for topic in topics:
            keywords.append(topic['keywords'])

        #writes the meta data to a file
        with open("metaData.json", "w") as file:
            json.dump(output, file)

        #create the list of users to return
        new_users = [
            NewUser(username="orealways3", name="John Danaher", description="Im just a chill guy"),
        ]
        return new_users


    def generate_content(self, datasets_json, users_list):
        #write the posts to a file for debugging 
        output = datasets_json.__dict__
        with open("posts.json", "w") as file:
            json.dump(output, file, indent=4)

        #we are subtracting one from the subsessionID in order to be able to index from the list
        subsessionID = output['sub_session_id'] - 1

        #choosing 5 posts to give the bot as an example
        outputPosts = output['posts']
        numSamples = 5
        randomTweets = random.sample(outputPosts, numSamples)
        sample_posts = []
        for i in range(numSamples):
            sample_posts.append(randomTweets[i]['text'])

        #defining start time and end time to create random times for posting later
        startTime = outputPosts[0]['created_at']
        endTime = outputPosts[len(outputPosts)-1]['created_at']

        # todo logic: It needs to return json with the users and their description and the posts to be inserted.
        posts = []
        session_keywords = ' '.join(keywords[subsessionID])
        sample_posts = "\n".join(sample_posts)

        prompt = f"""
        You are a human being tweeting on Twitter.

        Your task is to create a tweet that sounds like a real person wrote it. Your tweet should reflect a natural, conversational tone, as if you're interacting with your followers. Make sure to incorporate a range of emotions, just like a real user would in their posts.
        If the example is in french, please write it in french. 
        Here are some example tweets from a real user. Your tweet should match the tone, phrasing, and style of these examples:

        {sample_posts}

        **Keyword(s):** "{session_keywords}"  
        - Keep the tweet conversational, and avoid overusing hashtags or other trending elements. 
        - Focus on how the keyword(s) can be woven into the tweet naturally. 
        - No need to cram in multiple hashtags; just a few or none at all, depending on how it fits. 
        - Try to keep the tweet short, punchy, and reflective of the emotion or situation expressed in the sample posts.
        - Please make them around the average 28 character mark 
        Now, generate a tweet that matches the examples above and feels like a real post on Twitter.
        """


        for j in range(5):
            response = client.chat.completions.create(
            model="gpt-4", 
            messages=[
            {"role": "system", "content": "You are a social media content writer."},
            {"role": "user", "content": prompt},
            ])
            tweet = response.choices[0].message.content
            newPost = NewPost(text=tweet, author_id=users_list[0].user_id, created_at=Bot.random_time(startTime, endTime),user=users_list[0])
            posts.append(newPost)

        with open("botPosts.txt", "a") as file:
            for post in posts:
                file.write(post.text + "\n")

        return posts