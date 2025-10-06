#!/usr/bin/env python3
"""
Asset Manager - Handles loading and caching of game assets (sprites, backgrounds, sounds)
"""
import json
import os
from typing import Dict, Optional, List, Tuple
import pygame


class SpriteData:
    """Container for sprite metadata"""
    def __init__(self, sprite_json: Dict):
        self.name = sprite_json.get("name", "")
        self.width = sprite_json.get("width", 0)
        self.height = sprite_json.get("height", 0)
        self.frames = sprite_json.get("frames", [])
        self.bbox = sprite_json.get("bbox", {})
        
class BackgroundData:
    """Container for background metadata"""
    def __init__(self, bg_json: Dict):
        self.name = bg_json.get("name", "")
        self.width = bg_json.get("width", 0)
        self.height = bg_json.get("height", 0)
        

class AssetManager:
    """Manages loading and caching of game assets"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = base_path
        self.sprite_cache: Dict[str, pygame.Surface] = {}
        self.background_cache: Dict[str, pygame.Surface] = {}
        self.sprite_metadata: Dict[str, SpriteData] = {}
        self.background_metadata: Dict[str, BackgroundData] = {}
        
        # Paths
        self.sprite_dir = os.path.join(base_path, "sprites")
        self.bg_dir = os.path.join(base_path, "decompilation", "bg")
        self.texpage_dir = os.path.join(base_path, "decompilation", "texpage")
        self.decompilation_sprite_dir = os.path.join(base_path, "decompilation", "sprite")
        
    def load_sprite_metadata(self, sprite_name: str) -> Optional[SpriteData]:
        """Load sprite metadata from JSON"""
        if sprite_name in self.sprite_metadata:
            return self.sprite_metadata[sprite_name]
            
        json_path = os.path.join(self.decompilation_sprite_dir, f"{sprite_name}.json")
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r') as f:
                    data = SpriteData(json.load(f))
                    self.sprite_metadata[sprite_name] = data
                    return data
            except:
                pass
        return None
    
    def load_sprite(self, sprite_name: str, frame: int = 0) -> Optional[pygame.Surface]:
        """Load a sprite image"""
        cache_key = f"{sprite_name}_{frame}"
        
        if cache_key in self.sprite_cache:
            return self.sprite_cache[cache_key]
        
        # Try loading from sprites directory (PNG files)
        sprite_file = os.path.join(self.sprite_dir, f"{sprite_name}_{frame}.png")
        
        if os.path.exists(sprite_file):
            try:
                surface = pygame.image.load(sprite_file)
                self.sprite_cache[cache_key] = surface
                return surface
            except Exception as e:
                print(f"Error loading sprite {sprite_name}: {e}")
        
        return None
    
    def load_background(self, bg_name: str) -> Optional[pygame.Surface]:
        """Load a background image"""
        if bg_name in self.background_cache:
            return self.background_cache[bg_name]
        
        # Try different file patterns
        for pattern in [f"{bg_name}.png", f"{bg_name}_0.png"]:
            bg_file = os.path.join(self.sprite_dir, pattern)
            if os.path.exists(bg_file):
                try:
                    surface = pygame.image.load(bg_file)
                    self.background_cache[bg_name] = surface
                    return surface
                except:
                    pass
        
        # Try texpage directory
        for filename in os.listdir(self.texpage_dir) if os.path.exists(self.texpage_dir) else []:
            if bg_name.lower() in filename.lower():
                bg_file = os.path.join(self.texpage_dir, filename)
                try:
                    surface = pygame.image.load(bg_file)
                    self.background_cache[bg_name] = surface
                    return surface
                except:
                    pass
        
        return None
    
    def create_placeholder_surface(self, width: int, height: int, color: Tuple[int, int, int] = (128, 0, 128)) -> pygame.Surface:
        """Create a placeholder surface when asset is missing"""
        surface = pygame.Surface((width, height))
        surface.fill(color)
        return surface


# Global instance
_asset_manager = None

def get_asset_manager() -> AssetManager:
    """Get or create the global asset manager"""
    global _asset_manager
    if _asset_manager is None:
        _asset_manager = AssetManager()
    return _asset_manager


if __name__ == "__main__":
    pygame.init()
    manager = AssetManager()
    
    # Test loading some sprites
    test_sprites = ["spr_maincharad", "spr_heart", "spr_savepoint"]
    for sprite_name in test_sprites:
        sprite = manager.load_sprite(sprite_name, 0)
        if sprite:
            print(f"✓ Loaded {sprite_name}: {sprite.get_size()}")
        else:
            print(f"✗ Failed to load {sprite_name}")
    
    # Test loading backgrounds
    test_bgs = ["bg_ruinsplaceholder", "bg_ruins"]
    for bg_name in test_bgs:
        bg = manager.load_background(bg_name)
        if bg:
            print(f"✓ Loaded background {bg_name}: {bg.get_size()}")
        else:
            print(f"✗ Failed to load background {bg_name}")
