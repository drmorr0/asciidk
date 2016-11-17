from abc import ABCMeta
from abc import abstractmethod

import time
import random

from asciimatics.screen import Screen

from asciidk.interface.message import MessageQueue
from asciidk.util import make_damage_properties
from asciidk.util import move_pos

class DungeonObject:
    __metaclass__ = ABCMeta

    DMG_AMOUNT = 0
    DMG_TYPE = []
    TEAM = None

    def __init__(self, pos, name, char, colour=Screen.COLOUR_WHITE, bg=Screen.COLOUR_BLACK):
        self.name = name
        self.pos = pos
        self.char = char
        self.colour = colour
        self.bg = bg

        self.solid = True
        self.dungeon = None

    def __str__(self):
        return self.char

    def attack(self, opponent):
        return opponent.defend(make_damage_properties(
            amount=self.DMG_AMOUNT, 
            types=self.DMG_TYPES,
            team=self.TEAM
        ))

    @abstractmethod
    def defend(self, damage_properties):
        pass


class Mob(DungeonObject):

    __metaclass__ = ABCMeta
    TAUNTS = None
    
    def __init__(self, *args, **kwargs):
        DungeonObject.__init__(self, *args, **kwargs)
        self.MAX_IDLE_TIME = 2.0
        self._reset_update_time()

    def _reset_update_time(self):
        self._time_to_next_update = time.time() + random.random() * self.MAX_IDLE_TIME

    def should_update(self):
        if self.health and self.health <= 0:
            return False
        if time.time() < self._time_to_next_update:
            return False

        if self.TAUNTS and random.random() < 0.01:
            MessageQueue.send_message(self.name + ": " + random.choice(self.TAUNTS))

        return True

    def move(self, direction):
        new_pos = move_pos(self.pos, direction)
        move_successful = self.dungeon.attempt_move(self, new_pos)
        self._reset_update_time()
        return move_successful

    @abstractmethod
    def update(self):
        pass

