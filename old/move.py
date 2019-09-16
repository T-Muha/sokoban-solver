def MoveLeft():
    global pPos
    global levelArray
    global prevState
    global drawnLevel
    targetOne = levelArray[pPos[0]-1][pPos[1]]
    targetTwo = levelArray[pPos[0]-2][pPos[1]]
    if targetOne == 0 or (targetOne == 2 and (targetTwo == 0 or targetTwo == 2)):
        print("Invalid Move!!")
    else:
        if targetOne == 2:
            levelArray[pPos[0]-2][pPos[1]] = 2
            levelArray[pPos[0]-1][pPos[1]] = 4
            levelArray[pPos[0]][pPos[1]] = 1
        else:
            levelArray[pPos[0]-1][pPos[1]] = 4
            levelArray[pPos[0]][pPos[1]] = 1
        pPos[0] -= 1
        DrawDifference()

def MoveRight():
    global pPos
    targetOne = levelArray[pPos[0]+1][pPos[1]]
    targetTwo = levelArray[pPos[0]+2][pPos[1]]
    if targetOne == 0 or (targetOne == 2 and (targetTwo == 0 or targetTwo == 2)):
        print("Invalid Move!!")
    else:
        if targetOne == 2:
            levelArray[pPos[0]+2][pPos[1]] = 2
            levelArray[pPos[0]+1][pPos[1]] = 4
            levelArray[pPos[0]][pPos[1]] = 1
        else:
            levelArray[pPos[0]+1][pPos[1]] = 4
            levelArray[pPos[0]][pPos[1]] = 1
        pPos[0] += 1
        DrawDifference()

def MoveUp():
    global pPos
    targetOne = levelArray[pPos[0]][pPos[1]-1]
    targetTwo = levelArray[pPos[0]][pPos[1]-2]
    if targetOne == 0 or (targetOne == 2 and (targetTwo == 0 or targetTwo == 2)):
        print("Invalid Move!!")
    else:
        if targetOne == 2:
            levelArray[pPos[0]][pPos[1]-2] = 2
            levelArray[pPos[0]][pPos[1]-1] = 4
            levelArray[pPos[0]][pPos[1]] = 1
        else:
            levelArray[pPos[0]][pPos[1]-1] = 4
            levelArray[pPos[0]][pPos[1]] = 1
        pPos[1] -= 1
        DrawDifference()

def MoveDown():
    global pPos
    targetOne = levelArray[pPos[0]][pPos[1]+1]
    targetTwo = levelArray[pPos[0]][pPos[1]+2]
    if targetOne == 0 or (targetOne == 2 and (targetTwo == 0 or targetTwo == 2)):
        print("Invalid Move!!")
    else:
        if targetOne == 2:
            levelArray[pPos[0]][pPos[1]+2] = 2
            levelArray[pPos[0]][pPos[1]+1] = 4
            levelArray[pPos[0]][pPos[1]] = 1
        else:
            levelArray[pPos[0]][pPos[1]+1] = 4
            levelArray[pPos[0]][pPos[1]] = 1
        pPos[1] += 1
        DrawDifference()
