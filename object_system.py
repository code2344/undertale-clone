#!/usr/bin/env python3
"""
Object System - Handles game object behavior, interactions, and collisions
"""
import pygame
from typing import Optional, Dict, List, Callable
from asset_manager import get_asset_manager


class GameObjectBehavior:
    """Base class for object behaviors"""
    def __init__(self, game_object):
        self.obj = game_object
        
    def update(self, delta_time: float):
        """Update behavior"""
        pass
    
    def on_interact(self, player):
        """Called when player interacts"""
        pass


class SavePointBehavior(GameObjectBehavior):
    """Behavior for save points"""
    def on_interact(self, player):
        """Open save menu"""
        import popup
        import globals
        
        if not globals.event_lock:
            globals.event_lock = True
            save_popup = popup.SAVEPopup()
            
            # Wait for save popup to finish
            import input as inp
            while not save_popup.finished:
                key = inp.get_single_menu_interaction()
                save_popup.on_button(key)
                save_popup.update()
                pygame.time.wait(100)
            
            globals.event_lock = False


class DoorBehavior(GameObjectBehavior):
    """Behavior for doors/room transitions"""
    def __init__(self, game_object, target_room: str = None, target_marker: str = "A"):
        super().__init__(game_object)
        self.target_room = target_room
        self.target_marker = target_marker
    
    def on_interact(self, player):
        """Transition to target room"""
        if self.target_room:
            import globals
            import rooms
            
            # Load target room
            target = rooms.get_room(self.target_room)
            if target:
                globals.chara.go_to_room(target)


# Map object types to behaviors
OBJECT_BEHAVIORS: Dict[str, Callable] = {
    "obj_savepoint": SavePointBehavior,
    "obj_doorA": lambda obj: DoorBehavior(obj, target_room="room_ruins2", target_marker="B"),
    "obj_doorB": lambda obj: DoorBehavior(obj, target_room="room_ruins1", target_marker="A"),
}


def get_behavior_for_object(game_object) -> Optional[GameObjectBehavior]:
    """Get the appropriate behavior for a game object"""
    obj_type = game_object.obj_name
    
    if obj_type in OBJECT_BEHAVIORS:
        behavior_factory = OBJECT_BEHAVIORS[obj_type]
        if callable(behavior_factory):
            return behavior_factory(game_object)
    
    return None


class InteractiveGameObject:
    """Extended GameObject with behavior and interaction support"""
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
        self.collidable = self._is_collidable()
        self.interactable = self._is_interactable()
        
        # Behavior system
        self.behavior = get_behavior_for_object(self)
        
        # Load sprite
        self._load_sprite()
        
        # Collision rectangle
        if self.surface:
            self.rect = pygame.Rect(self.x, self.y, self.surface.get_width(), self.surface.get_height())
        else:
            self.rect = pygame.Rect(self.x, self.y, 20, 20)  # Default size
    
    def _is_collidable(self) -> bool:
        """Check if this object blocks movement"""
        return any(keyword in self.obj_name.lower() for keyword in 
                   ['solid', 'wall', 'block', 'collision'])
    
    def _is_interactable(self) -> bool:
        """Check if this object can be interacted with"""
        return any(keyword in self.obj_name.lower() for keyword in
                   ['save', 'door', 'sign', 'npc', 'item', 'chest'])
    
    def _load_sprite(self):
        """Load sprite for this object"""
        # Map object names to sprite names
        obj_to_sprite = {
            "obj_mainchara": "spr_maincharad",
            "obj_savepoint": "spr_savepoint",
            "obj_marker": None,
            "obj_markerA": None,
            "obj_markerB": None,
            "obj_markerX": None,
            "obj_doorA": "spr_doorA",
            "obj_doorB": "spr_doorA",
            "obj_doorBmusicfade": "spr_doorA",
            "obj_solidtall": None,
            "obj_solidsmall": None,
            "obj_solidlong": None,
            "obj_solidtall_2": None,
        }
        
        sprite_name = obj_to_sprite.get(self.obj_name)
        if sprite_name:
            self.surface = self.asset_manager.load_sprite(sprite_name, 0)
        elif "solid" not in self.obj_name.lower() and "marker" not in self.obj_name.lower():
            # Try loading sprite with same name as object
            sprite_name = self.obj_name.replace("obj_", "spr_")
            self.surface = self.asset_manager.load_sprite(sprite_name, 0)
    
    def update(self, delta_time: float):
        """Update object behavior"""
        if self.behavior:
            self.behavior.update(delta_time)
    
    def interact(self, player):
        """Handle interaction"""
        if self.behavior:
            self.behavior.on_interact(player)
    
    def check_collision(self, rect: pygame.Rect) -> bool:
        """Check if given rect collides with this object"""
        if not self.collidable:
            return False
        return self.rect.colliderect(rect)
    
    def draw(self, target_surface: pygame.Surface, camera_offset: tuple = (0, 0)):
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


if __name__ == "__main__":
    # Test object system
    import pygame
    pygame.init()
    
    asset_mgr = get_asset_manager()
    
    # Test creating a save point
    save_data = {
        "pos": {"x": 100, "y": 200},
        "obj": "obj_savepoint",
        "instanceid": 1
    }
    
    save_obj = InteractiveGameObject(save_data, asset_mgr)
    print(f"Created save point:")
    print(f"  Position: ({save_obj.x}, {save_obj.y})")
    print(f"  Interactable: {save_obj.interactable}")
    print(f"  Collidable: {save_obj.collidable}")
    print(f"  Has behavior: {save_obj.behavior is not None}")
