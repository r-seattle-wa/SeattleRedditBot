
import praw
import requests
import time
import markovify
from unidecode import unidecode
import re
import random

from bot import *

FOOTER = '\n\n-----\n\n[^^Info](https://github.com/trambelus/UserSim) ^^| [^^Subreddit](/r/User_Simulator)'


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


def get_history(subreddit):
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


def get_markov(subreddit, SUB):
    (history, num_comments, sentence_avg) = get_history(subreddit)
    try:
        model = PText(history, state_size=STATE_SIZE)
    except IndexError:
        return "Error: subreddit '{}' is too dank to simulate.".format(SUB), 0
    return model, int(sentence_avg)


def get_quote(subreddit, SUB):
    (model, sentence_avg) = get_markov(subreddit, SUB)
    if isinstance(model, str):
        return (model % '/r/' + SUB) + FOOTER
    else:
        quote_r = []
        if sentence_avg > 0:
            for _ in range(random.randint(1, sentence_avg)):
                tmp_s = model.make_sentence(tries=1000)
                if tmp_s is None:
                    break
                quote_r.append(tmp_s)
                return '> {}\n\n> ~ {}'.format(unidecode(' '.join(quote_r)), '/r/{}'.format(SUB))
        else:
            return ""
