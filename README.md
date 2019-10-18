# JBB.py
Discord bot programmed in Python

## Getting Started

### Setting up
- Create a virtual env
```
virtualenv .env
```

- Activate the virtual env
```
source .env/bin/activate
```

- Install all dependencies
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

- Get a discord bot Token and place it into a text file named `auth`

- Get a access key to wolfram alpha and place the key in a file named `WA_KEY`

- Get acess to google via `client_secret.json`

### Run the Bot
```
python bot.py
```
 - follow the instructions on screen to activate the access to youtube and google calendars

## Built With
* [discord.py](https://github.com/Rapptz/discord.py) - API for discord
* [baseconvert](https://github.com/squdle/baseconvert) - Convert numbers
* [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) - Search quotes
* [wolframalpha](https://github.com/jaraco/wolframalpha) - Python 3 wrapper for Wolfram|Alpha v2.0 API.
* [ftfy](https://github.com/LuminosoInsight/python-ftfy) - Fixes glitches in Unicode text.
* [deckofcards](https://deckofcardsapi.com/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
