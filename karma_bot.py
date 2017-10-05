#!/usr/bin/env python

import discord
import asyncio
import praw

from bot import *

client = discord.Client()

reddit = praw.Reddit(client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    password=PASSWORD,
                    user_agent=USER_AGENT,
                    username=USERNAME)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!karma'):
        user = message.content[len('!karma '):].strip()
        karma = 0
        u = reddit.redditor(user)

        for c in u.comments.new(limit=None):
            if c.subreddit.display_name == 'SeattleWA':
                karma += c.score

        await client.send_message(message.channel, 'User {} has {} karma in r/SeattleWA'.format(user, karma))

client.run(DISCORD_TOKEN)
