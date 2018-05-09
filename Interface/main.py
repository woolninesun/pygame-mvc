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
            self.API_play()
        elif isinstance(event, Event_Quit):
            pass
        elif isinstance(event, Event_Initialize):
            self.initialize()
    
    def API_play(self):
        for player in self.model.player:
            player.ai.decide()
        
    def initialize(self):
        for index, player in enumerate(self.model.player):
            # load TeamAI .py file
            try:
                loadtmp = imp.load_source('', './AI/team_' + player.name + '.py')
            except:
                print( "player:["+ str(index) +"]team_"+ player.name +"'s AI can't load." )
                player.name, player.IS_AI, player.ai= "Error" , False, None
                continue
            print("Load ["+ str(index) +"]team_" + player.name + ".py")
            # init TeamAI class
            try:
                player.ai = loadtmp.TeamAI( Helper(self.model, index) )
            except:
                print( "player:["+ str(index) +"]team_"+ player.name +"'s AI __init__ is crashed." )
                traceback.print_exc()
                player.name, player.IS_AI, player.ai= "Error" , False, None
                continue
            print("Successful to Load ["+ str(index) +"]team_" + player.name + ".py")
    