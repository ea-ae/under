from game.models import Member
from random import randint, randrange, shuffle

import json
from random import random
from datetime import timedelta
from django.utils.timezone import now


def members_data(self):
    db_members = self.cult.member_set.all()
    members = []

    recruit = None

    for db_member in db_members:
        spec_name, spec_level = db_member.specialization.split('/')
        skills = json.loads(db_member.skills)

        # Faster than db_member.supervisor.id
        if db_member.supervisor_id is None:
            supervisor = -1
        else:
            supervisor = db_member.supervisor_id

        if db_member.accepted:
            members.append({
                'id': db_member.id,
                'supervisor': supervisor,
                'name': db_member.name,
                'loyalty': db_member.loyalty,
                'wage': db_member.wage,
                'job': db_member.job,
                'stats': [db_member.intelligence,
                          db_member.social,
                          db_member.stealth,
                          db_member.strength],
                'spec_name': spec_name,
                'spec_level': int(spec_level),
                'skills': skills
            })
        else:
            recruit = {
                'id': db_member.id,
                'supervisor': supervisor,
                'name': db_member.name,
                'loyalty': db_member.loyalty,
                'wage': db_member.wage,
                'job': db_member.job,
                'stats': [db_member.intelligence,
                          db_member.social,
                          db_member.stealth,
                          db_member.strength],
                'spec_name': spec_name,
                'spec_level': int(spec_level),
                'skills': skills
            }

    self.send_json({
        'type': 'page_data',
        'page': 'members',
        'jobs': ['none', 'recruiting', 'researching', 'guarding', 'pickpocketing'],
        'recruit': recruit,
        'members': members
    })


def generate_member(self, owner, supervisor):
    """
    Creates a new randomly-generated Member.
    """
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
    stats = [primary_stat, secondary_stat, tertiary_stat, quaternary_stat]
    shuffle(stats)
    index = max(range(len(stats)), key=stats.__getitem__)

    loyalty = max(wrand(130, 2) - 30, 10)  # Random number between 10-100, weighted at 35
    tier = tier_picker(stats[index])

    if randint(stats[index], 250) > 180:
        spec_level = 2
    elif randint(stats[index], 250) > 195:
        spec_level = 3
    elif randint(stats[index], 250) > 210:
        spec_level = 4
    else:
        spec_level = 1

    first_name = random_line(open('game/consumers/first_names.txt'))
    last_name = random_line(open('game/consumers/last_names.txt'))

    if index == 0:  # Intelligence
        if tier == 4:
            spec_name = 'Mastermind'
        elif tier == 3:
            spec_name = 'Hacker'
        elif tier == 2:
            spec_name = 'Forger'
        else:
            spec_name = 'Technician'
    elif index == 1:  # Social (pimp?)
        if tier == 4:
            spec_name = 'Spy'
        elif tier == 3:
            spec_name = 'Manager'
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

    wage = int(((sum(stats)) * 4 + loyalty * 10 + pow((tier * 10), 2) + pow((spec_level * 8), 2)) * (randint(5, 15) / 40))

    member = Member(
        owner=owner,
        supervisor=supervisor,
        accepted=False,
        name=first_name + ' ' + last_name,
        loyalty=loyalty,
        wage=wage,
        intelligence=stats[0],
        social=stats[1],
        stealth=stats[2],
        strength=stats[3],
        specialization=str(spec_name) + '/' + str(spec_level)
    )

    return member


def process_ticks(self):
    """
    Processes job ticks.
    """
    print('Process ticks...')
    db_members = self.cult.member_set.all()  # We are querying the db for game members every single time

    minutes = int((now() - self.cult.last_check).total_seconds() / 60)

    member_weights = []  # Recruitment chance weights for all members
    member_count = 0
    recruitment_points = minutes  # One recruitment point earned per minute
    research_points = 0

    has_recruit = False

    for db_member in db_members:
        member_count += 1
        weight = 0

        if not db_member.accepted:
            # This means we have a recruit
            # While there is an available recruit, no recruitment points are earned
            has_recruit = True

        if db_member.job == 'recruiting':
            recruitment_points += db_member.social * minutes / 10
            # Check if the social stat is the largest (so the person has a social specialization)
            if all(st >= db_member.social for st in [db_member.intelligence, db_member.stealth, db_member.strength]):
                # Give bonus weight if that is true
                weight += 30
        elif db_member.job == 'researching':
            research_points += db_member.intelligence * minutes / 10

        weight += db_member.social  # Add weight equal to the social stat
        member_weights.append(weight)

    print('VVV MEMBER WEIGHTS')
    print(member_weights)
    print('^^^ MEMBER WEIGHTS')

    recruitment_target = int(2 ** member_count * 25)  # len(member_weights)
    recruitment_points = int(round(recruitment_points))
    research_points = int(round(research_points))

    if not has_recruit:
        if self.cult.recruitment_points + recruitment_points >= recruitment_target:
            # We have reached the required recruitment points that are needed to get a new recruit
            self.cult.recruitment_points = 0
            if randint(1, 7) == 1:
                supervisor = None  # Sometimes you will directly recruit new members
            else:
                supervisor = db_members[weighted_choice(member_weights)] if len(member_weights) else None
            recruit = self.generate_member(self.cult, supervisor)
            recruit.save()
        else:
            self.cult.recruitment_points += recruitment_points

    self.cult.research_points += research_points

    self.cult.last_check += timedelta(minutes=minutes)
    self.cult.save(update_fields=['recruitment_points', 'research_points', 'last_check'])
    print('=========')
    print('MINUTES PROCESSED: ' + str(minutes))
    print('RESEARCH POINTS ADDED: ' + str(research_points))
    print('RECRUITMENT POINTS ADDED: ' + str(recruitment_points))
    print('RECRUITMENT COST: ' + str(recruitment_target))
    print('time then: ' + str(self.cult.last_check))
    print('time now, not last check: ' + str(now()))


def process_recruit(self, choice):
    """
    Called when a recruit is accepted or rejected.
    """
    if choice is None:
        self.log('No recruit choice provided.')
        return False
    try:
        recruit = Member.objects.get(owner=self.cult, accepted=False)
    except Member.DoesNotExist:
        self.log('Called recruit accept/delete command when there isn\'t a recruit.')
    else:
        if choice == 'accept':
            self.process_ticks()  # To prevent cheating
            recruit.accepted = True
            recruit.save()
            self.log('Accepted recruit.', 'info')
            self.members_data()  # Refresh page
        elif choice == 'reject':
            recruit.delete()
            self.log('Declined recruit.', 'info')


def tier_picker(x):
    """
    Returns a random tier from 1 to 4.
    """
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
        return 1


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


def weighted_choice(weights):
    """
    Select weighted choice.
    """
    rnd = random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            print(i)
            print('^^^ OUR INDEX CHOSEN!')
            return i


def random_line(f):
    """
    Selects a random line from a file and strips the newline character.
    """
    lines = next(f)
    for num, line in enumerate(f):
        if randrange(num + 2):
            continue
        lines = line
    return lines.rstrip('\n')

