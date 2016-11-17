
from asciimatics.screen import Screen

from asciidk.util import in_region
from asciidk.types import Point

class Cursor:
    def __init__(self, pos, size, char='#', colour=Screen.COLOUR_GREEN):
        self.pos = pos
        self.size = size
        self.colour = colour
        self.char = char

    def contains(self, pos):
        return in_region(pos, (self.pos, self.pos + Point(self.size, self.size)))

    def update(self, pos, size):
        old_region = self.get_region()
        self.pos = pos
        self.size = size
        new_region = self.get_region()
        return list(set(old_region).symmetric_difference(set(new_region)))

    def get_region(self):
        return [Point(x, y) for x in range(self.pos.x, self.pos.x + self.size) \
                    for y in range(self.pos.y, self.pos.y + self.size)]

    def __str__(self):
        return self.char

