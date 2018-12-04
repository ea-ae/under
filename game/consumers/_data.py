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
                    'text': '<p>So, you\'re looking to start a cult? I\'ll help you get started. Don\'t worry about any payments; you\'ll return the favor when the time comes.</p><p>First of all, you\'ll need a building for your cult to operate in. I found you a quiet place in the corner of the city where nobody should bother you. Go and visit it right now and buy it an upgrade of your choice.</p><p><b>Objective:</b> Visit the headquarters using the sidebar and purchase an upgrade of your choice.</p>'
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
                            'conditional': False
                        },
                        {
                            'text': 'Tell me more about cultist stats, specializations, skills, and jobs.',
                            'conditional': False
                        }
                    ],
                    'text': '<p>Now you need to find people to join your cult. Recruitment isn\'t an easy task, but I know a person was happy to join and help you. That person is already in the cult and you can see him in the \'Members\' tab.</p><p>You should give your new cultist a job. I would recommend making the new cultist work as a recruiter, since that person has high social skills and your cult needs more members. A recruiter\'s job is to find and recruit new members to your cult.</p><p><b>Objective:</b> Visit the \'Members\' tab and make your new cult member work as a recruiter.</p>'
                },
                '1.1.1': {
                    'options': [
                        {
                            'text': 'Okay I\'m done, what now?',
                            'conditional': True
                        }
                    ],
                    'text': '<p>There are four stats: intelligence, social, stealth, and strength. The type of specialization your cultist will have will depend on the highest stat. A specialization\'s rarity depends on its tier. For instance, it is harder to find a spy (tier 4 social specialization) than a lockpicker (tier 2 stealth specialization). You can research new learnable skills and teach them to your cultists.</p><p>All cultists can be assigned passive jobs, such as recruiting, stealing, or researching. Some jobs are only available to certain specializations (such as pickpocketing), and some jobs are unlocked by research.</p><p><b>Objective:</b> Visit the \'Members\' tab and make your new cult member work as a recruiter.</p>'
                },
                '1.2.0': {
                    'options': [
                        {
                            'text': 'I have finished researching.',
                            'conditional': True
                        }
                    ],
                    'text': '<p>While your cultist is searching for new members, let\'s use your research points. You slowly earn research points as time passes, but you can earn them faster by upgrading your headquarters or assigning cultists with high intelligence stats to work as researchers.</p><p>Look at your options and spend your research points on whatever you like.</p><p><b>Objective:</b> Spend your research points.</p>'
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
                    'text': '<p>I see you have a new recruit. Secrecy and anonymity are very important in a cult. Cultists only know the identities of the people they recruited and were recruited by.</p><p>Let\'s say that one of your cultists gets caught by the police. The lower the cult member\'s loyalty, the higher the chance that the police successfully make him talk and give out the identities of every cult member he knows.</p><p>Having a police informant in your cult isn\'t even the biggest threat. A spy from a rival cult is significantly worse. Depending on the job you give to a spy, they could steal your research points, recruit more of their spies into your cult, or worse.</p>'
                },
                '1.4.1': {
                    'options': [
                        {
                            'text': 'I will pay for it myself.',
                            'conditional': True
                        },
                        {
                            'text': 'Okay, you can pay for the portal.',
                            'conditional': False
                        }
                    ],
                    'text': '<p>I believe you\'re ready now. Ready to venture into the Underworld. Believe me, it\'s much worse than whatever you\'ve heard about it.</p><p>You have to create a special portal to access it. The problem is that almost nobody knows how to build these portals - so I\'m quite lucky to know someone who does.</p><p>He said that in order to build it he\'ll require $10,000 and everything else will be taken care of. If you want, I can pay for it myself, but in return you will have to bring me one thing from there once you find it. Oh, and by the way, you can always check out the \'Wiki\' tab if anything is confusing or you want to learn more about some topics.</p><p><b>Objective:</b> Pay $10,000 or accept help.</p>'
                },
                '1.4.2': {
                    'options': [
                        {
                            'text': '???',
                            'conditional': True
                        }
                    ],
                    'text': '<p>This part is not done yet.</p>'
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
                            'text': 'Okay.',
                            'conditional': False
                        }
                    ],
                    'text': '<p>Hello, I am grateful to have the opportunity to work for you. I will make sure that everything will operate as it should in this ... organization.</p><p>We have successfully recruited a new member. You can look at the details of new recruits and either accept or reject them. Right now we can\'t really afford the luxury of being picky and refusing people, so I\'d recommend you accept the recruit.</p>'
                },
                '1.0.1': {
                    'options': [],
                    'text': '<p>Anyway, I will start working now, there are a lot of things to do. Let me know if you need anything.</p>'
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
                    'text': '<p>There are other ways to earn money, but they aren\'t good enough, at least not yet. You could for example invest in stocks or currencies, but it\'s a risky and unstable way to make income. You could also trade in the marketplace, but we don\'t have enough money and resources for it to be feasible yet.</p>'
                },
                '1.1.2': {
                    'options': [],
                    'text': '<p>He should contact you any moment. I will continue working now, let me know if you need anything.</p>'
                }
            }
        },
        'vincent': {
            'name': 'Vincent Polizzi',
            'id': 'vincent',
            'cards': {
                '1.0.0': {
                    'options': [
                        {
                            'text': 'I am ready, give me the task.',
                            'conditional': False
                        },
                        {
                            'text': 'Who exactly are you?',
                            'conditional': False
                        }
                    ],
                    'text': '<p>So, you\'re looking for a contract? I can offer you one contract every day; whether you will accept or decline it is your own decision. But before I give you a proper task, I need to make sure you are actually capable of doing this and won\'t let me down.</p>'
                },
                '1.0.1': {
                    'options': [
                        {
                            'text': 'I am ready, give me the task.',
                            'conditional': False
                        }
                    ],
                    'text': '<p>People tell me if they need something done. They pay me. Then I contact you, you do what I ask, and I give you a share of the money.</p>'
                },
                '1.0.2': {
                    'options': [],
                    'text': '<p>Here is your first mission. A person named Jonathan Harrison stole one very important thing from us. We found out where he was hiding, but he killed himself before we could capture and interrogate him.</p><p>He didn\'t have the item with him when we found him, but we found out that he has recently rented a storage unit from a nearby self-storage facility.</p><p>The company didn\'t tell us which storage unit is his, saying it was confidential information. Find the container, break into it, and bring us the item.</p>'
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
