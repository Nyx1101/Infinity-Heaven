# ai/fbb.py

from .fsm import FSM
from .bt import BT
from .blackboard import Blackboard
from battle.AI.ai_interface import IAI

class FBB(IAI):
    def __init__(self):
        self.fsm = FSM()
        self.bt = BT()
        self.blackboard = Blackboard()

    def update(self) -> None:
        self.fsm.update()
        self.bt.update()