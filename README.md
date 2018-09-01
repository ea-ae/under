# Under

Under is a text-based browser game about leading a cult.

## Features

### Missions

Dialogue options, objectives, important choices. Talk to various people who will
give you contracts, ask for help, or guide you in the right path.

![Missions](https://i.imgur.com/XG8y2LQ.png)

### Members

All of your cultists have different stats, specializations, tiers, and jobs.

![Members](https://i.imgur.com/9XaKHMW.png)

### Anonymity

Cultists know only the identities of the people they recruit and have recruited. Some of
your members might be snitches, spies, or secret informants. If a traitor finds out
your identity, it won't end well for you.

![Anonimity](https://i.imgur.com/gHUIExy.png)

### Crimes

A part of the game is similar to the many mafia/gang games out there. You can make
your cultists perform crimes, but there's a risk they'll get arrested or killed. The choices
you make and the specializations of your cultists play a big role in how a crime will turn out.

### The Underworld

Make your cultists explore the Underworld and find various artifacts that you can
use or sell. Fight, hide, and capture various creatures. Explore different areas
and venture deeper into the Underworld as you become more powerful.

### PVP

Another cult might find you. They could attack your headquarters or plant a spy in your cult and try to discover your identity. But it is possible to avoid this by being careful and staying low profile.

### Societies

Join one of the nine societies and serve the dark gods. Appease them and you'll be rewarded;
make them angry, and misfortune shall fall upon you. Fight other societies for influence and
raise in the ranks.

## Setup

You will need to install and run Redis. Once that's done, install the packages `django`, `django-channels`, `channels-redis`, `bcrypt`, `django-ratelimit`, and `psycopg2` (if you're using PostgreSQL).
Create the file `secret.py` in the `warfare/settings` directory and make it look something like this:
```python
config = {
    'SECRET_KEY': 'abcdef123456abcdef123456abcdef123456',
    'ALLOWED_HOSTS': ['1.2.3.4'],
    'REDIS_IP': '1.2.3.4',
    'DB_PASSWORD': 'hunter2'
}
```

## Testing

Django testing is done with `python manage.py test`. To test the consumers, use `pytest --ds=warfare.settings`.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.