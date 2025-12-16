#!/usr/bin/env python3
import sys

for line in sys.stdin:
    try:
        parts = line.strip().split()
        url = parts[6]
        status = int(parts[-2])

        if status < 400:
            print(f"{url}\t1\t0")
        else:
            print(f"{url}\t0\t1")
    except:
        continue
