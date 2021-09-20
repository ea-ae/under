# Under

Under is a text-based multiplayer browser game / PBBG centered around managing a cult. Project's primary purpose wasn't the creation of a proper & finished game, but learning-through-doing.

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

## Features

### Missions

Dialogue options, objectives, and game-changing choices.

![Missions](https://i.imgur.com/XG8y2LQ.png)

### Members

Member recruitment tree system with stats, specializations, tiers, and jobs.

![Members](https://i.imgur.com/9XaKHMW.png)

![Anonymity](https://i.imgur.com/gHUIExy.png)

### Registration

Fully functioning registration/login system ([mp4](https://i.imgur.com/semSmyj.mp4)).

### About

Created as a personal learn-by-doing project in 2018.
