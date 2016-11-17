import time

from asciimatics.screen import Screen
from asciimatics.widgets import Frame
from asciimatics.widgets import Layout
from asciimatics.widgets import Label

from asciidk.constants import CHUNK_SIZE_X
from asciidk.constants import CHUNK_SIZE_Y
from asciidk.constants import FRAME_HEIGHT

class MessageQueue:
    _current_message = None
    _messages = []
    _dungeon = None
    _screen = None
    _scene = None

    @classmethod
    def initialize(cls, screen, scene, dungeon):
        cls._screen = screen
        cls._scene = scene
        cls._dungeon = dungeon

    @classmethod
    def send_message(cls, msg, timeout=2, store_history=True):
        message_frame = Frame(cls._screen, FRAME_HEIGHT, CHUNK_SIZE_X - 20, x=2, y=2)
        message_frame.palette['background'] = (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)
        message_frame.palette['label'] = (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)
        message_frame.palette['borders'] = (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK)
        layout = Layout([1])
        message_frame.add_layout(layout)
        layout.add_widget(Label(msg))
        message_frame.fix()

        cls._messages.append({'frame': message_frame, 'timeout': timeout})

    @classmethod
    def update(cls):
        if cls._current_message:
            if cls._current_message['timeout'] > 0 and time.time() > cls._current_message['timeout']:
                cls._scene.remove_effect(cls._current_message['frame'])
                cls._current_message = None
                cls._dungeon.render(cls._screen, force_redraw=True)

        elif cls._messages:
            cls._current_message = cls._messages.pop(0)
            cls._scene.add_effect(cls._current_message['frame'])
            cls._current_message['frame'].update(0)
            if cls._current_message['timeout'] > 0:
                cls._current_message['timeout'] = time.time() + cls._current_message['timeout']


