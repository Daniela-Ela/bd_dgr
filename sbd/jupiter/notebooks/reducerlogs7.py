#!/usr/bin/env python3
import sys

current_method = None
count = 0

for line in sys.stdin:
    method, value = line.strip().split("\t")
    value = int(value)

    if method == current_method:
        count += value
    else:
        if current_method is not None:
            print(f"{current_method}: {count}")
        current_method = method
        count = value

if current_method is not None:
    print(f"{current_method}: {count}")
