from typing import Union, Dict, Optional, List
from pydantic import BaseModel

class CreateRoomResponse(BaseModel):
    room_code: str

class JoinRoomRequest(BaseModel):
    player_name: str

class JoinRoomResponse(BaseModel):
    player_id: str

class PlayerInfo(BaseModel):
    id: str
    name: str
    is_ready: bool
    card_count: int

class GameState(BaseModel):
    players: List[PlayerInfo]
    current_turn: Optional[str]
    is_game_started: bool
    hand: Optional[List[Dict[str, Union[str, int]]]]

class WebSocketMessage(BaseModel):
    type: str
    data: Optional[Dict] = None 