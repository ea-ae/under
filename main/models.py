from re import ASCII
from django.core import validators
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


@deconstructible
class AlphanumericUsernameValidator(validators.RegexValidator):
    regex = r'^[\w]+$'
    message = _(
        'Enter a valid username. This value may contain only English letters, '
        'numbers and underscores.'
    )
    flags = ASCII


class User(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=25,
        unique=True,
        help_text=_('Required. 4-25 characters. Letters, digits and underscores only.'),
        validators=[AlphanumericUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    display = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.display


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print(instance)
        Profile.objects.create(user=instance, display=instance.username)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
