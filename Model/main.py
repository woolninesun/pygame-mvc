import time, random

from Events.Manager import *
from Model.StateMachine import *
from Model.GameObject.Player import *
from Model.GameObject.Ball import *

import Model.const       as modelConst
import View.const        as viewConst
import Controller.const  as ctrlConst
import Interface.const   as IfaConst

class GameEngine(object):
    """
    Tracks the game state.
    """
    def __init__(self, evManager, AINames):
        """
        evManager (EventManager): Allows posting messages to the event queue.

        Attributes:
            running (bool): True while the engine is online. Changed via Event_Quit().
            state (StateMachine()): control state change, stack data structure.
            AIList (list.str): all AI name list.
            players (list.player()): all player object.
            TurnTo (int): current player
        """
        self.evManager = evManager
        evManager.RegisterListener(self)

        self.running = False
        self.state = StateMachine()
        self.AINames = AINames
        self.players = []
        self.TurnTo = 0
        self.balls = set()

        random.seed(time.time())

    def notify(self, event):
        """
        Called by an event in the message queue. 
        """
        if isinstance(event, Event_EveryTick):
            cur_state = self.state.peek()
            if cur_state == STATE_PLAY:
                self.UpdateObjects()
        elif isinstance(event, Event_StateChange):
            # if event.state is None >> pop state.
            if event.state is None:
                # false if no more states are left
                if not self.state.pop():
                    self.evManager.Post(Event_Quit())
            elif event.state == STATE_RESTART:
                self.state.clear()
                self.state.push(STATE_MENU)
            else:
                # push a new state on the stack
                self.state.push(event.state)
        elif isinstance(event, Event_Move):
            self.SetPlayerDirection(event.PlayerIndex, event.Direction)
        elif isinstance(event, Event_Quit):
            self.running = False
        elif isinstance(event, Event_Initialize) or \
             isinstance(event, Event_Restart):
            self.Initialize()

    def Initialize(self):
        self.SetPlayer()
        self.SetBall()

    def SetPlayer(self):
        # set AI Names List
        # "_" ==> default AI, "~" ==> manual player
        self.players, ManualPlayerNum = [], 0
        for index in range(modelConst.PlayerNum):
            if len(self.AINames) > index:
                PlayerName = self.AINames[index]
                if PlayerName == "~":
                    if ManualPlayerNum < modelConst.MaxManualPlayerNum:
                        ManualPlayerNum += 1
                    else:
                        self.AINames[index] = "_"
            else:
                if ManualPlayerNum < modelConst.MaxManualPlayerNum:
                    ManualPlayerNum += 1
                    self.AINames.append("~")
                else:
                    self.AINames.append("_")

        # init Player object
        for index in range(modelConst.PlayerNum):
            if self.AINames[index] == "~":
                Tmp_P = player("manual", index, False)
            elif self.AINames[index] == "_":
                Tmp_P = player("default", index, True)
            else:
                Tmp_P = player(self.AINames[index], index, True)
            self.players.append(Tmp_P)

    def SetPlayerDirection(self, playerIndex, direction):
        if self.players[playerIndex] != None:
            player = self.players[playerIndex]
            player.direction = direction

    def SetBall(self):
        for _ in range(5):
            self.balls.add(Ball())

    def UpdateObjects(self):
        # Update players
        for player in self.players:
            player.UpdatePos()
        # Update balls
        for ball in self.balls:
            ball.UpdatePos()
        
        #manage catch the ball and send balls to destination
        for player in self.players:
            for ball in self.balls:
                if (player.pos[0] - ball.pos[0])** 2 + (player.pos[1] - ball.pos[1])** 2 \
                    <= (viewConst.playerRadius + viewConst.ballRadius)** 2:
                    if not player.full():
                        player.own_balls.append(ball)
                        self.calcBallScore(ball)
                    self.balls.remove(ball)
                    self.balls.add(Ball())
            
            for ball in player.own_balls:
                if abs(player.pos[0] - viewConst.destination[ball.color][0]) <= viewConst.destination[ball.color][2] \
                    and abs(player.pos[1] - viewConst.destination[ball.color][1]) <= viewConst.destination[ball.color][3]:
                    player.score += ball.score
                    player.own_balls.remove(ball)
            
        
        
        
    def calcBallScore(self, ball):
        destination = viewConst.destination[ball.color]
        ball.score = int(abs(destination[0] - ball.pos[0]) + abs(destination[1] - ball.pos[1]))
        if ball.level == 'triangle':
            ball.score *= 2
        elif ball.level == 'square':
            ball.score *= 3
        

    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify(). 
        """
        self.running = True
        self.evManager.Post(Event_Initialize())
        self.state.push(STATE_MENU)
        while self.running:
            newTick = Event_EveryTick()
            self.evManager.Post(newTick)
