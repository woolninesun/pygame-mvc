import random

import Model.const       as modelConst

class player(object):
    def __init__(self, name, index, is_AI):
        self.name = name
        self.is_AI = is_AI
        self.index = index
        self.ai = None
        self.color = [ random.randint(0,255) for _ in range(3) ]
        self.own_balls = []
        self.score = 0
        
        self.pos = [ random.randint(20,780), random.randint(20,780) ]
        self.direction = 1

    def UpdatePos(self):
        [add_x, add_y] = modelConst.dirConst[self.direction]
        Bounce = modelConst.dirBounce
        if self.pos[0] + add_x < 20 \
            or self.pos[0] + add_x > 780 :
            self.direction = Bounce[0][self.direction]
        elif self.pos[1] + add_y < 20 \
            or self.pos[1] + add_y > 780 :
            self.direction = Bounce[1][self.direction]

        addDir = modelConst.dirConst[self.direction]

        self.pos[0] += addDir[0]
        self.pos[1] += addDir[1]
    
    def full(self):
        return len(self.own_balls) >= 3
    
