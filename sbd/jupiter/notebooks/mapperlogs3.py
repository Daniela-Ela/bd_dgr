#!/usr/bin/env python3
import sys

for line in sys.stdin:
    try:
        request = line.split('"')[1]  
        parts = request.split()
        url = parts[1]           
        print(f"{url}\t1")
    except:
        continue
