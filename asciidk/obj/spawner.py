import time
import random

from asciimatics.screen import Screen

from asciidk.obj.adventurer import Adventurer
from asciidk.obj.obj import DungeonObject

class Spawner(DungeonObject):
    def __init__(self, pos, name, spawn_rate=100, spawn_rate_variance=20):
        DungeonObject.__init__(self, pos, name, '+', colour=Screen.COLOUR_MAGENTA)

        self.spawn_rate = spawn_rate
        self.spawn_rate_variance = spawn_rate_variance
        self.reset()

    def _update_next_spawn_time(self):
        self.next_spawn_time = time.time() + random.randint(
            self.spawn_rate - self.spawn_rate_variance,
            self.spawn_rate + self.spawn_rate_variance,
        )

    def spawn(self):
        if self.mob:
            return None

        if self.next_spawn_time and time.time() > self.next_spawn_time:
            self.mob = Adventurer(self.pos, random.choice(self.NAMES), 'H')
            self.mob.spawner = self
            return self.mob

        return None

    def reset(self):
        self.mob = None
        self._update_next_spawn_time()
        
    def attack(self, opponent):
        pass

    def defend(self, dungeon_properties):
        pass

    NAMES = [
        "Sir George the Valiant",
        "Knight Light",
        "Lady Athena the Bold",
        "Bob",
        "xXx_d3M0n_k1lla_xXx",
        "Tim the Enchanter",
        "Peasant-with-a-Pitchfork",
        "Rebecca the Witch",
        "Vlad the Impaler's Twin Brother",
        "Ron F***ing Swanson",
        "Strong Bad",
        "Strong Sad",
        "Sir Lance Alot",
    ]
