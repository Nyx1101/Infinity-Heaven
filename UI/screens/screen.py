class Screen:
    def __init__(self, manager):
        self.manager = manager

    def swift(self, id=None):
        self.manager.switch_to(id)

    def handle_event(self, screen, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

    def on_exit(self):
        pass
