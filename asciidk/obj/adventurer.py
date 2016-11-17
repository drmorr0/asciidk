import time
import random

from asciimatics.screen import Screen

from asciidk.obj.obj import Mob
from asciidk import constants
from asciidk.ai.pathing import compute_path_to_target
from asciidk.interface.message import MessageQueue
from asciidk.interface.reviews import Reviews
from asciidk.util import make_damage_properties

class Adventurer(Mob):
    DMG_TYPES = [constants.DAMAGE_NORMAL]
    DMG_AMOUNT = 20
    TEAM = 1

    def __init__(self, pos, name, char):
        Mob.__init__(self, pos, name, char)
        MessageQueue.send_message("{name} has checked in to your dungeon!".format(name=self.name))
        self.health = 40
        self.last_target_pos = None
        self.path = None

    def update(self):
        if not self.should_update():
            return
        if not self.last_target_pos or self.last_target_pos != self.dungeon.player.pos:
            self.last_target_pos = self.dungeon.player.pos
            self.path = compute_path_to_target(self.pos, self.last_target_pos, self.dungeon)
        
        if len(self.path) == 1:
            direction = self.path[0]
        else: 
            direction = self.path.pop(0)
        self.move(direction)

    def defend(self, damage_properties):
        if damage_properties['team'] == self.TEAM:
            return False

        self.health -= damage_properties['amount']
        if self.health < 0:
            MessageQueue.send_message("{name} has left you a review!".format(name=self.name))
            Reviews.leave_review(self.name, 1, random.choice(self.REVIEWS))
            self.dungeon.update_state(self, constants.STATE_DEAD)

            if self.spawner:
                self.spawner.reset()
        return True

    TAUNTS = [
        "I'm coming for you!",
        "God, I hate dungeons.",
        "I want my mommmmyyyyy!",
        "Die demon die!!!",
        "I'm not dead yet!",
    ]

    REVIEWS = [
        "This dungeon sucks!  I got killed right away!",
        "Too many demons.  Do not want.",
        "The architecture was OK, I guess, but the service was terrible.",
        "Run away!  Run away!",
        "I came here expecting greatness but all I found was death.",
        "I never should have taken this job from that creepy hooded stranger in the bar."
        "asdasdfasdfasdf.  *headdesk*",
        "Blue!  No!  YELLOOOOOOOOooooooooowwwww....",
        "No health potions to be found!  dungeon--",
    ]

