


class Solver():

    def __init__(self, initData, *args, **kwargs):
        self.levelArray = [x[:] for x in initData["levelArray"]]
        self.prevState = []
        self.pPos = initData["pPos"][:]
        self.goals = [x[:] for x in initData["goals"]]
        self.width = initData["width"]
        self.height = initData["height"]

    def UpdateData(self, newData):
        self.prevState = [x[:] for x in newData["prevState"]]
        self.levelArray = [x[:] for x in newData["levelArray"]]
        self.pPos = newData["pPos"][:]

    def Decide(self):
        return "Left"