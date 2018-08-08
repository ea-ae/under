from .base import *
try:  # There will be no .local on the production server
    from .local import *
except ImportError:
    from .production import *
