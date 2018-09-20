import json


def inventory_data(self):
    """
    Returns a list of items in the player's inventory.
    """
    # Save this variable so that we can reuse it when getting item data
    self.inventory = json.loads(self.cult.inventory)

    self.send_json({
        'type': 'page_data',
        'page': 'inventory',
        'inventory': self.inventory
    })


def get_item(self, item_name):
    """
    Return data (type and description) about a requested item.
    """
    try:
        self.inventory
    except NameError:
        self.log('Inventory variable is missing; page data hasn\'t been asked for?', 'warning')
        return False

    if item_name is None or not isinstance(item_name, str):
        self.log('Requested item name is invalid.', 'warning')
    elif item_name.lower() in self.inventory:  # Make sure that the user even has the requested item
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
        'type': 'consumable',
        'desc': 'Paperwork is used to give a cultist a promotion. Promotions increase a cultist\'s wage by 50% and loyalty by 10.'
    },
    'contract': {
        'type': 'consumable',
        'desc': 'In order to get a mission from Vincent, you have to use up a contract.'
    },
    'keycap': {
        'type': 'collectible',
        'desc': 'These collectible keycaps are given out to players who report bugs and vulnerabilities in the game.'
    }
}
