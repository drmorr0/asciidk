from copy import copy
import time
import random
import sys

from asciimatics.screen import Screen

from asciidk import constants
from asciidk.interface.cursor import Cursor
from asciidk.obj.obj import Mob
from asciidk.obj.corpse import Corpse
from asciidk.obj.rock import Rock 
from asciidk.obj.spawner import Spawner
from asciidk.obj.player import Player
from asciidk.obj.trap import Trap
from asciidk.types import Grid
from asciidk.types import Point
from asciidk.util import in_region
from asciidk.util import make_damage_properties

class Dungeon:

    def __init__(self, save_file=None):
        self.chunk = Grid(
            width=constants.CHUNK_SIZE_X,
            height=constants.CHUNK_SIZE_Y, 
            dungeon=self,
        )
        self.spawn_point = Point()
        self.cursor = None
        self.player = None
        self.mobs = []
        self.spawners = []
        self.update_positions = []
        self.dig_locations = []

        if not save_file:
            self._generate_starting_area()
        else:
            self._load_save()

    def _generate_starting_area(self, bounds=None):
        bounds = bounds or ((0, constants.CHUNK_SIZE_X - 10), (0, constants.CHUNK_SIZE_Y - 10))
        first_room_pos = (random.randint(*bounds[0]), random.randint(*bounds[1]))
        for x in range(first_room_pos[0], first_room_pos[0] + 5):
            for y in range(first_room_pos[1], first_room_pos[1] + 5):
                self.chunk.set_stack(Point(x, y), [])

        self.spawn_point = Point(first_room_pos[0] + 2, first_room_pos[1] + 2)
        self.spawners = [Spawner(self.spawn_point + Point(0,3), "Adventurer Spawner", 100, 0)]
        for spawner in self.spawners:
            self.chunk.set_stack(spawner.pos, [spawner])

    def is_passable(self, point):
        for obj in self.chunk.stack(point):
            if obj.solid:
                return False
        return True

    def has_mob_or_player(self, point):
        for obj in self.chunk.stack(point):
            if isinstance(obj, Mob) or isinstance(obj, Player):
                return True
        return False

    def render(self, screen, offset=None, force_redraw=False):
        if force_redraw:
            self.update_positions = [Point(x, y) for x in range(constants.CHUNK_SIZE_X) 
                for y in range(constants.CHUNK_SIZE_Y)]

        for pos in self.update_positions:
            if self.cursor and self.cursor.contains(pos):
                screen.print_at(str(self.cursor), pos.x, pos.y, colour=self.cursor.colour)
            else:
                top = self.chunk.top_obj(pos)
                if top:
                    if top.char == constants.ROCK and pos in self.dig_locations:
                        colour = Screen.COLOUR_YELLOW
                    else:
                        colour = top.colour
                    screen.print_at(str(top), pos.x, pos.y, colour=colour, bg=top.bg)
                else:
                    screen.print_at(' ', pos.x, pos.y)

        self.update_positions = []

    def update(self):
        for mob in self.mobs:
            mob.update()

        for spawner in self.spawners:
            spawned_mob = spawner.spawn()
            if spawned_mob:
                self.add(spawned_mob, type='mob')

    def add(self, obj, type=''):
        obj.dungeon = self
        self.chunk.add_obj(obj)
        self.update_positions.append(obj.pos)
        if type == 'player':
            self.player = obj
        elif type == 'mob':
            self.mobs.append(obj)

    def remove(self, obj):
        self.chunk.rem_obj(obj)
        self.update_positions.append(obj.pos)
        if isinstance(obj, Rock) and obj.pos in self.dig_locations:
            self.dig_locations.remove(obj.pos)

    def attempt_move(self, obj, new_pos):
        if not in_region(new_pos):
            return False

        top = self.chunk.top_obj(new_pos)
        if not self.is_passable(new_pos):
            return obj.attack(top)

        old_pos = copy(obj.pos)
        self.chunk.rem_obj(obj)
        obj.pos = new_pos
        self.chunk.add_obj(obj)

        if isinstance(top, Trap):
            obj.defend(make_damage_properties(amount=top.DMG_AMOUNT, types=top.DMG_TYPES, team=top.TEAM))
            self.remove(top)

        self.update_positions.extend([old_pos, new_pos])
        return True

    def update_state(self, obj, state):
        if state == constants.STATE_DESTROYED:
            self.remove(obj)

        elif state == constants.STATE_DEAD:
            self.remove(obj)
            self.add(Corpse(obj.pos, obj.name))
            if obj in self.mobs:
                self.mobs.remove(obj)

        self.update_positions.append(obj.pos)

    def create_cursor(self, pos, size, char, colour=Screen.COLOUR_GREEN):
        self.cursor = Cursor(pos, size, char)
        self.update_positions.extend(self.cursor.get_region())
    
    def update_cursor(self, pos, size):
        changed_spaces = self.cursor.update(pos, size)
        self.update_positions.extend(changed_spaces)

    def delete_cursor(self):
        if self.cursor:
            marked = self.cursor.get_region()
            self.update_positions.extend(marked)
            self.cursor = None

    def mark_for_digging(self, pos, size):
        marked = self.cursor.get_region()
        for pos in marked:
            if self.chunk.top_obj(pos).char == constants.ROCK:
                self.dig_locations.append(pos)
        self.update_positions.extend(marked)
        self.cursor = None
