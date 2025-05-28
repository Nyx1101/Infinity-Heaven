from battle.AI.ai_interface import IAI

class DecisionTree(IAI):
    def decide(self) -> None:
        print("DecisionTree: deciding...")

    def update(self) -> None:
        self.decide()