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

v.3.0:  Hoping to make the word search faster by splitting the word list into multiple chunks.
        Python Multithreading: (Multiprocessing was a lot slower, because of the giant overhead)
        Average time per searched word:
            English: 0.0309s (with 16 threads)
            German: 0.1564s (with 8 threads)

v.3.1:  Tried the search using the Python multiprocessing library. The overhead
        turned out to be a too big of a problem, which is why multiprocessing won't
        be the way to go. For each separate process it took about an extra 0.1s.

v.3.2:  Cleaned up code and removed multithreading/multiprocessing completely, as it only
        made code slower.


v.4.0:  Numba implementation. Because it keeps having to compile, it made the code a
        lot slower.

German word list: https://gist.github.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4
English word list: https://github.com/dwyl/english-words

"""


import time
import os
from numba import jit, njit
from numba.typed import List
import numpy as np
import string

def get_freq_letters(wtg:str, ignore=[], language="english"):
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

    # create the np arrays
    t1 = time.perf_counter()
    print(f"T0")
    av_lets = string.ascii_lowercase + "äöüàéè"
    mx = ord(max(av_lets, key=ord))-97 + 1
    letter_count = np.zeros(mx, np.int32)  # index 0 is 'a', last index is the char with highest unicode
    words = np.array(words)
    fitting = np.zeros(len(words), dtype=f'<U{len(wtg)}')
    
    ignore = np.array(ignore)  # array to keep track of what chars are ignored
    
    print(f"T1: {time.perf_counter()-t1}")
    t1 = time.perf_counter()
    
    get_fitting(words, wtg, fitting, ignore)
    
    print(f"T fitting: {time.perf_counter()-t1}")
    t1 = time.perf_counter()
    
    count_chars(fitting, wtg, letter_count, ignore, mx)
    
    print(f"T counted: {time.perf_counter()-t1}")
    t1 = time.perf_counter()
    return letter_count, fitting


def count_chars(words, wtg, letter_count, ignore, mx):
    """
    Count the amount of words each letter is in.
    
    Note: we don't want to count all letters in each word,
          only the amount of words a letter is in.
    """
    
    for i in range(len(words)):
        w = words[i]
        if w == "":
            break
        if len(w) == len(wtg):  # only consider words of the same length
            marked_letters = np.zeros(mx, np.int8)
            for j in range(len(w)):
                let = w[j]
                o = ord(let) - 97
                if marked_letters[o] == 0:
                    letter_count[o] += 1
                    marked_letters[o] = 1
                

@njit
def get_fitting(words, wtg, fitting_words, ignore):
    fit_ind = 0
    for i in range(len(words)):
        w = words[i]
        fit = True
        if len(w) == len(wtg):  # only consider words of the same length
            for j in range(len(w)):
                let = w[j]
                if wtg[j] != "_" and let != wtg[j]:
                    fit = False
                    break
                if let in ignore:
                    fit = False
                    break
            if fit:
                fitting_words[fit_ind] = w
                fit_ind += 1


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
    wtg = "______"  # word to guess
    ignore = ["a", "e", "i", "o", "u"]  # unused letters
    result = get_freq_letters(wtg, ignore, "english")
    fitting = [x for x in result[1] if x != ""]
    #print(fitting)
    print(result[0])

if __name__ == "__main__":
    main()
