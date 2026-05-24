import os
import sys
import requests
from dotenv import load_dotenv
from generate_image import generate_verse_image
from post_tweet import post_image_tweet

load_dotenv()

API_URL = "https://labs.bible.org/api/?passage=random&type=json"
MAX_RETRIES = 5
MIN_LENGTH = 30
MAX_LENGTH = 300
OUTPUT_IMAGE = "verse_post.png"


def fetch_random_verse():
    """Fetch a random verse from labs.bible.org API with retry logic."""
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(API_URL, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data:
                continue

            verse_data = data[0]
            text = verse_data.get("text", "").strip()
            bookname = verse_data.get("bookname", "")
            chapter = verse_data.get("chapter", "")
            verse = verse_data.get("verse", "")

            # Clean up HTML tags that sometimes appear in the response
            text = text.replace("<b>", "").replace("</b>", "")
            text = text.replace("<i>", "").replace("</i>", "")
            text = text.replace("&mdash;", "\u2014")
            text = text.replace("&ldquo;", "\u201c").replace("&rdquo;", "\u201d")
            text = text.replace("&lsquo;", "\u2018").replace("&rsquo;", "\u2019")
            text = text.replace("&amp;", "&")

            # Check length constraints
            if len(text) < MIN_LENGTH or len(text) > MAX_LENGTH:
                print(f"Attempt {attempt + 1}: Verse too short/long ({len(text)} chars), retrying...")
                continue

            reference = f"{bookname} {chapter}:{verse}"
            print(f"Fetched verse: {reference}")
            return text, reference

        except (requests.RequestException, ValueError, KeyError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            continue

    print("ERROR: Failed to fetch a suitable verse after all retries.")
    sys.exit(1)


def main():
    """Main workflow: fetch verse → generate image → post to Twitter."""
    print("Fetching random Bible verse...")
    verse_text, reference = fetch_random_verse()
    print(f"Verse: \"{verse_text}\" \u2013 {reference}")

    print("Generating poster image...")
    image_path = generate_verse_image(verse_text, reference, OUTPUT_IMAGE)
    print(f"Image saved to: {image_path}")

    print("Posting to Twitter...")
    tweet_id = post_image_tweet(image_path)
    print(f"Done! Tweet ID: {tweet_id}")

    # Clean up the generated image
    if os.path.exists(OUTPUT_IMAGE):
        os.remove(OUTPUT_IMAGE)


if __name__ == "__main__":
    main()
