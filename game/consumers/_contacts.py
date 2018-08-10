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
            if option['conditional']:
                options.append({
                    'text': option['text'],
                    'enabled': self.option_check(data_contact['id'], db_contact['card'], i)
                })
            else:
                options.append({
                    'text': option['text'],
                    'enabled': True
                })

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
    db_contacts = json.loads(cult.contacts)

    for i, db_contact in enumerate(db_contacts):
        # Find the correct contact from the list in the database json
        if data['contact'] == db_contact['id']:
            # Get the card information (like the available options) from data.py
            data_card = gamedata['contacts'][data['contact']]['cards'][db_contact['card']]
            # Check if chosen option number is bigger than the amount of options
            if len(data_card['options']) > data['choice']:
                # Make sure that the objective has been completed
                if data_card['options'][data['choice']]['conditional']:
                    if not self.option_check(db_contact['id'], db_contact['card'], data['choice']):
                        # False returned, objective is not completed
                        self.user_error('User chose a disabled option.')
                        return False
                # Find what contact the choice was made for
                if db_contact['id'] == 'anonymous':
                    # Find what card the choice was made in
                    if db_contact['card'] == '1.0.0' or db_contact['card'] == '1.0.1':
                        if data['choice'] == 0:
                            self.set_card(cult, db_contacts, i, '1.1.0')
                        elif data['choice'] == 1:
                            self.set_card(cult, db_contacts, i, '1.0.1')
                    if db_contact['card'] == '1.1.0' or db_contact['card'] == '1.1.1':
                        if data['choice'] == 0:
                            self.set_card(cult, db_contacts, i, '1.2.0')
                        if data['choice'] == 1:
                            self.set_card(cult, db_contacts, i, '1.1.1')
                    if db_contact['card'] == '1.2.0':
                        pass


def option_check(self, contact_name, card, choice_index):
    """
    Checks whether an option should be enabled (mission completed) or not.
    """
    if contact_name == 'anonymous':
        if card == '1.0.0' or card == '1.0.1':
            if choice_index == 0:
                return True
        elif (card == '1.1.0' or card == '1.1.1') and choice_index == 0:
            return True
        elif card == '1.2.0':
            return False
    return False


def set_card(self, cult, db_contacts, i, card_value):
    db_contacts[i]['card'] = card_value
    cult.contacts = json.dumps(db_contacts)
    cult.save()
    self.page_data('contacts')
