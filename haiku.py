"""
Written By Onur Demiralay
MIT License Copyright(c) 2015 Onur Demiralay
Github: @odemiral
Haiku class is responsible for generating Haikus. You can easily use this class on its own by passing string to the
constructor.
"""
from typing import List, Optional, Tuple
from collections import defaultdict
import re
import random


class Haiku:
    """
    Lots of room for improvement,
    Implement a grammar checker to generate grammatically correct haikus
    Instead of heuristical approach, implement a dictionary of words in english to get syllable count instead.
    """

    def __init__(self, text: str) -> None:
        self.text = text
        self.multimap = defaultdict(list)
        self.haiku_list = None  # store each line of haiku as an element of the list.
        self.format_str()
        # self.generate_haiku()

    # main function, that generates a 5-7-5 haiku
    def generate_haiku(self) -> None:
        self.construct_multi_map()
        try:
            first_line = self.generate_lines(5)
            second_line = self.generate_lines(7)
            third_line = self.generate_lines(5)
            self.haiku_list = [first_line, second_line, third_line]
        except ValueError:
            self.haiku_list = []
        # print self.haikuList
        # haiku = self.construct_haiku(firstLine, secondLine, thirdLine)
        # return haiku

    """
    Return haiku in a list format. This function must be called after generateHaiku.
    """

    def get_haiku_list(self) -> List[str]:
        return self.haiku_list

    """
    Converts Haiku List to str.
    if Haiku List is empty, then return an empty string
    """

    def get_haiku_str(self) -> str:
        haiku_str = ""
        if self.haiku_list:
            haiku_str = self.construct_haiku(self.haiku_list[0], self.haiku_list[1], self.haiku_list[2])
        return haiku_str

    """
    Simple, yet accurate heuristic approach to count syllables.
    1 syllable per vowel assuming it satisfies following conditions:
        #don't count suffixes that end with -es -ed -e
        #consecutive vowels only counts as one
    TODO: Improve accuracy, and implement dictionaries to support other languages as well.
    """

    def count_syllables(self, word: str) -> int:
        # find words ending with laeiouy, es, ed or e
        pattern = r'(?:[^laeiouy]es|ed|[^laeiouy]e)$'
        word = re.sub(pattern, "", word)  # replace every occurence of above pattern.
        word = re.sub(r'^y', "", word)
        pattern = r'[aeiouy]{1,2}'  # find occurences with 1-2 consecutive vowels, queueing will return 3, ue, ue, i
        res = re.findall(pattern, word)  # using findall for /g
        return len(res)

    """
    Constructs a list with words with syllables sum to syllableLimits
    """

    def generate_lines(self, syllable_limits: int) -> List[str]:
        word_arr = []
        while syllable_limits != 0:
            word, syllable = self.pick_random_word(syllable_limits)
            syllable_limits = syllable_limits - syllable
            # print("found: ", word, "with", syllable, "syllables")
            word_arr.append(word)

        return word_arr

    """
    Formats str to get rid of special characters and split it to whitespace delimited list.
    transforms self.text to list.
    """

    def format_str(self) -> None:
        pattern = re.compile(r"[^\w\']")  # unicode friendly
        self.text = pattern.sub(' ', self.text)
        self.text = self.text.lower()
        self.text = self.text.split()

    """
    Constructs MultiMap like structure where value is a list of words and key is the number of syllables in those 
    words.
    ex: multimap[3] = [potato, lunatic, absolute, determine]
    words must have at least 1 syllables (no white spaces, digits, special chars) and it must be consist of at least 
    2 letters
    except for word 'I'
    """

    def construct_multi_map(self) -> None:
        for word in self.text:
            syllables = self.count_syllables(word)
            # print(word)
            if (syllables >= 1) and (len(word) >= 2 or word == 'I'):
                self.multimap[syllables].append(word)

    """
    concats all the lines and beutifies the final string.
    Currently not used by the redditBot
    """

    def construct_haiku(self, first_line: List[str], second_line: List[str], third_line: List[str]):
        haiku = ""
        for word in first_line:
            haiku += word + ' '
        haiku += '\n'
        for word in second_line:
            haiku += word + ' '
        haiku += '\n'
        for word in third_line:
            haiku += word + ' '
        return haiku

    # find a word by iterating through every element in the list
    def brute_force_find_word(self, syllable_size: int) -> Tuple[Optional[List[str]], int]:
        possible_words = None
        # key = None
        for key in self.multimap:
            if key <= syllable_size:
                # print("KEY:",key)
                # print(self.multimap[key])
                possible_words = self.multimap[key]
                syllable_size = key
                break
                # return possible_words, key
                # for val in self.multimap[key]:
                #     print("VAL:",val)
                #     print("KEY:",key)
                #     print(self.multimap[key])
                #     #word = val
                #     #syllableSize = key
                #     #check if the word is already in haiku, if it is then continue, if not use it.
                #     return word,key
        # print("returning", possible_words, "and", syllableSize)
        return possible_words, syllable_size

    """
    Given syllableSize, fetches a random word from multimap that has equal or less syllables than syllableSize
    after some tries, if it can't find words randomly it will find one by calling bruteForceFindWord function.
    If there are enough words in the multimap, calling bruteForceFindWord will be an unlikely possibility.
    You can always assume that this function will either terminate the program or return a word, no further
    error handling need to be done
    TODO: Poor Error handling, revise it so that it doesn't interrupt the flow of the program.
    """

    def pick_random_word(self, syllable_size: int) -> Tuple[str, int]:
        rnd_size = random.randint(1, syllable_size)
        # print("@@@@RANDSIZE: ", rndSize)
        possible_words = self.multimap[rnd_size]
        loop_limit = 1000  # limit of how many times it should try to find a word randomly before switching to

        # iterative mode
        for _ in range(loop_limit):
            rnd_size = random.randint(1, syllable_size)
            possible_words = self.multimap[rnd_size]
            if possible_words:
                break

        if not possible_words:
            print("Trying brute force")
            possible_words, rnd_size = self.brute_force_find_word(syllable_size)
            if not possible_words:
                raise ValueError('Not enough word combinations exist to generate a Haiku :(')
                # sys.exit(-1)
        rnd_pos = random.randint(0, len(possible_words) - 1)
        # print("possible_words[rndPos]:", possible_words[rndPos], "syllableSize:", rnd_size)
        return possible_words[rnd_pos], rnd_size
