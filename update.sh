#!/bin/bash

kill $(ps aux| grep 'python3 bot.py' | awk '{print $2}')

git pull

exec python3 bot.py
