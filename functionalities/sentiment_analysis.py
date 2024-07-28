from textblob import TextBlob

# Function to perform sentiment analysis
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # Range from -1 (negative) to 1 (positive)


def sentiment_change(initial_sentiment, final_sentiment):
    return (final_sentiment - initial_sentiment) * 100
