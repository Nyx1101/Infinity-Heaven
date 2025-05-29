class AIBase:
    def __init__(self, entity, sprite):
        self.entity = entity
        self.sprite = sprite
        self.blackboard = {}

    def update(self):
        raise NotImplementedError("AIBase is abstract.")
