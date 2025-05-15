import praw
import datetime
import time
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Reddit API configuration
reddit = praw.Reddit(client_id="5nQ6YKGv6wqcJOpAcXFDGg",
                     client_secret="7N_IBjX2qNGaMOkUUarSa_WldAFMog",
                     user_agent="DigitalSentimentAnalysisApp/1.0")

# Subreddits and search terms
subreddits = ["mentalhealth", "anxiety", "depression", "stress", "bipolarreddit", "CPTSD", "schizophrenia"]
search_terms = ["stress", "anxiety", "depression", "sadness", "happiness", "mental health support", "emotional support", "wellbeing", "crisis"]
post_limit = 10
max_comments_per_post = 5
time_filter = "all"

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    if text:
        vs = analyzer.polarity_scores(text)
        return vs['compound']
    return None

def collect_reddit_data():
    post_data = []
    post_ids = set()
    fetched_posts = {}

    for subreddit_name in subreddits:
        print(f"Fetching posts from subreddit: {subreddit_name}")
        subreddit = reddit.subreddit(subreddit_name)
        try:
            for i, post in enumerate(subreddit.search(query=' OR '.join(search_terms),
                                                      sort='relevance', time_filter=time_filter,
                                                      limit=post_limit)):
                if post.id in post_ids:
                    continue
                post_ids.add(post.id)
                sentiment_score = get_sentiment(post.title + " " + post.selftext)
                if sentiment_score is not None:
                    post_data.append({
                        'subreddit': subreddit_name,
                        'id': post.id,
                        'title': post.title,
                        'selftext': post.selftext,
                        'sentiment_score': sentiment_score,
                        'created_utc': datetime.datetime.fromtimestamp(post.created_utc)
                    })
                    fetched_posts[post.id] = post
                if i % 10 == 0 and i > 0:
                    print("Pausing for 2 seconds after 10 posts...")
                    time.sleep(2)
            time.sleep(5)
        except Exception as e:
            print(f"Error in subreddit {subreddit_name}: {e}")

    comment_data = []
    print("\nFetching comments from downloaded posts...")
    for post_id, post in fetched_posts.items():
        try:
            post.comments.replace_more(limit=0)
            comments = post.comments.list()[:max_comments_per_post]
            for i, comment in enumerate(comments):
                sentiment_score = get_sentiment(comment.body)
                if sentiment_score is not None:
                    comment_data.append({
                        'subreddit': post.subreddit.display_name,
                        'post_id': post.id,
                        'comment_id': comment.id,
                        'body': comment.body,
                        'sentiment_score': sentiment_score,
                        'created_utc': datetime.datetime.fromtimestamp(comment.created_utc)
                    })
                if i % 10 == 0 and i > 0:
                    print(f"Pausing for 0.5 seconds after {i+1} comments...")
                    time.sleep(0.5)
            time.sleep(1)
        except Exception as e:
            print(f"Error in post {post_id}: {e}")

    # Create DataFrames
    posts_df = pd.DataFrame(post_data)
    comments_df = pd.DataFrame(comment_data)

    return posts_df, comments_df
