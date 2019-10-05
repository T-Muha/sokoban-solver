import json


##converts text level files into json objects
##only needs to be used once on a text level, easier than manually writing json yourself

fileName = "10"

with open(fileName + '.txt', 'r') as txtFile:
    txtLevel = txtFile.readlines()

levelData = {
    "boxes": [],
    "goals": [],
    "floor": [],
}
txtLevel.reverse()

def txtSwitcher(val):
    switcher = {"s": "player", "o": "boxes", "x": "goals", "-": "floor"}
    return switcher.get(val)

height = len(txtLevel)
width = len(txtLevel[0]) - 1

levelData["size"] = [width, height]

for y in range(height):
    for x in range(width):
        switched = txtSwitcher(txtLevel[y][x])
        if switched:
            if switched == "player":
                levelData["player"] = [x,y]
            else:
                levelData[switched].append([x,y])

with open(fileName + '.json', 'w', encoding='utf-8') as jsonFile:
    json.dump(levelData, jsonFile, ensure_ascii=False, indent=4)