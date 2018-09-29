#!/bin/bash
until ping -q -c 1 www.github.com &> /dev/null
do
	true
done

cd ~/JBB.py
git pull
source .env/bin/activate
python3 bot.py
