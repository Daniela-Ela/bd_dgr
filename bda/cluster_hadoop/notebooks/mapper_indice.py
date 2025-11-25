#!/usr/bin/env python3

import sys
import os

filename = os.environ.get("map_input_file", "deconocido")

for line is sys.stdin:
    line = line.strip().split()
    for word in line:
        print(f"{word}\t{filename}")
