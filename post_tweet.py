import os
import tweepy


def post_image_tweet(image_path):
    """Upload an image and post a tweet with no caption (image only)."""
    # OAuth 1.0a credentials from environment variables
    api_key = os.environ["TWITTER_API_KEY"]
    api_secret = os.environ["TWITTER_API_SECRET"]
    access_token = os.environ["TWITTER_ACCESS_TOKEN"]
    access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

    # v1.1 auth for media upload
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api_v1 = tweepy.API(auth)

    # v2 client for creating the tweet
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    # Upload media via v1.1
    media = api_v1.media_upload(filename=image_path)

    # Create tweet with media, no text caption
    response = client.create_tweet(media_ids=[media.media_id])

    print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")
    return response.data["id"]


if __name__ == "__main__":
    # For manual testing
    post_image_tweet("test_output.png")
