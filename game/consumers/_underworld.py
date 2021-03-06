from game.models import Underworld
from ._utils import weighted_choice

import random
from string import ascii_letters, digits
from math import cos, sin, floor, sqrt, pi, ceil
import json


def underworld_data(self):
    self.underworld, self.field = map_data(self.cult)

    self.send_json({
        'type': 'page_data',
        'page': 'underworld',
        'field': self.field  # sending the whole field only for debugging purposes
    })


def map_data(cult):
    """
    Returns a cult's Underworld model and map data (or create a new one).
    """
    try:  # Map already exists
        underworld_model = Underworld.objects.get(owner=cult)
        field = generate_map(underworld_model.seed)
    except Underworld.DoesNotExist:  # Generate new map
        # Create a new random seed every time we create an Underworld map
        seed = ''.join(random.choice(ascii_letters + digits) for _ in range(32))
        field = generate_map(seed)
        underworld_model = Underworld(owner=cult, seed=seed, x=field['x'], y=field['y'], time=0)
        underworld_model.save()

    print('### ########################### Seed used: ' + underworld_model.seed)
    
    return underworld_model, field


def navigate_map(self, direction):
    """
    Accepts client navigation requests (north/east/south/west) and returns data about new location.
    """
    # Navigate on the map and return data about the new location.
    if direction == 'north' and self.underworld.y < len(self.map) - 1:
        self.underworld.y += 1
    elif direction == 'east' and self.underworld.y < len(self.map[0]) - 1:
        self.underworld.x += 1
    elif direction == 'south' and self.underworld.y > 0:
        self.underworld.y -= 1
    elif direction == 'west' and self.underworld.x > 0:
        self.underworld.x -= 1
    else:
        self.log('Invalid direction provided.', 'warning')
        return False

    self.underworld.time += 1  # Increase time
    self.underworld.save()  # Save new location to db
    
    self.send_json({
        'type': 'underworld_data',
        'location': self.field[self.underworld.y][self.underworld.x]
    })


def generate_map(seed):
    """
    Generates a map of the Underworld based on a seed.
    """
    def set_biomes(field, points):
        for row in range(len(field)):
            # For every cell, we find the closest point
            for cell in range(len(field[row])):
                # Store the currently closest point:
                shortest_dist = -1
                # Stores the biome of the current point:
                current_biome = '_'

                # Iterate over the points to find the closest one
                for point in points:
                    # Calculate the euclidean distance
                    xdiff = point[0] - row
                    ydiff = point[1] - cell
                    distance = xdiff * xdiff + ydiff * ydiff  # Square root not needed since we're only comparing

                    # If this is currently the shortest distance, set it
                    if distance < shortest_dist or shortest_dist == -1:
                        shortest_dist = distance
                        # Set the biome that will be chosen if a shorter distance isn't found
                        current_biome = point[2]

                # Select a random field in the biome, taking rarity into account

                # Get names/data of all fields in the chosen biome
                biome_fields = biomes[current_biome]['fields'].items()
                # Extract field names and their rarities (weights)
                field_data = [(name, data['rarity']) for name, data in biome_fields]
                # Choose a random field using the weights
                field_index = weighted_choice([field_weight[1] for field_weight in field_data])
                # Set the cell's field
                field[row][cell] = field_data[field_index][0]

        return field

    def poisson_disc_samples(width, height, r, k=5):
        """
        "Two-dimensional Poisson Disc Sampling using Robert Bridson's algorithm."
        Modified version of https://github.com/emulbreh/bridson.
        """
        tau = 2 * pi
        cellsize = r / sqrt(2)

        grid_width = int(ceil(width / cellsize))
        grid_height = int(ceil(height / cellsize))
        grid = [None] * (grid_width * grid_height)

        def distance(a, b):
            dx = a[0] - b[0]
            dy = a[1] - b[1]
            return sqrt(dx * dx + dy * dy)

        def grid_coords(p2):
            return [int(floor(p2[0] / cellsize)), int(floor(p2[1] / cellsize))]

        def fits(p2, gx, gy):
            yrange = list(range(max(gy - 2, 0), min(gy + 3, grid_height)))

            for x in range(max(gx - 2, 0), min(gx + 3, grid_width)):
                for y in yrange:
                    g = grid[x + y * grid_width]
                    if g is None:
                        continue
                    if distance(p2, g) <= r:
                        return False
            return True

        p = [width * rnd.random(), height * rnd.random()]
        queue = [p]
        grid_x, grid_y = grid_coords(p)
        grid[grid_x + grid_y * grid_width] = p

        while queue:
            qi = int(rnd.random() * len(queue))
            qx, qy = queue[qi]
            queue[qi] = queue[-1]
            queue.pop()

            for _ in range(k):
                alpha = tau * rnd.random()
                d = r * sqrt(3 * rnd.random() + 1)
                px = qx + d * cos(alpha)
                py = qy + d * sin(alpha)

                if not (0 <= px < width and 0 <= py < height):
                    continue
                p = [px, py]
                grid_x, grid_y = grid_coords(p)

                if not fits(p, grid_x, grid_y):
                    continue
                queue.append(p)
                grid[grid_x + grid_y * grid_width] = p
        return [p for p in grid if p is not None]

    # Define map dimensions and settings
    # Size should be at least 35x35

    height = 50
    width = 50

    # Create a new instance of Random() using a given seed

    rnd = random.Random(seed)

    # Generate a random starting location somewhere in the middle of the map

    x = rnd.randint(width - 10, width + 10)
    y = rnd.randint(height - 10, height + 10)

    # Create a 2-dimensional list for the game map

    field = [['_'] * width for _ in range(height)]

    # Create random points that will be the starting positions of biomes

    points = poisson_disc_samples(width, height, 3, 5)
    rnd.shuffle(points)

    for i in range(len(points)):
        biome = rnd.choice(list(biomes.keys()))  # Set a random biome

        points[i][0] = int(round(points[i][0])) - 1  # x
        points[i][1] = int(round(points[i][1])) - 1  # y
        points[i].append(biome)

        field[points[i][1]][points[i][0]] = 'X'  # not needed?

    # Set the biomes

    field = set_biomes(field, points)

    return ({
        'field': field,
        'x': x,
        'y': y
    })


# These variables might be moved to an ignored _data.py file later on

# Biome data

biomes = {
    'The Obsidian Plains': {  # Biomes have different fields in them that will be randomly picked from
        'description': 'You are out in the open, and they know where you are.',
        'difficulty': 'easy',
        'fields': {
            'Empty Plains': {
                'description': 'There is nothing of interest here.',
                'rarity': 100,
                'hostility': 50,
                'shard_rate': 20,
                'loot_rate': 10
            },
            'Mineral Plains': {
                'description': 'You can see some shards growing around in this area.',
                'rarity': 40,
                'hostility': 50,
                'shard_rate': 50,
                'loot_rate': 10
            }
        }
    },
    'The Limbo': {
        'description': 'You do not know where you\'re going. Stay there for too long, and The Limbo will \
        take you over and you\'ll be left wandering around aimlessly for eternity just like the others.',
        'difficulty': 'easy',
        'fields': {
            'Walking Grounds': {
                'description': 'Victims of The Limbo are walking aimlessly all around this place. Do not bother them, and they will not bother you.',
                'rarity': 100,
                'hostility': 15,
                'shard_rate': 20,
                'loot_rate': 10
            },
            'Crowded Walking Grounds': {
                'description': 'Something is attracting victims of The Limbo to this place. You should be cautious around here.',
                'rarity': 30,
                'hostility': 40,
                'shard_rate': 10,
                'loot_rate': 15
            },
            'Empty Walking Grounds': {
                'description': 'There is almost nobody here.',
                'rarity': 10,
                'hostility': 5,
                'shard_rate': 20,
                'loot_rate': 10
            }
        }
    },
    'The Living Mountains': {
        'description': 'The mountains are alive. Stay cautious and watch your step.',
        'difficulty': 'easy',
        'fields': {
            'Sleeping Mountains': {
                'description': 'These mountains are probably asleep, it should be safe to pass.',
                'rarity': 100,
                'hostility': 10,
                'shard_rate': 40,
                'loot_rate': 10
            },
            'Moving Mountains': {
                'description': 'These mountains are awake, going near them is extremely dangerous.',
                'rarity': 75,
                'hostility': 90,
                'shard_rate': 40,
                'loot_rate': 10
            }
        }
    },
    'The Prison': {
        'description': 'Screams of captured souls can be heard from inside.',
        'difficulty': 'hard',
        'fields': {
            'Catacombs': {
                'description': 'A labyrinth of dark corridors. Going in without a latern would not be wise.',
                'rarity': 100,
                'hostility': 50,
                'shard_rate': 0,
                'loot_rate': 30
            },
            'Prison Block': {
                'description': 'Captured creatures are held and tortured in here. The place is full of guards.',
                'rarity': 100,
                'hostility': 75,
                'shard_rate': 0,
                'loot_rate': 30
            }
        }
    }
}
