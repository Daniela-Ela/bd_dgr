#!/usr/bin/env python3
import sys
import re

pattern = re.compile(r"\[(\d{2}/\w{3}/\d{4}):(\d{2}):\d{2}:\d{2}")

for line in sys.stdin:
    match = pattern.search(line)
    if match:
        hour = match.group(2)
        print(f"{hour}\t1")
