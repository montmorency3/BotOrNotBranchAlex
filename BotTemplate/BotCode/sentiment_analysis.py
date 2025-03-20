from transformers import pipeline
import json
import matplotlib.pyplot as plt



def load_human_data(filepath):
    humanPosts = []
    try:
        with open(filepath, 'r') as file:
            # Read the first object from the file
            obj = json.load(file)
            
            # Process the object (e.g., extracting posts)
            for post in obj.get("posts", []):
                humanPosts.append(post["text"])
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        exit()  # Exit the script when an error occurs

    return humanPosts


def load_bot_data(inputfile):
    botPosts = []
    with open(inputfile, 'r') as file:
        data = file.readlines()  # Assuming each post is on a new line

    for botPost in data:
        botPosts.append(botPost.strip())
    return botPosts


def calculateHumanSentiemnts(filepath):
    pipe = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")

    humanPosts = load_human_data(filepath)
    humanPostsSentiment = {"Very Negative": 0, "Negative": 0,  "Neutral": 0, "Positive": 0, "Very Positive": 0}

    for index, text in enumerate (humanPosts):
        print(text)
        result = pipe(text)
        label = result[0]["label"]
        print("Index: "+ str(index) + " ||| Sentiment: "+ label )
        humanPostsSentiment[label] += 1

    print(humanPostsSentiment)

def calculateBotSentiments(filepath):
    pipe = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")

    botPosts = load_bot_data('botPosts.txt')
    botPostsSentiment = {"Very Negative": 0, "Negative": 0,  "Neutral": 0, "Positive": 0, "Very Positive": 0}
    
    for index, text in enumerate (botPosts):
        result = pipe(text)
        label = result[0]["label"]
        if label == "Very Negative":
            print(text)
        print("Index: "+ str(index) + " ||| Sentiment: "+ label )
        botPostsSentiment[label] += 1

    return botPostsSentiment
    print(botPostsSentiment)


def plot_sentiment_counts(sentiment_counts):
    # Compute total count
    total = sum(sentiment_counts.values())

    # Convert counts to proportions
    proportions = {label: count / total for label, count in sentiment_counts.items()}

    # Extract labels and proportion values
    labels = list(proportions.keys())
    values = list(proportions.values())

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color=['red', 'orange', 'gray', 'green', 'blue'])

    # Add title and labels
    plt.title('Sentiment Proportions')
    plt.xlabel('Sentiment')
    plt.ylabel('Proportion')

    # Format y-axis to show percentages
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))

    # Show the plot
    plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability
    plt.tight_layout()  # Ensure labels fit in the plot area
    plt.show()



if __name__ == "__main__":

    #calculateHumanSentiemnts('id13posts.json')
    #{'Very Negative': 1078, 'Negative': 374, 'Neutral': 1763, 'Positive': 333, 'Very Positive': 1374}
    #{'Very Negative': 13, 'Negative': 1, 'Neutral': 14, 'Positive': 2, 'Very Positive': 23}
    human = {'Very Negative': 1078, 'Negative': 374, 'Neutral': 1763, 'Positive': 333, 'Very Positive': 1374}
    #bot = {'Very Negative': 13, 'Negative': 1, 'Neutral': 14, 'Positive': 2, 'Very Positive': 23}
    bot = calculateBotSentiments("botPosts.txt")
    #plot_sentiment_counts( human )
    plot_sentiment_counts( bot ) 