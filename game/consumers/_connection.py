from game.models import WarfareGame, WarfarePlayer, Cult
from asgiref.sync import async_to_sync as ats
from channels.exceptions import StopConsumer
import json


def connect(self):
    """
    Handles incoming connections.
    """
    self.authorized = False
    self.user = self.scope['user']
    if self.user.is_authenticated:  # Check if user is logged in
        try:
            self.player = WarfarePlayer.objects.get(user=self.scope['user'])
        except WarfarePlayer.DoesNotExist:  # New user
            self.player = WarfarePlayer(user=self.user,
                                        game=WarfareGame.objects.get(name='alpha'))
            self.player.save()
            self.cult = Cult(owner=self.player)  # Create a new cult for the new player
            self.cult.save()
        else:  # Returning user
            try:
                self.cult = Cult.objects.get(owner=self.player)
            except Cult.DoesNotExist:
                self.log('Cult does not exist.')
                self.close()
                return False
        # Allow only one connection per user
        ats(self.channel_layer.group_send)('user-' + self.user.username, {
            'type': 'multiple_connections'
        })
        ats(self.channel_layer.group_add)('user-' + self.user.username, self.channel_name)
        ats(self.channel_layer.group_add)('warfare-1', self.channel_name)

        self.authorized = True

        db_contacts = json.loads(self.cult.contacts)
        ac = db_contacts[0]['card']  # Card of anonymous
        # Protect tutorial users from doing stupid things
        self.tutorial = ac in ('1.0.0', '1.0.1', '1.1.0', '1.1.1', '1.2.0', '1.3.0', '1.4.0')

        self.accept()
    else:
        self.log('User is unauthenticated.')
        self.close()


def disconnect(self, code):
    """
    Called when the websocket is closed.
    """
    if self.authorized:
        ats(self.channel_layer.group_discard)('warfare-1', self.channel_name)
        self.authorized = False
    self.close()  # Do I need this?
    raise StopConsumer


def multiple_connections(self, message):
    """
    Called when a new websocket connection is opened by the same user.
    The previous one has to be closed.
    """
    self.send_json({
        'type': 'multiple_connections'
    })
    self.close()


def receive_json(self, content, **kwargs):
    """
    Called when the customer sends data to us.
    """
    self.log('receive_json(): ' + str(content), 'debug')
    request_type = content.get('type')
    if request_type == 'page_data':  # Client requests data to load a tab
        self.page_data(content.get('page'))  # Send the requested page over to page_data()
    elif request_type == 'item_data':  # Requested data about an item
        self.get_item(content.get('item_name'))
    elif request_type == 'card_choice':  # User clicked on an option in a card
        self.process_choice({'contact': content.get('contact'),
                             'choice': content.get('choice')})
    elif request_type == 'manage_member':
        self.manage_member(content)
    elif request_type == 'recruit':
        self.process_recruit(content.get('choice'))
    elif request_type == 'hq_upgrade':
        self.process_upgrade({'command': content.get('command'),
                              'item': content.get('item')})
    elif request_type == 'create_cult':
        self.create_cult(content.get('cult_data'))
    else:
        self.log('Unknown message type received.')
