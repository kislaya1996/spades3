from typing import Dict, List, Optional
import random
import string
from datetime import datetime
from .card import Deck, Card

class Player:
    def __init__(self, player_id: str, name: str):
        self.id = player_id
        self.name = name
        self.hand: List[Card] = []
        self.is_ready = False
        self.last_active = datetime.now()

    def add_card(self, card: Card) -> None:
        self.hand.append(card)

    def remove_card(self, card: Card) -> None:
        self.hand.remove(card)

    def update_activity(self) -> None:
        self.last_active = datetime.now()

class GameRoom:
    def __init__(self, room_code: str, max_players: int = 4):
        self.room_code = room_code
        self.max_players = max_players
        self.players: Dict[str, Player] = {}
        self.deck = Deck()
        self.is_game_started = False
        self.current_turn: Optional[str] = None
        self.created_at = datetime.now()

    @classmethod
    def generate_room_code(cls, length: int = 6) -> str:
        """Generate a random room code."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def add_player(self, player_id: str, name: str) -> bool:
        """Add a player to the game room."""
        if len(self.players) >= self.max_players:
            return False
        if player_id in self.players:
            return False
        self.players[player_id] = Player(player_id, name)
        return True

    def remove_player(self, player_id: str) -> None:
        """Remove a player from the game room."""
        if player_id in self.players:
            del self.players[player_id]

    def start_game(self) -> bool:
        """Start the game if all players are ready."""
        if len(self.players) < 2:  # Minimum 2 players required
            return False
        if not all(player.is_ready for player in self.players.values()):
            return False
        
        self.is_game_started = True
        self.deck.reset()
        self.deck.shuffle()
        self.deal_cards()
        self.current_turn = next(iter(self.players.keys()))
        return True

    def deal_cards(self) -> None:
        """Deal cards to all players."""
        cards_per_player = 13  # Standard for most card games
        for _ in range(cards_per_player):
            for player in self.players.values():
                card = self.deck.draw()
                if card:
                    player.add_card(card)

    def next_turn(self) -> None:
        """Move to the next player's turn."""
        player_ids = list(self.players.keys())
        if not player_ids:
            return
        
        current_index = player_ids.index(self.current_turn)
        next_index = (current_index + 1) % len(player_ids)
        self.current_turn = player_ids[next_index]

    def get_player_hand(self, player_id: str) -> List[Card]:
        """Get a player's hand."""
        if player_id in self.players:
            return self.players[player_id].hand
        return []

    def is_player_turn(self, player_id: str) -> bool:
        """Check if it's the player's turn."""
        return self.current_turn == player_id 