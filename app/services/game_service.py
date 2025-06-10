from typing import Optional, Dict
from sqlalchemy.orm import Session
import uuid
from app.models.game_room import GameRoom
from app.dao.game_dao import GameRoomDAO, PlayerDAO
from app.mappers.game_mapper import GameMapper

class GameService:
    def __init__(self, db: Session):
        self.db = db
        self.game_room_dao = GameRoomDAO(db)
        self.player_dao = PlayerDAO(db)
        self.active_games: Dict[str, GameRoom] = {}

    def create_room(self) -> str:
        # Generate room code
        room_code = GameRoom.generate_room_code()
        
        # Create in database
        db_room = self.game_room_dao.create_room(room_code)
        
        # Create in-memory game
        game_room = GameRoom(room_code=room_code)
        self.active_games[room_code] = game_room
        
        return room_code

    def join_room(self, room_code: str, player_name: str) -> Optional[str]:
        # Check if room exists
        db_room = self.game_room_dao.get_room_by_code(room_code)
        if not db_room:
            return None

        # Create player
        player_id = str(uuid.uuid4())
        db_player = self.player_dao.create_player(player_id, player_name, db_room.id)

        # Add to in-memory game
        if room_code in self.active_games:
            self.active_games[room_code].add_player(player_id, player_name)

        return player_id

    def update_game_state(self, room_code: str):
        """Sync in-memory game state with database"""
        if room_code not in self.active_games:
            return

        game_room = self.active_games[room_code]
        db_room = self.game_room_dao.get_room_by_code(room_code)
        
        if db_room:
            # Update room state
            self.game_room_dao.update_room_state(
                db_room,
                game_room.is_game_started,
                game_room.current_turn
            )
            
            # Update player states
            for player in game_room.players.values():
                db_player = self.player_dao.get_player(player.id, db_room.id)
                if db_player:
                    self.player_dao.update_player_ready(db_player, player.is_ready)

    def load_game(self, room_code: str) -> Optional[GameRoom]:
        """Load game from database into memory"""
        db_room = self.game_room_dao.get_room_by_code(room_code)
        if not db_room:
            return None

        # Convert to domain model using mapper
        game_room = GameMapper.to_game_room(db_room)
        self.active_games[room_code] = game_room
        return game_room