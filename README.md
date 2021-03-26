# Under

Under is a text-based browser game centered around leading a cult.

## Features

### Missions

Dialogue options, objectives, game-changing choices. Talk to various people who will trade, ask for help, or give out contracts.

![Missions](https://i.imgur.com/XG8y2LQ.png)

### Members

All of your cultists have different stats, specializations, tiers, and jobs.

![Members](https://i.imgur.com/9XaKHMW.png)

### Anonymity

Cultists know only the identities of the people they recruit and have recruited. Some of
your members might be snitches, spies, or secret informants. If a traitor discovers your 
true identity, it won't end well for you.

![Anonymity](https://i.imgur.com/gHUIExy.png)

### The Underworld

Make your cultists explore the Underworld and find various artifacts that you can
use or sell. Fight, hide, and capture various creatures. Explore different areas
and venture deeper into the Underworld as you become more powerful.

### PVP

Other cults are a threat. They could attack your headquarters or plant a spy in your cult and attempt to discover your identity. 
One must be careful and stay low profile.

## Setup

### Packages and Requirements

Install the packages in `requirements.txt` by typing `pip install -r requirements.txt`. 
You only need `psycopg2` if you're using PostgreSQL and `pypiwin32` if you're using Windows.
You will also need to run a Redis server.

### Configuration

Go into the `python manage.py shell` and create a new game model named 'alpha':
```python
from game.models import WarfareGame
game = WarfareGame(name='alpha')
game.save()
```
Create a file named `config.py` in the `warfare/settings` directory and make it look something like this:
```python
config = {
    'DEBUG': True,  # Set to False in production
    'HTTPS': True,  # Set to True only if you're using https
    'SECRET_KEY': 'abcdef123456abcdef123456abcdef123456',
    'ALLOWED_HOSTS': ['1.2.3.4'],
    'REDIS_IP': '127.0.0.1',
    'DB_NAME': 'game_db',
    'DB_USER': 'django',
    'DB_PASSWORD': 'hunter2'
}
```

### Testing

Run tests with `python manage.py test`. To test the consumers, use `pytest --ds=warfare.settings`.
