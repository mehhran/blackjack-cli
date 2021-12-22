"""
Classes
"""

class Player:
	
	def __init__(self, name='player', bankroll=100):
		self.name = name
		self.bankroll = bankroll

	def __str__(self):
		return "Name: %s, Bankroll: %s" %(self.name, self.bankroll)

class Card:
	
	def __init__(self, rank, suit, **kwargs):
		self.rank = rank
		self.suit = suit
		
		if 'identifier' in kwargs:
			self.identifier = kwargs['identifier']	#A1-AE,B1-BE ...

		#unicode for printing purposes
		#self.unicode = f"U0001F0{self.identifier}"	#U0001FA1, ...

	def __str__(self):
		return "The %s of %s" %(self.rank, self.suit)
	 

import time
import random

def NewDeck():
	'''
	Defining the deck of cards
	'''
	deck = [Card(0,0) for i in range(52)]
	for i,card in enumerate(deck):
		if i in range(13):
			card.suit = 'Spades'
			card.rank = i + 1
		elif i in range(13,26):
			card.suit = 'Hearts'
			card.rank = i - 12
		elif i in range(26,39):
			card.suit = 'Diamonds'
			card.rank = i - 25
		else:
			card.suit = 'Clubs'
			card.rank = i - 38
		if i == 0 or i == 13 or i == 26 or i == 39:
			card.rank = 'Ace'
		elif i == 12 or i == 25 or i == 38 or i == 51:
			card.rank = 'King'
		elif i == 11 or i == 24 or i == 37 or i == 50:
			card.rank = 'Queen'
		elif i == 10 or i == 23 or i == 36 or  i == 49:
			card.rank = 'Jack'
	return deck

def NewHand(deck):
	'''
	Creates a new hand for either dealer or player.
	A new hand of two cards.
	'''
	hand = []
	hand.append(deck.pop())
	hand.append(deck.pop())
	return hand

def NumberValue(cards):
	'''
	first sums up all non-ace cards
	then check each ace with the value 11, if reaches over 21, change the value to 1
	arguments: list of cards
	'''
	sum = 0
	for card in cards:
		if card.rank != 'Ace':
			if type(card.rank) == int:
				sum += card.rank
			else:
				sum += 10
	#at this point sum is sum of non_ace cards
	for card in cards:
		if card.rank == 'Ace':
			if sum + 11 > 21:
				sum += 1
			else:
				sum += 11
	return sum

def ShowCards(cards, **kwargs):
	'''
	prints player cards or dealer cards
	also prints total number value of cards
	'''
	if 'person' in kwargs:
		print(f"{kwargs['person']}'s hand:\n")

	for card in cards:
		print(f"{card}\n")
	print(f"Total number value of cards: {NumberValue(cards)}")

def PlaceBet(player):
	while True:
		bet = int(input(f"How much do you bet {player.name}?(int)"))
		if bet > player.bankroll:
			print("Bet is bigger than your bankroll.")
		else:
			return bet

def LostBet(player, bet):
	player.bankroll -= bet

def WonBet(player, bet):
	player.bankroll += bet

def deal_player(cards, deck):
	while True:		
		choice = input('hit or stay?')		
		if choice == 'hit':
			cards.append(deck.pop())
			ShowCards(cards)
			if NumberValue(cards) > 21:
				print('BUST!')
				return 'BUST'		
		elif choice == 'stay':
			return 'STICK'

def deal_dealer(cards, deck):	
	while True:		
		if NumberValue(cards) >= 17:			
			if NumberValue(cards) > 21:
				print('BUST!')
				return 'BUST'			
			else:
				return 'STICK'
		else:
			cards.append(deck.pop())
			ShowCards(cards)
			time.sleep(2)

def replay():
	return input('Play again?(y/n)').lower()
	
"""
Gameplay
"""
#Main Menu

#define player
player = Player(input("What's your name?"), int(input("Your Bankroll?(integer)")))

while True:
#game start	
	print(player)	

	while True:	
		#define deck
		deck = NewDeck()
		# shuffle the deck
		random.shuffle(deck)
		
		#player bet
		bet = PlaceBet(player)

		#pop two cards for player
		player_hand = NewHand(deck)
		ShowCards(player_hand, person=player.name)
				
		#Player turn
		if deal_player(player_hand, deck) == 'BUST':
			print('Dealer wins.')
			LostBet(player, bet)
			break
		
		#Dealer turn
		dealer_hand = NewHand(deck)
		ShowCards(dealer_hand, person='Dealer')

		time.sleep(2)

		if deal_dealer(dealer_hand, deck) == 'BUST':
			print('Player wins.')
			WonBet(player, bet)
			break

		if NumberValue(dealer_hand) > NumberValue(player_hand):
			print('Dealer wins.')
			LostBet(player, bet)
			break
		elif NumberValue(dealer_hand) == NumberValue(player_hand):
			print('Tie game.')
			break
		else:
			print('Player wins.')
			WonBet(player, bet)
			break

	if replay() == 'n':
		print('Game Over.')
		break