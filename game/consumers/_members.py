import json


def members_data(self):
    db_members = self.cult.member_set.all()
    members = []

    for db_member in db_members:
        spec_name, spec_level = db_member.specialization.split('/')
        skills = json.loads(db_member.skills)
        members.append({
            'id': db_member.id,
            'supervisor': db_member.supervisor_id,
            'name': db_member.name,
            'loyalty': db_member.loyalty,
            'job': job_from_id(db_member.job_id),

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


def job_from_id(job_id):
    if job_id == 0:
        return 'None'
    elif job_id == 1:
        return 'Recruiting',
    elif job_id == 2:
        return 'Researching',
    elif job_id == 3:
        return 'Guarding'
    else:
        return 'Unknown'
