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
                    'text': '<p>Now you need to find people to join your cult. Recruitment isn\'t an easy task, but I know a person who would be happy to join and help you.</p><p>All members of your cult have different stats and skills. For example, if a cultist has a high enough intelligence stat, he might be a technician or a hacker.</p><p>You should give your new cultist a job. I would recommend making him a recruiter since he has high social skills and your cult needs more members. A recruiter\'s job is to find and recruit new members to your cult.</p><p><b>Objective:</b> Visit the \'Members\' tab and make your new cult member work as a recruiter.</p>'
                },
                '1.1.1': {
                    'options': [
                        {
                            'text': 'Okay I\'m done, what now?',
                            'conditional': True
                        }
                    ],
                    'text': '<p>There are four stats: intelligence, social, stealth, and strength. Some skills are rarer than others. For instance, it is harder to find a spy (social skill) than a lockpicker (stealth skill). Your cultists can learn new skills and become better at those that they already have, but it\'s a slow and expensive process.</p><p>You can assign cultists passive jobs, such as recruiting, stealing, or researching. You will unlock more jobs in the future as you meet new people. Cultists aren\'t free; you have to pay them daily wages whether they were assigned to a job or not.</p><p><b>Objective:</b> Visit the \'Members\' tab and make your new cult member work as a recruiter.</p>'
                },
                '1.2.0': {
                    'options': [
                        {
                            'text': 'I have finished researching.',
                            'conditional': True
                        }
                    ],
                    'text': '<p>While your cult member is searching for new members, let\'s use your research points. You slowly earn research points as time passes, but you can earn them faster by upgrading your headquarters or assigning cultists with high intelligence stats to work as researchers.</p><p>Look at your options and spend your research points on whatever you like.</p><p><b>Objective:</b> Spend your research points.</p>'
                },
                '1.3.0': {
                    'options': [
                        {
                            'text': 'What do I do next?',
                            'conditional': True
                        }
                    ],
                    'text': '<p>I hired you an assistant who will let you know whenever anything that you should know happens. Don\'t worry, she can be trusted.</p><p><b>Objective:</b> Talk to the assistant.</p>'
                },
                '1.4.0': {
                    'options': [
                        {
                            'text': 'Well, that wouldn\'t be good.',
                            'conditional': False
                        }
                    ],
                    'text': '<p>I see you have a new cult member. Secrecy and anonymity are very important in a cult. Cultists only know the identities of the people they recruited and were recruited by.</p><p>Let\'s say that one of your cultists gets caught by the police. The lower the cult member\'s loyalty, the higher the chance that the police successfully make him talk and give out the identities of every cult member he knows.</p><p>Having a police informant in your cult isn\'t even the biggest threat. A spy from a rival cult is significantly worse. Depending on the job you give to a spy, they could steal your research points, recruit more of their spies into your cult, or worse.</p>'
                },
                '1.4.1': {
                    'options': [
                        {
                            'text': 'I got everything you need.',
                            'conditional': True
                        }
                    ],
                    'text': '<p>I believe you\'re ready now. Ready to venture into the Underworld. You might have heard stories about different mythical creatures and demons that reside there, but it\'s much worse than in the stories.</p><p>You have to create a special portal to access it. Almost nobody knows how to build these portals, so I\'m lucky to know someone who does.</p><p>He said that in order to build it he\'ll require $50,000 and that he\'ll take care of the rest.</p><p><b>Objective:</b> Pay $50,000.</p>'
                },
                '1.4.2': {
                    'options': [
                        {
                            'text': '???',
                            'conditional': True
                        }
                    ],
                    'text': '<p>What? No, what is it? Tell me now, what is it? What? What? What? Nothing? Whatever. Is it nothing? Nothing at all? Fine. Whatever. Sure. Nothing.</p>'

                },
                '1.4.3': {
                    'options': [],
                    'text': '<p>The end.</p>'
                }
            }
        },
        'assistant': {
            'name': 'Jessica Becker',
            'id': 'assistant',
            'cards': {
                '1.0.0': {
                    'options': [
                        {
                            'text': 'Did as you suggested.',
                            'conditional': True
                        }
                    ],
                    'text': '<p>Hello, I am grateful to have the opportunity to work for you. I will make sure that everything will operate as it should in this ... organization.</p><p>Anyway, we have successfully recruited a new member. You can look at the details of new cult recruits and either accept or reject them. Right now we can\'t really afford the luxury of being picky and refusing people, so you should probably just accept him.</p><p><b>Objective:</b> Accept the recruit into the cult.</p>'
                },
                '1.0.1': {
                    'options': [],
                    'text': 'Okay, great. I will start working now, there are a lot of things to do. Let me know if you need anything.'
                },
                '1.1.0': {
                    'options': [
                        {
                            'text': 'Contact him.',
                            'conditional': False
                        },
                        {
                            'text': 'Any alternative, not-that-illegal options?',
                            'conditional': False
                        }
                    ],
                    'text': 'We really need to start earning more income. You could give cultists passive income-earning jobs, but that wouldn\'t be nearly enough. I know a person who might have some work available. He would give us the details, our cultists do it, and we get the money.</p><p>Due to the nature of this work, there is a risk some of your cultists might get arrested, but we cannot expand without money, so I think we should do it.</p>'
                },
                '1.1.1': {
                    'options': [
                        {
                            'text': 'Contact him, I\'ll think about it.',
                            'conditional': False
                        }
                    ],
                    'text': '<p>There are other ways to earn money, but they aren\'t good enough, at least yet. You could for example invest in stocks or currencies, but it\'s a risky and unstable way to make income. You could also trade in the marketplace, but we don\'t have enough money and resources for it to be feasible yet.</p>'
                },
                '1.1.2': {
                    'options': [],
                    'text': '<p>He should contact you any moment. I will continue working now, let me know if you need anything.</p>'
                }
            }
        },
        'mafioso': {
            'name': 'Vincent Polizzi',
            'id': 'mafioso',
            'cards': {
                '1.0.0': {
                    'options': [
                        {
                            'text': 'Alright, I am ready.',
                            'conditional': False
                        },
                        {
                            'text': 'Who exactly are you?',
                            'conditional': False
                        }
                    ],
                    'text': '<p>So, you\'re looking for a contract? I can offer you one contract every hour, whether you will accept or decline it is your own decision.</p>'
                },
                '1.0.1': {
                    'options': [
                        {
                            'text': 'Alright, I am ready.',
                            'conditional': False
                        }
                    ],
                    'text': '<p>People tell me if they need something done. They pay me. Then I contact you, you do what I ask, and I give you a share of the money.</p>'
                },
                '1.0.2': {
                    'options': [],
                    'text': '<p>Here is your first task...</p>'
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
        'upgrades': {
            'windowbars': 2500,
            'motionsensors': 5000,
            'cctv': 7500,
            'ups': 10000,
            'insurance': 25000,
            'doorsystem': 75000,
            'jammers': 100000,
            'fencing': 125000,
            'lockdownsystem': 150000
        },
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