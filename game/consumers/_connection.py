from game.models import WarfareGame, WarfarePlayer, Cult
from asgiref.sync import async_to_sync as ats


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


def disconnect(self, code):
    """
    Called when the WebSocket is closed.
    """
    if self.authorized:
        ats(self.channel_layer.group_discard)('wf1_chat_general', self.channel_name)
        self.authorized = False


def receive_json(self, content, **kwargs):
    """
    Called when the customer sends data to us.
    """
    print('receive_json(): ' + str(content))
    request_type = content.get('type')
    if request_type == 'page_data':  # Client requests data to load a tab
        self.page_data(content.get('page'))  # Send the requested page over to page_data()
    elif request_type == 'card_choice':  # User clicked on an option in a card
        self.process_choice({'contact': content.get('contact'),
                             'choice': content.get('choice')})
    elif request_type == 'create_cult':
        self.create_cult(content.get('cult_data'))
    else:
        self.user_error('Unknown message type received.')
