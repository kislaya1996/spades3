from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocket
from sqlalchemy.orm import Session
from app.database import get_db, init_db, check_db_connection
from app.config import settings
from app.services.game_service import GameService
from app.schemas import (
    JoinRoomRequest,
    CreateRoomResponse,
    GameState,
    WebSocketMessage,
    PlayerInfo
)
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global game service instance
game_service = None


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    global game_service
    
    logger.info("Starting Spades3 API...")
    
    # Check database connection
    if not check_db_connection():
        logger.error("Failed to connect to database")
        raise Exception("Database connection failed")
    
    # Initialize database tables
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    # Initialize game service
    try:
        db = next(get_db())
        game_service = GameService(db)
        logger.info("Game service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize game service: {e}")
        raise
    
    logger.info("Spades3 API started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    logger.info("Shutting down Spades3 API...")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Spades3 API is running",
        "version": settings.app_version,
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    db_status = check_db_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "version": settings.app_version
    }


@app.post("/rooms/create", response_model=CreateRoomResponse)
async def create_room(db: Session = Depends(get_db)):
    """Create a new game room"""
    try:
        room_code = game_service.create_room()
        return CreateRoomResponse(room_code=room_code)
    except Exception as e:
        logger.error(f"Failed to create room: {e}")
        raise HTTPException(status_code=500, detail="Failed to create room")


@app.post("/rooms/{room_code}/join")
async def join_room(room_code: str, player: JoinRoomRequest, db: Session = Depends(get_db)):
    """Join an existing game room"""
    try:
        player_id = game_service.join_room(room_code, player.player_name)
        if not player_id:
            raise HTTPException(status_code=404, detail="Room not found")
        return {"player_id": player_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to join room: {e}")
        raise HTTPException(status_code=500, detail="Failed to join room")


@app.get("/rooms/{room_code}/state", response_model=GameState)
async def get_game_state(room_code: str, db: Session = Depends(get_db)):
    """Get current game state for a room"""
    try:
        game_state = game_service.get_game_state(room_code)
        if not game_state:
            raise HTTPException(status_code=404, detail="Room not found")
        return game_state
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get game state: {e}")
        raise HTTPException(status_code=500, detail="Failed to get game state")


@app.websocket("/ws/{room_code}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, room_code: str, player_id: str):
    """WebSocket endpoint for real-time game communication"""
    await websocket.accept()
    
    try:
        # Load game if not in memory
        if room_code not in game_service.active_games:
            game_room = game_service.load_game(room_code)
            if not game_room:
                await websocket.close(code=1000)
                return
        
        # TODO: Implement WebSocket message handling
        # This will be expanded in the next phase with event-driven architecture
        
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            # Process incoming messages here
            
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close(code=1011)