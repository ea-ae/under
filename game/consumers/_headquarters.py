from ._data import gamedata
import json


def headquarters_data(self):
    self.send_json({
        'type': 'page_data',
        'page': 'headquarters',
        'upgrades': json.loads(self.cult.headquarters)
    })


def process_upgrade(self, data):
    if data['command'] == 'buy':
        db_headquarters = json.loads(self.cult.headquarters)
        if data['item'] in gamedata['headquarters']['upgrades'] and data['item'] not in db_headquarters:
            # The wanted item is valid and we do not own it yet
            self.cult.money -= gamedata['headquarters']['upgrades'][data['item']]
            if self.cult.money < 0:
                self.user_error('Not enough money to buy HQ upgrade.')
                return False
            db_headquarters.append(data['item'])
            self.cult.headquarters = json.dumps(db_headquarters)
            self.cult.save(update_fields=['headquarters'])
        else:
            self.user_error('Incorrect HQ upgrade item.')
    elif data['command'] == 'delete':
        db_headquarters = json.loads(self.cult.headquarters)
        if data['item'] in db_headquarters:
            # The wanted item is valid and we do not own it yet
            db_headquarters.remove(data['item'])
            self.cult.headquarters = json.dumps(db_headquarters)
            self.cult.save(update_fields=['headquarters'])
    else:
        print(data['command'])
        self.user_error('Incorrect HQ ugprade command.')
