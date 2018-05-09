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
        elif isinstance(event, Event_Initialize) or \
             isinstance(event, Event_Restart):
            self.initialize()
    
    def API_play(self):
        for player in self.model.players:
            if player.is_AI:
                AI_Dir = player.ai.decide()
                self.evManager.Post(Event_Move(player.index, AI_Dir))
        
    def initialize(self):
        for index, player in enumerate(self.model.players):
            if player.name == "manual":
                    continue
            # load TeamAI .py file
            try:
                loadtmp = imp.load_source('', './AI/team_' + player.name + '.py')
            except:
                print( "player:["+ str(index) +"]team_"+ player.name +"'s AI can't load." )
                player.name, player.is_AI, player.ai= "Error" , False, None
                continue
            print("Load ["+ str(index) +"]team_" + player.name + ".py")
            # init TeamAI class
            try:
                player.ai = loadtmp.TeamAI( Helper(self.model, index) )
            except:
                print( "player:["+ str(index) +"]team_"+ player.name +"'s AI __init__ is crashed." )
                traceback.print_exc()
                player.name, player.is_AI, player.ai= "Error" , False, None
                continue
            print("Successful to Load ["+ str(index) +"]team_" + player.name + ".py")
    