from fastapi import FastAPI, Depends, HTTPException
from fastapi.websockets import WebSocket
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.game_service import GameService
from app.schemas import (
    JoinRoomRequest,
    CreateRoomResponse,
    GameState,
    WebSocketMessage,
    PlayerInfo
)
app = FastAPI()

# Create a single GameService instance
game_service = None

@app.on_event("startup")
async def startup_event():
    global game_service
    db = next(get_db())
    game_service = GameService(db)

@app.post("/rooms/create")
async def create_room(db: Session = Depends(get_db)):
    room_code = game_service.create_room()
    return {"room_code": room_code}

@app.post("/rooms/{room_code}/join")
async def join_room(room_code: str, player: JoinRoomRequest, db: Session = Depends(get_db)):
    player_id = game_service.join_room(room_code, player.player_name)
    if not player_id:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"player_id": player_id}

@app.websocket("/ws/{room_code}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, room_code: str, player_id: str):
    # Load game if not in memory
    if room_code not in game_service.active_games:
        game_room = game_service.load_game(room_code)
        if not game_room:
            await websocket.close(code=1000)
            return

    # Rest of your WebSocket logic...
    # After any game state changes, call:
    game_service.update_game_state(room_code)