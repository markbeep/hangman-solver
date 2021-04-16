def word_guesser(inputted_word, unused_letters="", language="english"):
    # Ununused letters
    not_like_msg = ""
    for l in unused_letters:
        not_like_msg += f' AND NOT Word LIKE "%{l}%"'

    # sql query takes up the most time, so its performed in a separate thread to prevent the whole bot from blocking
    event_loop = asyncio.get_event_loop()
    blocking_task = [event_loop.run_in_executor(concurrent.futures.ThreadPoolExecutor(max_workers=1), self.dict_query, not_like_msg, language, inputted_word)]
    completed, pending = await asyncio.wait(blocking_task)

    fitting_words = []
    for t in completed:
        fitting_words.extend(t.result())

    alphabet = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0,
                'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0,
                'y': 0, 'z': 0, 'ä': 0, 'ö': 0, 'ü': 0, }
    total = 0

    if len(fitting_words) == 0:
        return {'fitting_words': [], 'alphabet': alphabet, 'total': total}
    else:
        count_words = []

        # Removes all duplicate characters from every word and puts the words in a list to count
        for i, word in enumerate(fitting_words):
            count_words.append(str(set(word)))

        # Puts all strings into one long string to count it easier.
        all_string = ''.join(count_words)

        # Counts all the letters in the words (but only letters that haven't been mentioned yet)
        for key in alphabet.keys():
            if key in inputted_word:
                continue
            else:
                count = all_string.count(key)
                if count > 0:
                    total += count
                    alphabet[key] = count
        return {'fitting_words': fitting_words, 'alphabet': alphabet, 'total': total}

def get_freq_letters(wtg:str, ignore=[], lang="english"):
    """
    Returns a type dict with all letters and the amount of words
    that contain that letter.

    Args:
        wtg (str): Word to guess
        ignore (list, optional): Letters to ignore. Defaults to [].
        lang (str, optional): Language to search words in. Defaults to "english".
    """
    alphabet = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0,
                'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0,
                'y': 0, 'z': 0, 'ä': 0, 'ö': 0, 'ü': 0, }
    fitting_words = []

    # get the word list


def main():
    wtg = "____"  # word to guess
    ignore = []  # unused letters
    get_freq_letters(wtg, ignore)

if __name__ == "__main__":
    main()