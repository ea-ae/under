from ._data import gamedata
import json


def page_data(self, page):
    """
    Sends data about the requested page back to the client.
    """
    if page == 'home':
        self.home_data()
    elif page == 'contacts':
        self.contacts_data()
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
    elif page == 'research':
        self.send_json({
            'type': 'page_data',
            'page': page
        })
    elif page == 'societies':
        self.send_json({
            'type': 'page_data',
            'page': page
        })
    elif page == 'headquarters':
        self.headquarters_data()
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
