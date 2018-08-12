from ._data import gamedata
import json


def contacts_data(self):
    db_contacts = json.loads(self.cult.contacts)
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
            or not isinstance(data.get('choice'), int)
            or not isinstance(data.get('contact'), str)
            or data['contact'] not in gamedata['contacts'].keys()
            or data['choice'] < 0):
        print(data)
        self.log('Invalid choice process data.')
        return False
    db_contacts = json.loads(self.cult.contacts)

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
                        self.log('User chose a disabled option.', 'warning')
                        return False
                # Find what contact the choice was made for
                if db_contact['id'] == 'anonymous':
                    # Find what card the choice was made in
                    if db_contact['card'] == '1.0.0' or db_contact['card'] == '1.0.1':
                        if data['choice'] == 0:
                            self.set_card(db_contacts, i, '1.1.0')
                        elif data['choice'] == 1:
                            self.set_card(db_contacts, i, '1.0.1')
                    elif db_contact['card'] == '1.1.0' or db_contact['card'] == '1.1.1':
                        if data['choice'] == 0:
                            self.set_card(db_contacts, i, '1.2.0')
                        elif data['choice'] == 1:
                            self.set_card(db_contacts, i, '1.1.1')
                    elif db_contact['card'] == '1.2.0':
                        db_contacts.append({'id': 'assistant', 'card': '1.0.0'})
                        self.cult.contacts = json.dumps(db_contacts)
                        self.cult.save(update_fields=['contacts'])
                        self.set_card(db_contacts, i, '1.3.0')
                    elif db_contact['card'] == '1.3.0':
                        self.set_card(db_contacts, i, '1.4.0')
                    elif db_contact['card'] == '1.4.0':
                        # Set assistant's card to '1.1.0'
                        db_contacts[1]['card'] = '1.1.0'
                        self.cult.contacts = json.dumps(db_contacts)
                        self.cult.save(update_fields=['contacts'])
                        self.set_card(db_contacts, i, '1.4.1')
                    elif db_contact['card'] == '1.4.1':
                        self.set_card(db_contacts, i, '1.4.2')

                elif db_contact['id'] == 'assistant':
                    if db_contact['card'] == '1.0.0':
                        self.set_card(db_contacts, i, '1.0.1')
                    elif db_contact['card'] == '1.1.0' or db_contact['card'] == '1.1.1':
                        if data['choice'] == 0:
                            db_contacts.append({'id': 'mafioso', 'card': '1.0.0'})
                            self.cult.contacts = json.dumps(db_contacts)
                            self.cult.save(update_fields=['contacts'])
                            self.set_card(db_contacts, i, '1.1.2')
                        elif data['choice'] == 1:
                            self.set_card(db_contacts, i, '1.1.1')
                elif db_contact['id'] == 'mafioso':
                    if db_contact['card'] == '1.0.0' or db_contact['card'] == '1.0.1':
                        if data['choice'] == 0:
                            self.set_card(db_contacts, i, '1.0.2')
                        if data['choice'] == 1:
                            self.set_card(db_contacts, i, '1.0.1')


def option_check(self, contact_name, card, choice_index):
    """
    Checks whether an option should be enabled (mission completed) or not.
    """
    if contact_name == 'anonymous':
        if card == '1.0.0' or card == '1.0.1':
            if choice_index == 0:
                # Objective: Visit the headquarters using the sidebar and purchase an upgrade of your choice.
                # Check if at least 1 upgrade has been bought
                return len(json.loads(self.cult.headquarters)) >= 1
        elif (card == '1.1.0' or card == '1.1.1') and choice_index == 0:
            return True
        elif card == '1.2.0':
            return True
        elif card == '1.3.0':
            contacts = json.loads(self.cult.contacts)
            # Check if the assistant's card is not '1.0.0'
            return contacts[1]['card'] != '1.0.0'
    elif contact_name == 'assistant':
        if card == '1.0.0':
            # Objective: Accept the recruit into the cult.
            return True
    return False


def set_card(self, db_contacts, i, card_value):
    self.log('Setting card of ' + db_contacts[i]['id'] + ' to "' + card_value + '".', 'info')
    db_contacts[i]['card'] = card_value
    self.cult.contacts = json.dumps(db_contacts)
    self.cult.save(update_fields=['contacts'])
    self.page_data('contacts')
