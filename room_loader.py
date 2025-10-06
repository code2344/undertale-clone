#!/usr/bin/env python3
"""
Room Loader - Loads and parses room data from decompilation JSON files
"""
import json
import os
from typing import Dict, List, Any, Optional
import pygame


class RoomData:
    """Container for parsed room data"""
    def __init__(self, room_json: Dict[str, Any]):
        self.json = room_json
        self.caption = room_json.get("caption", "")
        self.width = room_json.get("size", {}).get("width", 640)
        self.height = room_json.get("size", {}).get("height", 480)
        self.speed = room_json.get("speed", 30)
        self.colour = room_json.get("colour", "#000000FF")
        self.backgrounds = room_json.get("bgs", [])
        self.views = room_json.get("views", [])
        self.objects = room_json.get("objs", [])
        self.tiles = room_json.get("tiles", [])
        
    def get_background_color(self) -> pygame.Color:
        """Parse hex color string to pygame Color"""
        try:
            hex_color = self.colour.replace("#", "")
            if len(hex_color) == 8:  # RGBA
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                a = int(hex_color[6:8], 16)
                return pygame.Color(r, g, b, a)
            elif len(hex_color) == 6:  # RGB
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                return pygame.Color(r, g, b)
        except:
            return pygame.Color(0, 0, 0)
        return pygame.Color(0, 0, 0)


class RoomLoader:
    """Loads room data from JSON files"""
    
    def __init__(self, decompilation_path: str = "decompilation"):
        self.decompilation_path = decompilation_path
        self.room_path = os.path.join(decompilation_path, "room")
        self._cache: Dict[str, RoomData] = {}
        
    def list_rooms(self) -> List[str]:
        """List all available room files"""
        if not os.path.exists(self.room_path):
            return []
        
        rooms = []
        for filename in os.listdir(self.room_path):
            if filename.endswith(".json"):
                room_name = filename.replace(".json", "")
                rooms.append(room_name)
        return sorted(rooms)
    
    def load_room(self, room_name: str) -> Optional[RoomData]:
        """Load a room by name"""
        # Check cache first
        if room_name in self._cache:
            return self._cache[room_name]
        
        # Build file path
        room_file = os.path.join(self.room_path, f"{room_name}.json")
        
        if not os.path.exists(room_file):
            print(f"Warning: Room file not found: {room_file}")
            return None
        
        try:
            with open(room_file, 'r') as f:
                room_json = json.load(f)
            
            room_data = RoomData(room_json)
            self._cache[room_name] = room_data
            return room_data
            
        except Exception as e:
            print(f"Error loading room {room_name}: {e}")
            return None
    
    def get_ruins_rooms(self) -> List[str]:
        """Get all Ruins-related rooms"""
        all_rooms = self.list_rooms()
        return [r for r in all_rooms if 'ruins' in r.lower()]


# Global instance
_room_loader = None

def get_room_loader() -> RoomLoader:
    """Get or create the global room loader instance"""
    global _room_loader
    if _room_loader is None:
        _room_loader = RoomLoader()
    return _room_loader


if __name__ == "__main__":
    # Test the loader
    loader = RoomLoader()
    print(f"Total rooms available: {len(loader.list_rooms())}")
    
    ruins_rooms = loader.get_ruins_rooms()
    print(f"\nRuins rooms ({len(ruins_rooms)}):")
    for room in ruins_rooms[:10]:
        print(f"  - {room}")
    
    # Try loading room_ruins1
    room1 = loader.load_room("room_ruins1")
    if room1:
        print(f"\nLoaded room_ruins1:")
        print(f"  Size: {room1.width}x{room1.height}")
        print(f"  Objects: {len(room1.objects)}")
        print(f"  Tiles: {len(room1.tiles)}")
        print(f"  Backgrounds: {len(room1.backgrounds)}")
