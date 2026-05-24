# Daily Bible Verse Twitter Bot

Automated bot that posts Bible verse poster images to Twitter/X 10 times per day. Each post is an image-only tweet featuring a random verse on a beautiful heavenly gradient background.

## Example Output

![Example verse image](verse_post.png)

## Features

- Random Bible verses from [labs.bible.org](https://labs.bible.org) API (free, no key needed)
- Randomized heavenly gradient backgrounds (blues, purples, golds, teals, etc.)
- Adaptive text color (dark on light backgrounds, white on dark backgrounds)
- Cabin font with consistent bottom-left text placement
- Image size: 4088×2707 px
- Automated via GitHub Actions (10 posts/day)

## Setup

### 1. Twitter API Credentials

You need a [Twitter Developer Account](https://developer.twitter.com/) with Free tier access.

Required credentials:
- API Key
- API Secret
- Access Token
- Access Token Secret

### 2. GitHub Secrets

Add these secrets to your repository (Settings → Secrets and variables → Actions):

| Secret Name | Description |
|---|---|
| `TWITTER_API_KEY` | Twitter API Key |
| `TWITTER_API_SECRET` | Twitter API Secret |
| `TWITTER_ACCESS_TOKEN` | Twitter Access Token |
| `TWITTER_ACCESS_TOKEN_SECRET` | Twitter Access Token Secret |

### 3. Enable GitHub Actions

The workflow runs automatically on the cron schedule. You can also trigger it manually from the Actions tab using "workflow_dispatch".

## Local Testing

```bash
pip install -r requirements.txt

# Test image generation only (no Twitter posting)
python generate_image.py

# Full run (requires env vars set)
export TWITTER_API_KEY=your_key
export TWITTER_API_SECRET=your_secret
export TWITTER_ACCESS_TOKEN=your_token
export TWITTER_ACCESS_TOKEN_SECRET=your_token_secret
python main.py
```

## Schedule

The bot posts at these UTC hours: 01:00, 03:00, 05:00, 07:00, 09:00, 11:00, 13:00, 15:00, 17:00, 19:00

## Project Structure

```
├── main.py                # Orchestrator
├── generate_image.py      # Image generation (Pillow)
├── post_tweet.py          # Twitter API posting (tweepy)
├── assets/
│   └── overlay.png        # Decorative overlay image
├── fonts/
│   └── Cabin-Regular.ttf  # Cabin font
├── requirements.txt
├── pyproject.toml         # Project metadata & dependencies (uv)
├── .env.example           # Template for environment variables
├── .github/workflows/
│   └── post.yml           # GitHub Actions cron workflow
└── README.md
```
