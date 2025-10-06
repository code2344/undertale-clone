#!/usr/bin/python3
from rooms.common import *
from rooms.menus import *
from rooms.tests import *
from typing import *

# Import game room system
try:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from game_room import GameRoom
    HAS_GAME_ROOM = True
except:
    HAS_GAME_ROOM = False


def get_room(room: Union[str,int]):  # Load rooms from JSON data
    """Load a room by name or ID"""
    if isinstance(room, str):
        if HAS_GAME_ROOM:
            return GameRoom(room)
        else:
            return Room_TEST1()
    elif isinstance(room, int):
        # TODO: Map room IDs to names
        if HAS_GAME_ROOM:
            return GameRoom("room_ruins1")
        else:
            return Room_TEST1()
    return Room_TEST1()
