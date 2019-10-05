import random

class Node():
    def __init__(self, move, *args, **kwargs):
        self.move = move
        self.children = []
        self.completed = False
        self.knowChildren = False
        
    def GetNextNode(self):
        if not len(self.children):
            self.completed = True
            return 0
        found = 0
        indexes = []
        while not found:
            index = random.randint(0,len(self.children)-1)
            if not self.children[index].IsCompleted():
                return [self.children[index], index]
            elif index not in indexes:
                indexes.append(index)
            if len(indexes) == len(self.children):
                self.completed = True
                return 0, 0
        #for child in self.children:
        #    while not found:
        #        if not child.IsCompleted():
        #            return child
        

    def IsCompleted(self):
        return self.completed

    def KnowsChildren(self):
        return self.knowChildren

    def AddChildren(self, children):
        self.knowChildren = True
        for child in children:
            self.children.append(Node(child))

    def GetMove(self):
        return self.move