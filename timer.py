import hangman
import time
import random

def stopwatch(lng, n=100, process_count=1):
    """
    Tests how long the hangman method takes

    Args:
        n (int, optional): Amount of tests to execute. Defaults to 100.

    Returns:
        float: average time taken in seconds
    """
    max_length = hangman.max_length(lng)
    t1 = time.perf_counter()
    for i in range(n):
        wtg = "_" * random.randint(1, max_length)
        hangman.get_freq_letters(wtg, ignore=[], language=lng)
        if i % 50 == 0 and i > 0:
            print(i)
    t2 = time.perf_counter()
    print(f"{(t2 - t1) / n} seconds in average.")  


def main():
    stopwatch("german", 10)
    


if __name__ == "__main__":
    main()