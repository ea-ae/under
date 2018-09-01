from ._data import gamedata
import json


def headquarters_data(self):
    self.send_json({
        'type': 'page_data',
        'page': 'headquarters',
        'upgrades': json.loads(self.cult.headquarters)
    })


def process_upgrade(self, data):
    """
    Called when the client wants to buy or sell an HQ upgrade.
    """
    if data['command'] == 'buy':
        db_headquarters = json.loads(self.cult.headquarters)
        if data['item'] in gamedata['headquarters']['upgrades'] and data['item'] not in db_headquarters:
            self.cult.refresh_from_db(fields=['money'])  # Just in case something else modified the money field
            self.cult.money -= gamedata['headquarters']['upgrades'][data['item']]
            if self.cult.money < 0:
                self.log('Not enough money to buy HQ upgrade.')
                return False
            db_headquarters.append(data['item'])
            self.cult.headquarters = json.dumps(db_headquarters)
            self.cult.save(update_fields=['headquarters', 'money'])
            self.log('Bought HQ upgrade ' + data['item'] + '.', 'info')
        else:
            self.log('Incorrect HQ upgrade item.')
    elif data['command'] == 'delete':
        if self.tutorial:
            self.log('HQ upgrade deletion tutorial-idiot protection.', 'info')
            self.send_json({
                'type': 'tutorial_lock'
            })
            return False

        db_headquarters = json.loads(self.cult.headquarters)
        if data['item'] in db_headquarters:
            # The wanted item is valid and we do not own it yet
            db_headquarters.remove(data['item'])
            self.cult.headquarters = json.dumps(db_headquarters)
            self.cult.save(update_fields=['headquarters'])
            self.log('Deleted HQ upgrade ' + data['item'] + '.', 'info')
    else:
        print(data['command'])
        self.log('Incorrect HQ ugprade command.')
