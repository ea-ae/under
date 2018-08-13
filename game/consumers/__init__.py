from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync as ats
import logging


class WarfareConsumer(JsonWebsocketConsumer):
    """
    Handles the WebSocket connections for 'Warfare' games.
    self.player - the player object
    self.cult - currently selected cult
    """

    from ._connection import connect, disconnect, multiple_connections, receive_json
    from ._page_data import page_data
    from ._home import home_data, create_cult
    from ._contacts import contacts_data, process_choice, option_check, set_card
    from ._headquarters import headquarters_data, process_upgrade

    logger = logging.getLogger('warfare')

    # General Methods

    def get_cult_object(self):
        # We do not need to retrieve the cult object from the database every time
        # If no changes have been made to it, just send the latest self.cult to it
        # If the save() method has been called on the model, it will retrieve a new one
        pass

    def log(self, message, severity='error'):
        """
        Displays an error in the console.
        """
        if severity == 'error':  # Something is wrong, this should not happen
            # print('USER_ERROR: ' + message + ' (by ' + self.scope['user'].username + ')')
            self.logger.error(message + ' (by ' + self.scope['user'].username + ')')
        elif severity == 'warning':  # Something incorrect happened
            # print('USER_WARNING: ' + message + ' (by ' + self.scope['user'].username + ')')
            self.logger.warning(message + ' (by ' + self.scope['user'].username + ')')
        elif severity == 'info':
            # print('USER_INFO: ' + message + ' (by ' + self.scope['user'].username + ')')
            self.logger.info(message + ' (by ' + self.scope['user'].username + ')')


class NotFoundConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        print('USER_ERROR: Unknown routing URL!')
        self.close(code=404)