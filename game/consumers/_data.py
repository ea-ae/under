gamedata = {
    'contacts': {
        'anonymous': {
            'name': 'Anonymous',
            'id': 'anonymous',
            'cards': {
                # The numbering system is the following
                # 1st number: The Chapter (contains multiple objectives & cards)
                # 2nd number: The Mission (usually contains one objective sometimes multiple cards)
                # 3rd number: Card Number (one for every card, each containing options; like dialogue)
                '1.0.0': {
                    'options': [
                        {
                            'text': 'I\'m done.',
                            'conditional': True
                        },
                        {
                            'text': 'Who are you?',
                            'conditional': False
                        }
                    ],
                    'text': '<p>So, you\'re looking to start a cult? I\'ll help you get started. Don\'t worry about any payments; you\'ll return the favor when the time comes.</p><p>First of all, you\'ll need a building for your cult to operate in. I found you a quiet place in the corner of the city where nobody will bother you. Go and visit it right now and buy it an upgrade of your choice.</p><p><b>Objective:</b> Visit the headquarters using the sidebar and purchase an upgrade of your choice.</p>'
                },
                '1.0.1': {
                    'options': [
                        {
                            'text': 'I\'m done.',
                            'conditional': True
                        }
                    ],
                    'text': '<p>My identity is of no importance, and I would rather stay cautious for now. I got in contact with you and am ready to help you, and that is all that matters. Anyway, let me know when you are done upgrading the headquarters.</p><p><b>Objective:</b> Visit the headquarters using the sidebar and purchase an upgrade of your choice.</p>'
                },
                '1.1.0': {
                    'options': [
                        {
                            'text': 'Okay I\'m done, what now?',
                            'conditional': True
                        },
                        {
                            'text': 'Tell me more about cultist stats, skills and jobs.',
                            'conditional': False
                        }
                    ],
                    'text': '<p>Now you need to find people to join your cult. Recruitment isn\'t an easy task, but I know a person who would be happy to join and help you.</p><p>All members of your cult have different stats and skills. For example, if a cultist has a high enough intelligence stat, he might be a technician or a hacker.</p><p>You should give your new cultist a job. I would recommend making him a recruiter since he has high social skills and your cult needs more members. A recruiter\'s job is to find and recruit new members to your cult.</p><p><b>Objective:</b> Visit the \'Members\' ake your new cult member work as a recruiter.</p>'
                },
                '1.1.1': {
                    'options': [
                        {
                            'text': 'Okay I\'m done, what now?',
                            'conditional': True
                        }
                    ],
                    'text': '<p>There are four stats: intelligence, social, stealth, and strength. Some skills are rarer than others. For instance, it is harder to find a spy (social skill) than a lockpicker (stealth skill). Your cultists can learn new skills and become better at those that they already have, but it\'s a slow and expensive process.</p><p>You can assign cultists passive jobs, such as recruiting, stealing, or researching. You will unlock more jobs in the future as you meet new people. Cultists aren\'t free; you have to pay them daily wages whether they were assigned to a job or not.</p><p><b>Objective:</b> Visit the \'Members\' ake your new cult member work as a recruiter.</p>'
                },
                '1.2.0': {
                    'options': [
                        {
                            'text': 'I have finished researching.',
                            'conditional': True
                        }
                    ],
                    'text': '<p>While your cult member is searching for new members, you can use your research points. You slowly earn research points as time passes, but you can earn them faster by upgrading your headquarters or assigning cultists with high intelligence stats to work as researchers.</p><p>Look at your options and spend your research points on whatever you like.</p><p><b>Objective:</b> Spend your research points on a new technology.</p>'
                }
            }
        },
        'assistant': {
            'name': 'Jessica Becker',
            'id': 'assistant',
            'cards': {
                '1.0.0': {
                    'options': [],
                    'text': '<p>Hello, I am grateful to have an opportunity to work as your assistant. If anything that you should know happens, I will let you know immediately.</p>'
                }
            }
        },
        'merchant': {
            'name': 'The Merchant',
            'id': 'merchant'
        }
    },
    'headquarters': {
        # HQ building levels
        'upgrades': [
            {
                'name': 'Motion Sensors',
                'id': 'motionsensors',
                'cost': 1000,
                'description': 'Detect movement in unauthorized areas.'
            },
            {
                'name': 'Window Security Bars',
                'id': 'windowbars',
                'cost': 2000,
                'description': 'Prevent intruders from entering through the windows - unless they have a metal cutter.'
            },
            {
                'name': 'CCTV System',
                'id': 'cctv',
                'cost': 5000,
                'description': 'Set up security cameras around the area.'
            },
            {
                'name': 'Uninterruptible Power Supply',
                'id': 'ups',
                'cost': 10000,
                'description': 'An emergency power supply in case the power goes out.'
            },
            {
                'name': 'Burglary Insurance',
                'id': 'insurance',
                'cost': 25000,
                'description': 'In case of a successful burglary, you get back 10% of your loss.'
            },
            {
                'name': 'Door Access Control System',
                'id': 'doorsystem',
                'cost': 75000,
                'description': 'All employees are given keycards that are used to open doors. Even though it makes a lockpicker useless, a technician could bypass it easily.'
            },
            {
                'name': 'Signal Jammers',
                'id': 'jammers',
                'cost': 100000,
                'description': 'Block any incoming signals to protect against hackers.'
            },
            {
                'name': 'Perimeter Fencing',
                'id': 'fencing',
                'cost': 125000,
                'description': 'Barbed wire metal fences that circle the perimeter to prevent unauthorized property access.'
            },
            {
                'name': 'Emergency Lockdown System',
                'id': 'lockdownsystem',
                'cost': 150000,
                'description': 'In case of a detected intrusion, block all doors and windows from opening.'
            }
        ],
        'buildings': [
            {  # Default level 1 building
                'cost': 0,
                'bonus_upgrades': 5
            },
            {
                'cost': 1000000,
                'bonus_upgrades': 7
            },
            {
                'cost': 10000000,
                'bonus_upgrades': 10
            },
            {
                'cost': 25000000,
                'bonus_upgrades': 15
            },
            {
                'cost': 100000000,
                'bonus_upgrades': 25
            }
        ]
    }
}
