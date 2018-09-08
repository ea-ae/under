from .base import *
from .config import config

if config['DEBUG'] is True:
    try:
        from .local import *
    except ImportError:
        pass
else:
    try:
        from .production import *
    except ImportError:
        pass
