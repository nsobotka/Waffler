from viz import *
from boardGeneration import * 
from testBoards import *

# 5 letter word list
with open('5LetterWords.txt') as wordList:
    allWords = wordList.readlines()
    allWords = [line[:-1].upper() for line in allWords]

# Checks if the board is solved. If not add '?' into unsolved spots
def boardSolved(newPuzzle):
    returnVal = True
    for i in range(5):
        for j in range(5):
            if newPuzzle[i][j] == ' ' and ((i, j) != (1, 1) and (i, j) != (1, 3) and (i, j) != (3, 1) and (i, j) != (3, 3)):
                newPuzzle[i][j] = '?'
                returnVal = False
    return newPuzzle, returnVal

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

# solves for unknown solution
def solvePuzzle(p, color):
    possible_words = []
    possible_letters = []
    green_letters = []

    # fit possible words to greens and yellows for rows and cols
    def greens_yellows():
        # row words | green
        for r in range(0, 5, 2):
            greens = []
            greens_no_none = []
            for c in range(0, 5):
                if color[r][c][0] == '#6fb05c':
                    greens.append(p[r][c])
                    greens_no_none.append(p[r][c])
                else:
                    greens.append(None)
                    greens_no_none.append(' ')
            possible_words.append(fitGreens(greens))
            green_letters.append(greens_no_none)

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
            greens_no_none = []
            for r in range(0, 5):
                if color[r][c][0] == '#6fb05c':
                    greens.append(p[r][c])
                    greens_no_none.append(p[r][c])
                else:
                    greens.append(None)
                    greens_no_none.append(' ')
            possible_words.append(fitGreens(greens))
            green_letters.append(greens_no_none)

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

        # for w in range(6):
        possible_letters = [[], [], [], [], [], []]
        for i in range(6):
            possible_letters[i] = board_letters.copy()

        for r in range(5):
            for c in range(5):
                # This works under the assumption there is always green in the corners and centers.

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
                    elif (r, c) == (0, 2):
                        if not ((p[r][c] == p[4][1] and color[4][1][0] == '#e9ba3a') or (p[r][c] == p[4][3] and color[4][3][0] == '#e9ba3a')):
                            possible_letters[1].remove(p[r][c])
                            possible_letters[3].remove(p[r][c])
                            possible_letters[5].remove(p[r][c])
                    elif (r, c) == (4, 2):
                        if not ((p[r][c] == p[0][1] and color[0][1][0] == '#e9ba3a') or (p[r][c] == p[0][3] and color[0][3][0] == '#e9ba3a')):
                            possible_letters[1].remove(p[r][c])
                            possible_letters[3].remove(p[r][c])
                            possible_letters[5].remove(p[r][c])
                    elif (r, c) == (1, 2) or (r, c) == (3, 2):
                        if not ((p[r][c] == p[4][1] and color[4][1][0] == '#e9ba3a') or (p[r][c] == p[4][3] and color[4][3][0] == '#e9ba3a') or (p[r][c] == p[0][1] and color[0][1][0] == '#e9ba3a') or (p[r][c] == p[0][3] and color[0][3][0] == '#e9ba3a')):
                            possible_letters[1].remove(p[r][c])
                            possible_letters[3].remove(p[r][c])
                            possible_letters[5].remove(p[r][c])
                    elif (r, c) == (2, 0):
                        if not ((p[r][c] == p[1][4] and color[1][4][0] == '#e9ba3a') or (p[r][c] == p[3][4] and color[3][4][0] == '#e9ba3a')):
                            possible_letters[0].remove(p[r][c])
                            possible_letters[2].remove(p[r][c])
                            possible_letters[4].remove(p[r][c])
                    elif (r, c) == (2, 4):
                        if not ((p[r][c] == p[1][0] and color[1][0][0] == '#e9ba3a') or (p[r][c] == p[3][0] and color[3][0][0] == '#e9ba3a')):
                            possible_letters[0].remove(p[r][c])
                            possible_letters[2].remove(p[r][c])
                            possible_letters[4].remove(p[r][c])
                    elif (r, c) == (2, 1) or (r, c) == (2, 3):
                        if not ((p[r][c] == p[1][4] and color[1][4][0] == '#e9ba3a') or (p[r][c] == p[3][4] and color[3][4][0] == '#e9ba3a') or (p[r][c] == p[1][0] and color[1][0][0] == '#e9ba3a') or (p[r][c] == p[3][0] and color[3][0][0] == '#e9ba3a')):
                            possible_letters[0].remove(p[r][c])
                            possible_letters[2].remove(p[r][c])
                            possible_letters[4].remove(p[r][c])

        # Removes grey letters from possibilities in that row / column if there was not previously that same color that was yellow
        for r in range(5):
            for c in range(5):            
                if color[r][c][0] == '#edeff1':
                    if r == 0 or r == 2 or r == 4:
                        remove = True
                        for j in range(c):
                            if (color[r][j][0] == '#e9ba3a' and p[r][j] == p[r][c]):
                                remove = False
                        if remove:
                            possible_letters[int (r / 2)] = list(filter(lambda a: a != p[r][c], possible_letters[int (r / 2)]))
                    if c == 0 or c == 2 or c == 4:
                        remove = True
                        for j in range(r):
                            if (color[j][c][0] == '#e9ba3a' and p[j][c] == p[r][c]):
                                remove = False
                        if remove:
                            possible_letters[int (c / 2 + 3)] = list(filter(lambda a: a != p[r][c], possible_letters[int (c / 2 + 3)]))

        return possible_letters
    

    greens_yellows()
    possible_letters = require_board_letters()

    # Removes words that have letters that aren't originally in the board
    for i in range(6):
        newList = []
        for word in possible_words[i]:
            remove_word = False
            for letter in range(5):
                if word[letter] not in possible_letters[i] and word[letter] != green_letters[i][letter]:
                    remove_word = True
                    break
            if remove_word == False:
                newList.append(word)
        possible_words[i] = newList

    # Removes words that have letters in a yellow spot
    for r in range(5):
        for c in range(5):
            if color[r][c][0] == '#e9ba3a':
                if r == 0:
                    newList = []
                    for word in possible_words[0]:
                        if word[c] != p[r][c]:
                            newList.append(word)
                    possible_words[0] = newList
                elif r == 2:
                    newList = []
                    for word in possible_words[1]:
                        if word[c] != p[r][c]:
                            newList.append(word)
                    possible_words[1] = newList
                elif r == 4:
                    newList = []
                    for word in possible_words[2]:
                        if word[c] != p[r][c]:
                            newList.append(word)
                    possible_words[2] = newList
                if c == 0:
                    newList = []
                    for word in possible_words[3]:
                        if word[r] != p[r][c]:
                            newList.append(word)
                    possible_words[3] = newList
                elif c == 2:
                    newList = []
                    for word in possible_words[4]:
                        if word[r] != p[r][c]:
                            newList.append(word)
                    possible_words[4] = newList
                elif c == 4:
                    newList = []
                    for word in possible_words[5]:
                        if word[r] != p[r][c]:
                            newList.append(word)
                    possible_words[5] = newList
                                

    # Loops over various methods to remove words from the possibilities
    Change = True
    while Change:
        try: 
            all_letters = [letter for row in p for letter in row if letter != ' ']
            Change = False
            newPuzzle = [[' '] * 5 for i in range(5)]
            # Checks what rows / columns have only one option, and then what letters only have one option
            # Creates a new board with these filled in
            for i in range(6):
                if len(possible_words[i]) == 1:
                    if i < 3: 
                        newPuzzle[i * 2] = [x for x in possible_words[i][0]]
                    else:
                        for j in range(5):
                            newPuzzle[j][(i - 3) * 2] = possible_words[i][0][j]
                else: 
                    for j in range(5):
                        letter = possible_words[i][0][j]
                        sameLetter = True
                        for word in possible_words[i]:
                            if word[j] != letter:
                                sameLetter = False
                        if sameLetter:
                            if i < 3:
                                newPuzzle[i * 2][j] = letter
                            else:
                                newPuzzle[j][(i - 3) * 2] = letter

            # Removes words if they can't fit with the words already guaranteed to be correct
            for i in range(6):
                if len(possible_words[i]) != 1:
                    if i < 3:
                        newWords = []
                        for word in possible_words[i]:
                            remove_word = False
                            for j in range(5):
                                if word[j] != newPuzzle[i * 2][j] and newPuzzle[i * 2][j] != ' ':
                                    remove_word = True
                                    break
                            if not remove_word:
                                newWords.append(word)
                            else: 
                                Change = True
                        possible_words[i] = newWords
                    else: 
                        newWords = []
                        for word in possible_words[i]:
                            remove_word = False
                            for j in range(5):
                                if word[j] != newPuzzle[j][(i - 3) * 2] and newPuzzle[j][(i - 3) * 2] != ' ':
                                    remove_word = True
                                    break
                            if not remove_word:
                                newWords.append(word)
                            else: 
                                Change = True
                        possible_words[i] = newWords
            
            used_letters = [letter for row in newPuzzle for letter in row if letter != ' ']
            # Updates all letters to only have unused letters
            for i in used_letters:
                all_letters.remove(i)

            # Removes words if they have letters that don't exist in the board
            for i in range(6):
                if len(possible_words[i]) > 1:
                    new_possible_words = []
                    for word in possible_words[i]:
                        possible = True
                        for j in range(5):
                            if i < 3:
                                if word[j] not in all_letters and newPuzzle[i * 2][j] == ' ':
                                    possible = False
                                    break
                            else:
                                if word[j] not in all_letters and newPuzzle[j][(i - 3) * 2] == ' ':
                                    possible = False
                                    break
                        if possible:
                            new_possible_words.append(word)
                        else:
                            Change = True
                    possible_words[i] = new_possible_words

            # Removes words if the letters cannot fit in the intersections
            for i in range(6):
                if len(possible_words[i]) > 1:
                    new_possible_words = []
                    for word in possible_words[i]:
                        possible1 = False
                        possible2 = False
                        possible3 = False
                        if i < 3:
                            for other_word in possible_words[3]:
                                if other_word[i * 2] == word[0]:
                                    possible1 = True
                            for other_word in possible_words[4]:
                                if other_word[i * 2] == word[2]:
                                    possible2 = True
                            for other_word in possible_words[5]:
                                if other_word[i * 2] == word[4]:
                                    possible3 = True
                        else:
                            for other_word in possible_words[0]:
                                if other_word[(i - 3) * 2] == word[0]:
                                    possible1 = True
                            for other_word in possible_words[1]:
                                if other_word[(i - 3) * 2] == word[2]:
                                    possible2 = True
                            for other_word in possible_words[2]:
                                if other_word[(i - 3) * 2] == word[4]:
                                    possible3 = True
                        if possible1 and possible2 and possible3:
                            new_possible_words.append(word)
                        else:
                            Change = True
                    possible_words[i] = new_possible_words

            # Updating the board
            for i in range(6):
                if len(possible_words[i]) == 1:
                    if i < 3: 
                        newPuzzle[i * 2] = [x for x in possible_words[i][0]]
                    else:
                        for j in range(5):
                            newPuzzle[j][(i - 3) * 2] = possible_words[i][0][j]
                else: 
                    for j in range(5):
                        letter = possible_words[i][0][j]
                        sameLetter = True
                        for word in possible_words[i]:
                            if word[j] != letter:
                                sameLetter = False
                        if sameLetter:
                            if i < 3:
                                newPuzzle[i * 2][j] = letter
                            else:
                                newPuzzle[j][(i - 3) * 2] = letter

            all_letters = [letter for row in p for letter in row if letter != ' ']
            used_letters = [letter for row in newPuzzle for letter in row if letter != ' ']
            # Updates all letters to only have unused letters
            for i in used_letters:
                all_letters.remove(i)

            # If only one word can use a letter, that word must be correct
            for letter in all_letters:
                if letter not in all_letters:
                    continue
                count = 0
                location = (-1, -1)
                savedWord = ''
                oldI = -1
                for i in range(6):
                    if len(possible_words[i]) > 1:
                        for word in possible_words[i]:
                            for j in range(5):
                                if i < 3:
                                    if newPuzzle[i * 2][j] == ' ':
                                        if word[j] == letter:
                                            if (i * 2, j) != location or i == oldI:
                                                count = count + 1
                                                location=  (i * 2, j)
                                                savedWord = word
                                                oldI = i
                                else: 
                                    if newPuzzle[j][(i - 3) * 2] == ' ':
                                        if word[j] == letter:
                                            if (j, (i - 3) * 2) != location or i == oldI:
                                                count = count + 1
                                                location = (j, (i - 3) * 2)
                                                savedWord = word
                                                oldI = i
                if count == 1:
                    if oldI < 3: 
                        newPuzzle[oldI * 2] = [x for x in savedWord]
                    else:
                        for j in range(5):
                            newPuzzle[j][(oldI - 3) * 2] = savedWord[j]
                    new_possible_words = []
                    new_possible_words.append(savedWord)
                    possible_words[oldI] = new_possible_words
                    Change = True
                    all_letters = [letter for row in p for letter in row if letter != ' ']
                    used_letters = [letter for row in newPuzzle for letter in row if letter != ' ']
                    for i in used_letters:
                        all_letters.remove(i)
            # If a word needs multiple letters but there aren't enough of all of the letters
            for i in range(6):
                if len(possible_words[i]) > 1:
                    new_possible_words = []
                    for word in possible_words[i]:
                        possible = True
                        all_letters_copy = all_letters.copy()
                        if i < 3:
                            for letter in range(5):
                                if newPuzzle[i * 2][letter] == ' ':
                                    if word[letter] in all_letters_copy:
                                        all_letters_copy.remove(word[letter])
                                    else: 
                                        possible = False
                        else:
                            for letter in range(5):
                                if newPuzzle[letter][(i - 3) * 2] == ' ':
                                    if word[letter] in all_letters_copy:
                                        all_letters_copy.remove(word[letter])
                                    else: 
                                        possible = False
                        if possible:
                            new_possible_words.append(word)
                        else:
                            Change = True
                    possible_words[i] = new_possible_words
        except:
            break 

    # viz(newPuzzle)
    newPuzzle, val = boardSolved(newPuzzle)
    return newPuzzle, val