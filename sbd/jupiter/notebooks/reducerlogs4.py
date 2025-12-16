#!/usr/bin/env python3
import sys

current_browser = None
count = 0

for line in sys.stdin:
    browser, value = line.strip().split("\t")
    value = int(value)

    if browser == current_browser:
        count += value
    else:
        if current_browser is not None:
            print(f"{current_browser}: {count}")
        current_browser = browser
        count = value

if current_browser is not None:
    print(f"{current_browser}: {count}")
