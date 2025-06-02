class Artefact:
    def __init__(self, artefact_id):
        self.id = artefact_id

    def apply(self, data):
        if self.id == 1:
            data["cd"] /= 10
