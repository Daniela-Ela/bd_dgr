#!/usr/bin/env python3

current_word = None
docs = set()

for line in sys.stdin:
    word, doc = line.strip().split("\t",1)

    if current_word:
        docs.add( doc )
    else:
        if current_word:
            print(f"{current_word}\t{','.join(sorted(docs))}")
            current_word = word
            docs = {doc}
if current_word:
    print(f"{current_word}\t{','.join(sorted(docs))}")
