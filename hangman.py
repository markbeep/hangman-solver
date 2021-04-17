"""
Hangman Solver

v.1.0:  The basic and naive approach at finding matching words in the list of words.
        Average time per searched word:
            English: 0.0805s
            German: 0.4664s
        Word list sizes (words):
            English: 370'102
            German: 1908815

v.1.1:  Tried to clean up the words to remove any duplicates, words with punctuations and
        words that contain letters I don't account for. There were barely any words
        to remove though.
        Word list sizes (words):
            English: 370'000
            German: 1'908'814

v.2.0:  Splitting the word list into files depending on the length of the word.
        This way we reduce the file sizes by immense amounts.
        Average time per searched word:
            English: 0.0301s
            German: 0.2128s
        Max word list sizes (words):
            English: 53'403 (length 9 words)
            German: 190'217 (length 13 words)

v.3.0:  Parallelizing the word search by splitting the word list into multiple chunks
        Average time per searched word:
            English: 0.0309s (with 16 threads)
            German: 0.1564s (with 8 threads)
        


German word list: https://gist.github.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4
English word list: https://github.com/dwyl/english-words

"""


import time
import os
from multiprocessing import Process, Manager
from toolz import merge_with
from itertools import chain
import threading


class myThread(threading.Thread):
    def __init__(self, words:list, wtg:str, letter_count, fitting_words, ignore:list, start_index:int, length:int):
        threading.Thread.__init__(self)
        self.words = words
        self.wtg = wtg
        self.letter_count = letter_count
        self.fitting_words = fitting_words
        self.ignore = ignore
        self.start_index = start_index
        self.length = length
    
    def run(self):
        for i in range(self.length):
            w = self.words[i + self.start_index]
            if len(w) == len(self.wtg):  # only consider words of the same length
                marked_letters = []
                for i, letter in enumerate(w):
                    if (self.wtg[i] != "_" and w[i] != self.wtg[i]) or letter in self.ignore:
                        break
                    if letter not in marked_letters:
                        try:
                            self.letter_count[letter] += 1
                            marked_letters.append(letter)
                        except KeyError:  # KeyError is raised if letter is not part of the alphabet
                            pass
                else:  # else only gets called on a normal ending for loop (no break)
                    self.fitting_words.append(w)

def get_freq_letters(wtg:str, ignore=[], language="english", process_count=1):
    """Returns a type dict with all letters and the amount of words
    that contain that letter.

    Args:
        wtg (str): Word to guess
        ignore (list, optional): Letters to ignore. Defaults to [].
        word_list_path (str, optional): [description]. Defaults to "words.txt".

    Returns:
        tuple: (letter_count:dict, fitting_words:list)
    """

    word_list_path = get_filename(wtg, language)

    if word_list_path is None:
        return {}, []

    # get the word list
    with open(word_list_path, "r", encoding='utf-8') as f:
        cont = f.read()
    words = cont.split("\n")

    # count the amount of words each letter is in
    letter_count = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0,
                'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0,
                'y': 0, 'z': 0, 'ä': 0, 'ö': 0, 'ü': 0, }
    fitting_words = []
     
    all_threads = []
    step = len(words) // process_count
    for i in range(process_count):
        length = step
        if i == process_count-1:
            length = len(words) - length*i
        t = myThread(words, wtg, letter_count, fitting_words, ignore, step*i, length)
        t.start()
        all_threads.append(t)
    for t in all_threads:
        t.join()
            
    return letter_count, fitting_words

def count_chars(words:list, wtg:str, letter_count, fitting_words, ignore:list, start:int, length:int):
    """
    Count the amount of words each letter is in.
    
    Note: we don't want to count all letters in each word,
          only the amount of words a letter is in.
    """
    for i in range(length):
        w = words[i + start]
        if len(w) == len(wtg):  # only consider words of the same length
            marked_letters = []
            for i, letter in enumerate(w):
                if (wtg[i] != "_" and w[i] != wtg[i]) or letter in ignore:
                    break
                if letter not in marked_letters:
                    try:
                        letter_count[letter] += 1
                        marked_letters.append(letter)
                    except KeyError:  # KeyError is raised if letter is not part of the alphabet
                        pass
            else:  # else only gets called on a normal ending for loop (no break)
                fitting_words.append(w)

def get_filename(wtg:str, language:str):
    """We use this to easily return the name of the
    word list file. This can then easily be changed
    later on.

    Args:
        wtg (str): The word we're looking for
        language (str): The language we're looking for

    Returns:
        str: The filename of the word list
    """
    if language == "english":
        fp = f"english\\{len(wtg)}.txt"
        if os.path.isfile(fp):
            return f"english\\{len(wtg)}.txt"
    if language == "german":
        fp = f"german\\{len(wtg)}.txt"
        if os.path.isfile(fp):
            return f"german\\{len(wtg)}.txt"
    return None


def max_length(language:str):
    """Returns the maximum length word

    Args:
        language (str): [description]

    Returns:
        int: [description]
    """
    mx = 0
    for f in os.listdir(language):
        mx = max(mx, int(f.replace(".txt", "")))
    return mx


def main():
    wtg = "____"  # word to guess
    ignore = ["a", "e", "i", "o", "u"]  # unused letters
    result = get_freq_letters(wtg, ignore, "german")
    print(result[0])

if __name__ == "__main__":
    main()
