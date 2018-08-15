import json


def members_data(self):
    db_members = self.cult.member_set.all()
    members = []

    for db_member in db_members:
        spec_name, spec_level = db_member.specialization.split('/')
        skills = json.loads(db_member.skills)

        if db_member.supervisor is None:
            supervisor = -1
        else:
            supervisor = db_member.supervisor.id

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


def generate_member(self):
    pass
