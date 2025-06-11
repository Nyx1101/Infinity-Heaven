class Screen:
    def __init__(self, manager, info=None):
        """
        Base screen class for all UI screens.

        :param manager: ScreenManager instance controlling screen transitions.
        :param info: Optional data passed when this screen is initialized.
        """
        self.manager = manager
        self.info = info

    def swift(self, id=None, data=None):
        """
        Switch to another screen by ID.

        :param id: Target screen ID.
        :param data: Optional data to pass to the next screen.
        """
        self.manager.switch_to(id, data)

    def handle_event(self, screen, event):
        """
        Handle input events such as mouse or keyboard.

        :param screen: Pygame surface.
        :param event: Pygame event object.
        """
        pass

    def update(self):
        """
        Update screen logic (e.g., animations, timers).
        """
        pass

    def draw(self, screen):
        """
        Render screen elements.

        :param screen: Pygame surface to draw onto.
        """
        pass

    def on_exit(self):
        """
        Optional cleanup when the screen is exited.
        """
        pass