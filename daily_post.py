#!/usr/bin/env python

import datetime
import jinja2
import praw
import requests
import time


from bot import *
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

reddit = praw.Reddit(client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    password=PASSWORD,
                    user_agent=USER_AGENT,
                    username=USERNAME)

subreddit = reddit.subreddit('SeattleWARedditBot')

now = datetime.datetime.now()

def get_weather():
    resp = requests.get('http://forecast.weather.gov/MapClick.php?lat=47.62&lon=-122.36&unit=0&lg=english&FcstType=text&TextType=1')
    doc = resp.content
    soup_doc = BeautifulSoup(doc, 'html.parser')
    weather_info = soup_doc.findAll('table')[1]
    forecast = weather_info.contents[0].text
    reddit_comment = '* ' + str.replace(forecast, '\n\n',"\n* ")[:-3]

    return(reddit_comment)

def gen_post():
    j2_env = Environment(loader=FileSystemLoader('./templates'),trim_blocks=True)
    template = j2_env.get_template('daily_post.j2')

    return(template.render(forecast=get_weather()))


subreddit.submit(title=now.strftime("Seattle Reddit Community Open Chat, %A, %B %d, %Y"), 
                 selftext=gen_post(),
                 url=None, 
                 resubmit=True, 
                 send_replies=False)
