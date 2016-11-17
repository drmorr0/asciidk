class EventHandler:
    def __init__(self, screen):
        self.screen = screen
        self.watchers = {}
        self.is_propogating = False
        self.waiting_to_register = []
        self.waiting_to_deregister = []

    def register(self, obj):
        if not self.is_propogating:
            self._register(obj)
        else:
            self.waiting_to_register.append(obj)

    def deregister(self, obj):
        if not self.is_propogating:
            self._deregister(obj)
        else:
            self.waiting_to_deregister.append(obj)

    def propogate(self):
        event = self.screen.get_event()
        if not event:
            return

        event = chr(event.key_code)
        self.is_propogating = True
        for __, watcher in sorted(self.watchers.items(), key=lambda w: w[1].priority):
            if watcher.handle(event):
                break
        self.is_propogating = False

        for obj in self.waiting_to_register:
            self._register(obj)
        for obj in self.waiting_to_deregister:
            self._deregister(obj)
        self.waiting_to_register = []
        self.waiting_to_deregister = []

    def _toggle_mode(self):
        self.mode = 'movement' if self.mode == 'commands' else 'commands'

    def _register(self, obj):
        obj.event_handler = self
        self.watchers[obj.name] = obj

    def _deregister(self, obj):
        obj.event_handler = None
        if obj.name in self.watchers:
            del self.watchers[obj.name]
