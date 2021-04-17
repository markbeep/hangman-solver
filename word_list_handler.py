import string
import os
import time

def cleanup(fp, valid_chars=""):
    with open(fp, "r", encoding='utf-8') as f:
        cont = f.read()
    words = cont.split("\n")
    
    filtered_words = []
    lg = len(words)
    for i, w in enumerate(words):
        if i % 10000 == 0:
            print(f"{i} / {lg}")
            with open("copy_"+fp, "a", encoding='utf-8') as f:
                cont = "\n".join(filtered_words)
                f.write("\n"+cont)
                filtered_words = []
        w = w.lower()
        if w in filtered_words:
            continue
        for let in w:
            if let not in valid_chars:
                break
        else:
            filtered_words.append(w)

    return filtered_words


def split_by_length(fp, dir_name):
    os.mkdir(dir_name)
    with open(fp, "r", encoding='utf-8') as f:
        cont = f.read()
    words = cont.split("\n")
    mx = len(words)
    for i, w in enumerate(words):
        if i % 10_000 == 0:
            print(f"{i} / {mx}")
        lg = len(w)
        try:
            with open(f"{dir_name}/{lg}.txt", "a", encoding='utf-8') as f:
                f.write(f"\n{w}")
        except PermissionError:
            time.sleep(0.1)
            with open(f"{dir_name}/{lg}.txt", "a", encoding='utf-8') as f:
                f.write(f"\n{w}")


def count_words_in_file(fp):
    """
    Returns the length of the 
    """
    with open(fp, "r", encoding='utf-8') as f:
        cont = f.read()
    return len(cont.split("\n"))

def main():
    mx = 0
    fx = "0"
    directory = "english"
    for f in os.listdir(directory):
        fp = os.path.join(directory, f)
        c = count_words_in_file(fp)
        if mx < c:
            mx = c
            fx = f
    print(mx)
    print(fx)


if __name__ == "__main__":
    main()