import time
import random

from asciimatics.screen import Screen

from asciidk.obj.obj import Mob
from asciidk import constants
from asciidk.interface.message import MessageQueue
from asciidk.util import move_pos
from asciidk.util import make_damage_properties
from asciidk.util import manhattan_distance
from asciidk.util import sign

class Imp(Mob):
    DMG_TYPES = [constants.DAMAGE_DIGGING]
    DMG_AMOUNT = 1
    TEAM = 0

    def __init__(self, pos, name):
        Mob.__init__(self, pos, name, 'i', colour=Screen.COLOUR_RED)
        self.MAX_IDLE_TIME = 1
        self._reset_update_time()
        self.health = 10

    def update(self):
        if not self.should_update():
            return

        if self.dungeon.dig_locations:
            direction = self._move_to_dig_pos()
        else:
            direction = self._move_randomly()

        self.move(direction)

    def defend(self, damage_properties):
        if damage_properties['team'] == self.TEAM:
            MessageQueue.send_message("Ouch!", timeout=1, store_history=False)
            return False

        self.health -= damage_properties['amount']
        if self.health < 0:
            self.dungeon.update_state(self, constants.STATE_DEAD)
        return True

    def _move_to_dig_pos(self):
        closest_dig_dist = constants.CHUNK_SIZE_X + constants.CHUNK_SIZE_Y
        for dig_pos in self.dungeon.dig_locations:
            dist = manhattan_distance(self.pos, dig_pos)
            if dist < closest_dig_dist:
                closest_dig_dist = dist
                closest_dig_pos = dig_pos

        delta_x = self.pos.x - closest_dig_pos.x
        delta_y = self.pos.y - closest_dig_pos.y

        if delta_y == 0:
            direction = constants.RIGHT if sign(delta_x) < 0 else constants.LEFT
        else:
            direction = constants.DOWN if sign(delta_y) < 0 else constants.UP
        return direction

    def _move_randomly(self):
        return random.choice([constants.UP, constants.DOWN, constants.LEFT, constants.RIGHT])

    TAUNTS = [
        "Work, work!",
        "I liked Hell better.",
        "You're the king?  I didn't vote for ya.",
        "The Dark Lord is coming...",
        "Heeeehehehehehehehe"
    ]

