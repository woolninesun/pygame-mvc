PlayerNum = 1
MaxManualPlayerNum = 1

#dir const
dirConst = [
    [0,0],              # can't movw
    [0,-1],             # Up
    [0.707,-0.707],     # Right up
    [1,0],              # Roght
    [0.707,0.707],      # Right down
    [0,1],              # Down
    [-0.707,0.707],     # Left down
    [-1,0],             # Left
    [-0.707,-0.707]     # Left up
]
dirBounce = [
    [0, 1, 8, 7, 6, 5, 4, 3, 2], # x bouce
    [0, 5, 4, 3, 2, 1, 8, 7, 6], # y bouce
]
