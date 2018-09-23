#!/bin/bash

kill $(ps aux| grep 'python3 bot.py' | cut -d" " -f2)

git pull

python3 bot.py
