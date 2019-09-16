from modules import resources
from PIL import Image

##load images for elements of the puzzle####
floor = resources.floorImage
wall = resources.wallImage
goal = resources.goalImage
bFloor = resources.boxFloorImage
bGoal = resources.boxGoalImage
pFloor = resources.playerFloorImage
pGoal = resources.playerGoalImage

class Board():

    def __init__(self, levelData, *args, **kwargs):
        self.levelArray = []
        self.prevState = []
        self.pPos = [levelData["player"][0],levelData["player"][1]]
        self.goals = [x[:] for x in levelData["goals"]]
        self.width = levelData["size"][0]
        self.height = levelData["size"][1]
        self.drawnLevel = Image.new('RGB', (self.width*64, self.height*64))

        ######load into array here#############
        ##0 is wall, 1 is floor, 2 is box, 3 is goal, 4 is player, 5 is box/goal, 6 is player/goal
        #levelArray = [[0] * levelData["size"][1]] * levelData["size"][0]
        self.levelArray = [[0 for i in range(levelData["size"][1])] for j in range(levelData["size"][0])]
        for i in levelData["goals"]:
            self.levelArray[i[0]][i[1]] = 3
        for i in levelData["floor"]:
            if self.levelArray[i[0]][i[1]] == 0:
                self.levelArray[i[0]][i[1]] = 1
        for i in levelData["boxes"]:
            if self.levelArray[i[0]][i[1]] == 3:
                self.levelArray[i[0]][i[1]] = 5
            else:
                self.levelArray[i[0]][i[1]] = 2
        if self.levelArray[levelData["player"][0]][levelData["player"][1]] == 3:
            self.levelArray[levelData["player"][0]][levelData["player"][1]] = 6
        else:
            self.levelArray[levelData["player"][0]][levelData["player"][1]] = 4

        self.prevState = [x[:] for x in self.levelArray]

        ######Generate Initial Board#######
        #def draw_switch(id):
        #    switcher = {0: wall, 1: floor, 2: bFloor, 3: goal, 4: pFloor, 5: bGoal, 6: pGoal}
        #    return switcher.get(id)
        for i in range(self.width):
            for j in range(self.height):
                self.drawnLevel.paste(self.Draw_Switch(self.levelArray[i][j]),(i*64,j*64))

    #converts levelArray data into correct image
    def Draw_Switch(self, id):
        switcher = {0: wall, 1: floor, 2: bFloor, 3: goal, 4: pFloor, 5: bGoal, 6: pGoal}
        return switcher.get(id)

    #converts directional input into relevant values
    def Direction_Switch(self, id):
        switcher = {"Up": [0,0,1,-1],"Down": [0,0,1,1],"Left": [1,-1,0,0],"Right": [1,1,0,0]}
        return switcher.get(id)

    #updates image based on which positions changed
    def DetectDifference(self):
        for i in range(len(self.levelArray)):
            for j in range(len(self.levelArray)):
                if not (self.levelArray[i][j] == self.prevState[i][j]):
                        self.drawnLevel.paste(self.Draw_Switch(self.levelArray[i][j]),(i*64,j*64))
        self.prevState = [x[:] for x in self.levelArray]
        self.CheckSolve()

    #checks to see if solved
    def CheckSolve(self):
        for goal in self.goals:
            print(goal)
            print(self.levelArray[goal[0]][goal[1]])
            if not self.levelArray[goal[0]][goal[1]] == 5:
                return 0
        print("solved")
        return 1

    #moves player in given direction
    def Move(self, direction):
        [hor,hSign,ver,vSign] = self.Direction_Switch(direction)
        targetOnePos = [self.pPos[0]+(hor*hSign),self.pPos[1]+(ver*vSign)]
        targetOneVal = self.levelArray[targetOnePos[0]][targetOnePos[1]]
        targetTwoPos = [self.pPos[0]+2*(hor*hSign),self.pPos[1]+2*(ver*vSign)]
        targetTwoVal = self.levelArray[targetTwoPos[0]][targetTwoPos[1]]
        if targetOneVal == 0 or (targetOneVal == 2 and (targetTwoVal == 0 or targetTwoVal == 2)):
            print("Invalid Move!!")
        elif targetOnePos[0] < 0 or targetOnePos[1] >= self.width or (targetOneVal == 2 and (targetTwoPos[0] < 0 or targetTwoPos[1] >= self.height)):
            print("Invalid Move!!")
        else:
            if targetOneVal == 2:
                self.levelArray[targetOnePos[0]][targetOnePos[1]] = 4
                if targetTwoVal == 3:
                    self.levelArray[targetTwoPos[0]][targetTwoPos[1]] = 5
                else:
                    self.levelArray[targetTwoPos[0]][targetTwoPos[1]] = 2
            elif targetOneVal == 3:
                self.levelArray[targetOnePos[0]][targetOnePos[1]] = 6
            else:
                self.levelArray[targetOnePos[0]][targetOnePos[1]] = 4
            if self.levelArray[self.pPos[0]][self.pPos[1]] == 6:
                self.levelArray[self.pPos[0]][self.pPos[1]] = 3
            else:
                self.levelArray[self.pPos[0]][self.pPos[1]] = 1
            self.pPos[0] += hor * hSign
            self.pPos[1] += ver * vSign
            self.DetectDifference()

    def GetData(self):
        data = {
            "levelArray": self.levelArray,
            "prevState": self.prevState,
            "pPos": self.pPos,
            "goals": self.goals,
            "width": self.width,
            "height": self.height}
        return data