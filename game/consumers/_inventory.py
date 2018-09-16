import json


def inventory_data(self):
    """
    Returns a list of items in the player's inventory.
    """
    inventory = json.loads(self.cult.inventory)

    # Add item types and descriptions to the data sent
    for item_name in inventory:
        inventory[item_name].update(item_data[item_name])

    self.send_json({
        'type': 'page_data',
        'page': 'inventory',
        'inventory': inventory
    })


def alter_item(self, item_name, item_amount):
    """
    Add or remove some amount of an item from a player's inventory.
    Put a negative number in 'item_amount' to remove items.
    """
    inventory = json.loads(self.cult.inventory)
    if item_name not in inventory:  # Item is not owned yet
        inventory[item_name] = {'amount': 0}
        # inventory[item_name].update(item_data[item_name])

    if inventory[item_name]['amount'] + item_amount < 0:
        return False
    elif inventory[item_name]['amount'] + item_amount == 0:
        del inventory[item_name]  # Having zero of an item means we don't need it in our inventory anymore
    else:
        inventory[item_name]['amount'] += item_amount

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
