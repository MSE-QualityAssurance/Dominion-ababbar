import random
from typing import List

from dominion.cards import Card


def shuffle_deck(deck: List[Card]) -> None:
    random.shuffle(deck)