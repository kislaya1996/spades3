from app.models.database_models import GameRoomDB, PlayerDB
from app.models.game_room import GameRoom, Player

class GameMapper:
    @staticmethod
    def to_game_room(db_room: GameRoomDB) -> GameRoom:
        game_room = GameRoom(room_code=db_room.room_code)
        game_room.is_game_started = db_room.is_game_started
        game_room.current_turn = db_room.current_turn
        
        # Map players
        for db_player in db_room.players:
            player = GameMapper.to_player(db_player)
            game_room.players[player.id] = player
            
        return game_room

    @staticmethod
    def to_player(db_player: PlayerDB) -> Player:
        player = Player(player_id=db_player.player_id, name=db_player.name)
        player.is_ready = db_player.is_ready
        return player