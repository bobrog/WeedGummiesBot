# WeedGummiesBot

The TIRD Discord servers kinda buggy, kinda high assistant

### Usage

#### Reqs
1. Registered Discord bot and token (see link in resources)
2. Docker `brew cask install docker` 
 

#### Docker
1. `BOT_TOKEN=token ./run.sh`

Or..

1. Build: `docker build -t weedgummiesbot .`
2. Run: `docker run --rm -v $(pwd):/usr/src/app -e BOT_TOKEN=token weedgummiesbot`

#### Python Virtual Env (legacy)

1. Create and activate a Python3 virtual environment: `python3 -m venv .venv && source .venv/bin/activate`
2. Install Python dependencies: `pip install -r requirements.txt`

4. `BOT_TOKEN=token python bot.py`

### Resources

* [Python Discord Bot Quickstart](https://discordpy.readthedocs.io/en/latest/quickstart.html)
