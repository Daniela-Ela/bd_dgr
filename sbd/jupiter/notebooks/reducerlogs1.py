#!/usr/bin/env python3
import sys

current_code = None
current_count = 0

for line in sys.stdin:
    code, value = line.strip().split("\t")
    value = int(value)

    if code == current_code:
        current_count += value
    else:
        if current_code is not None:
            print(f"{current_code}: {current_count}")
        current_code = code
        current_count = value

if current_code is not None:
    print(f"{current_code}: {current_count}")
