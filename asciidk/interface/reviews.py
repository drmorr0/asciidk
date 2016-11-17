import time

from asciimatics.screen import Screen
from asciimatics.widgets import Divider
from asciimatics.widgets import Frame
from asciimatics.widgets import Layout
from asciimatics.widgets import Label

from asciidk.interface.status_bar import StatusBar
from asciidk.constants import CHUNK_SIZE_X
from asciidk.constants import CHUNK_SIZE_Y
from asciidk.constants import FRAME_HEIGHT

class Reviews:
    _review_frame = None
    _reviews= []
    _dungeon = None
    _screen = None
    _scene = None
    _visible = False

    @classmethod
    def initialize(cls, screen, scene, dungeon):
        cls._screen = screen
        cls._scene = scene
        cls._dungeon = dungeon
        cls._review_frame = Frame(cls._screen, CHUNK_SIZE_Y - 20, CHUNK_SIZE_X - 20, x=5, y=5)
        cls._review_frame.palette['background'] = (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)
        cls._review_frame.palette['label'] = (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)
        cls._review_frame.palette['borders'] = (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK)

    @classmethod
    def leave_review(cls, name, stars, msg):
        layout = Layout([1])
        cls._review_frame.add_layout(layout)
        name_star = name + '       '
        for i in range(stars):
            name_star += "☆ "
        layout.add_widget(Label(name_star))
        layout.add_widget(Label(msg))
        layout.add_widget(Divider())
        cls._review_frame.fix()

        cls._reviews.append(stars)
        StatusBar.update_rating(sum(cls._reviews) / len(cls._reviews))

    @classmethod
    def toggle(cls):
        if cls._visible:
            cls._scene.remove_effect(cls._review_frame)
            cls._dungeon.render(cls._screen, force_redraw=True)
        else:
            cls._review_frame.update(0)
            cls._scene.add_effect(cls._review_frame)
        cls._visible = not cls._visible
