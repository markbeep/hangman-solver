def get_freq_letters(wtg:str, ignore=[], word_list_path="words.txt"):
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

    # get the word list
    with open(word_list_path, "r") as f:
        ctx = f.read()
    words = ctx.split("\n")

    # count the amount of words each letter is in
    # note: we don't want to count all letters in each word,
    #       only the amount of words a letter is in.
    for w in words:
        if len(w) == len(wtg):  # only consider words of the same length
            marked_letters = []
            for i, letter in enumerate(w):
                if w[i] != wtf[i]:
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

def main():
    wtg = "____"  # word to guess
    ignore = []  # unused letters
    get_freq_letters(wtg, ignore)

if __name__ == "__main__":
    main()