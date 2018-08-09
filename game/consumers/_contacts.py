from game.models import Cult
from ._data import gamedata
import json


def contacts_data(self):
    db_contacts = json.loads(Cult.objects.get(owner=self.player).contacts)
    data_contacts = {}
    for db_contact in db_contacts:
        # Every single db_contact contains a {id: 'contact_name', card: 'card_name_like_2.1.7'}
        # We can get the text and options of a text_title
        data_contact = gamedata['contacts'][db_contact['id']]
        data_card = data_contact['cards'][db_contact['card']]  # Contains options/text of the card

        options = []

        for i, option in enumerate(data_card['options']):
            options.append({
                'text': option['text'],
                'enabled': self.option_check(data_contact['name'], db_contact['card'], i)
            })
            '''
            if option['conditional']:
                options.append({
                    'text': option['text'],
                    'enabled': self.option_check(contact['name'], db_contact['card'], i)
                })
            else:
                options.append({
                    'text': option['text'],
                    'enabled': True
                })
            '''

        data_contacts[data_contact['id']] = {
            'name': data_contact['name'],
            'id': data_contact['id'],
            'options': options,
            'text': data_card['text']
        }

    self.send_json({
        'type': 'page_data',
        'page': 'contacts',
        'contacts': data_contacts
    })


def process_choice(self, data):
    """
    Called when a dialog option is selected in the contacts menu.
    """
    if (data is None
            or not isinstance(data.get('choice', None), int)
            or not isinstance(data.get('contact', None), str)
            or data['contact'] not in gamedata['contacts'].keys()
            or data['choice'] < 0):
        print(data)
        self.user_error('Invalid choice process data.')
        return False
    cult = Cult.objects.get(owner=self.player)
    contacts = json.loads(cult.contacts)

    for i, contact in enumerate(contacts):
        # Find the correct contact from the list in the database json
        if data['contact'] == contact['id']:
            # Get the card information (like the available options) from data.py
            card = gamedata['contacts'][data['contact']]['cards'][contact['card']]
            # Check if chosen option number is bigger than the amount of options
            if len(card['options']) > data['choice']:
                # Find what contact the choice was made for
                if contact['id'] == 'anonymous':
                    # Find what card the choice was made in
                    if contact['card'] == '1.0.0' or contact['card'] == '1.0.1':
                        if data['choice'] == 0:
                            print('OPTION 0 SELECTED!')
                        elif data['choice'] == 1 and contact['card'] == '1.0.0':
                            print('OPTION 1 SELECTED!')
                            # if option_check(contact['id']):  # Make sure that objective was completed
                            contacts[i]['card'] = '1.0.1'
                            cult.contacts = json.dumps(contacts)
                            cult.save()
                            self.page_data('contacts')  # Send client updated contacts page data


def option_check(self, contact_name, card, choice_index):
    """
    Checks whether an option should be enabled (mission completed) or not.
    """
    if contact_name == 'anonymous':
        if card == '1.0.0' or card == '1.0.1':
            if choice_index == 0:
                return True  # TEMPORARY! HQ not implemented yet.
        elif card == '1.1.0':
            if choice_index == 0:
                return True  # TEMPORARY!
