#!/usr/bin/env python3
import sys

for line in sys.stdin:
    parts = line.strip().split()
    
    if len(parts) < 9:
        continue

    status_code = parts[-2]

    print(f"{status_code}\t1")
