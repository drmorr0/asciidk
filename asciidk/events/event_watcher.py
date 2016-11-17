from abc import ABCMeta
from abc import abstractmethod

class EventWatcher:
    __metaclass__ = ABCMeta

    def __init__(self, parent_handler = None):
        self.event_handler = None
        self.parent_handler = parent_handler
        self.priority = 0

    @abstractmethod
    def handle(self):
        pass
