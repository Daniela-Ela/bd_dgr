#!/usr/bin/env python3
import sys

current_ip = None
total_bytes = 0

for line in sys.stdin:
    ip, value = line.strip().split("\t")
    value = int(value)

    if ip == current_ip:
        total_bytes += value
    else:
        if current_ip is not None:
            print(f"{current_ip}: {total_bytes} bytes")
        current_ip = ip
        total_bytes = value

if current_ip is not None:
    print(f"{current_ip}: {total_bytes} bytes")
