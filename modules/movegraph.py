import node as Node

class MoveGraph():
    def __init__(self, initPos, *args, **kwargs):
        self.root = Node(initPos)
        self.currentNode = self.root

    def Return(self):
        self.currentNode = self.root

    def AddMove(self, move):
        if len(self.currentNode) == 1:
            self.currentNode.append([move])
        else:
            self.currentNode[1].append([move])

    