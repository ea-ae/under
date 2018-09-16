from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer
import logging


class WarfareConsumer(JsonWebsocketConsumer):
    """
    Handles the WebSocket connections for 'Warfare' games.
    self.user - user model
    self.player - warfare player model
    self.cult - currently selected cult
    """

    from ._connection import (connect,
                              disconnect,
                              multiple_connections,
                              receive_json)
    from ._page_data import page_data
    from ._home import (home_data,
                        create_cult)
    from ._contacts import (contacts_data,
                            process_choice,
                            option_check,
                            set_card)
    from ._members import (members_data,
                           generate_member,
                           manage_member,
                           process_ticks,
                           process_recruit,
                           change_job,
                           promote_member,
                           kick_member)
    from ._headquarters import (headquarters_data,
                                process_upgrade)

    logger = logging.getLogger('warfare')

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
