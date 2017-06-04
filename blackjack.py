import random

formatting_begin = '\033[91m'
formatting_end = '\033[0m'

values = {
	'two': 2,
	'three': 3,
	'four': 4,
	'five': 5, 
	'six': 6,
	'seven': 7, 
	'eight': 8,
	'nine': 9,
	'ten': 10,
	'jack': 10,
	'queen': 10,
	'king': 10,
	'ace': (1,11)
}

players = []

class BankException(Exception):
	pass

class Player(object):
	isStay = False
	isBust = False
	currentBet = 0

	def __init__(self, bankroll = 1000):
		self.bankroll = bankroll
		self.hand = Hand()
		self.score = self.hand.get_value()

	def __str__(self):
		return "Current Score: {s}; Current Bankroll: {b}".format(s=self.score, b=self.bankroll)

	def add_bankroll(self, amount):
		self.bankroll += amount

	def hit(self, card):
		self.hand = self.hand.addCard(card)
		self.score = self.hand.get_value()
		self.isBust = self.hand.isBust

	def stay(self):
		self.isStay = True

	def shouldHit(self):
		return self.score <= 17

	def canHit(self):
		return not (self.isStay or self.isBust)

	def set_currentBet(self, bet):
		self.currentBet = bet

	def showHandHidden(self, isDealer):
		if len(self.hand.cards) > 1:
			print("Hidden Card")
			if isDealer:
				for card in self.hand.cards[1:]:
					print(card)
			else:
				for card in self.hand.cards[1:]:
					print("Hidden Card")
			print("Score: Unknown")

	def revealHand(self):
		self.hand.showHand()

	def reset(self):
		self.isStay = False
		self.isBust = False
		self.hand.reset()
		self.score = self.hand.get_value()
		self.currentBet = 0

class Card(object):
	values = {
		'Two': 2,
		'Three': 3,
		'Four': 4,
		'Five': 5, 
		'Six': 6,
		'Seven': 7, 
		'Eight': 8,
		'Nine': 9,
		'Ten': 10,
		'Jack': 10,
		'Queen': 10,
		'King': 10,
		'Ace': (1,11)
	}

	def __init__(self, face, suit):
		self.face = face
		self.suit = suit
		self.value = self.values[face]

	def __str__(self):
		return "{} of {}".format(self.face, self.suit)


class Deck(object):
	cards = []
	def __init__(self):
		self.populateCards()

	def populateCards(self):
		for face in Card.values.keys():
			newCard = Card(face, 'Spades')
			self.cards.append(newCard)
		for face in Card.values.keys():
			newCard = Card(face, 'Hearts')
			self.cards.append(newCard)
		for face in Card.values.keys():
			newCard = Card(face, 'Diamonds')
			self.cards.append(newCard)
		for face in Card.values.keys():
			newCard = Card(face, 'Clubs')
			self.cards.append(newCard)

	def deal(self):
		index = random.randint(0,len(self.cards) - 1)
		return self.cards.pop(index)

	def reset(self):
		self.cards = []
		self.populateCards()

class Hand(object):
	isBust = False

	def __init__(self):
		self.cards = []
		self.value = 0

	def addCard(self, card):
		self.cards.append(card)
		if card.face == 'Ace':
			if self.value <= 10:
				self.value += 11
			else:
				self.value += 1
				self.isBust = self.value > 21
		else:
			self.value += Card.values[card.face]
			self.isBust = self.value > 21
		return self

	def showHand(self):
		for card in self.cards:
			print card
		print("Score: {}".format(self.value))
		if self.isBust:
			print("This hand is a bust.")

	def get_value(self):
		return self.value

	def reset(self):
		self.isBust = False
		self.cards = []
		self.value = 0


def printPlayerString(isDealer, playerIndex):
	global formatting_begin, formatting_end
	playerString = formatting_begin 
	if isDealer:
		playerString += "Dealer's Hand:"
	else:
		playerString += "Player {}'s Hand:".format(playerIndex)
	playerString += formatting_end
	print(playerString)

def showHand(player, isDealer, playerIndex = 0):
	printPlayerString(isDealer, playerIndex)
	if isDealer:
		player.showHandHidden(isDealer)
	else:
		player.revealHand()
	print("")

def revealHand(player, isDealer):
	printPlayerString(isDealer)
	player.revealHand()
	print("")

def dealInitialHand(players, deck):
	for i in range(2):
		for player in players:
			if player.bankroll > 0:
				player.hit( deck.deal() )

def takeTurn(playerIndex, player, deck):
	print("\nPlayer {}'s turn!".format(playerIndex))
	response = " "
	while player.canHit():
		print("Options: h) hit, s) stay, 'quit' to exit (h/s/'quit').")
		try:
			response = raw_input("Enter your choice: ")
			response = response.lower()
			if response != 'h' and response != 's':
				raise Exception('Invalid choice on turn')
		except:
			if response == 'quit':
				quit()
			else:
				print("That is not a valid option.")
		else:
			if response == 'h':
				player.hit( deck.deal() )
			else:
				player.isStay = True
			if playerIndex == 0:
				showHand(player, True)
			else:
				showHand(player, False, playerIndex)

def dealerTurn(dealer, deck):
	print("\nDealer's turn!")
	while dealer.shouldHit():
		print("Dealer hits.")
		dealer.hit( deck.deal() )
	showHand(dealer, True)

def adjustBankrolls(winners, losers):
	for winner in winners:
		winner.add_bankroll(winner.currentBet)
	for loser in losers:
		loser.add_bankroll(-loser.currentBet)

def showWinners(players):
	global formatting_begin, formatting_end
	scoreToBeat = 0
	winners = []
	losers = []
	if not players[0].isBust:
		scoreToBeat = players[0].score
	for idx, player in enumerate(players):
		playerString = formatting_begin
		if idx == 0:
			playerString += "Dealer: " + formatting_end
			if not player.isBust:
				playerString += str(player.score)
			else:
				playerString += "Bust"
		else:
			if player.bankroll > 0:
				playerString += "Player {}: ".format(idx) + formatting_end
				if not player.isBust:
					playerString += str(player.score)
					if player.score > scoreToBeat:
						playerString += "\nPlayer {} has a winning hand!".format(idx)
						winners.append(player)
					elif player.score == scoreToBeat:
						playerString += "\nPlayer {} pushes.".format(idx)
					else:
						playerString += "\nPlayer {} loses this round.".format(idx)
						losers.append(player)
				else:
					playerString += "Bust"
					playerString += "\nPlayer {} loses this round.".format(idx)
					losers.append(player)
		if player.bankroll > 0:
			print(playerString)
	adjustBankrolls(winners, losers)

	for player in players:
		player.reset()


def endGame():
	global players
	print("Evaluating winner(s) . . .\n")
	for idx, player in enumerate(players):
		if idx == 0:
			printPlayerString(True, idx)
		elif player.bankroll > 0:
			printPlayerString(False, idx)
		if player.bankroll > 0:
			player.revealHand()
			print("")
	showWinners(players)



def play():
	global formatting_end, formatting_begin, players
	deck = Deck()
	gameState = True
	dealInitialHand(players, deck)

	for idx, player in enumerate(players):
		if idx == 0:
			showHand(player, True)
		else:
			showHand(player, False, idx)
	
	for idx, player in enumerate(players[1:]):
		if player.bankroll > 0:
			takeTurn(idx + 1, player, deck)
		else:
			print("Skipping player {}, they're broke!".format(idx + 1))

	dealerTurn(players[0], deck)
	endGame()

	# while gameState:

def getBankRoll(playerIndex):
	bankroll = 0
	print("\nEnter the bankroll of player {}.".format(playerIndex))
	print("All players must have at least 100 to play.")
	while True:
		try:
			bankroll = raw_input("Enter a bankroll, or type 'quit' to exit: ")
			bankroll = int(bankroll)
			if bankroll < 100:
				raise Exception('Invalid bankroll.')
		except:
			if bankroll == 'quit':
				quit()
			else:
				print("That is not a valid bankroll.")
		else:
			return bankroll


def populatePlayers(numPlayers):
	global players
	for i in range(numPlayers + 1):
		if i == 0:
			players.append(Player())
		else:
			players.append(Player(getBankRoll(i)))

def placeBets(players):
	print("Now taking bets.")
	print("You may enter an integer up to your bankroll amount.")
	for idx, player in enumerate(players):
		if idx == 0:
			continue
		else:
			print("Player {}'s turn to bet.".format(idx))
			while True:
				bet = 0
				try:
					bet = raw_input("Place your bet: ")
					bet = int(bet)
					if bet > player.bankroll:
						raise BankException({'message':'The amount is greater than your bankroll!'})
					elif bet <= 0:
						raise BankException({'message':'The amound must be greater than 0!'})
				except BankException as e:
					details = e.args[0]
					print(details['message'])
					continue
				except:
					print("Invalid bet! Try again.")
					continue
				else:
					player.set_currentBet(bet)
					break



def gameSetup():
	print(" ~ Welcome to BlackJack ~ ")
	print("")
	print("Enter the number of players besides the dealer.")
	numPlayers = 0
	while True:
		try:
			numPlayers = raw_input("You may choose an integer from 1 to 4, or type 'quit' to exit: ")
			numPlayers = int(numPlayers)
			if numPlayers < 1 or numPlayers > 4:
				raise Exception('Invalid number of players.')
		except:
			if numPlayers == 'quit':
				quit()
			else:
				print("That is not a valid number of players.")
		else:
			populatePlayers(numPlayers)
			placeBets(players)
			break



def main():
	global players
	gameSetup()
	play()

	for player in players:
		print player 
	print("")
	playAgain = raw_input("Would you like to play again (y/n)? ")
	while playAgain == 'y':
		placeBets(players)
		play()
		for player in players:
			print player 
		print("")
		playAgain = raw_input("Would you like to play again (y/n)? ")




if __name__ == '__main__':
	main()








