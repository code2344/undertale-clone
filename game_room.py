#!/usr/bin/env python3
"""
Game Room - Complete room implementation that loads from JSON
"""
import pygame
from typing import Optional, List, Tuple
import os

from room_loader import RoomData, get_room_loader
from asset_manager import get_asset_manager
from object_system import InteractiveGameObject
import globals
from rooms.common import Room


class GameRoom(Room):
    """A room loaded from JSON decompilation data"""
    
    def __init__(self, room_name: str):
        super().__init__()
        self.room_name = room_name
        self.room_loader = get_room_loader()
        self.asset_manager = get_asset_manager()
        self.room_data: Optional[RoomData] = None
        self.game_objects: List[InteractiveGameObject] = []
        self.tile_surface: Optional[pygame.Surface] = None
        self.bg_surfaces: List[pygame.Surface] = []
        self.is_walkable = True
        
        # Load the room
        self._load_room()
    
    def _load_room(self):
        """Load room data and assets"""
        self.room_data = self.room_loader.load_room(self.room_name)
        
        if not self.room_data:
            print(f"Failed to load room: {self.room_name}")
            return
        
        # Set up room properties
        self.name = self.room_data.caption or self.room_name
        self.id = hash(self.room_name) % 10000
        
        # Create background surface
        self.background = pygame.Surface((self.room_data.width, self.room_data.height))
        self.background.fill(self.room_data.get_background_color())
        
        # Load backgrounds
        self._load_backgrounds()
        
        # Load tiles
        self._load_tiles()
        
        # Load objects
        self._load_objects()
    
    def _load_backgrounds(self):
        """Load background layers"""
        for bg_data in self.room_data.backgrounds:
            if not bg_data.get("enabled", False):
                continue
            
            bg_name = bg_data.get("bg", "")
            if bg_name:
                bg_surface = self.asset_manager.load_background(bg_name)
                if bg_surface:
                    self.bg_surfaces.append(bg_surface)
    
    def _load_tiles(self):
        """Render tiles to a surface"""
        if not self.room_data.tiles:
            return
        
        self.tile_surface = pygame.Surface((self.room_data.width, self.room_data.height), pygame.SRCALPHA)
        
        for tile_data in self.room_data.tiles:
            bg_name = tile_data.get("bg", "")
            pos = tile_data.get("pos", {})
            x = pos.get("x", 0)
            y = pos.get("y", 0)
            size = tile_data.get("size", {})
            width = size.get("width", 20)
            height = size.get("height", 20)
            source_pos = tile_data.get("sourcepos", {})
            src_x = source_pos.get("x", 0)
            src_y = source_pos.get("y", 0)
            
            # Load the background tile source
            bg_surface = self.asset_manager.load_background(bg_name)
            if bg_surface:
                try:
                    # Extract the tile region
                    tile_rect = pygame.Rect(src_x, src_y, width, height)
                    tile = bg_surface.subsurface(tile_rect).copy()
                    self.tile_surface.blit(tile, (x, y))
                except:
                    # If extraction fails, use placeholder
                    pass
    
    def _load_objects(self):
        """Load game objects"""
        for obj_data in self.room_data.objects:
            game_obj = InteractiveGameObject(obj_data, self.asset_manager)
            self.game_objects.append(game_obj)
    
    def get_nearby_objects(self, x: int, y: int, radius: int = 50) -> List[InteractiveGameObject]:
        """Get objects near a position"""
        nearby = []
        for obj in self.game_objects:
            dist = ((obj.x - x) ** 2 + (obj.y - y) ** 2) ** 0.5
            if dist < radius:
                nearby.append(obj)
        return nearby
    
    def check_collision(self, rect: pygame.Rect) -> bool:
        """Check if rect collides with any collidable object"""
        for obj in self.game_objects:
            if obj.check_collision(rect):
                return True
        return False
    
    def on_enter(self):
        """Called when entering the room"""
        if super().on_enter():
            # Set caption
            if self.room_data:
                pygame.display.set_caption(f'UNDERTALE - {self.name}')
            
            # Try to load ruins music
            try:
                pygame.mixer.music.load("mus/mus_ruins.ogg")
                pygame.mixer.music.play(-1)
            except:
                pass
            
            return True
        return False
    
    def draw(self):
        """Draw the room"""
        super().draw()
        
        if not self.room_data:
            return
        
        # Draw to background layer
        self.background_layer.surface.fill(self.room_data.get_background_color())
        
        # Draw background layers
        for bg_surface in self.bg_surfaces:
            self.background_layer.surface.blit(bg_surface, (0, 0))
        
        # Draw tiles
        if self.tile_surface:
            self.background_layer.surface.blit(self.tile_surface, (0, 0))
        
        self.background_layer.flip()
        
        # Draw objects (non-player)
        for obj in self.game_objects:
            if obj.obj_name != "obj_mainchara":
                obj.draw(self.background_layer.surface)
        
        self.background_layer.flip()


class WalkableGameRoom(GameRoom):
    """A walkable game room with collision detection and character control"""
    
    def __init__(self, room_name: str):
        super().__init__(room_name)
        self.clock = pygame.time.Clock()
        self.chara = globals.chara
        self.chara_layer = None
        
        if hasattr(self, 'room_data') and self.room_data:
            import draw
            self.chara_layer = draw.get_layer(128)
            self.walk_animate_init()
            self.walk_tick = 0
    
    def walk_animate_init(self):
        """Initialize walk animation"""
        scale_factor = 2
        
        def scale(img, times):
            return pygame.transform.scale(img, (int(img.get_width() * times), int(img.get_height() * times)))
        
        self.upcycle = [scale(pygame.image.load("sprites/spr_maincharau_" + str(i) + ".png"), scale_factor) for i in range(4)]
        self.down_cycle = [scale(pygame.image.load("sprites/spr_maincharad_" + str(i) + ".png"), scale_factor) for i in range(4)]
        self.left_cycle = [scale(pygame.image.load("sprites/spr_maincharal_" + str(i) + ".png"), scale_factor) for i in range(2)]
        self.right_cycle = [scale(pygame.image.load("sprites/spr_maincharar_" + str(i) + ".png"), scale_factor) for i in range(2)]
    
    def walk_animate_loop(self):
        """Update walk animation"""
        chara = self.chara
        chara.sprite = [self.upcycle, self.right_cycle, self.down_cycle, self.left_cycle][chara.dir][0]
        if chara.moving:
            self.walk_tick += 1
            if self.walk_tick % 10 == 0:
                for i in [self.upcycle, self.right_cycle, self.down_cycle, self.left_cycle][chara.dir]:
                    chara.sprite = i
    
    def draw(self):
        """Draw walkable room with character"""
        super().draw()
        
        if not self.chara_layer:
            return
        
        chara = self.chara
        self.walk_animate_loop()
        self.chara_layer.clear()
        self.chara_layer.surface.blit(chara.sprite, (int(chara.pos[0]), int(chara.pos[1])))
        self.chara_layer.flip()
        
        # Handle input
        if not globals.event_lock:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    globals.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        globals.quit()
                    if event.key in globals.accept:
                        nearby = self.get_nearby_objects(chara.x, chara.y, 50)
                        for obj in nearby:
                            if obj.interactable:
                                obj.interact(chara)
                                break
            
            keys_pressed = pygame.key.get_pressed()
            chara.moving = False
            old_pos = chara.pos
            
            if keys_pressed[globals.left]:
                chara.dir = 3
                chara.moving = True
                chara.pos = (chara.pos[0] - chara.movespeed, chara.pos[1])
            if keys_pressed[globals.right]:
                chara.dir = 1
                chara.moving = True
                chara.pos = (chara.pos[0] + chara.movespeed, chara.pos[1])
            if keys_pressed[globals.up]:
                chara.dir = 0
                chara.moving = True
                chara.pos = (chara.pos[0], chara.pos[1] - chara.movespeed)
            if keys_pressed[globals.down]:
                chara.dir = 2
                chara.moving = True
                chara.pos = (chara.pos[0], chara.pos[1] + chara.movespeed)
            
            # Check collision and revert if needed
            if chara.moving:
                chara_rect = pygame.Rect(chara.x, chara.y, 19, 29)
                if self.check_collision(chara_rect):
                    chara.pos = old_pos
        
        self.clock.tick(30)
        # Clamp position to room bounds
        if self.room_data:
            chara.pos = (
                max(0, min(chara.pos[0], self.room_data.width - 20)),
                max(0, min(chara.pos[1], self.room_data.height - 20))
            )


if __name__ == "__main__":
    # Test
    pygame.init()
    pygame.display.set_mode((640, 480))
    
    room = WalkableGameRoom("room_ruins1")
    print(f"Created walkable room: {room.name}")
    print(f"  Objects: {len(room.game_objects)}")
    print(f"  Interactable objects: {sum(1 for obj in room.game_objects if obj.interactable)}")
