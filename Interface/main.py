import imp, traceback

import Model.main as model
from Events.Manager import *

from Interface.helper import Helper

import Model.const       as modelConst
import View.const        as viewConst
import Controller.const  as ctrlConst
import Interface.const   as IfaConst

class Interface(object):
    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model

        self.playerAI = {}

        self.is_initAI = False
    
    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, Event_EveryTick):
            cur_state = self.model.state.peek()
            if cur_state == model.STATE_PLAY:
                self.API_play()
        elif isinstance(event, Event_Quit):
            pass
        elif isinstance(event, Event_Initialize):
            self.initialize()
    
    def API_play(self):
        for player in self.model.players:
            if player.is_AI:
                AI_Dir = self.playerAI[player.index].decide()
                self.evManager.Post(Event_Move(player.index, AI_Dir))
        
    def initialize(self):
        if self.is_initAI: return

        self.is_initAI = True
        for index, player in enumerate(self.model.players):
            if player.name == "manual":
                    continue
            # load TeamAI .py file
            try:
                loadtmp = imp.load_source('', './AI/team_'+ player.name +'.py')
            except:
                self.loadmsg( str(index), player.name, "AI can't load")
                player.name, player.is_AI, player.ai= "Error" , False, None
                continue
            self.loadmsg( str(index), player.name, "Loading")
            # init TeamAI class
            try:
                self.playerAI[player.index] = loadtmp.TeamAI( Helper(self.model, index) )
            except:
                self.loadmsg( str(index), player.name, "AI init crashed")
                traceback.print_exc()
                player.name, player.is_AI, player.ai= "Error" , False, None
                continue
            self.loadmsg( str(index), player.name, "Successful to Load")

    def loadmsg(self, index, name ,msg):
        print("["+ str(index) +"] team_" + name + ".py: "+ msg)
    