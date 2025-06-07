from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class GameRoomDB(Base):
    __tablename__ = "game_rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_code = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_game_started = Column(Boolean, default=False)
    current_turn = Column(String, nullable=True)
    
    # Relationships
    players = relationship("PlayerDB", back_populates="game_room")

class PlayerDB(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, unique=True, index=True)
    name = Column(String)
    is_ready = Column(Boolean, default=False)
    game_room_id = Column(Integer, ForeignKey("game_rooms.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    game_room = relationship("GameRoomDB", back_populates="players") 