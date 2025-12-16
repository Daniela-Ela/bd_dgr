#!/usr/bin/env python3
import sys

for line in sys.stdin:
    try:
        # El User-Agent suele ser la última cadena entre comillas
        user_agent = line.split('"')[-2]

        if "Chrome" in user_agent:
            print("Chrome\t1")
        elif "Firefox" in user_agent:
            print("Firefox\t1")
        elif "Mobile" in user_agent or "Android" in user_agent or "iPhone" in user_agent:
            print("Mobile\t1")
        elif "bot" in user_agent.lower():
            print("Bot\t1")
        else:
            print("Other\t1")
    except:
        continue
