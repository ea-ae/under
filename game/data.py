gamedata = {
    'contacts': {
        'anonymous': {
            'name': 'Anonymous',
            'id': 'anonymous',
            'cards': {
                # The numbering system is the following
                # 1st number: The Chapter (contains multiple objectives & cards)
                # 2nd number: The Mission (contains one objective & may contain multiple cads)
                # 3rd number: Card Number (one for every card, each containing options; like dialogue)
                '1.0.0': {
                    'options': [
                        {
                            'text': 'I\'m done.',
                            'conditional': True
                        }, {
                            'text': 'Who are you?',
                            'conditional': False
                        }
                    ],
                    'text': '<p>So, you\'re looking to start a cult? I\'ll help you get started. Don\'t worry about any payments for now, you\'ll return the favor when the time comes.</p><p>First of all, you\'ll need a building for your cult to operate in. I found you a quiet place in the corner of the city, nobody should bother you there. Go and visit it right now and buy it an upgrade of your choice.</p><p><b>Objective:</b> Visit the headquarters using the sidebar and purchase an upgrade of your choice.</p>'
                },
                '1.0.1': {
                    'options': [
                        {
                            'text': 'I\'m done.',
                            'conditional': True
                        }
                    ],
                    'text': '<p>My identity is of no importance, and I would rather stay cautious for now. I got in contact with you and am ready to help you, and that is all that matters. Anyway, tell me once you are done with upgrading the headquarters.</p><p><b>Objective:</b> Visit the headquarters using the sidebar and purchase an upgrade of your choice.</p>'
                }
            }
        },
        'merchant': {
            'name': 'The Merchant',
            'id': 'merchant'
        }
    }
}
