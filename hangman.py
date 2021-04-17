"""
Hangman Solver

v.1.0:  The basic and naive approach at finding matching words in the list of words.
        Average time per searched word:
            English: 0.1300s
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
        Max word list sizes (words):
            English: 53403 (length 9 words)
            German: 190217 (length 13 words)


German word list: https://gist.github.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4
English word list: https://github.com/dwyl/english-words


"""


import time


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
    letter_count = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0,
                'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0,
                'y': 0, 'z': 0, 'ä': 0, 'ö': 0, 'ü': 0, }
    fitting_words = []

    word_list_path = get_filename(wtg, language)

    # get the word list
    with open(word_list_path, "r", encoding='utf-8') as f:
        cont = f.read()
    words = cont.split("\n")

    # count the amount of words each letter is in
    # note: we don't want to count all letters in each word,
    #       only the amount of words a letter is in.
    for w in words:
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
            
    return letter_count, fitting_words


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
        return "english.txt"
    if language == "german":
        return "german.txt"
    return "words.txt"


def max_length(language:str):
    """Returns the maximum length word

    Args:
        language (str): [description]

    Returns:
        int: [description]
    """
    word_list_path = get_filename("_", language)
    # get the word list
    with open(word_list_path, "r", encoding='utf-8') as f:
        cont = f.read()
    words = cont.split("\n")
    mx = 0
    for w in words:
        if len(w) > mx:
            mx = len(w)
    return mx


def main():
    wtg = "____"  # word to guess
    ignore = ["a", "e", "i", "o", "u"]  # unused letters
    result = get_freq_letters(wtg, ignore)
    print(result[0])

if __name__ == "__main__":
    main()
