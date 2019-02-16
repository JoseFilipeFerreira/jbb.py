# JBB.py
Discord bot programmed in Python

## Getting Started

### Setting up
- Dowload python 3.6.6 from [here](https://www.python.org/ftp/python/3.6.6/) (If not already installed)

- Unpack it with
```
tar -xvzf Python-3.6.6.tgz
```
```
cd Python-3.6.6
```
```
./configure
```
```
make altinstall
```
- Create a virtual env
```
virtualenv --python=python3.6 .env
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
python3 bot.py
```
 - follow the instructions on screen to activate the access to youtube and google calendars

## Built With
* [discord.py](https://github.com/Rapptz/discord.py) - API for discord
* [baseconvert](https://github.com/squdle/baseconvert) - Convert numbers
* [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) - Search quotes
* [pokebase](https://github.com/GregHilmes/pokebase) - Python 3 wrapper for Pokéapi v2
* [wolframalpha](https://github.com/jaraco/wolframalpha) - Python 3 wrapper for Wolfram|Alpha v2.0 API.
* [mcstatus](https://github.com/Dinnerbone/mcstatus) - check the status of a Minecraft server

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
