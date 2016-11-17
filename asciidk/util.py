from copy import copy

from asciidk import constants
from asciidk.types import Point

def is_direction(d):
    return d in (constants.UP, constants.DOWN, constants.LEFT, constants.RIGHT)


def in_region(pos, bounds=None):
    bounds = bounds or (Point(), Point(constants.CHUNK_SIZE_X, constants.CHUNK_SIZE_Y))
    if pos.x < bounds[0].x or pos.x >= bounds[1].x or pos.y < bounds[0].y or pos.y >= bounds[1].y:
        return False
    return True


def manhattan_distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def make_damage_properties(amount=0, team=0, types=[constants.DAMAGE_NORMAL]):
    return {'amount': amount, 'team': team, 'types': types}


def move_pos(pos, direction):
    new_pos = copy(pos)
    if direction == constants.UP:
        new_pos.y -= 1
    elif direction == constants.DOWN:
        new_pos.y += 1
    elif direction == constants.LEFT:
        new_pos.x -= 1
    elif direction == constants.RIGHT:
        new_pos.x += 1

    return new_pos


def sign(value):
    return 1 if value > 0 else -1


def rotate_right(direction, steps=1):
    for i in range(steps):
        if direction == constants.UP:
            direction = constants.RIGHT
        elif direction == constants.RIGHT:
            direction = constants.DOWN
        elif direction == constants.DOWN:
            direction = constants.LEFT
        elif direction == constants.LEFT:
            direction = constants.UP
    return direction
