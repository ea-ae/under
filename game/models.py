from django.db import models

from main.models import User
from django.contrib.auth import get_user_model


# Variables that affect the whole game world
# Running multiple 'worlds' could be possible in the future
class WarfareGame(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class WarfarePlayer(models.Model):
    game = models.ForeignKey(WarfareGame, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.profile.display


class Cult(models.Model):
    owner = models.ForeignKey(WarfarePlayer, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, default='Unnamed Cult')
    type = models.CharField(max_length=5, default='none')
    money = models.BigIntegerField(default=5000)
    reputation = models.IntegerField(default=0)

    contacts = models.TextField(
        default='[{"id": "anonymous", "card": "1.0.0"}]',
        help_text='For example: [{"id": "anonymous", "card": "1.4.0"}, {"id": "assistant", "card": "1.0.1}]'
    )
    inventory = models.TextField(default='[]')
    research = models.TextField(default='[]')
    # Research categories:
    # Recruitment | Researching | Headquarters | Underworld
    headquarters = models.TextField(
        default='[]',
        help_text='For example: ["windowbars", "cctv"]'
    )
    marketplace = models.TextField(default='[]')

    def __str__(self):
        return self.name + ' [' + self.owner.user.username + ']'


class Member(models.Model):
    cult = models.ForeignKey(Cult, on_delete=models.CASCADE)
    # supervisor = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    supervisor_id = models.IntegerField(default=-1)  # Primary key of supervisor, -1 means the leader
    name = models.CharField(max_length=40)
    loyalty = models.SmallIntegerField()

    intelligence = models.SmallIntegerField()
    social = models.SmallIntegerField()
    stealth = models.SmallIntegerField()
    strength = models.SmallIntegerField()

    job_id = models.SmallIntegerField(
        default=0,
        help_text='0 = no job, 1 = recruiting, 2 = researching, 3 = guarding.'
    )
    specialization = models.CharField(
        max_length=20,
        help_text='Specialization name followed by a <b>/</b> and then the level, e.g. "Technician/3".'
    )
    skills = models.TextField(
        default='[]',
        help_text='For example: ["recruitmentstrategies", "silentwalking"]'
    )


    def __str__(self):
        return self.name

