from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync as ats

from .models import WarfareGame, WarfarePlayer, Cult
from .data import gamedata

import json
import re


class WarfareConsumer(JsonWebsocketConsumer):
    """
    Handles the WebSocket connections for 'Warfare' games.
    self.player - the player object
    self.cult - currently selected cult
    """

    def connect(self):
        """
        Handles incoming connections.
        """
        self.authorized = False
        print('Connect [1/4]: Attempted join')
        if self.scope['user'].is_authenticated:  # Check if user is logged in
            print('Connect [2/4]: Is authenticated')
            try:
                self.player = WarfarePlayer.objects.get(user=self.scope['user'])
            except WarfarePlayer.DoesNotExist:  # New user
                print('Connect [3/4]: New user connected.')
                self.player = WarfarePlayer(user=self.scope['user'],
                                            game=WarfareGame.objects.get(name='alpha'))
                self.player.save()
                self.cult = Cult(owner=self.player)  # Create a new cult for the new player
                self.cult.save()
            else:  # Returning user
                print('Connect [3/4]: Returning user connected.')
                try:
                    self.cult = Cult.objects.get(owner=self.player)
                except Cult.DoesNotExist:
                    self.user_error('Cult does not exist.')
                    self.close()
                    return False
            ats(self.channel_layer.group_add)('wf1_chat_general', self.channel_name)
            self.authorized = True
            print('Connect [4/4]: Connection established.')
            self.accept()
        else:
            self.user_error('User is unauthenticated.')

    def receive_json(self, content, **kwargs):
        """
        Called when the customer sends data to us.
        """
        print('receive_json(): ' + str(content))
        request_type = content.get('type', None)
        if request_type == 'page_data':  # Client requests data to load a tab
            self.page_data(content.get('page', None))  # Send the requested page over to page_data()
        elif request_type == 'card_choice':  # User clicked on an option in a card
            self.process_choice({'contact': content.get('contact', None),
                                 'choice': content.get('choice', None)})
        elif request_type == 'create_cult':
            self.create_cult(content.get('cult_data', None))
        else:
            self.user_error('Unknown message type received.')

    def page_data(self, page):
        """
        Sends data about the requested page back to the client.
        """
        if page == 'home':
            if self.cult.type == 'none':  # Cult is not created yet
                self.send_json({
                    'type': 'page_data',
                    'page': page
                })
            else:
                self.send_json({
                    'type': 'page_data',
                    'page': page,
                    'username': self.scope['user'].profile.display,
                    'cult': {
                        'name': self.cult.name,
                        'type': self.cult.type,
                        'money': self.cult.money,
                        'rep': self.cult.reputation
                    }
                })
        elif page == 'contacts':
            contacts = json.loads(Cult.objects.get(owner=self.player).contacts)
            contacts_data = {}
            for db_contact in contacts:
                # Every single db_contact contains a {id: 'contact_name', card: 'card_name_like_2.1.7'}
                # We can get the text and options of a text_title
                contact = gamedata['contacts'][db_contact['id']]
                card = contact['cards'][db_contact['card']]
                options = []  # Generate options dictionary, with enabled/disabled keys

                i = 0
                for option in card['options']:
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
                    i += 1  # Increase choice index

                contacts_data[contact['id']] = {
                    'name': contact['name'],
                    'id':  contact['id'],
                    'options': options,
                    'text': card['text']
                }

            self.send_json({
                'type': 'page_data',
                'page': page,
                'contacts': contacts_data
            })
        elif page == 'inventory':
            self.send_json({
                'type': 'page_data',
                'page': page
            })
        elif page == 'inventory':
            self.send_json({
                'type': 'page_data',
                'page': page
            })
        elif page == 'members':
            self.send_json({
                'type': 'page_data',
                'page': page
            })
        elif page == 'headquarters':
            self.send_json({
                'type': 'page_data',
                'page': page
            })
        elif page == 'marketplace':
            self.send_json({
                'type': 'page_data',
                'page': page
            })
        elif page == 'underworld':
            self.send_json({
                'type': 'page_data',
                'page': page
            })
        elif page == 'settings':
            self.send_json({
                'type': 'page_data',
                'page': page
            })
        elif page == 'wiki':
            self.send_json({
                'type': 'page_data',
                'page': page
            })
        elif page == 'rules':
            self.send_json({
                'type': 'page_data',
                'page': page
            })
        else:
            self.user_error('Unknown tab "' + page + '" requested.')

    def create_cult(self, data):
        """
        Creates a new cult.
        """
        if data is None:
            self.user_error('Cult creation data is None.')
        if (self.cult.type == 'none'
                and isinstance(data['cult_name'], str)
                and re.match('^[a-zA-Z ]{5,25}$', data['cult_name'])
                and data.get('cult_type', None) in {'chi', 'psi', 'omega'}):
            self.cult.name = ' '.join(data.get('cult_name', 'Script Kiddie Cult').split())  # Remove duplicate spaces
            self.cult.type = data['cult_type']
            self.cult.save()
            # Redirect the new user to the missions page
            self.send_json({
                'type': 'page_redirect',
                'page': 'messages'
            })
        else:
            self.user_error('Cult formatted incorrectly or already exists.')
            print(data)
        print(data)

    def disconnect(self, code):
        """
        Called when the WebSocket is closed.
        """
        if self.authorized:
            ats(self.channel_layer.group_discard)('wf1_chat_general', self.channel_name)
            self.authorized = False

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
            if data['contact'] == contact['id']:
                card = gamedata['contacts'][data['contact']]['cards'][contact['card']]
                if len(card['options']) > data['choice']:
                    if contact['id'] == 'anonymous':
                        if contact['card'] == '1.0.0' or contact['card'] == '1.0.1':
                            if data['choice'] == 0:
                                print('OPTION 0 SELECTED!')
                            elif data['choice'] == 1 and contact['card'] == '1.0.0':
                                print('OPTION 1 SELECTED!')
                                contacts[i]['card'] = '1.0.1'
                                cult.contacts = json.dumps(contacts)
                                cult.save()
                                self.page_data('contacts')  # Send client updated contacts page data

    @staticmethod
    def option_check(contact_name, mission_name, choice_index):
        """
        Checks whether an option should be enabled (mission completed) or disabled.
        """
        if contact_name == 'anonymous':
            if mission_name == '1.0.0':
                if choice_index == 0:
                    return False  # HQ is not implemented yet

    def user_error(self, error_message, severity='error'):
        """
        Displays an error in the console.
        """
        if severity == 'error':  # Something is wrong, this should not happen
            print('USER_ERROR: ' + error_message + ' [' + self.scope['user'].username + ']')
        elif severity == 'warning':  # Something incorrect happened
            print('USER_WARNING: ' + error_message + ' [' + self.scope['user'].username + ']')


class NotFoundConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        print('USER_ERROR: Unknown routing URL')
        self.close(code=404)
