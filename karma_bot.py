#!/usr/bin/env python
"""
karma_bot.py - Discord Bot for Reddit Karma Lookup

A Discord bot that allows users to check Reddit karma statistics.
Designed for the r/SeattleWA Discord server.

Commands:
    !karma <username>: Shows user's karma in r/SeattleWA
    !topkarma <username>: Shows user's top 5 subreddits by karma
    !bottomkarma <username>: Shows user's bottom 5 subreddits by karma

Configuration:
    Requires bot.py with DISCORD_TOKEN and Reddit API credentials.
"""
from typing import Dict
from collections import defaultdict
import operator

import discord
import praw

from bot import *

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     password=PASSWORD,
                     user_agent=USER_AGENT,
                     username=USERNAME)


@client.event
async def on_ready() -> None:
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


def get_user_subreddit_karma(user: str) -> Dict[str, int]:
    """
    Calculate karma breakdown by subreddit for a Reddit user.

    Args:
        user: Reddit username to look up

    Returns:
        Dictionary mapping subreddit names to karma totals
    """
    karma = defaultdict(int)
    reddit_user = reddit.redditor(user)

    for comment in reddit_user.comments.new(limit=None):
        karma[comment.subreddit.display_name] += comment.score

    return karma


@client.event
async def on_message(message: discord.Message) -> None:

    if message.author == client.user:
        return

    message_parts = message.content.split()

    if len(message_parts) < 2:
        return

    command, user = message_parts[0], message_parts[1]

    if command == '!karma':
        sub_karma = 0
        reddit_user = reddit.redditor(user)

        for comment in reddit_user.comments.new(limit=None):
            if comment.subreddit.display_name == 'SeattleWA':
                sub_karma += comment.score

        await message.channel.send(f'User {user} has {sub_karma} karma in r/SeattleWA')

    elif command == '!topkarma':
        all_karma = get_user_subreddit_karma(user)
        top_five = sorted(all_karma.items(), key=operator.itemgetter(1), reverse=True)[:5]

        await message.channel.send(f'Top 5 karma for user {user}: {top_five}')

    elif command == '!bottomkarma':
        all_karma = get_user_subreddit_karma(user)
        bottom_five = sorted(all_karma.items(), key=operator.itemgetter(1))[:5]

        await message.channel.send(f'Bottom 5 karma for user {user}: {bottom_five}')


if __name__ == '__main__':
    client.run(DISCORD_TOKEN)
