class ScreenManager:
    def __init__(self, initial_screen):
        self.current_screen = initial_screen

    def change_screen(self, new_screen):
        self.current_screen = new_screen

    def get_screen(self):
        return self.current_screen