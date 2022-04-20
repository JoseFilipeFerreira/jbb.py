# JBB.py
Discord bot programmed in Python

## Getting Started
### Setting up
### Credentials
* create a `config.yaml` with:
```yaml
credentials:
  discord: "DISCORD_API_TOKEN"
  github: "GITHUB_API_TOKEN"
  wolframalpha: "WOLFRAMALPHA_API_TOKEN"
```
* Get acess to google via `client_secret.json`

#### Manual
* Create a virtual env
```bash
virtualenv .env
```

* Activate the virtual env
```bash
source .env/bin/activate
```

* Install all dependencies
```bash
pip install -r requirements.txt
```

* Run the Bot
```
python bot.py
```
* follow the instructions on screen to activate the access to google calendar

## Contribuitors
* [João Teixeira](https://github.com/jtexeira) - [say](Extensions/manage.py)
* [Pedro Mendes](https://github.com/mendess2526) - [media](bot.py)
* [Rodrigo Pimentel](https://github.com/RodrigoProjects/) - [EGPP](Extensions/programming.py)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
