import json
import pyglet
from modules import resources, board

######import json level here###########


##create pyglet window
MainWindow = pyglet.window.Window(1280, 720)
mainBatch = pyglet.graphics.Batch()

with open('levels/test-level.json') as json_file:
    levelData = json.load(json_file)

board.Board(levelData)



#####load graphics based on levelArray
#drawnLevel = []
#for i in range(len(levelArray)):
#    tempList = []
#    for j in range(len(levelArray)):
#        if levelArray[i][j] == 0:
#            tempList.append(pyglet.sprite.Sprite(img=wall, x = i*64, y = j*64, batch = mainBatch))
#        elif levelArray[i][j] == 1:
#            tempList.append(pyglet.sprite.Sprite(img=floor, x = i*64, y = j*64, batch = mainBatch))
#        elif levelArray[i][j] == 2:
#            tempList.append(pyglet.sprite.Sprite(img=bFloor, x = i*64, y = j*64, batch = mainBatch))
#        elif levelArray[i][j] == 3:
#            tempList.append(pyglet.sprite.Sprite(img=goal, x = i*64, y = j*64, batch = mainBatch))
#        elif levelArray[i][j] == 4:
#            tempList.append(pyglet.sprite.Sprite(img=pFloor, x = i*64, y = j*64, batch = mainBatch))
#    drawnLevel.append(tempList[:])

####create previous level state
#prevState = levelArray[:][:]
#prevState = [x[:] for x in levelArray]

def DrawDifference():
    global levelArray
    global prevState
    global drawnLevel
    for i in range(len(levelArray)):
        for j in range(len(levelArray)):
            if not (levelArray[i][j] == prevState[i][j]):
                if levelArray[i][j] == 0:
                    #drawnLevel[i][j] = pyglet.sprite.Sprite(img=wall, x = i*64, y = j*64, batch = mainBatch)
                    drawnLevel[i][j].image = wall
                elif levelArray[i][j] == 1:
                    #drawnLevel[i][j] = pyglet.sprite.Sprite(img=floor, x = i*64, y = j*64, batch = mainBatch)
                    drawnLevel[i][j].image = floor
                elif levelArray[i][j] == 2:
                    #drawnLevel[i][j] = pyglet.sprite.Sprite(img=bFloor, x = i*64, y = j*64, batch = mainBatch)
                    drawnLevel[i][j].image = bFloor
                elif levelArray[i][j] == 3:
                    #drawnLevel[i][j] = pyglet.sprite.Sprite(img=goal, x = i*64, y = j*64, batch = mainBatch)
                    drawnLevel[i][j].image = goal
                elif levelArray[i][j] == 4:
                    #drawnLevel[i][j] = pyglet.sprite.Sprite(img=pFloor, x = i*64, y = j*64, batch = mainBatch)
                    #tempSprite = drawnLevel[i][j]
                    #tempSprite.image = pFloor
                    drawnLevel[i][j].image = pFloor
    prevState = [x[:] for x in levelArray]
    ##graphics should update


###Handles movement once decision has been made

#def MoveLeft():
#    global pPos
#    global levelArray
#    global prevState
#    global drawnLevel
#    targetOne = levelArray[pPos[0]-1][pPos[1]]
#    targetTwo = levelArray[pPos[0]-2][pPos[1]]
#    if targetOne == 0 or (targetOne == 2 and (targetTwo == 0 or targetTwo == 2)):
#        print("Invalid Move!!")
#    else:
#        if targetOne == 2:
#            levelArray[pPos[0]-2][pPos[1]] = 2
#            levelArray[pPos[0]-1][pPos[1]] = 4
#            levelArray[pPos[0]][pPos[1]] = 1
#        else:
#            levelArray[pPos[0]-1][pPos[1]] = 4
#            levelArray[pPos[0]][pPos[1]] = 1
#        pPos[0] -= 1
#        DrawDifference()

#def MoveRight():
#    global pPos
#    targetOne = levelArray[pPos[0]+1][pPos[1]]
#    targetTwo = levelArray[pPos[0]+2][pPos[1]]
#    if targetOne == 0 or (targetOne == 2 and (targetTwo == 0 or targetTwo == 2)):
#        print("Invalid Move!!")
#    else:
#        if targetOne == 2:
#            levelArray[pPos[0]+2][pPos[1]] = 2
#            levelArray[pPos[0]+1][pPos[1]] = 4
#            levelArray[pPos[0]][pPos[1]] = 1
#        else:
#            levelArray[pPos[0]+1][pPos[1]] = 4
#            levelArray[pPos[0]][pPos[1]] = 1
#        pPos[0] += 1
#        DrawDifference()

#def MoveUp():
#    global pPos
#    targetOne = levelArray[pPos[0]][pPos[1]-1]
#    targetTwo = levelArray[pPos[0]][pPos[1]-2]
#    if targetOne == 0 or (targetOne == 2 and (targetTwo == 0 or targetTwo == 2)):
#        print("Invalid Move!!")
#    else:
#        if targetOne == 2:
#            levelArray[pPos[0]][pPos[1]-2] = 2
#            levelArray[pPos[0]][pPos[1]-1] = 4
#            levelArray[pPos[0]][pPos[1]] = 1
#        else:
#            levelArray[pPos[0]][pPos[1]-1] = 4
#            levelArray[pPos[0]][pPos[1]] = 1
#        pPos[1] -= 1
#        DrawDifference()

#def MoveDown():
#    global pPos
#    targetOne = levelArray[pPos[0]][pPos[1]+1]
#    targetTwo = levelArray[pPos[0]][pPos[1]+2]
#    if targetOne == 0 or (targetOne == 2 and (targetTwo == 0 or targetTwo == 2)):
#        print("Invalid Move!!")
#    else:
#        if targetOne == 2:
#            levelArray[pPos[0]][pPos[1]+2] = 2
#            levelArray[pPos[0]][pPos[1]+1] = 4
#            levelArray[pPos[0]][pPos[1]] = 1
#        else:
#            levelArray[pPos[0]][pPos[1]+1] = 4
#            levelArray[pPos[0]][pPos[1]] = 1
#        pPos[1] += 1
#        DrawDifference()

#def Action(dt):
#    move.MoveLeft()

#def update(dt):
#    MoveLeft()

#pyglet.clock.schedule_once(Action, 2)
#pyglet.clock.schedule_interval(update, 2)

@MainWindow.event
def on_draw():
    MainWindow.clear()
    mainBatch.draw()

if __name__ == '__main__':
    pyglet.app.run()

###Make a function to return to a saved array state