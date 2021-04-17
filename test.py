import string

lets = string.ascii_lowercase + "àäöüéè"

for l in lets:
    print(f"{l}: {ord(l)} {ord(l)-97}")