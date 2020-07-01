class Node(object):
    def __init__(self, par, pos, ntype, dst):
        self.parent=par
        self.nPos = pos
        self.nType=ntype
        self.obstacle=False
        if(ntype == 3):
            self.obstacle = True
        self.dst = 0

    def __eq__(self,other):
        return self.nPos[0] == other.nPos[0] and self.nPos[1] == self.nPos[1]

    def __lt__(self,other):
        return (self.nPos[0]+self.nPos[0]) < (self.nPos[1]+self.nPos[1])
    
    def __hash__(self):
        return self.nPos[0]*self.nPos[1]

    def __dir__(self):
        return [self.parent, self.nPos, self.nType, self.obstacle, self.dst]