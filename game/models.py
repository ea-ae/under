from django.db import models
from main.models import User
from django.utils.timezone import now


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
        help_text='For example: [{"id": "anonymous", "card": "1.4.0"}, {"id": "assistant", "card": "1.0.1}]<br>\
                  Assistant added at anonymous "1.3.0". Mafioso added at assistant "1.1.2".'
    )
    inventory = models.TextField(default='{}')
    research = models.TextField(default='[]')
    headquarters = models.TextField(
        default='[]',
        help_text='For example: ["windowbars", "cctv"]'
    )
    marketplace = models.TextField(default='[]')

    research_points = models.IntegerField(default=50)
    recruitment_points = models.IntegerField(default=0)

    last_check = models.DateTimeField(default=now)  # Last time we processed ticks

    def __str__(self):
        return self.name + ' [' + self.owner.user.username + ']'


class Member(models.Model):
    owner = models.ForeignKey(Cult, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    accepted = models.BooleanField()
    name = models.CharField(max_length=40)
    loyalty = models.SmallIntegerField()
    wage = models.IntegerField()

    intelligence = models.SmallIntegerField()
    social = models.SmallIntegerField()
    stealth = models.SmallIntegerField()
    strength = models.SmallIntegerField()

    job = models.CharField(
        max_length=15,
        default='none',
        help_text='Options: none, recruiting, researching, guarding, pickpocketing, spying.'
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


class Underworld(models.Model):
    owner = models.ForeignKey(Cult, on_delete=models.CASCADE)
    seed = models.CharField(max_length=32)  # Seed of the map
    x = models.IntegerField()
    y = models.IntegerField()
    time = models.IntegerField()  # The amount of moves that has been made

    def __str__(self):
        return self.seed
