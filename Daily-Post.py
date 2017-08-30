#!/usr/bin/python

import praw
import os
import time
import datetime

from bot import *

# Create the Reddit instance
reddit = praw.Reddit(client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    password=PASSWORD,
                    user_agent=USER_AGENT,
                    username=USERNAME)

subreddit = reddit.subreddit('seattlewa')

now = datetime.datetime.now()

subreddit.submit(title=now.strftime("Seattle Reddit Community Open Chat, %A, %B %d, %Y"), 
                 selftext=(open('daily-post.txt', 'r').read()),
                 url=None, 
                 resubmit=True, 
                 send_replies=False)
