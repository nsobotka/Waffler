import random, math
from turtle import pos

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

# fit greens to word
def fitGreens(greens):
    l = []
    for w in allWords:
        if ((w[0] == greens[0] or greens[0] is None) and
            (w[1] == greens[1] or greens[1] is None) and
            (w[2] == greens[2] or greens[2] is None) and
            (w[3] == greens[3] or greens[3] is None) and
            (w[4] == greens[4] or greens[4] is None)):
            l.append(w)

    return l

# positions 2 and 4
def fitYellows(yellows, l):
    newList = []

    for w in l:
        flag = True
        for y in yellows:
            if y not in w:
                flag = False
        if flag: newList.append(w)

    return newList

def viz_solutions(l):
    for i in range(len(l)):
        if i < 3:
            print(f'row {i + 1} {l[i]} \n \n')
        else:
            print(f'col {i - 2} {l[i]} \n \n')

# solves for unknown solution
def solvePuzzle(p, color):
    possible_words = []

    # fit possible words to greens and yellows for rows and cols
    def greens_yellows():
        # row words | green
        for r in range(0, 5, 2):
            greens = []
            for c in range(0, 5):
                if color[r][c][0] == '#6fb05c':
                    greens.append(p[r][c])
                else:
                    greens.append(None)
            possible_words.append(fitGreens(greens))

        # row words | yellow
        for r in range(0, 5, 2):
            yellow = []
            for c in range(1, 4, 2):
                if color[r][c][0] == '#e9ba3a':
                    yellow.append(p[r][c])
            possible_words[int(r / 2)] = fitYellows(yellow, possible_words[int(r / 2)])

        # column words | green
        for c in range(0, 5, 2):
            greens = []
            for r in range(0, 5):
                if color[r][c][0] == '#6fb05c':
                    greens.append(p[r][c])
                else:
                    greens.append(None)
            possible_words.append(fitGreens(greens))

        # column words | yellow
        for c in range(0, 5, 2):
            yellow = []
            for r in range(1, 4, 2):
                if color[r][c][0] == '#e9ba3a':
                    yellow.append(p[r][c])
            possible_words[int(c / 2) + 3] = fitYellows(yellow, possible_words[int(c / 2) + 3])

    def require_board_letters():
        # get non-empty letters
        board_letters = [letter for row in p for letter in row if letter != ' ']
        
        # remove greens
        for r in range(5):
            for c in range(5):
                if color[r][c][0] == '#6fb05c':
                    board_letters.remove(p[r][c])

        # print(board_letters)

        # for w in range(6):
        possible_letters = [[], [], [], [], [], []]
        possible_letters[0] = board_letters.copy()
        possible_letters[1] = board_letters.copy()
        possible_letters[2] = board_letters.copy()
        possible_letters[3] = board_letters.copy()
        possible_letters[4] = board_letters.copy()
        possible_letters[5] = board_letters.copy()

        for r in range(5):
            for c in range(5):
    # This works under the assumption there is always green in the corners and centers.
                if (r, c) != (0, 0) and (r, c) != (4, 0) and (r, c) != (0, 4) and (r, c) != (4, 4) and (r, c) != (2, 2):
                    # deals with yellow letters
                    if color[r][c][0] == '#e9ba3a':
                        if (r, c) == (0, 1) or (r, c) == (0, 3):
                            possible_letters[1].remove(p[r][c])
                            possible_letters[2].remove(p[r][c])
                            possible_letters[3].remove(p[r][c])
                            possible_letters[5].remove(p[r][c])
                        elif (r, c) == (1, 0) or (r, c) == (3, 0):
                            possible_letters[0].remove(p[r][c])
                            possible_letters[2].remove(p[r][c])
                            possible_letters[4].remove(p[r][c])
                            possible_letters[5].remove(p[r][c])
                        elif (r, c) == (4, 1) or (r, c) == (4, 3):
                            possible_letters[0].remove(p[r][c])
                            possible_letters[1].remove(p[r][c])
                            possible_letters[3].remove(p[r][c])
                            possible_letters[5].remove(p[r][c])
                        elif (r, c) == (1, 4) or (r, c) == (3, 4):
                            possible_letters[0].remove(p[r][c])
                            possible_letters[2].remove(p[r][c])
                            possible_letters[3].remove(p[r][c])
                            possible_letters[4].remove(p[r][c])
                        elif (r, c) == (0, 2) or (r, c) == (1, 2) or (r, c) == (3, 2) or (r, c) == (4, 2):
                            possible_letters[1].remove(p[r][c])
                            possible_letters[3].remove(p[r][c])
                            possible_letters[5].remove(p[r][c])
                        elif (r, c) == (2, 0) or (r, c) == (2, 1) or (r, c) == (2, 3) or (r, c) == (2, 4):
                            possible_letters[0].remove(p[r][c])
                            possible_letters[2].remove(p[r][c])
                            possible_letters[4].remove(p[r][c])

        for r in range(5):
            for c in range(5):            
                # removes grey letters from the possibilites in that row / column
                if color[r][c][0] == '#edeff1':
                    if r == 0 or r == 2 or r == 4:
                        possible_letters[int (r / 2)] = list(filter(lambda a: a != p[r][c], possible_letters[int (r / 2)]))
                    if c == 0 or c == 2 or c == 4:
                        possible_letters[int (c / 2 + 3)] = list(filter(lambda a: a != p[r][c], possible_letters[int (c / 2 + 3)]))
    
        return possible_letters

    greens_yellows()
    # require_board_letters()
    viz_solutions(require_board_letters())

    # viz_solutions(possible_letters)
    
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


scrambled = [['v', 'l', 'e', 's', 'e'], 
             ['t', ' ', 'r', ' ', 'a'],
             ['r', 's', 'l', 'e', 'u'],
             ['i', ' ', 'g', ' ', 'e'],
             ['a', 'a', 's', 'r', 'y']]

color = [[('#6fb05c', '#FFFFFF'), ('#edeff1', '#000000'), ('#e9ba3a', '#FFFFFF'), ('#edeff1', '#000000'), ('#6fb05c', '#FFFFFF')], 
         [('#e9ba3a', '#FFFFFF'), ' ', ('#e9ba3a', '#FFFFFF'), ' ', ('#e9ba3a', '#FFFFFF')],
         [('#edeff1', '#000000'), ('#e9ba3a', '#FFFFFF'), ('#6fb05c', '#FFFFFF'), ('#e9ba3a', '#FFFFFF'), ('#edeff1', '#000000')],
         [('#e9ba3a', '#FFFFFF'), ' ', ('#edeff1', '#000000'), ' ', ('#edeff1', '#000000')],
         [('#6fb05c', '#FFFFFF'), ('#e9ba3a', '#FFFFFF'), ('#edeff1', '#000000'), ('#e9ba3a', '#FFFFFF'), ('#6fb05c', '#FFFFFF')]]

solvePuzzle(scrambled, color)

solved =[['v', 'e', 'r', 'g', 'e'], 
         ['i', ' ', 'u', ' ', 's'],
         ['s', 'e', 'l', 'l', 's'],
         ['t', ' ', 'e', ' ', 'a'],
         ['a', 'r', 'r', 'a', 'y']]

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