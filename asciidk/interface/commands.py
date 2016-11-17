from asciidk.interface.digger import Digger
from asciidk.interface.trapper import Trapper
from asciidk.interface.message import MessageQueue
from asciidk.interface.reviews import Reviews
from asciidk.events.event_watcher import EventWatcher

class CommandWatcher(EventWatcher):

    def __init__(self, dungeon):
        EventWatcher.__init__(self)

        self.running = True
        self.dungeon = dungeon
        self.name = 'CommandWatcher'
        self.current_tool = None

    def handle(self, event):
        if event == 'q':
            self.running = False
            return True
        elif event == 'r':
            Reviews.toggle()
            return True
        elif event == ' ':
            self.reset_tool()
            self.current_tool = Digger(self.dungeon, self, pos=self.dungeon.player.pos)
            self.event_handler.register(self.current_tool)
            return True
        elif event == 't':
            if self.dungeon.player.traps == 0:
                MessageQueue.send_message("You don't have any traps")
                return True

            self.reset_tool()
            self.current_tool = Trapper(self.dungeon, self, pos=self.dungeon.player.pos)
            self.event_handler.register(self.current_tool)
            return True

    def reset_tool(self):
        self.dungeon.delete_cursor()
        if self.current_tool:
            self.event_handler.deregister(self.current_tool)
            self.current_tool = None

    def remove_child(self, obj):
        if self.current_tool == obj:
            self.reset_tool()

