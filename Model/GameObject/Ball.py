import Model.const       as modelConst

import random

class Ball(object):
    def __init__(self):
        self.color = random.choice([(255,0,0), (255,255,0), (0,0,255), (0,255,0)])#red, yellow, blue, green
        self.level = random.choice(['circle', 'triangle', 'square'])
        self.score = 0
        if random.randint(0, 1) == 0:#up-down or left-right
            self.velocity = [random.uniform(-1, 1), 0.0]
        else:
            self.velocity = [0.0, random.uniform(-1, 1)]
        self.pos = [random.randint(20, 780), random.randint(20, 780)]

    def UpdatePos(self):
        if (self.pos[0] + self.velocity[0] < 20 and self.velocity[0] < 0) \
            or (self.pos[0] + self.velocity[0] > 780 and self.velocity[0] > 0):
            self.velocity[0] *= -1
        if (self.pos[1] + self.velocity[1] < 20 and self.velocity[1] < 0) \
            or (self.pos[1] + self.velocity[1] > 780 and self.velocity[1] > 0):
            self.velocity[1] *= -1
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        
        
