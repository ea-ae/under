import json


def inventory_data(self):
    """
    Returns a list of items in the player's inventory.
    """

    self.send_json({
        'type': 'page_data',
        'page': 'inventory',
        'inventory': json.loads(self.cult.inventory)
    })


def get_item(self, item_name):
    """
    Return data (type and description) about a requested item.
    """
    inventory = json.loads(self.cult.inventory)

    if item_name is None or not isinstance(item_name, str):
        self.log('Requested item name is invalid.', 'warning')
    elif item_name.lower() in inventory:  # Make sure that the user even has the requested item
        data = {
            'name': item_name.lower()
        }
        data.update(item_data[item_name.lower()])

        self.send_json({
            'type': 'item_data',
            'item_data': data
        })
    else:
        self.log('User requested data about item he does not own.', 'warning')


def alter_item(self, item_name, item_amount):
    """
    Add or remove some amount of an item from a player's inventory.
    Put a negative number in 'item_amount' to remove items.
    """
    inventory = json.loads(self.cult.inventory)

    if item_name is None or not isinstance(item_name, str):
        self.log('To-be-altered item name is null or invalid.', 'warning')
        return False

    item_name = item_name.lower()

    if item_name not in inventory:  # Item is not owned yet
        inventory[item_name] = 0

    new_amount = inventory[item_name] + item_amount

    if new_amount < 0:
        return False
    elif new_amount == 0:
        del inventory[item_name]  # Having zero of an item means we don't need it in our inventory anymore
    else:
        inventory[item_name] = new_amount

    self.cult.inventory = json.dumps(inventory)
    self.cult.save(update_fields=['inventory'])

    return True


# Once we have items in the game that we don't want to be publicly visible, we will move this to _data.py

item_data = {
    'paperwork': {
        'type': 'resource',
        'desc': 'Paperwork is used to give a cultist a promotion. Promotions increase a cultist\'s wage by 50% and loyalty by 10.'
    },
    'contract': {
        'type': 'resource',
        'desc': 'In order to get a mission from Vincent, you have to use up a contract. You earn contracts every day.'
    },
    'keycap': {
        'type': 'collectible',
        'desc': 'These collectible keycaps are given out to players who report bugs and vulnerabilities in the game.'
    },
    'black shard': {
        'type': 'resource',
        'desc': 'Black shards are mysterious crystals found only in the Underworld and are extremely important in alchemy.'
    },
    'red shard': {
        'type': 'resource',
        'desc': 'If you direct enough energy into black shards, then they will transform into red shards that are mainly used for upgrading hellgates.'
    },
    'crystal powder': {
        'type': 'resource',
        'desc': 'Crystal powder is used to transform black shards into other forms. The more shards you are transforming, the more powder you must use.'
    },
    'power cell': {
        'type': 'resource',
        'desc': 'A power cell is spent every single time that a transformation or cleansing machine is activated.'
    }
}
