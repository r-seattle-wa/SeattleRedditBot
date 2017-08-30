#!/usr/bin/python

# import
import praw
import pdb
import re
import os
import time
import datetime

##
# Create the Reddit instance
reddit = praw.Reddit('SeattleRedditBot')

subreddit = reddit.subreddit('seattlewa')
#subreddit = reddit.subreddit('seattleredditbot')

# what's the date and time?
now = datetime.datetime.now()

subreddit.submit(
                 title=now.strftime("Seattle Reddit Community Open Chat, %A, %B %d, %Y"),
#                 selftext='stuff', 
                 selftext=(open('daily-post.txt', 'r').read()),
                 url=None, 
                 resubmit=True, 
                 send_replies=False
                 )
