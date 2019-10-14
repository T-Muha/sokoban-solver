import math, collections, random
from modules import node

class Solver():
    def __init__(self, initData, *args, **kwargs):
        self.levelArray = initData["levelArray"]
        self.prevState = initData["prevState"]
        self.pPos = initData["pPos"]
        self.goals = initData["goals"]
        self.width = initData["width"]
        self.height = initData["height"]
        self.open = []
        self.availGoal = []
        self.boxMoves = []
        self.prevMove = []
        self.prunedBoxMoves = []

        self.root = node.Node('root', None)
        self.currentNode = self.root
        self.allNodes = [self.root]

        self.depth = 0
        self.maxDepth = 3
        self.numResetAtDepth = 0
        self.maxResetAtDepth = 5

    def Decide(self):
        self.open = []
        self.boxMoves = []
        self.SeeAvailable(self.pPos)
        goalPath = self.GoalPathSearch()
        if goalPath:
            self.prevMove = []
            return goalPath
        else:
            #self.depth += 1
            #if self.depth == self.maxDepth:
            #    self.depth = 0
            #    if self.numResetAtDepth == self.maxResetAtDepth:
            #        self.numResetAtDepth = 0
            #        self.maxResetAtDepth *= 2
            #        self.maxDepth += 1
            #    print("YUH")
            #    return "Reset"
            move = self.MakeIntermediateMove()
        return move

    #Used if level is reset
    def UpdateData(self, newData):
        self.levelArray = newData["levelArray"]
        self.goals = newData["goals"]
        self.pPos = newData["pPos"]
        self.prevState = newData["prevState"]
        self.width = newData["width"]
        self.height = newData["height"]
        self.currentNode = self.root

    #Used if a level is selected
    def NewLevel(self, newData):
        self.UpdateData(newData)
        self.root = node.Node('root')

    def TempCheck(self, move):
        ##check to see if box's only option is a dead space surrounded by walls - Reset condition
        tempX = move[1][0]
        tempY = move[1][1]
        tempDir = self.PositionToDirection(move[0], move[1])
        touchingOne = self.levelArray[tempX+tempDir[0]][tempY+tempDir[1]]
        touchingTwo = self.levelArray[tempX+abs(tempDir[0])-1][tempY+abs(tempDir[1])-1]
        touchingThree = self.levelArray[tempX-(abs(tempDir[0])-1)][tempY-(abs(tempDir[1])-1)]
        if touchingOne == 0 and touchingTwo == 0 and touchingThree == 0:
            self.prunedBoxMoves = []

    def MakeIntermediateMove(self):
        if not self.currentNode.KnowsChildren():      #see if node has been visited yet
            self.prunedBoxMoves = [x[:] for x in self.boxMoves[:]]
            for move in self.boxMoves:
                self.TempCheck(move)
                if len(self.prunedBoxMoves) and (self.IsBlockLocked(move[1], move[0]) or self.IsRingBlocked(move[1], move[0])):
                    self.prunedBoxMoves.remove(move)
            ##add pruned moves to the graph
            self.currentNode.AddChildren([x[:] for x in self.prunedBoxMoves[:]])
            children = self.currentNode.GetChildren()
            for child in children:
                self.allNodes.append(child)
        self.currentNode, index = self.currentNode.GetNextNode()
        if not self.currentNode:        #if there are no possible moves
            return "Reset"
        move = self.currentNode.GetMove()
        self.prevMove = move
        playerPath = self.ConstructPlayerPath(move)
        return self.MakeMoveSet(playerPath[:])
    
    #prunes dead end node paths
    def CompressNodes(self):
        if len(self.allNodes):
            for i in range(len(self.allNodes)-1,-1,-1):
                self.allNodes[i].Compress()

    #Checks to see if tile is part of a locked ring of 3x3
    def IsRingBlocked(self, pos, prevPos):

        #groupOneLeft = [pos, [pos[0], pos[1]-1], [pos[0], pos[1]-2]]
        #groupOneRight = [[pos[0]+2, pos[1]], [pos[0]+2, pos[1]-1], [pos[0]+2, pos[1]-2]]
        #groupOneTop = [pos, [pos[0]+1, pos[1]], [pos[0]+2, pos[1]]]
        #groupOneBottom = [pos, [pos[0]+1, pos[1]-2], [pos[0]+2, pos[1]-2]]
        #groupBottomRight = [groupOneLeft, groupOneRight, groupOneTop, groupOneBottom]

        #groupTwoRight = [pos, [pos[0], pos[1]-1], [pos[0], pos[1]-2]]
        #groupTwoLeft = [[pos[0]-2, pos[1]], [pos[0]-2, pos[1]-1], [pos[0]-2, pos[1]-2]]
        #groupTwoTop = [pos, [pos[0]-1, pos[1]], [pos[0]-2, pos[1]]]
        #groupTwoBottom = [pos, [pos[0]-1, pos[1]-2], [pos[0]-2, pos[1]-2]]
        #groupBottomLeft = [groupTwoLeft, groupTwoRight, groupTwoTop, groupTwoBottom]

        #groupThreeLeft = [pos, [pos[0], pos[1]+1], [pos[0], pos[1]+2]]
        #groupThreeRight = [[pos[0]+2, pos[1]], [pos[0]+2, pos[1]+1], [pos[0]+2, pos[1]+2]]
        #groupThreeBottom = [pos, [pos[0]+1, pos[1]], [pos[0]+2, pos[1]]]
        #groupThreeTop = [pos, [pos[0]+1, pos[1]+2], [pos[0]+2, pos[1]+2]]
        #groupTopRight = [groupThreeLeft, groupThreeRight, groupThreeTop, groupThreeBottom]

        #groupFourLeft = [[pos[0]-2, pos[1]], [pos[0]-2, pos[1]+1], [pos[0], pos[1]+2]]
        #groupFourRight = [pos, [pos[0], pos[1]+1], [pos[0], pos[1]+2]]
        #groupFourBottom = [pos, [pos[0]-1, pos[1]], [pos[0]-2, pos[1]]]
        #groupFourTop = [pos, [pos[0]-1, pos[1]+2], [pos[0]-2, pos[1]+2]]
        #groupTopLeft = [groupFourLeft, groupFourRight, groupFourTop, groupFourBottom]

        #groups = [groupTopLeft, groupTopRight, groupBottomLeft, groupBottomRight]
        #tempLevelArray = [x[:] for x in self.levelArray[:]]
        #tempLevelArray[pos[0]][pos[1]] = 2
        #tempLevelArray[prevPos[0]][prevPos[1]] = 1
        #blockCounter = 0
        #for group in groups:
        #    for side in group:
        #        for pos in side:
        #            if self.CheckRange(pos) and (tempLevelArray[pos[0]][pos[1]] == 2 or tempLevelArray[pos[0]][pos[1]] == 0):
        #                blockCounter += 1
        #    if blockCounter == 8:
        #        return True
        #    blockCounter = 0




        #tempLevelArray = [x[:] for x in self.levelArray[:]]
        #tempLevelArray[pos[0]][pos[1]] = 2
        #tempLevelArray[prevPos[0]][prevPos[1]] = 1
        #turnMultipliers = [[1,1,-1,-1], [1,-1,-1,1], [-1,1,1,-1], [-1,-1,1,1]]
        #for set in turnMultipliers:
        #    for mul in set:
        #        blockCounter = 0
        #        for side in range(1,4):
        #            vectorDir = side * mul
        #            checkPos = [pos[0]+vectorDir, pos[1]]
        #            posGood = self.CheckRange(checkPos)
        #            checkVal = 0
        #            if posGood and side % 2:
        #                checkVal = tempLevelArray[checkPos[0]][checkPos[1]]
        #            elif posGood:
        #                checkVal = tempLevelArray[checkPos[0]][checkPos[1]]
        #            if checkVal == 0 or checkVal == 2:
        #                blockCounter += 1
        #        if blockCounter == 7:
        #            return True
        #return False

        tempLevelArray = [x[:] for x in self.levelArray[:]]
        tempLevelArray[pos[0]][pos[1]] = 2
        tempLevelArray[prevPos[0]][prevPos[1]] = 1
        dirMultipliers = [[1,1],[1,-1],[-1,1],[-1,-1]]
        for dir in dirMultipliers:
                blockCounter = 0
                for y in range(3):
                    for x in range(3):
                        vecPos = [pos[0]+dir[0]*x, pos[1]+dir[1]*y]
                        if self.CheckRange(vecPos) and (x != 1 and y != 1):
                            val = tempLevelArray[vecPos[0]][vecPos[1]]
                            if val == 0 or val == 2:
                                blockCounter += 1
                if blockCounter == 8:
                    return True
        return False


    #sees if a tile is part of a locked group of four
    def IsBlockLocked(self, pos, prevPos):
        groupOne = [pos, [pos[0]+1,pos[1]], [pos[0]+1,pos[1]-1], [pos[0],pos[1]-1]]
        groupTwo = [pos, [pos[0]+1,pos[1]], [pos[0]+1,pos[1]+1], [pos[0],pos[1]+1]]
        groupThree = [pos, [pos[0]-1,pos[1]], [pos[0]-1,pos[1]-1], [pos[0],pos[1]-1]]
        groupFour = [pos, [pos[0]-1,pos[1]], [pos[0]-1,pos[1]+1], [pos[0],pos[1]+1]]
        groups = [groupOne, groupTwo, groupThree, groupFour]
        blockCounter = 0
        tempLevelArray = [x[:] for x in self.levelArray[:]]
        tempLevelArray[pos[0]][pos[1]] = 2
        tempLevelArray[prevPos[0]][prevPos[1]] = 1
        for group in groups:
            for position in group:
                if tempLevelArray[position[0]][position[1]] == 0 or tempLevelArray[position[0]][position[1]] == 2:
                    blockCounter += 1
            if blockCounter == 4:
                return True
            blockCounter = 0
        return False

    #Tries to find shortest open path from a box to a goal
    def GoalPathSearch(self):
        #print("Searching for a clear box-goal path")
        verifiedPaths = []
        for move in self.boxMoves:
            start = move[1]
            for goal in self.goals:
                boxPath = self.FindPath(start, goal)#check to see if path is even there
                if boxPath:
                    boxPath.insert(0, move[0])
                    playerPath = self.ConstructPlayerPath(boxPath)
                    if playerPath:
                        ##save pPostions so they wont have to be found again when a path is chosen
                        verifiedPaths.append(playerPath) #add it to verified paths
        if len(verifiedPaths):
            minLen = len(verifiedPaths[0])
            minPath = verifiedPaths[0][:]
            #more can go here to decide path?
            for path in verifiedPaths:
                pathLen = len(path)
                if pathLen > minLen:
                    minLen = pathLen
                    minPath = path[:]
            return self.MakeMoveSet(minPath[:])
        else:
            return False

    #Constructs path player must take to push box along the input path
    #return false if path is not possible
    def ConstructPlayerPath(self, boxPath):
        pPrevPos = self.pPos[:]
        prevPos = boxPath[0][:]
        constructedPath = []
        constructedPath.append(self.pPos[:])
        for pos in boxPath[1:]:
            direction = self.PositionToDirection(prevPos, pos)
            position = [prevPos[0]-1*direction[0],prevPos[1]-1*direction[1]]
            intermediatePath = self.FindPath(pPrevPos, position, modifiers=[[boxPath[0][0],boxPath[0][1],1],[prevPos[0],prevPos[1],2]]) #figure out when no path possible?
            if not intermediatePath:
                return False
            for node in intermediatePath[1:]:
                constructedPath.append(node[:])
            constructedPath.append(prevPos)
            pPrevPos = prevPos[:]
            prevPos = pos[:]
        return constructedPath

    #Controls process of updating open space and available box moves
    def SeeAvailable(self, pos):
        #0: wall, 1: floor, 2: bFloor, 3: goal, 4: pFloor, 5: bGoal, 6: pGoal
        if self.LookOpen(pos,[-1,0]):
            if not [pos[0]-1,pos[1]] in self.open:
                self.open.append([pos[0]-1,pos[1]])
                self.SeeAvailable([pos[0]-1,pos[1]])
        if self.LookOpen(pos,[1,0]):
            if not [pos[0]+1,pos[1]] in self.open:
                self.open.append([pos[0]+1,pos[1]])
                self.SeeAvailable([pos[0]+1,pos[1]])
        if self.LookOpen(pos,[0,-1]):
            if not [pos[0],pos[1]-1] in self.open:
                self.open.append([pos[0],pos[1]-1])
                self.SeeAvailable([pos[0],pos[1]-1])
        if self.LookOpen(pos,[0,1]):
            if not [pos[0],pos[1]+1] in self.open:
                self.open.append([pos[0],pos[1]+1])
                self.SeeAvailable([pos[0],pos[1]+1])
        return

    #Determines if position is open space or an available box move
    def LookOpen(self, pos, direction):
        if self.CheckRange([pos[0]+direction[0],pos[1]+direction[1]]):
            oneAway = self.levelArray[pos[0]+direction[0]][pos[1]+direction[1]]
            if oneAway == 1 or oneAway == 3:
                return 1
            elif oneAway == 2 and self.CheckRange([pos[0]+2*direction[0],pos[1]+2*direction[1]]):
                twoAway = self.levelArray[pos[0]+2*direction[0]][pos[1]+2*direction[1]]
                if twoAway == 1 and not [[pos[0]+direction[0],pos[1]+direction[1]],[pos[0]+2*direction[0],pos[1]+2*direction[1]]] in self.boxMoves:
                    self.boxMoves.append([[pos[0]+direction[0],pos[1]+direction[1]],[pos[0]+2*direction[0],pos[1]+2*direction[1]]])
        return 0

    #A* algorithm for finding a path. Modifier allows you to use level state different than the current one
    def FindPath(self, posOne, posTwo, modifiers=None):
        if modifiers:
            modifiedLevel = [x[:] for x in self.levelArray]
            for modifier in modifiers:
                modifiedLevel[modifier[0]][modifier[1]] = modifier[2]
        openSet = [posOne[:]]
        cameFrom = {}
        closedSet = []
        gScore = collections.defaultdict(lambda: 10000)
        fScore = collections.defaultdict(lambda: 10000)
        gScore[(posOne[0],posOne[1])] = 0
        fScore[(posOne[0],posOne[1])] = self.Distance(posOne, posTwo)
        while not len(openSet) == 0:
            current = openSet[0]
            for node in openSet:
                if fScore[(node[0],node[1])] < fScore[(current[0],current[1])]:
                    current = node
            if current == posTwo:
                totalPath = [current[:]]
                while (current[0],current[1]) in cameFrom:
                    current = cameFrom[(current[0],current[1])]
                    totalPath.insert(0,current[:])
                return totalPath
            openSet.remove(current)
            closedSet.append(current)
            for adjacent in [[current[0]+1,current[1]],[current[0]-1,current[1]],[current[0],current[1]+1],[current[0],current[1]-1]]:
                if self.CheckRange(adjacent):
                    if modifiers:
                        adjacentVal = modifiedLevel[adjacent[0]][adjacent[1]]
                    else:
                        adjacentVal = self.levelArray[adjacent[0]][adjacent[1]]
                    if not adjacent in closedSet and not adjacentVal == 0 and not adjacentVal == 2 and not adjacentVal == 5:
                        tentativeGScore = gScore[(current[0],current[1])] + self.Distance(current, adjacent)
                        if tentativeGScore < gScore[(adjacent[0],adjacent[1])]:
                            cameFrom[(adjacent[0],adjacent[1])] = current
                            gScore[(adjacent[0],adjacent[1])] = tentativeGScore
                            fScore[(adjacent[0],adjacent[1])] = gScore[(adjacent[0],adjacent[1])] + self.Distance(adjacent, posTwo)
                            if not adjacent in openSet:
                                openSet.append(adjacent)
    
    #Converts a set of positions to the moves made
    def MakeMoveSet(self, positions):
        if not positions:
            return "Pass"
        moveSet = []
        prevPos = positions[0][:]
        for pos in positions[1:]:
            moveSet.append(self.PositionToMove(prevPos, pos))
            prevPos = pos[:]
        return moveSet

   #Converts two positions to the move made
    def PositionToMove(self, prevPos, nextPos):
        if prevPos[0] == nextPos[0]:
            if prevPos[1] < nextPos[1]:
                return "Up"
            else:
                return "Down"
        else:
            if prevPos[0] < nextPos[0]:
                return "Right"
            else:
                return "Left"

    #converts two positions to the direction taken to make the move
    def PositionToDirection(self, prevPos, nextPos):
        if prevPos[0] == nextPos[0]:
            if prevPos[1] < nextPos[1]:
                return [0,1]
            else:
                return [0,-1]
        else:
            if prevPos[0] < nextPos[0]:
                return [1,0]
            else:
                return [-1,0]

    #Checks to see if space is available to player
    def IsAccessible(self, position):
        if position in self.open:
            return True
        return False

    #Verifies position is within bounds
    def CheckRange(self, pos):
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= self.width or pos[1] >= self.height:
            return 0
        else:
            return 1

    #finds absolute distance between two points
    def Distance(self, posOne, posTwo):
        return math.sqrt((posOne[0] - posTwo[0])**2 + (posOne[1] - posTwo[1])**2)