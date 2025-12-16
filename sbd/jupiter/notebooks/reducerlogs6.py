#!/usr/bin/env python3
import sys

current_url = None
ok_total = 0
error_total = 0

for line in sys.stdin:
    url, ok, error = line.strip().split("\t")
    ok = int(ok)
    error = int(error)

    if url == current_url:
        ok_total += ok
        error_total += error
    else:
        if current_url is not None:
            total = ok_total + error_total
            error_rate = (error_total / total) * 100 if total > 0 else 0
            print(f"{current_url}: {error_rate:.2f}%")
        current_url = url
        ok_total = ok
        error_total = error

if current_url is not None:
    total = ok_total + error_total
    error_rate = (error_total / total) * 100 if total > 0 else 0
    print(f"{current_url}: {error_rate:.2f}%")
