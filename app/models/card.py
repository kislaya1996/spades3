from enum import Enum
from typing import List, Optional
import random

class Suit(Enum):
    HEARTS = "hearts"
    DIAMONDS = "diamonds"
    CLUBS = "clubs"
    SPADES = "spades"

class Card:
    def __init__(self, suit: Suit, value: int):
        self.suit = suit
        self.value = value  # 1-13 (Ace through King)
    
    @property
    def name(self) -> str:
        if self.value == 1:
            return "Ace"
        elif self.value == 11:
            return "Jack"
        elif self.value == 12:
            return "Queen"
        elif self.value == 13:
            return "King"
        return str(self.value)
    
    def __str__(self) -> str:
        return f"{self.name} of {self.suit.value}"

class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self.reset()
    
    def reset(self) -> None:
        """Reset the deck to a full 52-card deck."""
        self.cards = []
        for suit in Suit:
            for value in range(1, 14):
                self.cards.append(Card(suit, value))
    
    def shuffle(self) -> None:
        """Shuffle the deck."""
        random.shuffle(self.cards)
    
    def draw(self) -> Optional[Card]:
        """Draw a card from the deck."""
        if not self.cards:
            return None
        return self.cards.pop()
    
    def remaining_cards(self) -> int:
        """Return the number of remaining cards in the deck."""
        return len(self.cards) 