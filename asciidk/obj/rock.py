from asciidk.obj.obj import DungeonObject
from asciidk.constants import ROCK
from asciidk.constants import DAMAGE_DIGGING
from asciidk.constants import STATE_DESTROYED

class Rock(DungeonObject):
    def __init__(self, pos, dungeon):
        DungeonObject.__init__(self, pos, "Rock ({x}, {y})".format(x=pos.x, y=pos.y), ROCK)
        self.dungeon = dungeon

    def attack(self, opponent):
        pass

    def defend(self, damage_properties):
        if DAMAGE_DIGGING not in damage_properties['types']:
            return

        self.dungeon.update_state(self, STATE_DESTROYED)
