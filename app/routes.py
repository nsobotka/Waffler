from flask import render_template, request, redirect, url_for
from app import app
from waffleLogic import *
from scrape import *
from viz import *
from boardGeneration import * 
from testBoards import *
from shortestPath import *

# Things to do: 
# publish to website
    # erase this checklist 
    # multiple players at once
    # add link to readme
# reach out to waffle man

class puzzle:
    def __init__(self):
        self.solvedPuzzle = getPuzzle()
        self.scrambledPuzzle = scramble(solvedPuzzle)
        while(len(main(scrambledPuzzle, solvedPuzzle)) != 10):
                self.scrambledPuzzle = scramble(solvedPuzzle)
        self.scrambledPuzzleUnmodified = [row[:] for row in scrambledPuzzle]
        self.states, self.draggable, self.numGreen = getStates(solvedPuzzle, scrambledPuzzle)
        self.swaps = 15
        self.official_puzzle = 0
        self.solvable = 1
        self.movesList = [(('', ''), ('', ''))] * 15
        self.shown = 0
        self.tableColor = ['#6fb05c'] * 15

    def getAll(self):
        return (solvedPuzzle, scrambledPuzzle, scrambledPuzzleUnmodified, states, draggable, numGreen, swaps, official_puzzle, solvable, movesList, shown, tableColor)

# Splash page
@app.route('/')
def splash():
    p = puzzle()
    return index(p)

# Main page
@app.route('/index', methods = ['GET'])
def index(p):
    # p = puzzle()
    solvedPuzzle, scrambledPuzzle, scrambledPuzzleUnmodified, states, draggable, numGreen, swaps, official_puzzle, solvable, movesList, shown, tableColor = p.getAll()
    return render_template('index.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList, shown = shown, tableColor = tableColor)

# New board
@app.route('/newBoard', methods = ['POST'])
def newBoard():
    p = puzzle()
    return index(p)

# Swap two pieces
@app.route('/swap', methods = ['GET', 'POST'])
def swap(p):
    box1 = request.form['box1']
    box2 = request.form['box2']
    if len(box1) == 4:
        coord1 = int(box1[3]) - 1
    else: 
        coord1 = int(box1[3]) * 10 + int(box1[4]) - 1
    if len(box2) == 5:
        coord2 = int(box2[3]) * 10 + int(box2[4]) - 1
    else: 
        coord2 = int(box2[3]) - 1
    tempChar = p.scrambledPuzzle[math.floor(coord1 / 5)][coord1 % 5]
    p.scrambledPuzzle[math.floor(coord1 / 5)][coord1 % 5] = p.scrambledPuzzle[math.floor(coord2 / 5)][coord2 % 5]
    p.scrambledPuzzle[math.floor(coord2 / 5)][coord2 % 5] = tempChar
    p.states, p.draggable, p.numGreen = getStates(p.solvedPuzzle, p.scrambledPuzzle)
    if p.movesList[15 - p.swaps] != (((coord2 + 1, p.scrambledPuzzle[math.floor(coord1 / 5)][coord1 % 5]), (coord1 + 1, p.scrambledPuzzle[math.floor(coord2 / 5)][coord2 % 5]))):
        p.movesList[15 - p.swaps] = (((coord1 + 1, p.scrambledPuzzle[math.floor(coord2 / 5)][coord2 % 5]), (coord2 + 1, p.scrambledPuzzle[math.floor(coord1 / 5)][coord1 % 5])))
    p.swaps = p.swaps - 1
    # lose condition
    if p.swaps == 0 and p.numGreen != 21:
        p.draggable = [["false"] * 5 for i in range(5)]
        for i in range(0, 5):
            for j in range(0, 5):
                p.states[i][j] = ('#454747', '#FFFFFF')
        return index(p)
    # win condition
    elif p.numGreen == 21:
        return index(p)
    return index(p)

# Restart the board
@app.route('/reload', methods = ['GET', 'POST'])
def reload():
    global scrambledPuzzle
    global swaps
    global states
    global draggable
    global numGreen
    global movesList
    global shown
    shown = 0
    movesList = [((' ', ' '), (' ', ' '))] * 15
    swaps = 15
    scrambledPuzzle = [row[:] for row in scrambledPuzzleUnmodified]
    states, draggable, numGreen = getStates(solvedPuzzle, scrambledPuzzle)
    return redirect(url_for('index'))

# Shows the solution
@app.route('/showSolution', methods = ['GET', 'POST'])
def showSolution():
    global scrambledPuzzle
    global swaps
    global states
    global draggable
    global numGreen
    global movesList
    # Fill in letters
    scrambledPuzzle = [row[:] for row in solvedPuzzle]
    states, draggable, numGreen = getStates(solvedPuzzle, scrambledPuzzle)
    numGreen = -5
    return redirect(url_for('index'))

# About page
@app.route('/about', methods = ['GET', 'POST'])
def about():
    return render_template('about.html')

# Solve page
@app.route('/solve', methods = ['GET', 'POST'])
def solve():
    global solvable
    global tableColor
    global movesList
    solvable = 3
    tableColor = ['#6fb05c'] * 15
    for i in range(15 - swaps):
            tableColor[i] = '#000000'
    return render_template('table.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList, shown = shown, tableColor = tableColor)

# Solve page and show next steps
@app.route('/solveShow', methods = ['GET', 'POST'])
def solveShow():
    global solvable
    global shown
    global states
    global draggable
    global numGreen
    global tableColor
    shown = 1
    solvable = 3
    newList = main(scrambledPuzzle, solvedPuzzle)
    swapsTemp = swaps
    # colorings for the table
    if numGreen == -5:
        newList = main(scrambledPuzzleUnmodified, solvedPuzzle)
        for i in range(10):
            movesList[i] = newList[i]
        return render_template('table.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList, shown = shown, tableColor = tableColor)
    tableColor = ['#6fb05c'] * 15
    for i in range(len(newList)):
        if (swaps - len(newList) < 0): 
            draggable = [["false"] * 5 for i in range(5)]
            numGreen = -1
            tableColor = ['#000000'] * 15
            for i in range(0, 5):
                for j in range(0, 5):
                    states[i][j] = ('#454747', '#FFFFFF')
            return render_template('table.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList, shown = shown, tableColor = tableColor)
        movesList[15 - swapsTemp] = newList[i]
        for i in range(15 - swaps):
            tableColor[i] = '#000000'
        swapsTemp = swapsTemp - 1
    if numGreen == 21:
        tableColor = ['#000000'] * 15
    return render_template('table.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList, shown = shown, tableColor = tableColor)

# Back arrow
@app.route('/back', methods = ['GET', 'POST'])
def back():
    if solvable == 1:
        return redirect(url_for('index'))
    elif solvable == 0:
        return render_template('Error.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList, shown = shown, tableColor = tableColor)
    elif solvable == 3:
        return render_template('table.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList, shown = shown, tableColor = tableColor)
    else:
        return render_template('ErrorShowBoard.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList, shown = shown, tableColor = tableColor)

# Shows the solution on the unsolvable boards with '?' filled into unknown slots
@app.route('/showSolution2', methods = ['GET', 'POST'])
def showSolution2():
    global scrambledPuzzle
    global swaps
    global states
    global draggable
    global numGreen
    global solvable
    global movesList
    global shown
    shown = 0
    movesList = [((' ', ' '), (' ', ' '))] * 15
    solvable = 2
    scrambledPuzzle = [row[:] for row in solvedPuzzle]
    states, draggable, numGreen = getStates(solvedPuzzle, scrambledPuzzle)
    for i in range(0, 5):
            for j in range(0, 5):
                if scrambledPuzzle[i][j] == '?':
                    states[i][j] = ('#FF0000', '#FFFFFF')
    return render_template('ErrorShowBoard.html', puzzle = solvedPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList, shown = shown, tableColor = tableColor)

# Scrapes the actual waffle and solves the puzzle (or tries to)
@app.route('/getActualWaffle', methods = ['GET', 'POST'])
def getActualWaffle():
    global scrambledPuzzle
    global swaps
    global states
    global draggable
    global numGreen
    global scrambledPuzzleUnmodified
    global solvedPuzzle
    global official_puzzle 
    global solvable
    global movesList
    global shown
    shown = 0
    movesList = [((' ', ' '), (' ', ' '))] * 15
    solvable = 1
    official_puzzle = 1
    swaps = 15
    scrambledPuzzle, states = scrapeWeb()
    scrambledPuzzleUnmodified = [row[:] for row in scrambledPuzzle]
    # Uncomment when you want to see the error pages
    # Delete the last two words from 5LetterWords.txt "admin", "admen"
    # scrambledPuzzle = [['A', 'T', 'I', 'T', 'N'], 
    #                    ['I', ' ', 'N', ' ', 'D'],
    #                    ['L', 'F', 'T', 'I', 'N'],
    #                    ['E', ' ', 'R', ' ', 'O'],
    #                    ['G', 'E', 'M', 'E', 'H']]

    # # #6... = GREEN, #E9... = YELLOW, #ED... = GREY
    # states = [[('#6fb05c', '#FFFFFF'), ('#edeff1', '#000000'), ('#e9ba3a', '#FFFFFF'), ('#edeff1', '#000000'), ('#6fb05c', '#FFFFFF')], 
    #         [('#edeff1', '#FFFFFF'), ' ', ('#edeff1', '#FFFFFF'), ' ', ('#edeff1', '#FFFFFF')],
    #         [('#e9ba3a', '#000000'), ('#6fb05c', '#FFFFFF'), ('#6fb05c', '#FFFFFF'), ('#edeff1', '#FFFFFF'), ('#6fb05c', '#000000')],
    #         [('#edeff1', '#FFFFFF'), ' ', ('#e9ba3a', '#000000'), ' ', ('#edeff1', '#000000')],
    #         [('#6fb05c', '#FFFFFF'), ('#edeff1', '#FFFFFF'), ('#e9ba3a', '#000000'), ('#edeff1', '#FFFFFF'), ('#6fb05c', '#FFFFFF')]]
    solvedPuzzle, trulySolved = solvePuzzle(scrambledPuzzle, states)
    if trulySolved:
        solvable = 1
    else:
        solvable = 0
    if not trulySolved:
        numGreen = 0
        draggable = [["false"] * 5 for i in range(5)]
        for i in range(0, 5):
            for j in range(0, 5):
                states[i][j] = ('#454747', '#FFFFFF')
        return render_template('Error.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList, shown = shown, tableColor = tableColor)
    states, draggable, numGreen = getStates(solvedPuzzle, scrambledPuzzle)
    return redirect(url_for('index'))
