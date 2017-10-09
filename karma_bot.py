#!/usr/bin/env python

import asyncio
import discord
import operator
import praw

from bot import *
from collections import defaultdict

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

    def gen_karma_hash(user):
        karma = defaultdict(int)
        u = reddit.redditor(user)
    
        for c in u.comments.new(limit=None):
            karma[c.subreddit.display_name] += c.score

        return karma
            

    if message.author == client.user:
        return

    if message.content.startswith('!karma'):
        user = message.content.split()[1]
        karma = 0
        u = reddit.redditor(user)

        for c in u.comments.new(limit=None):
            if c.subreddit.display_name == 'SeattleWA':
                karma += c.score

        await client.send_message(message.channel, 'User {} has {} karma in r/SeattleWA'.format(user, karma))

    if message.content.startswith('!topkarma'):
        user = message.content.split()[1]
        karma = gen_karma_hash(user)

        top_five = sorted(karma.items(), key=operator.itemgetter(1), reverse=True)[:5]

        await client.send_message(message.channel, 'Top 5 karma for user {}: {}'.format(user, top_five))

        

    if message.content.startswith('!bottomkarma'):
        user = message.content.split()[1]
        karma = gen_karma_hash(user)

        bottom_five = sorted(karma.items(), key=operator.itemgetter(1))[:5]

        await client.send_message(message.channel, 'Bottom 5 karma for user {}: {}'.format(user, bottom_five))

client.run(DISCORD_TOKEN)
