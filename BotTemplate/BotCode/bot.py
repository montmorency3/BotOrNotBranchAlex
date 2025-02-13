from abc_classes import ABot
from teams_classes import NewUser, NewPost
import json
import openai
import os
import random
from datetime import datetime, timedelta



# client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = os.getenv('ENV_VAR1')
keywords = []
times = []

class Bot(ABot):
    @staticmethod
    def random_time(start_date: str, end_date: str) -> str:
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        output_format = "%Y-%m-%dT%H:%M:%S.000Z"  # Force milliseconds to .000Z
        
        start = datetime.strptime(start_date, date_format)
        end = datetime.strptime(end_date, date_format)

        random_seconds = random.randint(0, int((end - start).total_seconds()))
        random_datetime = start + timedelta(seconds=random_seconds)

        return random_datetime.strftime(output_format)  # Use correct format

    def create_user(self, session_info):
        #print("CREATE this has triggered")
        output = session_info.__dict__.get('metadata', None)

        topics = output['topics']

        times = output['user_distribution_across_time']
        #print("PRINTING TIMES")
        #print(times)

        for topic in topics:
            keywords.append(topic['keywords'])

        #print(keywords)
        with open("create_user.txt", "w") as file:
            json.dump(output, file)


        #print(dict(list(session_info.__dict__.items())[:10]))
        # todo logic
        # Example:

        new_users = [
            NewUser(username="asapRunny", name="Felix Donovan", description="Yup, i'm that guy"),
        ]
        return new_users

    def generate_content(self, datasets_json, users_list):


        #print("GENERATE CONTENT HAS BEEN CALLED")
        output = datasets_json.__dict__
        with open("generate.txt", "a") as file:
            json.dump(output, file, indent=4)

        #we are subtracting one from the subsessionID in order to be able to index from the list
        subsessionID = output['sub_session_id'] - 1

        outputPosts = output['posts']
        numSamples = 5

        startTime = outputPosts[0]['created_at']
        endTime = outputPosts[len(outputPosts)-1]['created_at']
        randomTweets = random.sample(outputPosts, numSamples)
        sample_posts = []



        for i in range(numSamples):
            sample_posts.append(randomTweets[i]['text'])

            

        # todo logic
        # It needs to return json with the users and their description and the posts to be inserted.
        # Example:
        posts = []
        session_keywords = ' '.join(keywords[subsessionID])
        sample_posts = "\n".join(sample_posts)
        #print(sample_posts)

        prompt = f"""
        You are a human being tweeting on Twitter.

        Your task is to create a tweet that sounds like a real person wrote it. 

        Here are some example tweets from a real user. Your tweet must closely follow the tone, phrasing, and style of these examples:

        {sample_posts}

        Your tweet should be in the same style as these examples.  
        It must be casual, engaging, and feel natural.  

        **Keyword:** "{session_keywords}"  
        **Now, generate a tweet that matches the examples above.**
        """
        for j in range(5):
            response = client.chat.completions.create(
            model="gpt-4",  # Or "gpt-3.5-turbo"
            messages=[
            {"role": "system", "content": "You are a social media content writer."},
            {"role": "user", "content": prompt},
            ])
            tweet = response.choices[0].message.content
            posts.append(NewPost(text=tweet, author_id=users_list[0].user_id, created_at=Bot.random_time(startTime, endTime),user=users_list[0]))
        return posts
    
    
