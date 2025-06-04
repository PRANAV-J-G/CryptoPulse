import praw
from textblob import TextBlob
from kafka import KafkaProducer
import json
import time

# Reddit Authentication
reddit = praw.Reddit(
    client_id='EJry3A0dwgrcP56foFMSEA',
    client_secret='Jgm3zHMZc2TjF-wzb5yPwfqOQH6fvw',
    user_agent='crypto_sentiment_app',
    username='Striking-Sport3015',
    password='pranav._36'
)

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Sentiment Analyzer Function
def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # range: -1 (negative) to 1 (positive)

# Subreddit Sentiment Scraper
def fetch_sentiment_from_subreddit(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.new(limit=10):
        sentiment = get_sentiment(submission.title)
        data = {
            "subreddit": subreddit_name,
            "title": submission.title,
            "sentiment": sentiment,
            "score": submission.score,
            "created": submission.created_utc
        }
        producer.send("crypto_sentiment", data)
        print(f"Produced: {data}")

# Main loop
if __name__ == "__main__":
    while True:
        fetch_sentiment_from_subreddit("cryptocurrency")
        fetch_sentiment_from_subreddit("bitcoin")
        time.sleep(60)
