from chromaconsole import *
import random, os

colors = [Color.text("#03f"), Color.text("#0f0"), Color.text("#ff0"), Color.text("#f00")]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
jokers = ["+4", "color change", "shufle hands", "custom"]
others = ["reverse", "+2", "block"]

gameLoop = True
players = {}
playerNames = []
lastCard = ""
gameReversed = False
gameCounter = 0

loop = 0

def reverseGame():
    global gameReversed
    if gameReversed:
        gameReversed = False
    else:
        gameReversed = True

def getRandomCard(pullType="all"):
    if pullType == "all" and random.random() >= 0.1:
        return f"{random.choice(colors)}{random.choice(numbers + others)}{Color.default_text()}"
    elif pullType == "all":
        return f"{Color.text('#65350F')}{random.choice(jokers)}{Color.default_text()}"
    elif pullType == "num":
        return f"{random.choice(colors)}{random.choice(numbers)}{Color.default_text()}"

def setupGame():
    playerCount = input("enter player count: ")
    cardsPerPlayer = input("enter card count per player: ")
    if type(playerCount) != int:
        playerCount = 2
    if type(cardsPerPlayer) != int:
        cardsPerPlayer = 5

    setupPlayers(playerCount, cardsPerPlayer)

    global lastCard
    lastCard = getRandomCard("num")

def setupPlayers(playerCount, cardsPerPlayer):
    for i in range(playerCount):
        playerName = str(input(f"enter player{i}'s name: "))
        players[playerName] = [getRandomCard() for _ in range(cardsPerPlayer)]
        playerNames.append(playerName)

def printPlayerHand(playerName):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Color.text('#83a')}last played card: {Style.bold()}{lastCard}{Style.reset()}")
    print(f"{Style.bold()}{Color.text(random.choice(['#d9e9c4','#c4e9e6','#c4d5e9','#c4c5e9','#e4c4e9']))}{playerName}{Style.reset()}{Color.text('#83a')}'s turn{Style.reset()}\n")
    for counter in range(len(players[playerName])):
        print(f"{Style.bold()}{Color.text('#5cc')}{counter}: {players[playerName][counter]}{Style.reset()}")

def removeColor(card,returnType):
    colorCode, cardText = card.split("\x1b[")[1].split("m", 1)
    return "\x1b["+colorCode+"m" if returnType == "color" else cardText

def isCardPlayable(selectedCard):
    if removeColor(selectedCard,"color") == removeColor(lastCard,"color"):
        return True
    elif removeColor(selectedCard,"text") == removeColor(lastCard,"text"):
        return True
    elif removeColor(selectedCard,"text") in jokers:
        return removeColor(selectedCard,"text")
    else:
        return False

def getCardFromPlayer():
    global cardId

    playerInput = input("enter card number to chose: ")
    try:
        cardId = int(playerInput)
    except:
        print("please enter a valid number")
        getCardFromPlayer()

    if cardId > len(players[playerNames[gameCounter]]) or cardId < 0: #check is entered number is valid for the list length
        print("please enter a valid card id")
        getCardFromPlayer()

    chosenCard = players[playerNames[gameCounter]][cardId]     
    if isCardPlayable(chosenCard) == True or isCardPlayable(chosenCard) in jokers:
        global lastCard

        if not isCardPlayable(chosenCard) in jokers:
            lastCard = chosenCard

            Bin = players[playerNames[gameCounter]]
            del Bin[cardId]
            players[playerNames[gameCounter]] = Bin
            return

        if isCardPlayable(chosenCard) in jokers:
            Bin = players[playerNames[gameCounter]]
            del Bin[cardId]
            players[playerNames[gameCounter]] = Bin

            if chosenCard == "+4":
                print(f"0: {colors[0]}██\n1: {colors[1]}██\n2: {colors[2]}██\n3: {colors[3]}██")

                Pass = False
                while Pass:
                    try:
                        choice = int(input("please enter the color: "))
                    except:
                        print("please enter a valid choice")
                    if choice in [0,1,2,3]:
                        Pass = True
                lastCard = f"{colors[choice]}██"

                nextPlayer()

                Bin = players[playerNames[gameCounter]]
                Bin.append(getRandomCard())
                Bin.append(getRandomCard())
                Bin.append(getRandomCard())
                Bin.append(getRandomCard())
                players[playerNames[gameCounter]] = Bin

                nextPlayer()
                    
        

    else:
        global loop
        loop = 0
        checkPlayerCanPlay()
        printPlayerHand(playerNames[gameCounter])
        getCardFromPlayer()
        
def nextPlayer():
    global gameLoop
    global gameCounter
    if gameLoop:
        gameCounter += 1
    else:
        gameCounter -= 1
    if gameCounter > len(playerNames) - 1:
        gameCounter = 0
    if gameCounter < 0:
        gameCounter = len(playerNames) - 1

def checkPlayerCanPlay():
    global cardStates
    cardStates = []
    global gameCounter

    for i in range(len(players[playerNames[gameCounter]])):
        cardStates.append(isCardPlayable(players[playerNames[gameCounter]][i]))

    if True in cardStates or "joker" in cardStates:            # return true if player can play
        return True
    
    else:
        Bin = players[playerNames[gameCounter]]
        Bin.append(getRandomCard())
        players[playerNames[gameCounter]] = Bin          # add one card to player
        
        global loop
        loop += 1
        if loop > 2:
            nextPlayer()
            return True
        else:
            loop = 0
            checkPlayerCanPlay()
    

def game():
    setupGame()
    while gameLoop:
        
        global gameCounter
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Color.text('#83a')}last played card: {Style.bold()}{lastCard}{Style.reset()}")
        input(f"press ENTER to play {Color.text(random.choice(['#d9e9c4','#c4e9e6','#c4d5e9','#c4c5e9','#e4c4e9']))}{playerNames[gameCounter]}{Style.reset()}'s turn")
        os.system('cls' if os.name == 'nt' else 'clear')
        loop = 0
        checkPlayerCanPlay()
        printPlayerHand(playerNames[gameCounter])
        getCardFromPlayer()

        nextPlayer()
game()