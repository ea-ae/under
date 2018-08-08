from django.contrib.auth.hashers import BCryptSHA256PasswordHasher


class BCryptSHA256Custom(BCryptSHA256PasswordHasher):
    rounds = 13  # Default: 12
