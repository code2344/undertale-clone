#!/usr/bin/env python3
"""
Game Room - Complete room implementation that loads from JSON
"""
import pygame
from typing import Optional, List, Tuple
import os

from room_loader import RoomData, get_room_loader
from asset_manager import get_asset_manager
import globals
from rooms.common import Room


class GameObject:
    """Represents a game object in a room"""
    def __init__(self, obj_data: dict, asset_manager):
        self.x = obj_data.get("pos", {}).get("x", 0)
        self.y = obj_data.get("pos", {}).get("y", 0)
        self.obj_name = obj_data.get("obj", "")
        self.instance_id = obj_data.get("instanceid", 0)
        self.scale_x = obj_data.get("scale", {}).get("x", 1.0)
        self.scale_y = obj_data.get("scale", {}).get("y", 1.0)
        self.rotation = obj_data.get("rotation", 0.0)
        self.asset_manager = asset_manager
        self.surface = None
        self.visible = True
        
        # Try to load sprite for this object
        self._load_sprite()
    
    def _load_sprite(self):
        """Attempt to load sprite for this object"""
        # Map object names to sprite names (simplified)
        obj_to_sprite = {
            "obj_mainchara": "spr_maincharad",
            "obj_savepoint": "spr_savepoint",
            "obj_marker": None,  # Invisible markers
            "obj_door": "spr_doorA",
            "obj_solidtall": None,  # Collision objects
            "obj_solidsmall": None,
            "obj_solidlong": None,
        }
        
        sprite_name = obj_to_sprite.get(self.obj_name)
        if sprite_name:
            self.surface = self.asset_manager.load_sprite(sprite_name, 0)
        elif "solid" not in self.obj_name.lower() and "marker" not in self.obj_name.lower():
            # Try loading sprite with same name as object
            sprite_name = self.obj_name.replace("obj_", "spr_")
            self.surface = self.asset_manager.load_sprite(sprite_name, 0)
    
    def draw(self, target_surface: pygame.Surface, camera_offset: Tuple[int, int] = (0, 0)):
        """Draw this object"""
        if not self.visible or not self.surface:
            return
        
        draw_x = self.x - camera_offset[0]
        draw_y = self.y - camera_offset[1]
        
        if self.scale_x != 1.0 or self.scale_y != 1.0:
            w = int(self.surface.get_width() * self.scale_x)
            h = int(self.surface.get_height() * self.scale_y)
            scaled = pygame.transform.scale(self.surface, (w, h))
            target_surface.blit(scaled, (draw_x, draw_y))
        else:
            target_surface.blit(self.surface, (draw_x, draw_y))


class GameRoom(Room):
    """A room loaded from JSON decompilation data"""
    
    def __init__(self, room_name: str):
        super().__init__()
        self.room_name = room_name
        self.room_loader = get_room_loader()
        self.asset_manager = get_asset_manager()
        self.room_data: Optional[RoomData] = None
        self.game_objects: List[GameObject] = []
        self.tile_surface: Optional[pygame.Surface] = None
        self.bg_surfaces: List[pygame.Surface] = []
        
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
                    # If extraction fails, create placeholder
                    pygame.draw.rect(self.tile_surface, (100, 100, 100), (x, y, width, height))
    
    def _load_objects(self):
        """Load game objects"""
        for obj_data in self.room_data.objects:
            game_obj = GameObject(obj_data, self.asset_manager)
            self.game_objects.append(game_obj)
    
    def on_enter(self):
        """Called when entering the room"""
        if super().on_enter():
            # Set caption
            if self.room_data:
                pygame.display.set_caption(f'UNDERTALE - {self.name}')
            
            # Load music if specified
            # TODO: Implement music loading from room data
            
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
        
        # Draw objects (non-player objects)
        for obj in self.game_objects:
            # Skip player character object - it's handled separately
            if obj.obj_name != "obj_mainchara":
                obj.draw(self.background_layer.surface)
        
        self.background_layer.flip()


if __name__ == "__main__":
    # Test loading a room
    pygame.init()
    pygame.display.set_mode((640, 480))
    
    room = GameRoom("room_ruins1")
    print(f"Loaded room: {room.name}")
    print(f"  Dimensions: {room.room_data.width}x{room.room_data.height}")
    print(f"  Objects: {len(room.game_objects)}")
    print(f"  Backgrounds: {len(room.bg_surfaces)}")
    print(f"  Has tiles: {room.tile_surface is not None}")
