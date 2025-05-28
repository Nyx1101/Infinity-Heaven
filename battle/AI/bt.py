# ai/bt.py

class BTNode:
    def tick(self):
        pass

class BT:
    def __init__(self):
        self.root: BTNode = None
        self.running_node: BTNode = None

    def set_root(self, node: BTNode) -> None:
        self.root = node

    def tick(self) -> None:
        if self.root:
            self.root.tick()

    def update(self) -> None:
        self.tick()