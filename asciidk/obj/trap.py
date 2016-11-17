from asciimatics.screen import Screen

from asciidk.obj.obj import DungeonObject
from asciidk.constants import DAMAGE_NORMAL

class Trap(DungeonObject):
    DMG_AMOUNT = 30
    DMG_TYPES = [DAMAGE_NORMAL]
    TEAM = None

    def __init__(self, pos):
        DungeonObject.__init__(self, pos, "Trap {p}".format(p=str(pos)), "!", colour=Screen.COLOUR_RED)
        self.solid = False

    def attack(self, opponent):
        pass

    def defend(self, damage_properties):
        pass
