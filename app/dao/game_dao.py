from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.database_models import GameRoomDB, PlayerDB

class GameRoomDAO:
    def __init__(self, db: Session):
        self.db = db

    def create_room(self, room_code: str) -> GameRoomDB:
        db_room = GameRoomDB(room_code=room_code)
        self.db.add(db_room)
        self.db.commit()
        self.db.refresh(db_room)
        return db_room

    def get_room_by_code(self, room_code: str) -> Optional[GameRoomDB]:
        return self.db.query(GameRoomDB).filter(GameRoomDB.room_code == room_code).first()

    def update_room_state(self, db_room: GameRoomDB, is_game_started: bool, current_turn: Optional[str] = None) -> GameRoomDB:
        db_room.is_game_started = is_game_started
        if current_turn:
            db_room.current_turn = current_turn
        self.db.commit()
        self.db.refresh(db_room)
        return db_room

class PlayerDAO:
    def __init__(self, db: Session):
        self.db = db

    def create_player(self, player_id: str, name: str, game_room_id: int) -> PlayerDB:
        db_player = PlayerDB(
            player_id=player_id,
            name=name,
            game_room_id=game_room_id
        )
        self.db.add(db_player)
        self.db.commit()
        self.db.refresh(db_player)
        return db_player

    def get_player(self, player_id: str, game_room_id: int) -> Optional[PlayerDB]:
        return self.db.query(PlayerDB).filter(
            PlayerDB.player_id == player_id,
            PlayerDB.game_room_id == game_room_id
        ).first()

    def update_player_ready(self, db_player: PlayerDB, is_ready: bool) -> PlayerDB:
        db_player.is_ready = is_ready
        self.db.commit()
        self.db.refresh(db_player)
        return db_player