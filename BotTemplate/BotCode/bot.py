from abc_classes import ABot
from teams_classes import NewUser, NewPost

class Bot(ABot):
    def create_user(self, session_info):
        #print(dict(list(session_info.__dict__.items())[:10]))
        #print("*********************************************************************************")
        # todo logic
        # Example:
        new_users = [
            NewUser(username="IAmHuman", name="notBot", description="Hello I'm a human"),
            # NewUser(username="IAmMammal", name="notBot", description="Hello I'm a human"),
            # NewUser(username="IAmApe", name="notBot", description="Hello I'm a human"),
            # NewUser(username="IAmFire", name="notBot", description="Hello I'm a human"),
            # NewUser(username="IAmStone", name="notBot", description="Hello I'm a human"),
            # NewUser(username="IAmLizard", name="notBot", description="Hello I'm a human"),
            # NewUser(username="IAmMachine", name="notBot", description="Hello I'm a human"),
            # NewUser(username="IAmBot", name="notBot", description="Hello I'm a human"),
            # NewUser(username="IAmCrane", name="notBot", description="Hello I'm a human"),
            # NewUser(username="IAmTurner", name="notBot", description="Hello I'm a human"),
        ]
        return new_users

    def generate_content(self, datasets_json, users_list):
       # print(datasets_json.__dict__)
        # todo logic
        # It needs to return json with the users and their description and the posts to be inserted.
        # Example:
        posts = []
        positive_adjectives = ["amazing", "brilliant", "charming", "delightful", "energetic",  "fantastic", "generous", "happy", "inspiring", "joyful", "kind", "lively", "marvelous", "noble", "outstanding"]
        for j in range(11):
            index = hash(str(id(positive_adjectives))) % len(positive_adjectives)  
            tweet = "Pandas are " + positive_adjectives[index]
            posts.append(NewPost(text=tweet, author_id=users_list[0].user_id, created_at='2024-03-17T00:20:30.000Z',user=users_list[0]))
        return posts
