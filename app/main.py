from typing import Union, Dict, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import uuid

from models.game_room import GameRoom
from models.card import Card

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active game rooms
game_rooms: Dict[str, GameRoom] = {}

# Store active WebSocket connections
active_connections: Dict[str, Dict[str, WebSocket]] = {}

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/rooms/create")
async def create_room():
    """Create a new game room."""
    room_code = GameRoom.generate_room_code()
    game_rooms[room_code] = GameRoom(room_code)
    active_connections[room_code] = {}
    return {"room_code": room_code}

@app.post("/rooms/{room_code}/join")
async def join_room(room_code: str, player_name: str):
    """Join an existing game room."""
    if room_code not in game_rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    
    player_id = str(uuid.uuid4())
    if game_rooms[room_code].add_player(player_id, player_name):
        return {"player_id": player_id}
    raise HTTPException(status_code=400, detail="Could not join room")

@app.websocket("/ws/{room_code}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, room_code: str, player_id: str):
    """WebSocket endpoint for real-time game updates."""
    if room_code not in game_rooms:
        await websocket.close(code=1000)
        return
    
    await websocket.accept()
    active_connections[room_code][player_id] = websocket
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message["type"] == "ready":
                game_rooms[room_code].players[player_id].is_ready = True
                await broadcast_game_state(room_code)
            
            elif message["type"] == "play_card":
                if game_rooms[room_code].is_player_turn(player_id):
                    # Handle card play logic here
                    await broadcast_game_state(room_code)
            
            elif message["type"] == "start_game":
                if game_rooms[room_code].start_game():
                    await broadcast_game_state(room_code)
    
    except WebSocketDisconnect:
        if room_code in active_connections:
            del active_connections[room_code][player_id]
        if room_code in game_rooms:
            game_rooms[room_code].remove_player(player_id)
            await broadcast_game_state(room_code)

async def broadcast_game_state(room_code: str):
    """Broadcast the current game state to all players in the room."""
    if room_code not in active_connections:
        return
    
    game_state = {
        "players": [
            {
                "id": player.id,
                "name": player.name,
                "is_ready": player.is_ready,
                "card_count": len(player.hand)
            }
            for player in game_rooms[room_code].players.values()
        ],
        "current_turn": game_rooms[room_code].current_turn,
        "is_game_started": game_rooms[room_code].is_game_started
    }
    
    for player_id, connection in active_connections[room_code].items():
        try:
            # Include player's hand only for that player
            player_state = game_state.copy()
            if player_id in game_rooms[room_code].players:
                player_state["hand"] = [
                    {"suit": card.suit.value, "value": card.value}
                    for card in game_rooms[room_code].get_player_hand(player_id)
                ]
            await connection.send_json(player_state)
        except:
            continue