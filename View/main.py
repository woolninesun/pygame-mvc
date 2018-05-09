import pygame as pg

import Model.main as model
from Events.Manager import *

import Model.const       as modelConst
import View.const        as viewConst
import Controller.const  as ctrlConst
import Interface.const   as IfaConst

class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """
    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model

        self.is_initialized = False
        self.screen = None
        self.clock = None
        self.smallfont = None

        self.last_update = 0
    
    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, Event_EveryTick) \
           and self.is_initialized:
            cur_state = self.model.state.peek()
            if cur_state == model.STATE_MENU:
                self.render_menu()
            if cur_state == model.STATE_PLAY:
                self.render_play()
            if cur_state == model.STATE_STOP:
                self.render_stop()

            self.display_fps()
            # limit the redraw speed to 30 frames per second
            self.clock.tick(viewConst.FramePerSec)
        elif isinstance(event, Event_Quit):
            # shut down the pygame graphics
            self.is_initialized = False
            pg.quit()
        elif isinstance(event, Event_Initialize) or\
             isinstance(event, Event_Restart):
            self.initialize()
    
    def render_menu(self):
        """
        Render the game menu.
        """
        if self.last_update != model.STATE_MENU:
            self.last_update = model.STATE_MENU

            # draw backgound
            self.screen.fill(viewConst.Color_Black)
            # write some word
            somewords = self.smallfont.render(
                        'You are in the Menu. Space to play. Esc exits.', 
                        True, (0, 255, 0))
            (SurfaceX, SurfaceY) = somewords.get_size()
            pos_x = (viewConst.ScreenSize[0] - SurfaceX)/2
            pos_y = (viewConst.ScreenSize[1] - SurfaceY)/2
            self.screen.blit(somewords, (pos_x, pos_y))
            # update surface
            pg.display.flip()
        
    def render_play(self):
        """
        Render the game play.
        """
        if self.last_update != model.STATE_PLAY:
            self.last_update = model.STATE_PLAY
        # draw backgound
        self.screen.fill(viewConst.Color_White)

        for player in self.model.players:
            pos = ( int(player.pos[0]), int(player.pos[1]) )
            pg.draw.circle( self.screen, player.color, pos, 20 )

        # update surface
        pg.display.flip()
        
    def render_stop(self):
        """
        Render the stop screen.
        """
        if self.last_update != model.STATE_STOP:
            self.last_update = model.STATE_STOP

            # draw backgound
            s = pg.Surface(viewConst.ScreenSize, pg.SRCALPHA)
            s.fill((0, 0, 0, 128)); self.screen.blit(s, (0,0))

            # write some word
            somewords = self.smallfont.render(
                        'stop the game. space, escape to return the game.', 
                        True, (0, 255, 0))
            (SurfaceX, SurfaceY) = somewords.get_size()
            pos_x = (viewConst.ScreenSize[0] - SurfaceX)/2
            pos_y = (viewConst.ScreenSize[1] - SurfaceY)/2
            self.screen.blit(somewords, (pos_x, pos_y))

            # update surface
            pg.display.flip()

    def display_fps(self):
        """Show the programs FPS in the window handle."""
        caption = "{} - FPS: {:.2f}".format(
            viewConst.GameCaption, self.clock.get_fps()
        )
        pg.display.set_caption(caption)
        
    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """
        pg.init(); pg.font.init()
        pg.display.set_caption(viewConst.GameCaption)
        self.screen = pg.display.set_mode(viewConst.ScreenSize)
        self.clock = pg.time.Clock()
        self.smallfont = pg.font.Font(None, 40)
        self.is_initialized = True
