import sys
import random


TILES_USED = 0 # records how many tiles have been returned to user
SHUFFLE = False # records whether to shuffle the tiles or not

# inserts tiles into myTiles
def getTiles(myTiles):
    global TILES_USED
    while len(myTiles) < 7  and TILES_USED < len(Tiles):
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
    line = line.strip()
    Tiles.append(line)
tilesFile.close()

# decide whether to return random tiles
rand = input("Do you want to use random tiles (enter Y or N): ")
if rand == "Y":
    SHUFFLE = True
else:
    if rand != "N":
        print("You did not enter Y or N. Therefore, I am taking it as a Yes :P.")
        SHUFFLE = True
        
if SHUFFLE:
    random.shuffle(Tiles)


myTiles = []
getTiles(myTiles)
printTiles(myTiles)

########################################################################
# Write your code below this
########################################################################

dictionaryFile = open('dictionary.txt')
# Puts contents the dictionary file into a list
# Only words of len(myTiles) are appended to decrease running time during a search
# Assume that the player will not type anything greater than the number of tiles they have
dictionary = []
for item in dictionaryFile:
    item = item.replace('\n', '')
    if len(item) < 8:
        dictionary.append(item)

dictionaryFile.close()


# Checks if word exists in dictionary
def dictSearch(word):
    for term in dictionary:
        if word == term:
            return True
        

# Checks if word can be formed by the given tiles
def validWord(letters):
    alphabet = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0,
            'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0,
            'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0,
            'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0,
            'Y': 0, 'Z': 0
            }

    # Counts the number of each letter available in myTiles
    for tile in myTiles:        
        for key in alphabet:
            # adds 1 to the value of found letter in alphabet
            if tile == key:
                alphabet[key] += 1
                
    # if a letter in the player's word equates to an available letter in
    # alphabet, minus 1 from the value of that letter in alphabet
    tmp = []
    for letter in letters:
        for key in alphabet:
            if letter == key and alphabet[key] > 0:
                alphabet[key] -= 1
                tmp.append(letter)

    # If the strin of tmp equals the player's word, return True
    if ''.join(tmp) == letters:
        return True
    else:
        return False


# Calculates score
def total(word):
    count = 0
    for line in Scores:
        letter = line[0]
        score = line[1]
        for i in word:
            if letter == i:
                count += score
    return count


# Finds the word with the highest score for the given tiles
def highestScore(userWord):
    bestWord = userWord
    hiScore = total(userWord)
    for text in dictionary:
        # If word in dictionary is valid and higher than the player's
        # reassign hiScore and bestWord
        if validWord(text) and total(text) > hiScore:
            hiScore = total(text)
            bestWord = text
    return bestWord



# Game start
keepplaying = True
keepasking = 'YEP'

# While keepplaying stays True, keep running scrabble game
while keepplaying == True:
    
    # While keepasking remains 'YEP', keep prompting the player
    # to enter a word until they quit or enter a valid word
    while keepasking == 'YEP':
        word = input('\nEnter a word: ')
        word = word.upper()
        # Checks if word only contains English letters
        if word.isalpha() == True:

            # If word is in dictionary and can be made with tiles break keepasking loop
            # and calculate score
            if dictSearch(word) and validWord(word):
                print('Cool, this is a valid word.')
                print('Score for the word ' + word + ' is: ', total(word))
                break

            # If word is in dictionary but cannot be made with tiles go to start of loop
            elif dictSearch(word) and validWord(word) == False:
                print('This word cannot be made with your tiles.')

            # If word is not valid at all, go to start of loop
            else:
                print('I have never heard of this word.')

        # If the player quits, break loop
        elif word == '***':
            print('Better luck next time!')
            break

        # If word does not contain English letters, go to start of loop
        else:
            print('Only use English letters!!')

    
    # Prints out the highest scoring word
    if highestScore(word) != '***':
        print('\n' + str(highestScore(word)), 'has the highest score of', str(total(highestScore(word))) + '.')
    else:
        print('No word can be made using these tiles.')

    # Checks if the player wants to keep playing
    rand = input("Do you want to keep playing? (enter Y or N): ")
    # If player enters 'Y', keeplaying is True and SHUFFLE is true
    if rand == 'Y':
        keepplaying = True
        SHUFFLE = True

    # If player does not enter 'Y' or 'N', make keepplaying True and SHUFFLE True
    elif rand != 'N':
        print("You did not enter Y or N. Therefore, I am taking it as a Yes :P.")
        keepplaying = True
        SHUFFLE = True

    # If player enters 'N', end game completely
    else:
        if rand == 'N':
            keepplaying = False
            SHUFFLE = False

    # If player wants to keepplaying, shuffle tiles and print tiles
    if SHUFFLE == True:
        random.shuffle(Tiles)
        myTiles = []
        getTiles(myTiles)
        printTiles(myTiles)



    
