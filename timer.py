import hangman
import time
import random


def stopwatch(func):
    """
    Tests how long the hangman method takes

    Args:
        n (int, optional): Amount of tests to execute. Defaults to 100.

    Returns:
        float: average time taken in seconds
    """
    t1 = time.perf_counter()
    n = 100
    for i in range(n):
        func()
    t2 = time.perf_counter()
    print(f"{(t2 - t1) / n} seconds in average.")  


@stopwatch
def test_hangman():
    lng = "english"
    max_length = hangman.max_length(lng)
    #print(max_length)
    wtg = "_" * random.randint(1, max_length)
    hangman.get_freq_letters(wtg, ignore=[], language=lng)
    

def main():
    test_hangman
    


if __name__ == "__main__":
    main()