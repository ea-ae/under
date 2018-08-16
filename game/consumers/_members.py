from game.models import Member
import json
from random import random, randint, randrange, shuffle


def members_data(self):
    db_members = self.cult.member_set.all()
    members = []

    for db_member in db_members:
        spec_name, spec_level = db_member.specialization.split('/')
        skills = json.loads(db_member.skills)

        # Faster than db_member.supervisor.id
        if db_member.supervisor_id is None:
            supervisor = -1
        else:
            supervisor = db_member.supervisor_id

        members.append({
            'id': db_member.id,
            'supervisor': supervisor,
            'name': db_member.name,
            'loyalty': db_member.loyalty,
            'job': db_member.job,

            'intelligence': db_member.intelligence,
            'social': db_member.social,
            'stealth': db_member.stealth,
            'strength': db_member.strength,

            'spec_name': spec_name,
            'spec_level': int(spec_level),
            'skills': skills
        })

    self.send_json({
        'type': 'page_data',
        'page': 'members',
        'members': members
    })


def generate_member(self, owner, supervisor):
    primary_stat = max(wrand(90, 2) + 10, 38)  # Average: 55 [56]
    # 01-10  0.0%
    # 11-20  0.0%
    # 21-30  0.0%
    # 31-40  22.9%
    # 41-50  17.4%
    # 51-60  21.1%
    # 61-70  17.0%
    # 71-80  12.1%
    # 81-90  7.2%
    # 91-100 2.2%
    secondary_stat = max(wrand(130, 2) - 30, randint(16, 24))  # Average: 35 [39]
    # 01-10  0.0%
    # 11-20  30.1%
    # 21-30  13.1%
    # 31-40  14.8%
    # 41-50  12.8%
    # 51-60  10.6%
    # 61-70  8.2%
    # 71-80  5.8%
    # 81-90  3.5%
    # 91-100 1.1%
    tertiary_stat = max(wrand(130, 3) - 30, randint(6, 14))  # Average: 30 [32]
    # 01-10  21.0%
    # 11-20  13.9%
    # 21-30  15.8%
    # 31-40  15.7%
    # 41-50  13.6%
    # 51-60  9.8%
    # 61-70  5.9%
    # 71-80  3.0%
    # 81-90  1.1%
    # 91-100 0.1%
    quaternary_stat = max(wrand(155, 3) - 55, randint(1, 6))  # Average: 27 [25]
    # 01-10  33.0%
    # 11-20  14.1%
    # 21-30  14.4%
    # 31-40  13.2%
    # 41-50  10.6%
    # 51-60  7.2%
    # 61-70  4.4%
    # 71-80  2.2%
    # 81-90  0.8%
    # 91-100 0.1%
    stats = [primary_stat, secondary_stat, tertiary_stat, quaternary_stat].shuffle()
    index = max(range(len(stats)), key=stats.__getitem__)

    loyalty = max(wrand(100, 2), 15)  # Random number between 15-100, weighted at 50
    tier = tier_picker(stats[index])

    if randint(stats[index], 250) > 180:
        spec_level = 2
    elif randint(stats[index], 250) > 195:
        spec_level = 3
    elif randint(stats[index], 250) > 210:
        spec_level = 4
    else:
        spec_level = 1

    first_name = random_line(open('first_names.txt'))
    last_name = random_line(open('last_names.txt'))

    if index == 0:  # Intelligence
        if tier == 4:
            spec_name = 'Forger'
        elif tier == 3:
            spec_name = 'Technician'
        elif tier == 2:
            spec_name = 'Hacker'
        else:
            spec_name = 'Forger'
    elif index == 1:  # Social (pimp?)
        if tier == 4:
            spec_name = 'Spy'
        elif tier == 3:
            spec_name = 'Recruiter'
        elif tier == 2:
            spec_name = 'Social Engineer'
        else:
            spec_name = 'Blackmailer'
    elif index == 2:  # Stealth
        if tier == 4:
            spec_name = 'Investigator'
        elif tier == 3:
            spec_name = 'Disguiser'
        elif tier == 2:
            spec_name = 'Lockpicker'
        else:
            spec_name = 'Pickpocketer'
    else:  # Strength (drug dealer?)
        if tier == 4:
            spec_name = 'Sniper'
        elif tier == 3:
            spec_name = 'Interrogator'
        elif tier == 2:
            spec_name = 'Soldier'
        else:
            spec_name = 'Guard'

    member = Member(
        owner=owner,
        supervisor=supervisor,
        name=first_name + ' ' + last_name,
        loyalty=loyalty,
        wage=0,  # TODO: Calculate with formula
        intelligence=stats[0],
        social=stats[1],
        stealth=stats[2],
        strength=stats[3],
        specialization=spec_name + '/' + spec_level
    )
    member.save()


def tier_picker(x):
    # Tier 4 [9.56%]
    if x > 75 and randint(min(x, 130), 130) > 100:
        return 4
    # Tier 3 [19.27%]
    elif x > 60 and randint(min(x, 130), 130) > 90:
        return 3
    # Tier 2 [28.76%]
    elif x > 40 and randint(min(x, 130), 130) > 85:
        return 2
    # Tier 1 [42.38%]
    else:
        return


def wrand(maximum, weight):
    """
    Returns a weighted random number.
    """
    # r = random() * (maximum / weight) + random() * (maximum / weight)
    r = 0
    for i in range(weight):
        r += random() * (maximum / weight)
    return int(round(r))

    # return int(minimum + (maximum - minimum) * pow(random.random(), power))


def random_line(f):
    lines = next(f)
    for num, line in enumerate(f):
        if random.randrange(num + 2):
            continue
        lines = line
    return lines

