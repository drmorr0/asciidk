import time
import random

from asciimatics.screen import Screen
from asciimatics.scene import Scene

from asciidk import constants
from asciidk.obj.player import Player 
from asciidk.obj.imp import Imp
from asciidk.dungeon.dungeon import Dungeon
from asciidk.events.event_handler import EventHandler
from asciidk.interface.commands import CommandWatcher
from asciidk.interface.message import MessageQueue
from asciidk.interface.reviews import Reviews
from asciidk.interface.status_bar import StatusBar
from asciidk.types import Point


def run(screen):
    seed = time.time()
    random.seed(seed)

    dungeon = Dungeon()
    event_handler = EventHandler(screen)
    command_watcher = CommandWatcher(dungeon)

    StatusBar.initialize(screen)
    scene = Scene([StatusBar.get_frame()])
    screen.set_scenes([scene])
    MessageQueue.initialize(screen, scene, dungeon)
    Reviews.initialize(screen, scene, dungeon)

    pc = Player(dungeon.spawn_point)
    imp = Imp(dungeon.spawn_point - Point(1,1), 'Imp1')

    event_handler.register(command_watcher)
    event_handler.register(pc)

    dungeon.add(pc, type='player')
    dungeon.add(imp, type='mob')

    dungeon.render(screen, force_redraw=True)
    screen.draw_next_frame()

    while command_watcher.running:
        dungeon.update()
        dungeon.render(screen)
        event_handler.propogate()
        MessageQueue.update()
        screen.draw_next_frame()


if __name__ == '__main__':
    Screen.wrapper(run)
