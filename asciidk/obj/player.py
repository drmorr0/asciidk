from copy import copy
import time

from asciimatics.screen import Screen

from asciidk.obj.obj import DungeonObject
from asciidk import constants
from asciidk.events.event_watcher import EventWatcher
from asciidk.interface.message import MessageQueue
from asciidk.interface.status_bar import StatusBar
from asciidk.util import is_direction
from asciidk.util import make_damage_properties
from asciidk.util import move_pos

class Player(DungeonObject, EventWatcher):
    ATTACK_COOLDOWN = 0.5
    TEAM = 0
    DMG_AMOUNT = 10
    DMG_TYPES = [constants.DAMAGE_NORMAL]

    def __init__(self, pos):
        DungeonObject.__init__(self, pos, 'Player', 'D', colour=Screen.COLOUR_BLACK, bg=Screen.COLOUR_RED)
        EventWatcher.__init__(self)

        self.priority = 10
        self.health = 100
        self.last_attack_time = None
        self.traps = 50

    def attack(self, opponent):
        if self.last_attack_time and time.time() < self.last_attack_time + self.ATTACK_COOLDOWN:
            return

        opponent.defend(make_damage_properties(amount=self.DMG_AMOUNT, types=self.DMG_TYPES, team=self.TEAM))
        self.last_attack_time = time.time()

    def defend(self, damage_properties):
        if damage_properties['team'] == self.TEAM:
            return False

        self.health -= damage_properties['amount']
        StatusBar.update_health(self.health)
        if self.health <= 0:
            MessageQueue.send_message("You have died.", timeout=-1)
            self.dungeon.update_state(self, constants.STATE_DEAD)
        return True

    def handle(self, event):
        if self.health <= 0:
            return False

        if not is_direction(event):
            return False

        new_pos = move_pos(self.pos, event)
        self.dungeon.attempt_move(self, new_pos)
        return True
