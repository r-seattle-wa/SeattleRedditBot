# Seattle Reddit Bot

[![pipeline status](https://gitlab.com/seattlewa/SeattleRedditBot/badges/master/pipeline.svg)](https://gitlab.com/seattlewa/SeattleRedditBot/commits/master)

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

The post template is defined in templates/daily_post.j2.

### daily_markov.py - Text Generation

Generates quotes and haikus using Markov chains trained on recent subreddit comments:

- get_quote(): Generates a random quote from subreddit comment history
- get_haiku(): Generates a 5-7-5 syllable haiku for Fri-ku-day

### karma_bot.py - Discord Karma Checker

Discord bot that checks Reddit karma for users. Commands:

- !karma username: Shows user karma in r/SeattleWA
- !topkarma username: Shows user top 5 subreddits by karma
- !bottomkarma username: Shows user bottom 5 subreddits by karma

Note: Uses deprecated Discord.py API (send_message). May need updates for current Discord.py versions.

### haiku.py - Haiku Generator

Syllable-counting haiku generator (by @odemiral). Constructs 5-7-5 haikus from input text using heuristic syllable counting.

## Project Structure

SeattleRedditBot/
  daily_post.py          - Main daily post generator
  daily_markov.py        - Markov chain text generation
  karma_bot.py           - Discord karma lookup bot
  haiku.py               - Haiku generator module
  bot.py                 - Configuration file (not in repo)
  moon_phases.json       - Precomputed moon phase data
  requirements.txt       - Python dependencies
  Dockerfile             - Container definition
  .gitlab-ci.yml         - CI/CD pipeline
  templates/
    daily_post.j2        - Jinja2 template for daily post
  aws_resources/
    ecs_task_definition.json
    fargate_event_target.json

## Configuration

Create a bot.py configuration file in the project root:

    # Discord API Token (for karma_bot.py)
    DISCORD_TOKEN = your-discord-token

    # Reddit API credentials
    REDDIT_CLIENT_ID = your-client-id
    REDDIT_CLIENT_SECRET = your-client-secret
    REDDIT_PASSWORD = your-bot-password
    REDDIT_USERNAME = your-bot-username
    REDDIT_USER_AGENT = A praw based bot for r/SeattleWA

    # Target subreddit (without r/ prefix)
    REDDIT_SUB = SeattleWA

    # Markov chain state size (recommended: 2)
    STATE_SIZE = 2

### Getting Reddit API Credentials

1. Go to https://www.reddit.com/prefs/apps
2. Click create another app...
3. Select script as the app type
4. Note your client ID (under the app name) and client secret

### Getting Discord API Token

1. Go to https://discord.com/developers/applications
2. Create a new application
3. Go to Bot section and create a bot
4. Copy the token

## Installation

    pip install -r requirements.txt
    python daily_post.py
    python karma_bot.py

## Deployment

The bot is designed to run on AWS Fargate with CloudWatch Events triggering the daily post. The GitLab CI/CD pipeline handles:

1. Building the Docker image
2. Pushing to Amazon ECR
3. Updating the Fargate task definition
4. Configuring CloudWatch Events scheduling

See .gitlab-ci.yml and aws_resources/ for deployment configuration.

## Dependencies

- praw: Reddit API wrapper
- discord.py: Discord API wrapper
- markovify: Markov chain text generation
- jinja2: Template engine
- requests: HTTP client for NWS weather API
- unidecode: Unicode text normalization

## Data Files

### moon_phases.json

Contains precomputed moon phase transitions. This file needs periodic updates to extend coverage beyond its current date range.

## License

Apache-2.0
