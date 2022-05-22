import random, math

# 5 letter word list
with open('5LetterWords.txt') as wordList:
    allWords = wordList.readlines()
    allWords = [line[:-1] for line in allWords]

# forces words into crossword
def constrainedWords(a, b, c):
    l = []

    for w in allWords:
        if w[0] == a and w[2] == b and w[4] == c:
            l.append(w)

    return l

def isDuplicateWord(l, word):
    return word in l

# attempts to find a valid set of 6 words
# returns -1 if there is no valid word, otherwise returns a set of 6 words.
def generatePuzzle():
    words = []

    # picks three distinct random 5 letter words
    firstWord = random.choice(allWords)
    words.append(firstWord)

    secondWord = random.choice(allWords)
    while(isDuplicateWord(words, secondWord)):
        secondWord = random.choice(allWords)
    
    words.append(secondWord)
    
    thirdWord = random.choice(allWords)

    while(isDuplicateWord(words, thirdWord)):
        thirdWord = random.choice(allWords)
    
    words.append(thirdWord)

    # picks 3 more vertical words that fit with the horizontals
    fourthList = constrainedWords(firstWord[0], secondWord[0], thirdWord[0])
    if (len(fourthList) == 0):
        return -1

    fourthWord = random.choice(fourthList)
    tracker = True
    if len(fourthList) <= 3:
        for i in fourthList:
            if i not in words:
                tracker = False
    if tracker and len(fourthList) <= 3:
        return -1

    while(isDuplicateWord(words, fourthWord)):
        fourthWord = random.choice(fourthList)
    words.append(fourthWord)
    
    fifthList = constrainedWords(firstWord[2], secondWord[2], thirdWord[2])
    if (len(fifthList) == 0):
        return -1

    tracker = True
    if len(fifthList) <= 4:
        for i in fifthList:
            if i not in words:
                tracker = False
    if tracker and len(fifthList) <= 4:
        return -1

    fifthWord = random.choice(fifthList)
    while(isDuplicateWord(words, fifthWord)):
        fifthWord = random.choice(fifthList)
    words.append(fifthWord)

    sixthList = constrainedWords(firstWord[4], secondWord[4], thirdWord[4])
    if (len(sixthList) == 0):
        return -1

    tracker = True
    if len(sixthList) <= 5:
        for i in sixthList:
            if i not in words:
                tracker = False
    if tracker and len(sixthList) <= 5:
        return -1

    sixthWord = random.choice(sixthList)
    while(isDuplicateWord(words, sixthWord)):
        sixthWord = random.choice(sixthList)
    words.append(sixthWord)

    return([word.upper() for word in words])

# visualizer
def viz(p):
    for row in p:
        print(f"{row}\n")


# creates the puzzle by running generate puzzle until success
def getPuzzle():
    p = generatePuzzle()
    while (p == -1):
        p = generatePuzzle()

    # builds 2d array
    letterArr = [[" "] * 5 for i in range(5)]

    letterArr[0] = [l for l in p[0]]
    letterArr[2] = [l for l in p[1]]
    letterArr[4] = [l for l in p[2]]
    
    for i in range(0, 5):
        letterArr[i][0] = p[3][i]

    for i in range(0, 5):
        letterArr[i][2] = p[4][i]

    for i in range(0, 5):
        letterArr[i][4] = p[5][i]
    
    # prints out visualization
    return letterArr

# creates unsolved board using solved board

# NEEDS WORK - limit greens and yellows, perhaps make it more like the real waffle?
def scramble(solved):
    p = [row[:] for row in solved]
    moves = []
    pickedSquares = []
    numPicked = 0
    # makes 10 random distinct moves
    for i in range(0, 10): 
        # finds positions to swap
        checker = True
        while checker:
            # picks two coordinates
            coord1 = random.choice([i for i in range(0,25) if i not in [0,4,6,8,12,16,18,20,24]])
            while numPicked < 14 and coord1 in pickedSquares: 
                coord1 = random.choice([i for i in range(0,25) if i not in [0,4,6,8,12,16,18,20,24]])

            coord2 = random.choice([i for i in range(0,25) if i not in [0,4,6,8,12,16,18,20,24]])
            while (coord1 == coord2) or (p[math.floor(coord1 / 5)][coord1 % 5] == p[math.floor(coord2 / 5)][coord2 % 5]) or (numPicked < 14 and coord2 in pickedSquares):
                coord2 = random.choice([i for i in range(0,25) if i not in [0,4,6,8,12,16,18,20,24]])
            
            if coord1 < coord2: 
                temp = coord1
                coord1 = coord2
                coord2 = temp
            newTuple = ((coord1, p[math.floor(coord1 / 5)][coord1 % 5]), 
            (coord2, p[math.floor(coord2 / 5)][coord2 % 5]))
            if newTuple not in moves:
                checker = False

        if coord1 not in pickedSquares:
            numPicked = numPicked + 1
        if coord2 not in pickedSquares:
            numPicked = numPicked + 1
        pickedSquares.append(coord1)
        pickedSquares.append(coord2)
        moves.append(newTuple)

        # swaps the characters
        tempChar = p[math.floor(coord1 / 5)][coord1 % 5]
        p[math.floor(coord1 / 5)][coord1 % 5] = p[math.floor(coord2 / 5)][coord2 % 5]
        p[math.floor(coord2 / 5)][coord2 % 5] = tempChar
        
    return p

# gets all values in a column
def getCol(col, arr):
    return [x[col] for x in arr]

# compares given board to correct board
# 0 = green, 1 = yellow, 2 = grey, 3 = not used
def getStates(correct, curr):
    p = [row[:] for row in correct]
    q = [row[:] for row in correct]
    states = [[2] * 5 for i in range(5)]
    for i in range(0, 5):
        for j in range(0, 5):
            if curr[i][j] == " ": 
                states[i][j] = 3
                p[i][j] = " "
                q[i][j] = " "
            elif curr[i][j] == correct[i][j]:
                states[i][j] = 0
                p[i][j] = " "
                q[i][j] = " "
    
    for i in range(0, 5):
        for j in range(0, 5):
            if i % 2 == 0 and curr[i][j] in p[i] and states[i][j] == 2:
                removeCounter = 0
                for k in range(0, 5):
                    if p[i][k] == curr[i][j] and removeCounter == 0:
                        p[i][k] = " "
                        removeCounter = 1
                states[i][j] = 1
            
    for j in range(0, 5):
        for i in range(0, 5):
            if j % 2 == 0 and curr[i][j] in getCol(j, q) and states[i][j] == 2:
                removeCounter = 0
                for k in range(0, 5):
                    if q[k][j] == curr[i][j] and removeCounter == 0:
                        q[k][j] = " "
                        removeCounter = 1
                states[i][j] = 1
    
    draggable = [row[:] for row in correct]
    numGreen = 0
    for i in range(0, 5):
        for j in range(0, 5):
            if states[i][j] == 0:
                draggable[i][j] = "false"
                states[i][j] = ('#6fb05c', '#FFFFFF')
                numGreen = numGreen + 1
            elif states[i][j] == 1: 
                draggable[i][j] = "true"
                states[i][j] = ('#e9ba3a', '#FFFFFF')
            else:
                draggable[i][j] = "true"
                states[i][j] = ('#edeff1', '#000000')

    return states, draggable, numGreen

# solves for unknown solution
def solvePuzzle(p):
    return

# print("-----")
# solvedPuzzle = getPuzzle()
# viz(solvedPuzzle)
# scrambledPuzzle = scramble(solvedPuzzle)
# print("-----")
# viz(scrambledPuzzle)
# states = getStates(solvedPuzzle, scrambledPuzzle)
# print("-----")
# viz(states)
# print("-----")

# solvedTest = [[" "] * 5 for i in range(5)]
# solvedTest = [['a', 'b', 'y', 'c', 'a'], ['d', ' ', 'l', ' ', 'b'], ['e', 'e', 'k', 'x', 'h'], 
# ['f', ' ', 'm', ' ', 'i'], ['g', 'o', 'n', 'o', 'j']]
# scrambledTest = [['a', 'a', 'f', 'a', 'b'], ['g', ' ', 'l', ' ', 'f'], ['d', 'f', 'h', 'e', 'f'], 
# ['d', ' ', 'e', ' ', 'f'], ['b', 'o', 'n', 'g', 'f']]
# statesTest = getStates(solvedTest, scrambledTest)
# print("-----")
# viz(solvedTest)
# print("-----")
# viz(scrambledTest)
# print("-----")
# viz(statesTest)
# print("-----")
