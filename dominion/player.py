from typing import Optional, List

from dominion.cards import *


class Player:
    def __init__(self, name: str):
        self.name = name
        self.deck: List[Card] = []
        self.hand: List[Card] = []
        self.discard_pile: List[Card] = []
        self.actions: int = 1
        self.money: int = 0
        self.buys: int = 1

    def choose_action_card(self) -> Optional[ActionCard]:
        # Example: choose the first action card in hand
        for card in self.hand:
            if isinstance(card, ActionCard):
                return card
        return None

    def choose_purchase(self, game) -> Optional[Card]:
        # Example: choose the first affordable card in the supply
        for card_name, card_stack in game.supply.items():
            if card_stack and card_stack[0].cost <= self.money:
                return card_stack[0]
        return None

    def buy_card(self, card: Card, game):
        if card.cost <= self.money and game.supply[card.name]:
            self.money -= card.cost
            purchased_card = game.supply[card.name].pop()
            self.discard_pile.append(purchased_card)

    def discard_hand(self):
        # Move all cards from hand to discard pile
        self.discard_pile.extend(self.hand)
        self.hand.clear()

    def reset_for_new_turn(self):
        self.actions = 1
        self.money = 0
        self.buys = 1

    # Add other player methods like play_card, buy_card, etc.
    def draw_card(self):
        pass

    def discard_card(self, card):
        pass
