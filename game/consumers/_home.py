from game.models import Cult
import re


def home_data(self):
    if self.cult.type == 'none':  # Cult is not created yet
        self.send_json({
            'type': 'page_data',
            'page': 'home'
        })
    else:
        self.send_json({
            'type': 'page_data',
            'page': 'home',
            'username': self.scope['user'].profile.display,
            'cult': {
                'name': self.cult.name,
                'type': self.cult.type,
                'money': self.cult.money,
                'rep': self.cult.reputation
            }
        })


def create_cult(self, data):
    """
    Creates a new cult in the Home tab.
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
