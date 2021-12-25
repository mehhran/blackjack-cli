import time
import random
from classes import Player, Game


# Main Menu

# Define Player
player = Player(input("What's your name?"), int(input("Your Bankroll?(integer)")))

# Game Start
while True:
	
	print(player)	

	while True:	
		# Define a new deck
		deck = Game.NewDeck()
		
		# Shuffle the deck
		random.shuffle(deck)
		
		# Player bet
		bet = Game.PlaceBet(player)

		# Pop two cards for player
		player_hand = Game.NewHand(deck)
		Game.ShowCards(player_hand, person=player.name)
				
		# Player turn
		if Game.deal_player(player_hand, deck) == 'BUST':
			print('Dealer wins.')
			Game.LostBet(player, bet)
			break
		
		# Dealer turn
		dealer_hand = Game.NewHand(deck)
		Game.ShowCards(dealer_hand, person='Dealer')

		time.sleep(2)

		if Game.deal_dealer(dealer_hand, deck) == 'BUST':
			print('Player wins.')
			Game.WonBet(player, bet)
			break

		if Game.NumberValue(dealer_hand) > Game.NumberValue(player_hand):
			print('Dealer wins.')
			Game.LostBet(player, bet)
			break
		elif Game.NumberValue(dealer_hand) == Game.NumberValue(player_hand):
			print('Tie game.')
			break
		else:
			print('Player wins.')
			Game.WonBet(player, bet)
			break

	if Game.replay() == 'n':
		print('Game Over.')
		break