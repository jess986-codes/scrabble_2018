from sys import stdin
import math
import sys
import random


TILES_USED = 0 # records how many tiles have been returned to user
CELL_WIDTH = 3 # cell width of the scrabble board
SHUFFLE = False # records whether to shuffle the tiles or not

# inserts tiles into myTiles
def getTiles(myTiles):
    global TILES_USED
    while len(myTiles) < 7 and TILES_USED < len(Tiles):
        myTiles.append(Tiles[TILES_USED])
        TILES_USED += 1


# prints tiles and their scores
def printTiles(myTiles):
    tiles = ""
    scores = ""
    for letter in myTiles:
        tiles += letter + "  "
        thisScore = getScore(letter)
        if thisScore > 9:
            scores += str(thisScore) + " "
        else:
            scores += str(thisScore) + "  "

    print("\nTiles : " + tiles)
    print("Scores: " + scores)


# gets the score of a letter
def getScore(letter):
    for item in Scores:
        if item[0] == letter:
            return item[1]

# initialize n x n Board with empty strings
def initializeBoard(n):
    Board = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append("")
        Board.append(row)

    return Board

# put character t before and after the string s such that the total length
# of the string s is CELL_WIDTH.
def getString(s,t):
    global CELL_WIDTH
    s = str(s)
    rem = CELL_WIDTH - len(s)
    rem = rem//2
    s = t*rem + s
    rem = CELL_WIDTH - len(s)
    s = s + t*rem
    return s

# print the Board on screen
def printBoard(Board):
    global CELL_WIDTH
    print("\nBoard:")
    spaces = CELL_WIDTH*" "
    board_str =  "  |" + "|".join(getString(item," ") for item in range(len(Board)))  +"|"
    line1 = "--|" + "|".join(getString("","-") for item in range(len(Board)))  +"|"


    print(board_str)
    print(line1)

    for i in range(len(Board)):
        row = str(i) + " "*(2-len(str(i))) +"|"
        for j in range(len(Board)):
            row += getString(Board[i][j]," ") + "|"
        print(row)
        print(line1)

    print()

scoresFile = open('scores.txt')
tilesFile = open('tiles.txt')

# read scores from scores.txt and insert in the list Scores
Scores = []
for line in scoresFile:
    line = line.split()
    letter = line[0]
    score = int(line[1])
    Scores.append([letter,score])
scoresFile.close()

# read tiles from tiles.txt and insert in the list Tiles
Tiles = []
for line in tilesFile:
    line= line.strip()
    Tiles.append(line)
tilesFile.close()

# decide whether to return random tiles
rand = input("Do you want to use random tiles (enter Y or N): ")
if rand == "Y":
    SHUFFLE = True
else:
    if rand != "N":
        print("You did not enter Y or N. Therefore, I am taking it as a Yes :P.")

if SHUFFLE:
    random.shuffle(Tiles)


validBoardSize = False
while not validBoardSize:
    BOARD_SIZE = input("Enter board size (a number between 5 to 15): ")
    if BOARD_SIZE.isdigit():
        BOARD_SIZE = int(BOARD_SIZE)
        if BOARD_SIZE >= 5 and BOARD_SIZE <= 15:
            validBoardSize = True
        else:
            print("Your number is not within the range.\n")
    else:
        print("Are you a little tipsy? I asked you to enter a number.\n")


Board = initializeBoard(BOARD_SIZE)
printBoard(Board)

myTiles = []
getTiles(myTiles)
printTiles(myTiles)

########################################################################
# Write your code below this
########################################################################

# Reads the data from a file and returns a list containing those items (\n removed)
# Assume that the player will not type anything greater than the maximum size of the board (max boardsize = 15)def readFromFile(filename):
def readFromFile(filename):
    fileList = []
    file = open(filename)
    for line in file:
        line = line.strip()
        if len(line) < 16:
            fileList.append(line)
    file.close()
    return fileList

# returns True if and only if target is in the collection (e.g., a string or a list)
def isIn(target, collection):
    for item in collection:
        if target == item:
            return True
    return False

# Checks if word can be formed by the given tiles
def validWord(word, myTiles):
    # create a copy of the tiles as we do not want to change myTiles
    backupTiles = myTiles.copy()
    for letter in word:
        if not isIn(letter,backupTiles):
            return False
        else:
            backupTiles.remove(letter)
    return True

# Checks if there are letters in the word that are already on the board (e.g. 'E' in 'NINE' is a tile on the board)
def letterInBoard(word):
    for letter in word:
        for item in Board:
            if letter in item:
                return True

# Checks if the word can be placed on the board (e.g. right location has been entered, is within the boundaries of the board
# and uses a previously placed tile on the board)
def checkBoard(word, location):
    # Ensures the row and column numbers are not negative
    row = abs(int(location[0]))
    col = abs(int(location[1]))
    n = len(word)
    # Counts how many previously placed tiles have been used
    letterUsedInBoard = 0
    boardLetters = ''
    myTilesCopy = myTiles.copy()

    temp = ''
    # If the move is horizontal, check if the last tile does not exceed the board by adding the length of the word
    # to the column number
    if 'H' in location and col + n <= BOARD_SIZE:
        for letter in word:
            if Board[row][col] == letter:
                letterUsedInBoard += 1
                boardLetters += letter
                col += 1
                temp += letter

            elif Board[row][col] == '' and isIn(letter, myTilesCopy):
                myTilesCopy.remove(letter)
                col += 1
                temp += letter
    # If the move is vertical, check if the last tile does not exceed the board by adding the length of the word
    # to the row number
    elif 'V' in location and row + n <= BOARD_SIZE:
        for letter in word:
            if Board[row][col] == letter:
                letterUsedInBoard += 1
                boardLetters += letter
                row += 1
                temp += letter

            elif Board[row][col] == '' and isIn(letter, myTilesCopy):
                myTilesCopy.remove(letter)
                row += 1
                temp += letter
    else:
        return False


    if temp == word and (letterUsedInBoard >= 1 or round == 1):
        return boardLetters
    else:
        return False

# Place the player's word on the board
def placeOnBoard(word, location):
    row = int(location[0])
    col = int(location[1])
    n = len(word)

    # Only place the tiles onto the board if the word has been checked and the move is valid
    if checkBoard(word, location) != False:
        if 'H' in location and col + n <= BOARD_SIZE:
            for letter in word:
                Board[row][col] = letter
                col += 1

        elif 'V' in location and row + n <= BOARD_SIZE:
            for letter in word:
                Board[row][col] = letter
                row += 1
    # If it is not a valid move, return False and do not place anything on the board
    else:
        return False

# Removes the tiles from the player's hand that have been used
def removeTiles(myTiles, word, tilesUsed):
    for letter in word:
        # Ensure the letters that have not been used and letters on the board that have been used are not removed
        if not isIn(letter, myTiles) or isIn(letter, tilesUsed):
            pass
        # Add to the list of letters that are available on the board so that they can be accounted for
        # the next round
        else:
            onBoard.append(letter)
            myTiles.remove(letter)
    return myTiles

# Calculates score of entire word
def total(word):
    score = 0
    for letter in word:
        score += getScore(letter)

    return score

#Calculates score of word excluding the tiles that have been used from the board
def calcuateScore(word, location):
    if checkBoard(word, location) != False:
        # Score of the tiles on the board is subtracted from the total score of the entire word
        score = total(word) - total(checkBoard(word, location))
        return score
    else:
        return 0

# Makes a list of all the possible words that can be made with the tiles on the board and from the player's hand
def possibleWords(availableTiles):
    possibleWords = []
    aList = []
    for item in dictionary:
        if validWord(item, availableTiles) == True and (letterInBoard(item) or round == 1):
            aList = [total(item), item]
            possibleWords.append(aList)
            aList = []

    # Sorts the list into ascending order of score to descending order of score (makes finding the best move
    # of the first round easier)
    possibleWords.sort()
    possibleWords.reverse()

    # Makes a sorted list of just the words and not the totals
    wordsList = []
    for words in possibleWords:
        wordsList.append(words[1])

    return wordsList

# Takes a letter as a parameter and finds all locations of it on the board in row : column form
def findLetterLocation(letter):
    # A list of all locations for that particular letter
    locationList = []
    col = 0
    for row in range(len(Board)):
        if letter in Board[row]:
            col = Board[row].index(letter)
            locationList.append([row, col])
    return locationList

# Finds which letters of the word are available on the board
def findLettersInBoard(word):
    inBoard = []

    for letter in word:
        for row in Board:
            if letter in row and letter not in inBoard:
                inBoard.append(letter)
    return inBoard

# Gets the best move
def getBestMove(availableTiles):
    # List of all the possible words for the current round
    myList = possibleWords(availableTiles)
    # Current maximum score found (continuously updated)
    maxScore = 0
    # Current location of best move
    location = ''
    # Current best word for the best move
    bestWord = ''

    # Loop through the entire list of possible words
    for word in myList:
        # If it is the first round, get the location of the middle tile
        if round == 1:
            middle = len(Board) // 2
            location1 = [middle, middle, 'H']
            # Check if placement of word is valid, if it is, break loop by returning the word and location
            if checkBoard(word, location1) != False:
                return word, location1

        # If it is not the first round, find which letters of the word are available on the board
        elif round != 1:
            # Loop through the list of words on the board and find their locations
            inBoard = findLettersInBoard(word)
            for letter in inBoard:
                locationList = findLetterLocation(letter)

                # If the number of locations of the letter found is greater than 1
                if len(locationList) > 1:
                    i = 0
                    # Loop through the list of locations (e.g. locationsList = [[3, 6], [4, 5], [7, 10]])
                    while i < len(locationList):
                        locationA = locationList[i]
                        locationB = locationA[:]
                        # Vertical location = subtract the index of the letter in the word from the row number location
                        locationA[0] = abs(locationA[0] - (word.index(letter)))
                        locationA += 'V'
                        # Horizontal location = subtract the index of the letter in the word from
                        # the column number location
                        locationB[1] = abs(locationB[1] - (word.index(letter)))
                        locationB += 'H'

                        # If the vertical placement is valid and has a greater score than the current max
                        # update best word, location and maximum score
                        if checkBoard(word, locationA) != False and calcuateScore(word, locationA) > maxScore:
                            bestWord = word
                            location = locationA
                            maxScore = calcuateScore(word, locationA)
                        # If the horizontal placement is valid and has a greater score than the current max
                        # update best word, location and maximum score
                        elif checkBoard(word, locationB) != False and calcuateScore(word, locationB) > maxScore:
                            bestWord = word
                            location = locationB
                            maxScore = calcuateScore(word, locationB)

                        # Otherwise go to the next location in the list or, if unable to, go to the next word
                        else:
                            i += 1

                # If the number of locations of the letter found is equal to 1, do the same with without the while loop
                elif len(locationList) == 1:
                    locationA = locationList[0]
                    locationB = locationA[:]
                    locationA[0] = abs(locationA[0] - (word.index(letter)))
                    locationA += 'V'
                    locationB[1] = abs(locationB[1] - (word.index(letter)))
                    locationB += 'H'

                    if checkBoard(word, locationA) != False and calcuateScore(word, locationA) > maxScore:
                        bestWord = word
                        location = locationA
                        maxScore = calcuateScore(word, locationA)
                    elif checkBoard(word, locationB) != False and calcuateScore(word, locationB) > maxScore:
                        bestWord = word
                        location = locationB
                        maxScore = calcuateScore(word, locationB)

    # After looping through the entire list, return the best word and location found
    return bestWord, location

dictionary  = readFromFile("dictionary.txt")

#++++++++++++++++##++++++++++++++++##++++++++++++++++##`
# - G----A----M----E ---------- S----T----A----R----T #
#++++++++++++++++##++++++++++++++++##++++++++++++++++##

keepplaying = True
keepasking = 'YEP'
round = 1
score = 0
# Tiles currently on the board
onBoard = []

while keepplaying == True:
    while keepasking == 'YEP':
        tilesUsed = []
        # letters the player can choose from to make a word (from myTiles and on the board)
        availableTiles = myTiles + onBoard
        word = input('\nEnter your word: ').upper()
        # Find  the best word and its position
        bestWord = getBestMove(availableTiles)
        bestPosition = bestWord[1]
        # Format location into string form (e.g. '1:5:H')
        bestPosition = '{}:{}:{}'.format(*bestPosition)
        # Calculate the score of the best move, excluding the score of the tiles on the board
        scoreOfBestMove = calcuateScore(bestWord[0], bestPosition.split(':'))

        # If the word only contains English letters, is in the dictionary and can be made with the available tiles
        # ask player to input location
        if word.isalpha() == True and isIn(word, dictionary) and validWord(word, availableTiles):
            location = input('Enter the location in row:col:direction format: ').split(':')

            # Calculates the location of the middle tile
            middle = str(len(Board) // 2)
            middleLocationH = [middle, middle, 'H']
            middleLocationV = [middle, middle, 'V']

            # If the location is not in digit:digit:alphabet form, print invalid
            if (location[0].isdigit() and location[1].isdigit() and location[2].isalpha()) == False:
                print('INVALID MOVE')

            # If round 1 and location entered is equivalent to middle location calculate score of move
            elif round == 1 and (location == middleLocationH or location == middleLocationV):
                scoreOfMove = calcuateScore(word, location)
                # Checks if valid and places tiles on board
                placeOnBoard(word, location)
                break

            # If round 1 but location entered is invalid, tell player the middle location
            elif round == 1 and location != middleLocationH and location != middleLocationV:
                print('The location for the first move must be ' + '{}:{}:{}'.format(*middleLocationH) + ' or ' +
                      '{}:{}:{}'.format(*middleLocationV))

            # If round is not 1, calculate score of move
            elif round != 1:
                # makes a list of the tiles that have been used in the board
                tilesUsed = checkBoard(word, location)
                scoreOfMove = calcuateScore(word, location)
                # Checks if valid and places tiles on board
                placeOnBoard(word, location)
                break

            else:
                print('INVALID MOVE!!')

        # If the player quits, break inner loop
        elif word == '***':
            break

        # If word is not valid, ask for input again
        else:
            print('INVALID MOVE!!')

    # If the player quits, break outer loop and stop game
    if word == '***':
        print('Better luck next time!')
        keepplaying = False

    # If the word has been placed on the board, therefore False has not been returned, print the board
    elif placeOnBoard(word, location) != False:
        printBoard(Board)
        # Update the total score by adding score of the current move
        score += scoreOfMove

        # If the score of the current move is not equivalent to the score of the best move, tell the player
        # the word, postion and score of the best move
        if scoreOfMove != scoreOfBestMove:
            print('Maximum possible score in this move was ' + str(scoreOfBestMove) + ' with the word ' + bestWord[0] + ' at ' + bestPosition)

        # If the score of the current move is equivalent to the best move, congratulate the player
        else:
            print('Your move was the best move. Well done!')

        print('Your score in this move: ' + str(scoreOfMove))
        print('Your total score is: ' + str(score))

        # Remove the tiles used from the player's hand
        removeTiles(myTiles, word, tilesUsed)
        getTiles(myTiles)
        printTiles(myTiles)
        round += 1

    # If the word have not been placed on the board, therefore False has been returned, print invalid and ask again
    else:
        print('INVALID MOVE!!')
