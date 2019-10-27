#!/bin/bash
cd $(dirname "$0")

until ping -q -c 1 www.github.com &> /dev/null
do
    true
done

git pull

if [ -e '.env' ]
then
    source '.env/bin/activate'
else
    virtualenv '.env' || exit 2
    source '.env/bin/activate' || exit 3
    pip install -r 'requirements.txt' --upgrade || exit 4
fi

while true 
do 
    python bot.py
    git pull
    while ! ping -c 1 github.com &> /dev/null; do true; done
done
