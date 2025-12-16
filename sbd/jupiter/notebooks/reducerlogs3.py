#!/usr/bin/env python3
import sys

current_url = None
count = 0

for line in sys.stdin:
    url, value = line.strip().split("\t")
    value = int(value)

    if url == current_url:
        count += value
    else:
        if current_url is not None:
            print(f"{current_url}: {count}")
        current_url = url
        count = value

if current_url is not None:
    print(f"{current_url}: {count}")
