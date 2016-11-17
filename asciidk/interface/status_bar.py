
from asciimatics.widgets import Frame
from asciimatics.widgets import Layout
from asciimatics.widgets import Label

from asciidk.constants import CHUNK_SIZE_X
from asciidk.constants import CHUNK_SIZE_Y
from asciidk.constants import FRAME_HEIGHT

class StatusBar:
    _status_bar = None
    _player_name_label = None
    _player_health_label = None
    _dungeon_rating_label = None

    @classmethod
    def initialize(cls, screen, name="Vlad the Impaler"):
        cls._status_bar = Frame(screen, FRAME_HEIGHT, CHUNK_SIZE_X, x=0, y=CHUNK_SIZE_Y+1)
        layout = Layout([1, 1, 1])
        cls._status_bar.add_layout(layout)

        cls._player_name_label = Label(name)
        cls._player_health_label = Label("Health: 100")
        cls._dungeon_rating_label = Label("Dungeon Rating: ?????")

        layout.add_widget(cls._player_name_label, 0)
        layout.add_widget(cls._player_health_label, 1)
        layout.add_widget(cls._dungeon_rating_label, 2)

        cls._status_bar.fix()

    @classmethod
    def update_health(cls, value):
        cls._player_health_label.value = "Health: {health}".format(health=value)

    @classmethod
    def update_rating(cls, num_stars):
        stars = ""
        for i in range(round(num_stars)):
            stars += "☆ "
        cls._dungeon_rating_label.value = "Dungeon Rating: " + stars

    @classmethod
    def get_frame(cls):
        return cls._status_bar
