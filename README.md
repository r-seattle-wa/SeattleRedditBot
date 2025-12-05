# Seattle Reddit Bot

A collection of bots for the r/SeattleWA Reddit community and Discord server.

## Features

### daily_post.py - Daily Community Thread Generator

Creates and posts the daily Seattle Reddit Community Open Chat thread to r/SeattleWA. Each post includes:

- **Event Calendars**: Links to local Seattle event listings (MoPOP, The Stranger, Seattle Met, etc.)
- **Weather Forecast**: 2-day forecast from the National Weather Service with emoji representations
- **Moon Phases**: Current moon phase displayed with the weather
- **Quote of the Day**: Markov chain-generated quote from recent subreddit comments
- **Fri-ku-day**: On Fridays, generates a haiku instead of a quote
- **Community Links**: Discord server invite and archive links

### daily_markov.py - Text Generation

Generates quotes and haikus using Markov chains trained on recent subreddit comments:

- `get_quote()`: Generates a random quote from subreddit comment history
- `get_haiku()`: Generates a 5-7-5 syllable haiku for Fri-ku-day

### karma_bot.py - Discord Karma Checker

Discord bot that checks Reddit karma for users. Commands:

- `!karma username`: Shows user karma in r/SeattleWA
- `!topkarma username`: Shows user top 5 subreddits by karma
- `!bottomkarma username`: Shows user bottom 5 subreddits by karma

### haiku.py - Haiku Generator

Syllable-counting haiku generator. Constructs 5-7-5 haikus from input text using heuristic syllable counting.

## Project Structure

```
SeattleRedditBot/
├── daily_post.py       # Main daily post generator
├── daily_markov.py     # Markov chain text generation
├── karma_bot.py        # Discord karma lookup bot
├── haiku.py            # Haiku generator module
├── bot.py              # Configuration file (create this)
├── moon_phases.json    # Precomputed moon phase data
├── requirements.txt    # Python dependencies
└── templates/
    └── daily_post.j2   # Jinja2 template for daily post
```

## Configuration

Create a `bot.py` configuration file:

```python
DISCORD_TOKEN = 'your-discord-token'
REDDIT_CLIENT_ID = 'your-client-id'
REDDIT_CLIENT_SECRET = 'your-client-secret'
REDDIT_PASSWORD = 'your-bot-password'
REDDIT_USERNAME = 'your-bot-username'
REDDIT_USER_AGENT = 'A praw based bot for r/SeattleWA'
REDDIT_SUB = 'SeattleWA'
STATE_SIZE = 2
```

## Installation

```bash
pip install -r requirements.txt
python daily_post.py
```

## License

Apache-2.0
