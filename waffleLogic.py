import random

with open('5LetterWords.txt') as wordList:
    allWords = wordList.readlines()
    allWords = [line[:-1] for line in allWords]


def constrainedWords(a, b, c):
    l = []

    for w in allWords:
        if w[0] == a and w[2] == b and w[4] == c:
            l.append(w)

    return l

def isDuplicateWord(l, word):
    return word in l

def generatePuzzle():
    words = []

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

    fourthList = constrainedWords(firstWord[0], secondWord[0], thirdWord[0])
    if (len(fourthList) == 0):
        return -1

    fourthWord = random.choice(fourthList)
    while(isDuplicateWord(words, fourthWord)):
        fourthWord = random.choice(fourthList)
    words.append(fourthWord)

    fifthList = constrainedWords(firstWord[2], secondWord[2], thirdWord[2])
    if (len(fifthList) == 0):
        return -1

    fifthWord = random.choice(fifthList)
    while(isDuplicateWord(words, fifthWord)):
        fifthWord = random.choice(fifthList)
    words.append(fifthWord)

    sixthList = constrainedWords(firstWord[4], secondWord[4], thirdWord[4])
    if (len(sixthList) == 0):
        return -1

    sixthWord = random.choice(sixthList)
    while(isDuplicateWord(words, sixthWord)):
        sixthWord = random.choice(sixthList)
    words.append(sixthWord)

    return(words)

def viz(p):
    for row in p:
        print(f"{row}\n")


def getPuzzle():
    p = generatePuzzle()
    while (p == -1):
        p = generatePuzzle()

    print(p)

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
    
    viz(letterArr)

getPuzzle()