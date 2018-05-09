import pygame as pg

import Model.main as model
from Events.Manager import *

import Model.const       as modelConst
import View.const        as viewConst
import Controller.const  as ctrlConst
import Interface.const   as IfaConst

class Control(object):
    """
    Handles control input.
    """
    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model

        self.ControlKeys = {}

        self.SecEventType = pg.USEREVENT

    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, Event_EveryTick):
            # Called for each game tick. We check our keyboard presses here.
            for event in pg.event.get():
                # handle window manager closing our window
                if event.type == pg.QUIT:
                    self.evManager.Post(Event_Quit())
                else:
                    cur_state = self.model.state.peek()
                    if cur_state == model.STATE_MENU:
                        self.ctrl_menu(event)
                    if cur_state == model.STATE_PLAY:
                        self.ctrl_play(event)
                    if cur_state == model.STATE_STOP:
                        self.ctrl_stop(event)
        elif isinstance(event, Event_Initialize):
            self.initialize()

    def ctrl_menu(self, event):
        """
        Handles menu events.
        """
        if event.type == pg.KEYDOWN:
            # escape pops the menu
            if event.key == pg.K_ESCAPE:
                self.evManager.Post(Event_StateChange(None))
            # space plays the game
            if event.key == pg.K_SPACE:
                self.evManager.Post(Event_StateChange(model.STATE_PLAY))

    def ctrl_stop(self, event):
        """
        Handles help events.
        """
        if event.type == pg.KEYDOWN:
            # space, enter or escape pops help
            if event.key in [pg.K_ESCAPE, pg.K_SPACE ]:
                self.evManager.Post(Event_StateChange(None))

    def ctrl_play(self, event):
        """
        Handles play events.
        """
        if event.type == pg.KEYDOWN:
            # escape pops the menu
            if event.key == pg.K_ESCAPE:
                self.evManager.Post(Event_StateChange(None))
                self.evManager.Post(Event_Restart())
            # space to stop the game
            elif event.key == pg.K_SPACE:    
                self.evManager.Post(Event_StateChange(model.STATE_STOP))
            # player controler
            for player in self.model.players:
                if player.is_AI:
                    continue
                DirKeys = self.ControlKeys[player.index][0:4]
                if event.key in DirKeys:
                    NowPressedKeys = self.Get_KeyPressIn(DirKeys)
                    DirHashValue = self.Get_DirHashValue(NowPressedKeys, DirKeys)
                    if ctrlConst.DirHash[DirHashValue] != 0:
                        self.evManager.Post(
                            Event_Move( player.index, ctrlConst.DirHash[DirHashValue] )
                        )
        
    def Get_KeyPressIn(self, keylist):
        return [key for key, value in enumerate(pg.key.get_pressed()) if value == 1 and key in keylist]

    def Get_DirHashValue(self, PressList, DirKeyList):
        HashValue = 0
        for index, key in enumerate(DirKeyList):
            if key in PressList:
                HashValue += 2**index
        return HashValue

    def initialize(self):
        """
        # init pygame event and set timer
        # # Document
        # pg.event.Event(event_id)
        # pg.time.set_timer(event_id, TimerDelay)
        """
        pg.time.set_timer(self.SecEventType, 1000)

        NowManualIndex = 0
        for index, AIName in enumerate(self.model.AINames):
            if AIName == "~":
                self.ControlKeys[index] = \
                    ctrlConst.ManualPlayerKeys[NowManualIndex]
                NowManualIndex += 1
