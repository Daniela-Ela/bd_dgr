#!/usr/bin/env python3
import sys

for line in sys.stdin:
    parts = line.strip().split()

    if len(parts) < 10:
        continue

    ip = parts[0]
    bytes_sent = parts[-1]

    if bytes_sent == "-":
        bytes_sent = 0

    print(f"{ip}\t{bytes_sent}")
