from asciidk.types import Point
from asciidk.events.event_watcher import EventWatcher
from asciidk.obj.trap import Trap
from asciidk.util import is_direction
from asciidk.util import move_pos 

class Trapper(EventWatcher):

    def __init__(self, dungeon, parent_handler, pos=Point(0,0)):
        EventWatcher.__init__(self, parent_handler=parent_handler)
        self.name = 'Trapper'
        self.dungeon = dungeon
        self.pos = pos
        self.priority = -1
        self.dungeon.create_cursor(self.pos, 1, char='!')

    def handle(self, event):
        if is_direction(event):
            self.pos = move_pos(self.pos, event)
            self.dungeon.update_cursor(self.pos, 1)
            return True

        elif event == '\n':
            self.dungeon.add(Trap(self.pos))
            self.event_handler.deregister(self)
            self.dungeon.delete_cursor()
            self.dungeon.player.traps -= 1
            self.parent_handler.remove_child(self)
            return True

        return False
