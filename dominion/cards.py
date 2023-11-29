class Card:
    def __init__(self, name: str, cost: int, card_type: str, description: str = ''):
        self.name = name
        self.cost = cost
        self.card_type = card_type
        self.description = description

    def play(self, player: 'Player', game: 'Game'):
        """
        Play the card. This method should be overridden in subclasses to implement specific effects.
        :param player: The player who plays the card.
        :param game: The current game state.
        """
        pass

    def effect(self, player: 'Player', game: 'Game'):
        """
        Define the specific effect of the card. This is where the card's unique functionality will be implemented.
        :param player: The player who plays the card.
        :param game: The current game state.
        """
        pass

    def on_draw(self, player: 'Player', game: 'Game'):
        """
        Optional method triggered when the card is drawn. By default, it does nothing but can be overridden.
        :param player: The player who drew the card.
        :param game: The current game state.
        """
        pass

    def on_discard(self, player: 'Player', game: 'Game'):
        """
        Optional method triggered when the card is discarded. By default, it does nothing but can be overridden.
        :param player: The player who discards the card.
        :param game: The current game state.
        """
        pass

    def on_gain(self, player: 'Player', game: 'Game'):
        """
        Optional method triggered when the card is gained (added to a player's deck). Can be overridden.
        :param player: The player who gains the card.
        :param game: The current game state.
        """
        pass

    def on_trash(self, player: 'Player', game: 'Game'):
        """
        Optional method triggered when the card is trashed. Can be overridden.
        :param player: The player who trashes the card.
        :param game: The current game state.
        """
        pass

    def __str__(self):
        """
        String representation of the card, showing its name, cost, type, and description.
        """
        return f"{self.name} (Cost: {self.cost}, Type: {self.card_type}, Description: {self.description})"


class TreasureCard(Card):
    def __init__(self, name: str, cost: int, value: int):
        """
        Initialize a treasure card.
        :param name: The name of the card.
        :param cost: The cost to acquire the card.
        :param value: The monetary value the card provides when played.
        """
        super().__init__(name, cost, 'Treasure')
        self.value = value

    def play(self, player: 'Player', game: 'Game'):
        """
        Play the treasure card by adding its value to the player's available money.
        :param player: The player who plays the card.
        :param game: The current game state.
        """
        # Check if the player can play the treasure card (e.g., during the Buy phase)
        if game.can_play_treasure(player):
            player.money += self.value
            # Optionally, log this action for the player
            game.log_action(player, f"{player.name} played {self.name} for {self.value} money.")
        else:
            # If the card cannot be played, inform the player (optional)
            game.inform_player(player, "You cannot play treasure cards at this time.")

    def __str__(self):
        """
        String representation of the treasure card, including its monetary value.
        """
        return f"{super().__str__()}, Value: {self.value}"


class VictoryCard(Card):
    def __init__(self, name: str, cost: int, points: int):
        """
        Initialize a victory card.
        :param name: The name of the card.
        :param cost: The cost to acquire the card.
        :param points: The victory points this card provides.
        """
        super().__init__(name, cost, 'Victory')
        self.points = points

    def play(self, player: 'Player', game: 'Game'):
        """
        Play the victory card. In most cases, victory cards do not have an immediate effect when played.
        :param player: The player who plays the card.
        :param game: The current game state.
        """
        # Victory cards typically do not have a play effect. However, this method is implemented
        # for consistency and can be extended if there are cards with special play effects.
        pass

    def get_points(self, player: 'Player', game: 'Game'):
        """
        Calculate and return the points this card provides, which may depend on the game state or player's deck.
        :param player: The player who owns the card.
        :param game: The current game state.
        :return: The number of victory points this card provides.
        """
        # By default, return the static point value. This can be overridden in subclasses
        # for cards whose points depend on other factors.
        return self.points

    def __str__(self):
        """
        String representation of the victory card, including its victory points.
        """
        return f"{super().__str__()}, Points: {self.points}"


class ActionCard(Card):
    def __init__(self, name: str, cost: int, description: str = ''):
        """
        Initialize an action card.
        :param name: The name of the card.
        :param cost: The cost to acquire the card.
        :param description: A description of the card's effect.
        """
        super().__init__(name, cost, 'Action', description)

    def play(self, player: 'Player', game: 'Game'):
        """
        Play the action card. This method should be overridden in subclasses to implement specific effects.
        :param player: The player who plays the card.
        :param game: The current game state.
        """
        # Check if the player can play an action card
        if player.actions > 0:
            player.actions -= 1  # Consume an action
            self.effect(player, game)  # Implement the card's specific effect
        else:
            # If the player cannot play an action card, inform them (optional)
            game.inform_player(player, "You have no actions left to play this card.")

    def effect(self, player: 'Player', game: 'Game'):
        """
        Define the specific effect of the action card. This method should be overridden in subclasses.
        :param player: The player who plays the card.
        :param game: The current game state.
        """
        pass  # This method is meant to be overridden in specific action card subclasses

    def __str__(self):
        """
        String representation of the action card, including its effect description.
        """
        return f"{super().__str__()}, Effect: {self.description}"

class Smithy(ActionCard):
    def __init__(self):
        super().__init__("Smithy", 4, "Draw 3 cards.")

    def effect(self, player: 'Player', game: 'Game'):
        for _ in range(3):
            player.draw_card()

class Village(ActionCard):
    def __init__(self):
        super().__init__("Village", 3, "Draw 1 card, +2 Actions.")

    def effect(self, player: 'Player', game: 'Game'):
        player.draw_card()
        player.actions += 2

class Market(ActionCard):
    def __init__(self):
        super().__init__("Market", 5, "Draw 1 card, +1 Action, +1 Buy, +1 Coin.")

    def effect(self, player: 'Player', game: 'Game'):
        player.draw_card()
        player.actions += 1
        player.buys += 1
        player.money += 1
class Cellar(ActionCard):
    def __init__(self):
        super().__init__("Cellar", 2, "Discard any number of cards, then draw that many.")

    def effect(self, player: 'Player', game: 'Game'):
        # Assuming there's a method for the player to choose cards to discard
        discarded_cards = player.choose_cards_to_discard()
        for card in discarded_cards:
            player.discard_card(card)
        for _ in range(len(discarded_cards)):
            player.draw_card()
class Moat(ActionCard):
    def __init__(self):
        super().__init__("Moat", 2, "Draw 2 cards. When another player plays an Attack card, you may reveal this from your hand. If you do, you are unaffected by that Attack.")

    def effect(self, player: 'Player', game: 'Game'):
        for _ in range(2):
            player.draw_card()

    def react(self, player: 'Player', game: 'Game', attack_card: 'ActionCard'):
        # Logic for reacting to an attack card
        player.reveal_card(self)
        # Implement reaction logic, such as preventing the attack's effect on this player

class Mine(ActionCard):
    def __init__(self):
        super().__init__("Mine", 5, "Trash a Treasure card from your hand. Gain a Treasure card costing up to 3 more.")

    def effect(self, player: 'Player', game: 'Game'):
        # Assuming there's a method for the player to choose a treasure card to trash
        trashed_card = player.choose_treasure_card_to_trash()
        if trashed_card:
            player.trash_card(trashed_card)
            # Assuming there's a method to choose a new treasure card to gain
            gained_card = game.choose_treasure_card_to_gain(trashed_card.cost + 3)
            player.gain_card(gained_card)

class Witch(ActionCard):
    def __init__(self):
        super().__init__("Witch", 5, "Draw 2 cards, each other player gains a Curse.")

    def effect(self, player: 'Player', game: 'Game'):
        for _ in range(2):
            player.draw_card()
        for opponent in game.get_other_players(player):
            opponent.gain_card(game.curse_supply)

class Laboratory(ActionCard):
    def __init__(self):
        super().__init__("Laboratory", 5, "Draw 2 cards, +1 Action.")

    def effect(self, player: 'Player', game: 'Game'):
        for _ in range(2):
            player.draw_card()
        player.actions += 1