

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 10:03:15 2021

@author: matthewoneill
"""
import random


def init():	
	global bet
	bet = 0
	global balance
	balance = 0
	global prevSum
	prevSum = 0
	global deck
	deck = {}
	global runningDeck
	runningDeck = []
	global count
	count = 0	
	global trueCount
	trueCount = 0

#Here we build a dictionary to hold the name, numeric value, count value, and number of total cards left in the deck.
def houseDeck(decks):
    

    deck = {
            0:["Two",2,1,4*decks],
            1:["Three",3,1,4*decks],
            2:["Four",4,1,4*decks],
            3:["Five",5,1,4*decks],
            4:["Six",6,1,4*decks],
            5:["Seven",7,0,4*decks],
            6:["Eight",8,0,4*decks],
            7:["Nine",9,0,4*decks],
            8:["Ten",10,-1,4*decks],
            9:["Jack",10,-1,4*decks],
            10:["Queen",10,-1,4*decks],
            11:["King",10,-1,4*decks],
            12:["Ace",1,-1,4*decks]
            }
    return deck

#List of indexs of cards to serve as our total deck in a game of blackjack. Will contain an equal number of 0s, 1s,...,12s
def buildDeck(houseDeck):
    
    runningDeck = []
    for i in range(13):
        j = houseDeck[i][3]
        while j > 0:
            runningDeck.append(i)
            j -= 1
    
    return runningDeck
        



def blackjack():
	print("")
	print("Welcome to the BlackJack table!")
	print("The minimum bet is $10, the maximum bet is $1000. All bet sizes must be an increment of $10.")
	print("All hands have an even odds payout, including Blackjack.")
	global balance
	balance = 0
	print("")
	global bet
	bet = int(input(("In order to have an optimal betting strategy. we need to pick a base betting unit. How much would you like your betting unit to be? "))) ##User bet size
	print("")
	print("Great! Let's get started.")
	print("--------------------")
	global deck
	deck = houseDeck(4) 
    ##Deck is the dictionary that contains keys 0 through 12 with a list as a value. 
    # The list contains a string of the cards value(One, Two, King, etc), the numeric value for blackjack,
    # the value the new card changes the count by, and the number of cards of this type are contained in the total
    # deck. In casino blackjack, the casino uses more than one deck, in our case we use 4, which means there are 
    # sixteen cards of each in the total deck.
	global runningDeck
	runningDeck = buildDeck(deck) #Builds a list with 16 of each numeric value 0-12 to be our running deck.
	global count
	count = 0
	playerHasAce = False
	
	card1 = runningDeck[random.randint(0,207)] #Pulls a card from the running deck
	runningDeck.remove(card1) #Removes from the running deck
	count += deck[card1][2] #Updates the count 
	print("Players first card: "+deck[card1][0])
    
    #Same prodcedure as before but we must specify that the first dealer card is face up.
	# 
	dealerFace = runningDeck[random.randint(0,206)]
	runningDeck.remove(dealerFace)
	count += deck[dealerFace][2]
    
	card2 = runningDeck[random.randint(0,205)]
	runningDeck.remove(card2)
	count += deck[card2][2]

    
	print("Player's second card: "+deck[card2][0])   
	dealerDown = runningDeck[random.randint(0,204)]
	runningDeck.remove(dealerDown)

	print("")
	print("The dealer is showing a: "+deck[dealerFace][0])
    
	global prevSum
	prevSum = deck[card1][1] + deck[card2][1]

    #Check if player has an ace or not.
	if card1 == 12 or card2 == 12:
		playerHasAce = True
		decision = bookStartWithAce(card1, card2, dealerFace)
		if card1 == card2:
			playerDecisionTreeWSplit(decision, card1, card1, prevSum, dealerFace,dealerDown, playerHasAce)
		else:
			playerDecisionTree(decision, prevSum, dealerFace, dealerDown, playerHasAce)
	else:
		decision = bookStartNoAce(card1, card2, dealerFace)
		if card1 == card2:
			playerDecisionTreeWSplit(decision, card1, card1, prevSum, dealerFace,dealerDown, playerHasAce)
		else:
			playerDecisionTree(decision,prevSum,dealerFace,dealerDown,playerHasAce)

	
	
	print("--------------------")
	nb = balance
	c = count 
	print("Your new balance is: "+str(nb))
	print("The current running count is: "+str(c))
	length = len(runningDeck)
	decksRemain = length / 52
	trueCount = count / decksRemain
	trueCount = round(trueCount)
	tc = trueCount
	print("The true count is "+str(tc))
	newbet = bet

	if trueCount <= 1:
		print("We recommend continuing to bet one betting unit: $"+str(newbet))
	else:
		newBet = bet*(trueCount - 1)
		strnewbet = newBet
		print("The true count has gone up to "+str(tc)+", so we suggest betting "+str(strnewbet))
	print("--------------------")

	play = input("Would you like to continue playing?(y/n) ")

	while play != 'y' and play != 'n':
		play = input("Please enter a valid input: ")
	if play == 'y':
		bet = int(input("Wonderful, how much would you like to bet? "))
		blackjackCont()
	elif play == 'n':
		if balance > 0:
			print("You walked away from the table with a gain of "+str(nb))
		elif balance == 0:
			print("You walked away from the table with a breakeven balance!")
		else:
			print("You walked away from the table with a loss of "+str(nb))

	


def blackjackCont():
	global prevSum
	global runningDeck
	global deck
	global count
	global bet
	global balance
	if len(runningDeck) <= 52:
		print("The running deck is below 52 cards and needs to be reshuffled before we can begin.")
		runningDeck == buildDeck(deck)

	print("All set! We're ready to get started!")
	print("")

	playerHasAce = False
	
	length = len(runningDeck)
	card1 = runningDeck[random.randint(0,length - 1)]
	runningDeck.remove(card1)
	count += deck[card1][2]
	print("Players first card: "+deck[card1][0])
    
	dealerFace = runningDeck[random.randint(0,206)]
	runningDeck.remove(dealerFace)
	count += deck[dealerFace][2]
    
	card2 = runningDeck[random.randint(0,205)]
	runningDeck.remove(card2)
	count += deck[card2][2]
	print("Player's second card: "+deck[card2][0])   
	
	dealerDown = runningDeck[random.randint(0,204)]
	runningDeck.remove(dealerDown)
    
	print("")
	print("The dealer is showing a: "+deck[dealerFace][0])
    
	global prevSum
	prevSum = deck[card1][1] + deck[card2][1]
	if card1 == 12 or card2 == 12:
		playerHasAce = True
		decision = bookStartWithAce(card1, card2, dealerFace)
		if card1 == card2:
			playerDecisionTreeWSplit(decision, card1, card1, prevSum, dealerFace,dealerDown, playerHasAce)
		else:
			playerDecisionTree(decision, prevSum, dealerFace, dealerDown, playerHasAce)
	else:
		decision = bookStartNoAce(card1, card2, dealerFace)
		if card1 == card2:
			playerDecisionTreeWSplit(decision, card1, card1, prevSum, dealerFace,dealerDown, playerHasAce)
		else:
			playerDecisionTree(decision,prevSum,dealerFace,dealerDown,playerHasAce)
	
	print("--------------------")
	nb = balance
	print("Your new balance is: "+str(nb))
	c = count
	print("The current running count is: "+str(c))
	length = len(runningDeck)
	decksRemain = length / 52
	trueCount = count / decksRemain
	trueCount = round(trueCount)
	tc = trueCount
	print("The true count is "+str(tc))

	if trueCount <= 1:
		nb = bet
		print("We recommend continuing to bet one betting unit: $"+str(nb))
	else:
		newBet = bet*(trueCount - 1)
		nb - newBet
		tc = trueCount
		print("The true count has gone up to "+str(tc)+", so we suggest betting "+str(nb))
	print("--------------------")

	play = input("Would you like to continue playing?(y/n) ")

	while play != 'y' and play != 'n':
		play = input("Please enter a valid input: ")
	if play == 'y':
		bet = input("Wonderful, how much would you like to bet? ")
		blackjackCont()
	elif play == 'n':
		strBal = balance
		if balance > 0:
			print("You walked away from the table with a gain of "+str(strBal))
		elif balance == 0:
			print("You walked away from the table with a breakeven balance!")
		else:
			print("You walked away from the table with a loss of "+str(strBal))



def bookStartNoAce(card1, card2, dealerFace):
	global prevSum
	global deck
	prevSum = deck[card1][1] + deck[card2][1]
	print("Your total is "+str(prevSum))
	print("--------------------")
	if card1 == card2:
		print("You do have the option to split these as they are both "+deck[card1][0]+"'s")
		if card1 == 0 or card1  == 1:
			if dealerFace <= 5:
				print("The dealer recommendation is to split.")
			else:
				print("The dealer recommendation is to hit.")
		elif card1 == 2:
			if dealerFace == 3 or dealerFace == 4:
				print("The book recommendation is to split.")
			else:
				print("The book recommendation is to hit.")
		elif card1 == 3:
			if dealerFace <= 7:
				print("The book recommendation is to double down.")
			else:
				print("The book recommendation is to hit.")
		elif card1 == 4:
			if dealerFace <= 4:
				print('The book recommendation is to split.')
			else:
				print("The book recommendation is to hit.")
		elif card1 == 5:
			if dealerFace <= 5:
				print("The book recommendation is to split.")
			else:
				print("The book recommendation is to hit.")
		elif card1 == 6:
			print("The book recommendation is to split.")
		elif card1 == 7:
			if dealerFace <= 4 or (dealerFace >= 6 and dealerFace <= 7):
				print("The book recommendation is to split.")
			else:
				print("The book recommendation is to stand.")
		elif card1 >= 8:
			print("The book recommendation is to stand.")
		print("Would you like to hit, stand, double down, or split?")
		decision = int(input("Enter 0 for hit, 1 for stand, 2 for double down, and 3 for split: "))
		print("--------------------")
		print("")
		return decision
	else:
		if prevSum >= 17:
			print("The book recommendation is to stand.")
		elif prevSum >= 13:
			if dealerFace >= 5:
				print("The book recommendation is to hit.")
			else:
				print("The book recommendation is to stand.")
		elif prevSum == 12:
			if dealerFace >= 2 and dealerFace <= 4:
				print("The book recommendation is to stand.")
			else:
				print("The book recommendation is to hit.")
		elif prevSum == 11:
			if dealerFace != 12:
				print("The book recommendation is to double down.")
			else:
				print("The book recommendation is to hit.")
		elif prevSum == 10:
			if dealerFace <= 7:
				print("The book recommendation is to double down.")
			else:
				print("The book recommendation is to hit.")
		elif prevSum == 9:
			if dealerFace >= 1 and dealerFace <= 4:
				print("The book recommendation is to double down.")
			else:
				print("The book recommendation is to hit.")
		else:
			print("The book recommendation is to hit.")
		print("Would you like to hit, stand, or double down?")
		decision = int(input("Enter 0 for hit, 1 for stand, and 2 for double down: "))
		print("--------------------")
		print("")
		return decision

def bookStartWithAce(card1,card2,dealerFace):
	global prevSum
	global deck
	lowerTotal = 0
	otherCard = 0
	if card1 == 12 and card2 == 12:
		print("Your total is 2 or 12.")
		print("--------------------")
		print("The book recommendation is always to split aces!")
		print("Would you like to hit, stand, double down, or split?")
		decision = int(input("Enter 0 for hit, 1 for stand, 2 for double down, and 3 for split: "))
		print("--------------------")
		print("")
		return decision
	else:
		if card1 == 12:
			lowerTotal = deck[card2][1] + 1
			prevSum = lowerTotal
			higherTotal = deck[card2][1] + 11
			otherCard = card2       
		else:
			lowerTotal = deck[card1][1] + 1
			prevSum = lowerTotal
			higherTotal = deck[card1][1] + 11
			otherCard = card1
        
		print("Your total is "+str(lowerTotal)+" or "+str(higherTotal))
		print("--------------------")
		if otherCard >= 8:
			print("21! Nice job!")
			return
		elif otherCard >= 6:
			print("The book recommendation is to stand.")
		elif otherCard == 5:
			if dealerFace == 0 or dealerFace == 5 or dealerFace == 6:
				print("The book recommendation is to stand.")
			elif dealerFace >= 1 and dealerFace <= 4:
				print("The book recommendation is to double down.")
			else:
				print("The book recommendation is to hit.")
		elif otherCard == 4:
			if dealerFace == 0:
				print("The book recommendation is to stand.")
			elif dealerFace >= 1 and dealerFace <= 4:
				print("The book recommendation is to double down.")
			else:
				print("The book recommendation is to hit.")
		elif otherCard == 2 or otherCard == 3:
			if dealerFace >= 2 or dealerFace <= 4:
				print("The book recommendation is to double down.")
			else:
				print("The book recommendation is to hit.")
		else:
			if dealerFace >= 3 or dealerFace <= 4:
				print("The book recommendation is to double down.")
			else:
				print("The book recommendation is to hit.")
		print("Would you like to hit, stand, or double down?")
		decision = int(input("Enter 0 for hit, 1 for stand, and 2 for double down: "))
		print("--------------------")
		print("")
		return decision

#Prints book recommendations given the user does not have an ace in the 
def bookFromHitNoAce(prevLow, newCard, dealerFace):
	global deck
	if newCard == 12:
		return bookFromHitWithAce(prevSum, newCard,dealerFace)
	else:
		prevLow = prevLow + deck[newCard][1]
		print("Your current total is "+str(prevLow))
		if prevLow >= 22:
			print("Oh no! You went over 21! Dealer wins.")
			return
		elif prevLow == 21:
			print("21! Nice job!")
			return
		elif prevLow >= 17:
			print("The book recommendation is to stand.")
		elif prevLow >= 13:
			if dealerFace <= 4:
				print("The book recommendation is to stand.")
			else:
				print("The book recommendation is to hit.")
		elif prevLow == 12:
			if dealerFace >= 2 and dealerFace <= 4:
				print("The book recommendation si to stand.")
			else:
				print("The book recommendation is to hit.")
		else:
			print("The book recommendation is to hit.")
	print("Would you like to hit or stand?")
	decision = int(input("Enter 0 for hit and 1 for stand: "))
	print("--------------------")
	print("")
	return decision

   

def bookFromHitWithAce(prevLow, newCard, dealerFace):
	global deck
	prevLow = prevLow + deck[newCard][1]
	newHigh = prevLow + deck[newCard][1] + 10
	if newHigh <= 21:
		print("Your current total is "+str(prevLow)+" or "+str(newHigh))
	else:
		print("Your current total is "+str(prevLow))
	if prevLow >= 22:
		print("Oh no! You went over 21! Dealer wins.")
		return
	elif prevLow == 21 or prevLow == 11:
		print("21! Nice job!")
		return
	elif prevLow >= 17:
		print("The book recommendation is to stand.")
	elif prevLow >= 13:
		if dealerFace <= 4:
			print("The book recommendation is to stand.")
		else:
			print("The book recommendation is to hit.")
	elif prevLow == 12:
		if dealerFace >= 2 and dealerFace <= 4:
			print("The book recommendation is to stand.")
		else:
			print("The book recommendation is to hit.")
	elif prevLow >= 9:
		print("The book recommendation is to stand.")
	elif prevLow == 8:
		if dealerFace == 0 or dealerFace == 5 or dealerFace == 6:
			print("The book recommendation is to stand.")
		else:
			print("The book recommendation is to hit.")
	elif prevLow == 7:
		if dealerFace == 0:
			print("The book recommendation is to stand.")
		else:
			print("The book recommendation is to hit.")
	else:
		print("The book recommendation is to hit.")
	print("Would you like to hit or stand?")
	decision = int(input("Enter 0 for hit and 1 for stand: "))
	print("--------------------")
	print("")
	return decision


def playerDecisionTree(decision, prevLow, dealerFace, dealerDown,playerHasAce):
	global count
	global balance
	global bet
	global prevSum
	global deck
	global runningDeck
	if decision == 0:
		length = len(runningDeck)
		newCard = runningDeck[random.randint(0,length - 1)]
		runningDeck.remove(newCard)
		count += deck[newCard][2]
		print("Your new card is "+deck[newCard][0])
		if playerHasAce:
			decision = bookFromHitWithAce(prevLow,newCard,dealerFace)
			prevSum = prevSum + deck[newCard][1]
			playerDecisionTree(decision,prevSum, dealerFace, dealerDown,playerHasAce)
		else:
			if newCard == 12:
				playerHasAce = True
				decision = bookFromHitNoAce(prevLow, newCard,dealerFace)
				prevSum = prevSum + deck[newCard][1]
				playerDecisionTree(decision,prevSum, dealerFace, dealerDown, playerHasAce)

			else:
				decision = bookFromHitNoAce(prevLow, newCard,dealerFace) 
				prevSum = prevSum + deck[newCard][1]
				playerDecisionTree(decision,prevSum, dealerFace, dealerDown, playerHasAce)
	elif decision == 1:
		dealerSum = dealerFlip(prevSum, dealerFace, dealerDown)
		checkWin(prevSum, dealerSum)
	elif decision == 2:
		bet = bet * 2
		stringBet = bet
		print("Betsize has been increased to "+str(stringBet))
		length = len(runningDeck)
		newCard = runningDeck[random.randint(0,length - 1)]
		runningDeck.remove(newCard)
		count += deck[newCard][2]
		print("Your new card is: "+deck[newCard][0])
		if playerHasAce:
			prevSum = prevSum + deck[newCard][1]
			newHigh = prevSum + deck[newCard][1] + 10
			if newHigh < 22:
				prevSum = newHigh
		else:
			prevSum = prevSum + deck[newCard][1]
	
		sum = prevSum
		print("Your new total is "+str(sum))
		dealerSum = dealerFlip(prevSum, dealerFace, dealerDown)
		checkWin(prevSum,dealerSum)
	elif decision == None:
		dealerSum = dealerFlip(prevSum, dealerFace,dealerDown)
		checkWin(prevSum, dealerSum)
	else:
		decision = input("Please enter a valid input: ")
		playerDecisionTree(decision, prevLow, dealerFace, dealerDown, runningDeck, deck, count,playerHasAce,bet)

def playerDecisionTreeWSplit(decision, prevLow, card1, card2, dealerFace, dealerDown, playerHasAce):
	global count
	global balance
	global bet
	global prevSum
	global deck
	global runningDeck
	if decision == 0:
		playerDecisionTree(0, prevLow, dealerFace, dealerDown,playerHasAce)
	elif decision == 1:
		playerDecisionTree(1, prevLow, dealerFace, dealerDown,playerHasAce)
	elif decision == 2:
		playerDecisionTree(2, prevLow, dealerFace, dealerDown,playerHasAce)
	elif decision == 3:
		playerSplit(card1, card2,dealerFace,dealerDown)
	else:
		decision = input("Please enter a valid input: ")
		playerDecisionTreeWSplit(decision, prevLow, card1, card2, dealerFace, dealerDown)


def dealerFlip(playerSum, dealerFace, dealerDown):
	global deck
	print("The dealer is showing "+deck[dealerDown][0]+" as their second card.")
	global count
	global balance
	global bet
	global prevSum
	global runningDeck
	count += deck[dealerDown][2]
	if prevSum >= 22:
		dealerSum = deck[dealerFace][1] + deck[dealerDown][1]
		sum = dealerSum 
		print("The dealer has "+str(sum)+" as their total.")
		return dealerSum
	if dealerFace == 12 or dealerDown == 12:
		dealerSum = deck[dealerFace][1] + deck[dealerDown][1]
		if dealerSum >= 8:
			sum = dealerSum
			print("The dealer has "+str(sum)+" as their total.")
			return dealerSum + 10
		else:
			sum = dealerSum
			print("The dealer has "+str(sum)+" as their total.")
			length = len(runningDeck)
			newPull = runningDeck[random.randint(0,length-1)]
			runningDeck.remove(newPull)
			count += deck[newPull][2]
			return dealerPullWAce(playerSum, dealerSum, newPull)
	else:
		dealerSum = deck[dealerFace][1] + deck[dealerDown][1]
		sum = dealerSum
		print("The dealer has "+str(sum)+" as their total.")
		print("")
		if dealerSum >= 17:
			return dealerSum
		else:
			length = len(runningDeck)
			newPull = runningDeck[random.randint(0,length-1)]
			runningDeck.remove(newPull)
			count += deck[newPull][2]
			return dealerPullNoAce(playerSum, dealerSum, newPull)




def dealerPullNoAce(playerSum, dealerSum, newPull):
	global deck
	print("The dealer's new card is "+deck[newPull][0])
	global count
	global balance
	global bet
	global prevSum
	global runningDeck
	dealerSum += deck[newPull][1]
	if newPull == 12:
		if dealerSum >= 8 and dealerSum <= 11:
			sum = dealerSum
			print("The dealer's new total is "+str(sum + 10))
			return dealerSum + 10
		elif dealerSum >= 17:
			sum = dealerSum
			print("The dealer's new total is "+str(sum))
			return dealerSum
		else:
			sum = dealerSum
			print("The dealer's new total is "+str(sum))
			length = len(runningDeck)
			newPull = runningDeck[random.randint(0,length-1)]
			runningDeck.remove(newPull)
			count += deck[newPull][2]
			return dealerPullWAce(playerSum, dealerSum, newPull)
	else:
		if dealerSum >= 17:
			sum = dealerSum
			print("The dealer's new total is "+str(sum))
			return dealerSum
		else:
			sum = dealerSum
			print("The dealer's new total is "+str(sum))
			length = len(runningDeck)
			newPull = runningDeck[random.randint(0,length-1)]
			runningDeck.remove(newPull)
			count += deck[newPull][2]
			return dealerPullNoAce(playerSum, dealerSum, newPull)

	

def dealerPullWAce(playerSum, dealerSum, newPull):
	global deck
	print("The dealer's new card is "+deck[newPull][0])
	dealerSum += deck[newPull][1]
	global runningDeck
	global count

	if dealerSum >= 17:
		sum = dealerSum
		print("The dealer's new total is "+str(sum))
		return dealerSum
	elif dealerSum >= 8 and dealerSum <= 11:
		print("The dealer's new total is "+str(dealerSum + 10))
		return dealerSum + 10
	else:
		sum = dealerSum
		print("The dealer's new total is "+str(sum))
		length = len(runningDeck)
		newPull = runningDeck[random.randint(0,length-1)]
		runningDeck.remove(newPull)
		count += deck[newPull][2]
		return dealerPullNoAce(playerSum, dealerSum, newPull)

def playerSplit(card1, card2,dealerFace,dealerDown):

	global runningDeck
	global deck
	global count
	global bet
	global balance

	length = len(runningDeck)
	newCard1 = runningDeck[random.randint(0,length - 1)]
	runningDeck.remove(newCard1)
	count += deck[newCard1][2]
	handOneAce = False
	prevLowOne = deck[card1][1] + deck[newCard1][1]
	
	if card1 == 12 or newCard1 == 12:
		print("Your new total on for your first split hand is "+str(prevLowOne)+" or "+str(prevLowOne + 10)+".")
		handOneAce = True
		decision = bookStartWithAce(card1, newCard1, dealerFace)
		if card1 == newCard1:
			playerDecisionTreeWSplit(decision, prevLowOne, card1, newCard1,dealerFace,dealerDown,handOneAce)
		else:
			playerDecisionTree(decision,prevLowOne, dealerFace, dealerDown,handOneAce)
	else:
		print("Your new total on for your first split hand is "+str(prevLowOne)+".")
		decision = bookStartNoAce(card1, newCard1, dealerFace)
		if card1 == newCard1:
			playerDecisionTreeWSplit(decision, prevLowOne, card1, newCard1,dealerFace,dealerDown,handOneAce)
		else:
			playerDecisionTree(decision,prevLowOne,dealerFace,dealerDown,handOneAce)
	
	length2 = len(runningDeck)
	newCard2 = runningDeck[random.randint(0,length - 1)]
	runningDeck.remove(newCard2)
	count += deck[newCard2][2]
	handTwoAce = False
	prevLowTwo = deck[card2][1] + deck[newCard2][1]
	handTwoWin = False
	if card2 == 12 or newCard2 == 12:
		print("Your new total on for your first split hand is "+str(prevLowTwo)+" or "+str(prevLowTwo + 10)+".")
		handTwoAce = True
		decision = bookStartWithAce(card2, newCard2, dealerFace)
		if card2 == newCard2:
			playerDecisionTreeWSplit(decision,prevLowTwo, card2, newCard2,dealerFace,dealerDown,handTwoAce)
		else:
			playerDecisionTree(decision,prevLowOne, dealerFace, dealerDown, handOneAce)
	else:
		print("Your new total on for your other split hand is "+str(prevLowTwo)+".")
		decision = bookStartNoAce(card2, newCard2, dealerFace)
		if card2 == newCard2:
			playerDecisionTreeWSplit(decision,prevLowTwo,card2, newCard2,dealerFace,dealerDown,handTwoAce)
		else:
			playerDecisionTree(decision,prevLowTwo,dealerFace,dealerDown,handTwoAce)


def checkWin(playerSum,dealerSum):
	global bet
	global balance
	
	if playerSum >= 22:
		stringBet = bet
		balance -= bet
		print("Oh no, you went over and busted! You lose "+str(stringBet)+".")
	elif dealerSum >= 22:
		stringBet = bet
		balance += bet
		print("The dealer busted and you win "+str(stringBet)+"!")
	elif dealerSum == 21:
		if playerSum == 21:
			print("Unlucky! The dealer matched your 21! You push.")
		else:
			stringBet = bet
			balance -= bet
			print("Oh no! The dealer has a higher total and wins. You lose "+str(stringBet)+".")
	else:
		if playerSum > dealerSum:
			stringBet = bet
			balance += bet
			print("Nice job! You win "+str(stringBet)+"!")
		elif playerSum == dealerSum:
			print("Push!")
		else:
			stringBet = bet
			balance -= bet
			print("Oh no! The dealer has a higher total and wins. You lose "+str(stringBet)+".")
    




def main():
	init()
	blackjack()

if __name__ == "__main__":
    main()
