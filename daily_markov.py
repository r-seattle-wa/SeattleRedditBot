from typing import Optional, Tuple
import random
import re

from haiku import Haiku
from praw.exceptions import PRAWException
from praw.models import Subreddit
from unidecode import unidecode
import markovify
import praw

from bot import *

FOOTER = '\n\n-----\n\n[^^Info](https://github.com/trambelus/UserSim) ^^| [^^Subreddit](/r/User_Simulator)'


class PText(markovify.Text):

    def test_sentence_input(self, sentence: str) -> bool:
        emote_pat = re.compile(r"\[.+?\]\(\/.+?\)")
        reject_pat = re.compile(r"(^')|"
                                r"('$)|"
                                r"\s'|"
                                r"'\s|"
                                r"([\"(\(\)\[\])])|"
                                r"(github.com/trambelus/UserSim)|"
                                r"(/r/User_Simulator)|"
                                r"(~\ [\w\d\-_]{3,20}\ -----)")
        decoded = unidecode(sentence)
        filtered_str = re.sub(emote_pat, '', decoded).replace('  ', ' ')
        if re.search(reject_pat, filtered_str):
            return False
        if filtered_str in FOOTER:
            return False
        return True


def get_history(subreddit: Subreddit, limit: int) -> Tuple[Optional[str], int, float]:
    try:
        comments = subreddit.comments(limit=limit)
        if comments is None:
            return None, 0, 0
        c_finished = False
        body = []
        total_sentences = 0
        while not c_finished:
            try:
                for c in comments:
                    if (not c.distinguished) and ((not subreddit) or c.subreddit.display_name == subreddit):
                        body.append(c.body)
                        try:
                            total_sentences += len(markovify.split_into_sentences(c.body))
                        except Exception:
                            total_sentences += 1
                c_finished = True
            except PRAWException:
                body = []
                total_sentences = 0
        num_comments = len(body)
        sentence_avg = total_sentences / num_comments if num_comments > 0 else 0
        return ' '.join(body), num_comments, sentence_avg

    except praw.exceptions.PRAWException:
        return None, 0, 0


def get_markov(subreddit: Subreddit) -> Tuple[PText, int]:
    (history, num_comments, sentence_avg) = get_history(subreddit, 1000)
    model = PText(history, state_size=STATE_SIZE)
    return model, int(sentence_avg)


def get_quote(subreddit: Subreddit) -> str:
    try:
        (model, sentence_avg) = get_markov(subreddit)
        quote_r = []
        if sentence_avg > 0:
            for _ in range(random.randint(1, sentence_avg)):
                tmp_s = model.make_sentence(tries=1000)
                if tmp_s is None:
                    break
                quote_r.append(tmp_s)
                return '> {}\n\n> ~ {}'.format(unidecode(' '.join(quote_r)), '/r/{}'.format(subreddit.display_name))
        return ""
    except IndexError:
        error_msg = "Error: subreddit '{}' is too dank to simulate.".format(subreddit.display_name)
        return error_msg + FOOTER


def get_haiku(subreddit: Subreddit) -> str:
    (history, num_comments, sentence_avg) = get_history(subreddit, 5000)

    if not history:
        return ''

    my_haiku = Haiku(history)
    my_haiku.generate_haiku()
    haiku_list = my_haiku.get_haiku_list()
    formatted_haiku = ""
    if haiku_list:  # if list is not empty:
        for line in haiku_list:
            formatted_line = "> *"
            for word in line:
                formatted_line = "{}{} ".format(formatted_line, word)
            formatted_line = "{}* \n\n".format(formatted_line[:-1])
            formatted_haiku = "{}{}".format(formatted_haiku, formatted_line)
    return formatted_haiku
