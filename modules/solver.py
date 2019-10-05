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

        self.root = node.Node('root')
        self.currentNode = self.root

        self.decisionIndices = []
        self.indices = []

    def Decide(self):
        self.open = []
        self.boxMoves = []
        self.SeeAvailable(self.pPos)
        goalPath = self.GoalPathSearch()
        if goalPath:
            self.prevMove = []
            return goalPath
        else:
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

    def MakeIntermediateMove(self):
        if not self.currentNode.KnowsChildren():      #see if node has been visited yet
            ##clear out dead-end moves
            if len(self.prevMove):
                for move in self.boxMoves:
                    if move == [self.prevMove[1], self.prevMove[0]]:
                        self.boxMoves.remove(move)
            for move in self.boxMoves:
                if self.CheckDeadEnd(move) or self.IsBlockLocked(move[1], move[0]):
                    self.boxMoves.remove(move)
            ##add moves to the graph
            self.currentNode.AddChildren(self.boxMoves)

        self.currentNode, index = self.currentNode.GetNextNode()
        self.indices.append(index)
        if not self.currentNode:        #if there are no possible moves
            self.ResetChecker()
            return "Reset"
        move = self.currentNode.GetMove()
        self.prevMove = move
        playerPath = self.ConstructPlayerPath(move)
        return self.MakeMoveSet(playerPath[:])
        

        
        #isDeadEnd = True
        #deadEndMoves = []
        #moveDeadEnd = True
        #isBlocked = True
        #while isDeadEnd or isBlocked:
            
        #    moveIndex = random.randint(0,len(self.boxMoves)-1)
        #    boxPath = self.boxMoves[moveIndex]
        #    isDeadEnd = self.CheckDeadEnd(boxPath)
        #    isBlocked = self.IsBlockLocked(boxPath[1], boxPath[0])
        #    if isDeadEnd or isBlocked:
        #        self.boxMoves.remove(boxPath)
        #self.prevMove = boxPath
        #playerPath = self.ConstructPlayerPath(boxPath)
        ##print("Found random move")
        #return self.MakeMoveSet(playerPath[:]), moveIndex



    #currently only checks for corner dead ends
    def CheckDeadEnd(self, move):
        deadValues = [0]
        pos = move[0]
        target = move[1]
        prevDir = self.PositionToDirection(move[0],move[1])
        targetExtended = self.levelArray[target[0]+prevDir[0]][target[1]+prevDir[1]]
        extCatOne = self.levelArray[target[0]+prevDir[1]][target[1]+prevDir[0]]
        extCatTwo = self.levelArray[target[0]-prevDir[1]][target[1]-prevDir[0]]
        if targetExtended in deadValues:
            if extCatOne in deadValues or extCatTwo in deadValues:
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
        tempLevelArray = [x[:] for x in self.levelArray]
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

    #Verifies position is within bounds
    def CheckRange(self, pos):
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= self.width or pos[1] >= self.height:
            return 0
        else:
            return 1

    #finds absolute distance between two points
    def Distance(self, posOne, posTwo):
        return math.sqrt((posOne[0] - posTwo[0])**2 + (posOne[1] - posTwo[1])**2)

    #A* algorithm for finding a path
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
    
    def MakeMoveSet(self, positions):
        if not positions:
            return "Pass"
        moveSet = []
        prevPos = positions[0][:]
        for pos in positions[1:]:
            moveSet.append(self.PositionToMove(prevPos, pos))
            prevPos = pos[:]
        return moveSet

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

    def ResetChecker(self):
        for indices in self.decisionIndices:
            if self.indices == indices:
                print("SONOFABITCH")
        self.decisionIndices.append([x[:] for x in self.indices])
        return