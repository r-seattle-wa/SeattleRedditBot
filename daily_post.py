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

subreddit = reddit.subreddit('SeattleWA')

now = datetime.datetime.now()


def get_weather():
    resp = requests.get('http://forecast.weather.gov/MapClick.php?lat=47.62&lon=-122.36&unit=0&lg=english&FcstType=text&TextType=1')
    doc = resp.content
    soup_doc = BeautifulSoup(doc, 'html.parser')
    weather_info = soup_doc.find_all('table')[1].contents[0].contents[0]
    reddit_comment = ''
    if len(weather_info.find_all('div')) > 0:
        advisories = weather_info.div.extract().find_all('a')
        reddit_comment += '* Advisories: \n'
        for advis in advisories:
            reddit_comment += ' * {}\n'.format(advis.span.string)
    forecast = str(weather_info).split("<br/>\n<br/>")
    top_three = '<br/>\n<br/>'.join(str(x) for x in forecast[1:5])
    top_three_doc = BeautifulSoup(top_three, 'html.parser')
    reddit_comment += '* ' + str.replace(top_three_doc.text, '\n\n', "\n* ")[:-3]

    return reddit_comment


def gen_post():
    j2_env = Environment(loader=FileSystemLoader('./templates'),trim_blocks=True)
    template = j2_env.get_template('daily_post.j2')

    return template.render(forecast=get_weather())


subreddit.submit(title=now.strftime("Seattle Reddit Community Open Chat, %A, %B %d, %Y"),
                 selftext=gen_post(),
                 url=None,
                 resubmit=True,
                 send_replies=False)
