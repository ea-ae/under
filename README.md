# Under

Under is a text-based browser game about leading a cult.

## Setup

Install the packages `django`, `django-channels`, `channels-redis`, `bcrypt`, `django-ratelimit`, and `psycopg2` (if you're using PostgreSQL).
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