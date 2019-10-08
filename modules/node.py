import random

class Node():
    def __init__(self, move, parent, *args, **kwargs):
        self.move = move
        self.children = []
        self.completed = False
        self.knowChildren = False
        self.parent = parent
        
    def GetNextNode(self):
        if self.parent and self.GetAncestor(1) and self.GetAncestor(5) and self.GetAncestor(1).GetMove() == self.GetAncestor(5).GetMove():
            self.completed = True
            return 0,0
        if not len(self.children):
            self.completed = True
            return 0, 0
        found = 0
        indexes = []
        while not found:
            index = random.randint(0,len(self.children)-1)
            if not self.children[index].IsCompleted():
                return self.children[index], index
            elif index not in indexes:
                indexes.append(index)
            if len(indexes) == len(self.children):
                self.completed = True
                return 0, 0        

    def IsCompleted(self):
        return self.completed

    def KnowsChildren(self):
        return self.knowChildren

    def AddChildren(self, children):
        self.knowChildren = True
        for child in children:
            self.children.append(Node(child, self))

    def GetChildren(self):
        return self.children

    def GetMove(self):
        return self.move

    def GetParent(self):
        if self.parent == None:
            return False
        return self.parent

    def GetAncestor(self, generation):
        if self.parent == None:
            return False
        if generation == 1:
            return self.GetParent()
        return self.GetParent().GetAncestor(generation-1)

    def Compress(self):
        if self.completed:
            return
        self.complete = 1
        for child in self.children:
            if not child.IsCompleted():
                self.complete = 0