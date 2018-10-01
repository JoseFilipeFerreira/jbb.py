# JBB.py
Discord bot programmed in Python

## Getting Started

### Setting up

Create a virtual env
```
python3 -m venv .env
```

Activate the virtual env
```
source .env/bin/activate
```

Install all dependencies
```
$ pip install -r requirements.txt --upgrade
```

<details><summary>Update dependencies</summary>
<p>

```
pip3 freeze > requirements.txt
```
</p>
</details>

### Credentials

get a discord bot Token and place it into a text file named `auth`

get a acess key to wolfram alpha and place the key in a file named `WA_KEY`

get acess credentials to the google calendar containig the menu and place them in `credentials.json` and `client_secret.json`

### Run the Bot
```
python3 bot.py
```

## Built With
* [discord.py](https://github.com/Rapptz/discord.py) - API for discord
* [baseconvert](https://github.com/squdle/baseconvert) - Convert numbers
* [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) - Search quotes
* [pokebase](https://github.com/GregHilmes/pokebase) - Python 3 wrapper for Pokéapi v2
* [wolframalpha](https://github.com/jaraco/wolframalpha) - Python 3 wrapper for Wolfram|Alpha v2.0 API.
* [py-googletrans](https://github.com/ssut/py-googletrans) - Python 3 wrapper for Google Translate API
* [urbandictionary-py](https://github.com/bcyn/urbandictionary-py) - Python 3 wrapper for Urban Dictionary API.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
