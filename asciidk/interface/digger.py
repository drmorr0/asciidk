from asciidk.types import Point
from asciidk.events.event_watcher import EventWatcher
from asciidk.util import is_direction
from asciidk.util import move_pos 

class Digger(EventWatcher):

    def __init__(self, dungeon, parent_handler, size=5, pos=Point(0,0)):
        EventWatcher.__init__(self, parent_handler=parent_handler)
        self.name = 'Digger'
        self.dungeon = dungeon
        self.size = size
        self.pos = pos
        self.priority = -1
        self.dungeon.create_cursor(self.pos, self.size, '#')

    def handle(self, event):
        if event.isdigit() and 0 < int(event) < 10:
            self.size = int(event)
            self.dungeon.update_cursor(self.pos, self.size)
            return True
        
        elif is_direction(event):
            self.pos = move_pos(self.pos, event)
            self.dungeon.update_cursor(self.pos, self.size)
            return True

        elif event == '\n':
            self.dungeon.mark_for_digging(self.pos, self.size)
            self.event_handler.deregister(self)
            self.parent_handler.remove_child(self)
            return True

        return False
