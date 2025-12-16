#!/usr/bin/env python3
import sys

current_hour = None
count = 0

for line in sys.stdin:
    hour, value = line.strip().split("\t")
    value = int(value)

    if hour == current_hour:
        count += value
    else:
        if current_hour is not None:
            print(f"{current_hour}: {count}")
        current_hour = hour
        count = value

if current_hour is not None:
    print(f"{current_hour}: {count}")
