class Artefact:
    def __init__(self, artefact_id):
        self.id = artefact_id

    def apply(self, data):
        if self.id == 1:
            data["redeployment_time"] /= 2
        if self.id == 2:
            data["atk"] *= 1.3
        if self.id == 3:
            data["defense"] *= 1.3
        if self.id == 4:
            data["hp"] *= 1.3
        if self.id == 5:
            data["resistance"] += 30
        if self.id == 6:
            data["duration"] *= 1.5
        if self.id == 7:
            data["attack_speed"] /= 1.3
