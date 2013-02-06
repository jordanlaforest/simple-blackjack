import random
import time

#Constants
CPU_SLEEP_TIME = 1.5 #How much time the cpu takes to do actions
NUM_DECKS = 2

def main():
	if(NUM_DECKS == 1):
		plural = ""
	else:
		plural = "s"
	print "Play blackjack until you run out of cards from " + str(NUM_DECKS) + " deck" + plural + "."
	print "Try to turn your $500 into as much as you can by the end."
	print "Dealer stays on anything 17 or above."

	deck = createDeck()
	random.shuffle(deck)
	
	playing = True
	pushed = False
	playerCash = 500
	
	while playing:
		playingHand = True
		
		if(len(deck) <= 4):
			print "Not enough cards for next hand"
			break
		
		if(not pushed):
			bet = getBet(playerCash)
		else:
			print "Previous bet still on table"
			bet += getBet(playerCash-bet)
		pushed = False
		

		dealerHand = []
		playerHand = []

		# Draw 2 cards for the player and the dealer
		draw(dealerHand, deck)
		draw(playerHand, deck)
		
		draw(dealerHand, deck)
		draw(playerHand, deck)
		
		while playingHand: #Player's turn
			printStatus(playerCash, bet, dealerHand, playerHand, True)
			a = getAction((playerCash >= bet * 2))
			if(a == "h"):
				drawRet = draw(playerHand, deck)
				printStatus(playerCash, bet, dealerHand, playerHand, True)
				handVal = getHandValue(playerHand)
				if(handVal > 21): 
					print "Bust!"
					playingHand = False
				elif(handVal == 21):
					print "21!"
					playingHand = False
				if(drawRet): #Ran out of cards in the deck, time to end the game
					playing = False
					break
			elif(a == "s"):
				break #Go to dealer's loop
			elif(a == "d"):
				draw(playerHand, deck)
				bet *= 2
				printStatus(playerCash, bet, dealerHand, playerHand, True)
				handVal = getHandValue(playerHand)
				if(handVal > 21): 
					print "Bust!"
					playingHand = False
				elif(handVal == 21):
					print "21!"
					playingHand = False
				break
		
		printStatus(playerCash, bet, dealerHand, playerHand)
		
		while playingHand and playing: #Dealer's turn
			handVal = getHandValue(dealerHand)
			if(handVal < 17):
				drawRet = draw(dealerHand, deck)
				print "Dealer drew the card: [" + dealerHand[-1] + "]"
				printStatus(playerCash, bet, dealerHand, playerHand)
				time.sleep(CPU_SLEEP_TIME)
				if(drawRet): #Ran out of cards in the deck, time to end the game
					playing = False
					break
			elif(handVal > 21):
				print "Dealer bust!"
				time.sleep(CPU_SLEEP_TIME)
				break
			else:
				print "Dealer is staying"
				time.sleep(CPU_SLEEP_TIME)
				break
		
		if(not playing):
			print "Deck is empty, results for final hand:"
		
		playerVal = getHandValue(playerHand)
		dealerVal = getHandValue(dealerHand)

		if(playerVal > dealerVal and playerVal <= 21 or dealerVal > 21):
			print "You won the hand!"
			playerCash += bet
		elif(playerVal < dealerVal and dealerVal <= 21 or playerVal > 21):
			print "Dealer wins the hand"
			playerCash -= bet
		else:
			print "Push"
			pushed = True 
	
		printStatus(playerCash, bet, dealerHand, playerHand)
		if(playerCash <= 0):
			break

	print "Game is over, you finished with $" + str(playerCash)

def draw(hand, deck):
	hand.append(deck.pop())
	if(len(deck) == 0):
		return True	#Means this is the last card
	return False

def getBet(maxBet):
	while True:
		try:
			bet = int(raw_input("Place your bet:"))
		except ValueError:
			bet = -1

		if(bet > maxBet or bet < 0):
			print "Please enter a valid bet"
		else:
			return bet

def getAction(canDouble):
	while True:
		action = raw_input("What do you want to do? (h = hit, s = stay, d = double):")
		if(action == "h" or action == "hit"):
			return "h"
		if(action == "s" or action == "stay"):
			return "s"
		if((action == "d" or action == "double") and canDouble):
			return "d"
		
		print "Invalid input, try again."

def createDeck():
	deck = []

	for x in range(0, NUM_DECKS * 4):
		deck.append('A')
		for y in range(2, 11):
			deck.append(str(y))
		deck.append('J')
		deck.append('Q')
		deck.append('K')

	return deck

def getHandString(hand, hideFirst=False):
	handStr = ""
	for i in range(0, len(hand)):
		if(i == 0 and hideFirst):
			handStr += "[#]"
		else:
			handStr += "[" + hand[i] + "]"
	return handStr

#Both hands and current sum of cards
def printStatus(cash, bet, dealer, player, hideFirst=False):
	print "Your cash: $" + str(cash) + " Bet: $" + str(bet)
	print "Dealer: " + getHandString(dealer, hideFirst) + " (" + str(getHandValue(dealer, hideFirst)) + ")"
	print "You:    " + getHandString(player) + " (" + str(getHandValue(player)) + ")"


def getHandValue(hand, hideFirst=False):
	numAces = 0
	value = 0
	start = 0
	if(hideFirst): #Skip first card in dealers hand if it is not shown yet
		start = 1
	for i in range(start, len(hand)):
		if(hand[i] == "A"):
			numAces += 1
		else:
			value += getCardValue(hand[i])
	for j in range(0, numAces):
		if(21 - value - (numAces - j - 1) >= 11): #This makes sure there is "room" for an ace valued at 11
			value += 11
		else:
			value += 1
	return value

#Assumes it's getting valid input, there is no case for ace because it is handled in getHandValue
def getCardValue(c):
	if(c == "J" or c == "Q" or c == "K"):
		return 10
	return int(c)


if __name__ == '__main__':
	main()
