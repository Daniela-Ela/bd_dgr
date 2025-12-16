#!/usr/bin/env python3
import sys

for line in sys.stdin:
    try:
        request = line.split('"')[1]   
        method = request.split()[0]    
        print(f"{method}\t1")
    except:
        continue
