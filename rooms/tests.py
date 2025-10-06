#!/usr/bin/python3
# coding=utf-8
import pygame
import objects
import globals
from rooms.common import Room, RoomWalkable


class Room_TEST1(RoomWalkable):
    def __init__(self):
        RoomWalkable.__init__(self)
        self.name = 'Test Room 1'
        self._display_ = pygame.display.get_surface()
        self.objects = [objects.RaiseException((100, 100)), objects.SAVEPoint((200, 200)),
                        objects.TestTextBoxObject((300, 300))]


class Room_TEST2(RoomWalkable):
    def __init__(self):
        RoomWalkable.__init__(self)
        self.name = 'Test Room 2'
        self.background.fill(pygame.Color(127, 127, 127, 255))
        self._display_ = pygame.display.get_surface()
        self.objects = [objects.RaiseException((100, 100))]


class Room_Unwalkable_Test(Room):
    def __init__(self):
        Room.__init__(self)
        self.id = 0
        self.background = pygame.Surface((800, 600))
        self.bg_pan = (0, 0)
        self.objects = []
        self.song = None
        self._display_ = globals.display
        self.objects = [objects.TestMovingObject((200, 200))]
        self.fade_phase = 0
        self.fade_direction = 1

    def update_loop(self):
        self.fade_phase = 0
        self.fade_direction = 1
        while self.run_update:
            self.fade_phase += self.fade_direction
            if self.fade_phase >= 255:
                self.fade_direction = -1
            elif self.fade_phase <= 0:
                self.fade_direction = 1
            self.background.fill(pygame.Color(self.fade_phase, abs(self.fade_phase - 127), 255 - self.fade_phase))


class Room_Ruins_Start(RoomWalkable):
    """The starting area of the Ruins."""
    def __init__(self):
        RoomWalkable.__init__(self)
        self.name = 'Ruins - Start'
        self.id = 10
        # Create a simple purple background to represent the Ruins
        self.background.fill(pygame.Color(80, 50, 100, 255))
        self._display_ = pygame.display.get_surface()
        # Add a SAVE point in the center
        self.objects = [objects.SAVEPoint((300, 240))]
        self.menu_open = False
        
    def on_enter(self):
        if super().on_enter():
            # Play Ruins music
            try:
                pygame.mixer.music.load("mus/mus_ruins.ogg")
                pygame.mixer.music.play(-1)
            except:
                pass
            pygame.display.set_caption('UNDERTALE - Ruins')
            return True
        return False
    
    def draw(self):
        """Override draw to handle menu key"""
        import input as inp
        import popup
        import font
        
        # First call parent draw
        super().draw()
        
        # Check for menu key (C/Ctrl)
        if not globals.event_lock:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_c] or keys_pressed[pygame.K_LCTRL] or keys_pressed[pygame.K_RCTRL]:
                if not self.menu_open:
                    self.menu_open = True
                    self.show_menu()
        
    def show_menu(self):
        """Display a simple game menu"""
        import font
        import draw
        
        # Create menu overlay
        menu_layer = draw.get_layer(128)
        menu_surface = pygame.Surface((320, 240))
        menu_surface.fill(pygame.Color(0, 0, 0))
        pygame.draw.rect(menu_surface, pygame.Color(255, 255, 255), menu_surface.get_rect(), 4)
        
        # Draw menu text
        chara = globals.chara
        name_text = font.render(chara.charname, color=pygame.Color(255, 255, 255))
        lv_text = font.render('LV ' + str(chara.lv), color=pygame.Color(255, 255, 255))
        hp_text = font.render('HP ' + str(chara.hp) + '/' + str(chara.maxhp), color=pygame.Color(255, 255, 255))
        gold_text = font.render('G ' + str(chara.gold), color=pygame.Color(255, 255, 255))
        
        menu_surface.blit(name_text, (20, 20))
        menu_surface.blit(lv_text, (20, 50))
        menu_surface.blit(hp_text, (20, 80))
        menu_surface.blit(gold_text, (20, 110))
        
        # Blit to layer
        menu_layer.surface.blit(menu_surface, (160, 120))
        menu_layer.flip()
        
        # Wait a bit then close
        pygame.time.wait(2000)
        menu_layer.clear()
        menu_layer.flip()
        self.menu_open = False
