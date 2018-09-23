#!/bin/bash

kill $(ps aux| grep 'python3 bot.py' | cut -d" " -f2)

git pull

exec python3 bot.py
