#!/usr/bin/env python

import datetime
import jinja2
import praw
import requests
import time
import markovify
from unidecode import unidecode
import re
import random


from bot import *
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader


STATE_SIZE = 2
INFO_URL = 'https://github.com/trambelus/UserSim'
SUB_URL = '/r/User_Simulator'
SUB = 'SeattleWA'

FOOTER = '\n\n-----\n\n[^^Info](%s) ^^| [^^Subreddit](%s)' % (INFO_URL, SUB_URL)

reddit = praw.Reddit(client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    password=PASSWORD,
                    user_agent=USER_AGENT,
                    username=USERNAME)

subreddit = reddit.subreddit(SUB)

now = datetime.datetime.now()


class PText(markovify.Text):

    def test_sentence_input(self, sentence):
        emote_pat = re.compile(r"\[.+?\]\(\/.+?\)")
        reject_pat = re.compile(r"(^')|('$)|\s'|'\s|([\"(\(\)\[\])])|(github.com/trambelus/UserSim)|(/r/User_Simulator)|(~\ [\w\d\-_]{3,20}\ -----)")
        decoded = unidecode(sentence)
        filtered_str = re.sub(emote_pat, '', decoded).replace('  ', ' ')
        if re.search(reject_pat, filtered_str):
            return False
        if filtered_str in FOOTER:
            return False
        return True


def get_history():
    try:
        comments = subreddit.comments(limit=1000)
        if comments is None:
            return None, None, None
        c_finished = False
        while not c_finished:
            body = []
            total_sentences = 0
            try:
                for c in comments:
                    if (not c.distinguished) and ((not subreddit) or c.subreddit.display_name == subreddit):
                        body.append(c.body)
                        try:
                            total_sentences += len(markovify.split_into_sentences(c.body))
                        except Exception:
                            total_sentences += 1
                c_finished = True
            except praw.exceptions.PRAWException as ex:
                pass
        num_comments = len(body)
        sentence_avg = total_sentences / num_comments if num_comments > 0 else 0
        body = ' '.join(body)
        return body, num_comments, sentence_avg

    except praw.exceptions.PRAWException:
        pass


def get_markov():
    (history, num_comments, sentence_avg) = get_history()
    try:
        model = PText(history, state_size=STATE_SIZE)
        model = PText(history, state_size=STATE_SIZE, chain=model.chain)
    except IndexError:
        return "Error: subreddit '" + SUB + "' is too dank to simulate.", 0
    return model, int(sentence_avg)


def get_weather():
    resp = requests.get('http://forecast.weather.gov/MapClick.php?lat=47.62&lon=-122.36&unit=0&lg=english&FcstType=text&TextType=1')
    doc = resp.content
    soup_doc = BeautifulSoup(doc, 'html.parser')
    weather_info = soup_doc.find_all('table')[1]
    reddit_comment = ''
    if weather_info.find_all('div'):
        advisories = weather_info.div.extract().find_all('a')
        reddit_comment += '* Advisories:\n'
        for advis in advisories:
            reddit_comment += ' * [{}](http://forecast.weather.gov/{})\n'.format(advis.span.string, advis.get('href'))
    forecast = str(weather_info).split("<br/>\n<br/>")
    top_three = '<br/>\n<br/>'.join(str(x) for x in forecast[1:5])
    top_three_doc = BeautifulSoup(top_three, 'html.parser')
    reddit_comment += '* ' + str.replace(top_three_doc.text, '\n\n', "\n* ")[:-3]

    return reddit_comment


def gen_post():
    j2_env = Environment(loader=FileSystemLoader('./templates'),trim_blocks=True)
    template = j2_env.get_template('daily_post.j2')
    quote_of_the_day = ""
    (model, sentence_avg) = get_markov()
    if isinstance(model, str):
        quote_of_the_day = ((model % '/r/' + SUB) + FOOTER)
    else:
        quote_r = []
        if sentence_avg > 0:
            for _ in range(random.randint(1, sentence_avg)):
                tmp_s = model.make_sentence(tries=1000)
                if tmp_s is None:
                    break
                quote_r.append(tmp_s)
                quote_of_the_day = '> %s\n\n> ~ %s%s' % (unidecode(' '.join(quote_r)), '/r/' + SUB, FOOTER)

    return template.render(forecast=get_weather(), qotd=quote_of_the_day)


print(gen_post())


subreddit.submit(title=now.strftime("Seattle Reddit Community Open Chat, %A, %B %d, %Y"),
                 selftext=gen_post(),
                 url=None,
                 resubmit=True,
                 send_replies=False)
