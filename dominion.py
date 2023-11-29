import random
from typing import List, Optional, Dict


class Card:
    def __init__(self, name: str, cost: int, card_type: str):
        self.name = name
        self.cost = cost
        self.card_type = card_type
        # Add other properties as needed, like effects, etc.

class TreasureCard(Card):
    def __init__(self, name: str, cost: int, value: int):
        super().__init__(name, cost, 'Treasure')
        self.value = value  # Value represents the amount of money this card provides.

    def play(self, player: 'Player', game: 'Game'):
        player.money += self.value

class VictoryCard(Card):
    def __init__(self, name: str, cost: int, points: int):
        super().__init__(name, cost, 'Victory')
        self.points = points  # Points represents the victory points this card provides.

class ActionCard(Card):
    def __init__(self, name: str, cost: int):
        super().__init__(name, cost, 'Action')

    def play(self, player: 'Player', game: 'Game'):
        # Implement specific action card logic
        pass



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

class Game:
    def __init__(self, players: List[Player]):
        self.players = players
        self.supply: Dict[str, List[Card]] = {}  # Supply of cards available for purchase
        self.turn: int = 0

    def setup_game(self):
        # Initialize the supply piles
        self.initialize_supply()

        # Deal starting decks to players and shuffle them
        for player in self.players:
            self.deal_starting_deck(player)
            shuffle_deck(player.deck)

        # Set the initial turn to the first player
        self.turn = 0

    def initialize_supply(self):
        # Setup the supply piles for the game
        # This includes adding a set number of each card type to the supply
        # You will need to define the supply structure based on the game rules
        self.supply = {
            "Copper": [TreasureCard("Copper", cost=0, value=1) for _ in range(60)],
            "Silver": [TreasureCard("Silver", cost=3, value=2) for _ in range(40)],
            "Gold": [TreasureCard("Gold", cost=6, value=3) for _ in range(30)],
            # Add other cards like Estates, Duchies, Provinces, and various action cards
            # The number of these cards depends on the number of players
        }

    def deal_starting_deck(self, player: Player):
        # Deal 7 Copper cards and 3 Estate cards to each player
        for _ in range(7):
            player.deck.append(TreasureCard("Copper", cost=0, value=1))
        for _ in range(3):
            player.deck.append(VictoryCard("Estate", cost=2, points=1))

    def play_round(self):
        current_player = self.players[self.turn % len(self.players)]

        # Action Phase
        self.action_phase(current_player)

        # Buy Phase
        self.buy_phase(current_player)

        # Cleanup Phase
        self.cleanup_phase(current_player)

        # Prepare for the next player's turn
        self.turn += 1

    def action_phase(self, player: Player):
        # Implement the logic for the Action phase
        # Players can play action cards from their hand
        while player.actions > 0:
            action_card = player.choose_action_card()
            if action_card:
                action_card.play(player, self)
                player.actions -= 1
            else:
                break

    def buy_phase(self, player: Player):
        # Implement the logic for the Buy phase
        # Players can buy cards from the supply
        while player.buys > 0:
            purchase = player.choose_purchase()
            if purchase and self.supply[purchase.name]:
                player.buy_card(purchase, self)
                player.buys -= 1
            else:
                break

    def cleanup_phase(self, player: Player):
        # Implement the logic for the Cleanup phase
        # Players discard their hand and draw a new hand of 5 cards
        player.discard_hand()
        for _ in range(5):
            player.draw_card()

        # Reset actions, money, and buys for the next turn
        player.reset_for_new_turn()


# Utility functions
def shuffle_deck(deck: List[Card]) -> None:
    random.shuffle(deck)

# Add more utility functions as needed.

# Example of initializing a game
players = [Player("Alice"), Player("Bob")]
game = Game(players)
game.setup_game()
