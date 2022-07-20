from flask import render_template, request, redirect, url_for
from app import app
from waffleLogic import *
from scrape import *
from viz import *
from boardGeneration import * 
from testBoards import *
from shortestPath import *

class puzzle:
    def __init__(self):
        self.solvedPuzzle = getPuzzle()
        self.scrambledPuzzle = scramble(self.solvedPuzzle)
        while(len(main(self.scrambledPuzzle, self.solvedPuzzle)) != 10):
                self.scrambledPuzzle = scramble(self.solvedPuzzle)
        self.scrambledPuzzleUnmodified = [row[:] for row in self.scrambledPuzzle]
        self.states, self.draggable, self.numGreen = getStates(self.solvedPuzzle, self.scrambledPuzzle)
        self.swaps = 15
        self.official_puzzle = 0
        self.solvable = 1
        self.movesList = [(('', ''), ('', ''))] * 15
        self.shown = 0
        self.tableColor = ['#6fb05c'] * 15

    def getAll(self):
        return (self.solvedPuzzle, self.scrambledPuzzle, self.scrambledPuzzleUnmodified, self.states, self.draggable, self.numGreen, self.swaps, self.official_puzzle, self.solvable, self.movesList, self.shown, self.tableColor)

p = puzzle()

# Splash page
@app.route('/')
def splash():
    global p
    p = puzzle()
    return redirect(url_for('index'))

# Main page
@app.route('/index', methods = ['GET', 'POST'])
def index():
    global p
    return render_template('index.html', puzzle = p.scrambledPuzzle, colors = p.states, swaps = p.swaps, draggable = p.draggable, numGreen = p.numGreen, official_puzzle = p.official_puzzle, moves = p.movesList, shown = p.shown, tableColor = p.tableColor)

# New board
@app.route('/newBoard', methods = ['GET', 'POST'])
def newBoard():
    global p
    p = puzzle()
    return redirect(url_for('index'))

# Swap two pieces
@app.route('/swap', methods = ['GET', 'POST'])
def swap():
    global p
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
        return redirect(url_for('index'))
    # win condition
    elif p.numGreen == 21:
        return redirect(url_for('index'))
    return redirect(url_for('index'))

# Restart the board
@app.route('/reload', methods = ['GET', 'POST'])
def reload():
    global p
    p.shown = 0
    p.movesList = [((' ', ' '), (' ', ' '))] * 15
    p.swaps = 15
    p.scrambledPuzzle = [row[:] for row in p.scrambledPuzzleUnmodified]
    p.states, p.draggable, p.numGreen = getStates(p.solvedPuzzle, p.scrambledPuzzle)
    return redirect(url_for('index'))

# Shows the solution
@app.route('/showSolution', methods = ['GET', 'POST'])
def showSolution():
    global p
    # Fill in letters
    p.scrambledPuzzle = [row[:] for row in p.solvedPuzzle]
    p.states, p.draggable, p.numGreen = getStates(p.solvedPuzzle, p.scrambledPuzzle)
    p.numGreen = -5
    return redirect(url_for('index'))

# About page
@app.route('/about', methods = ['GET', 'POST'])
def about():
    return render_template('about.html')

# Solve page
@app.route('/solve', methods = ['GET', 'POST'])
def solve():
    global p
    p.solvable = 3
    p.tableColor = ['#6fb05c'] * 15
    for i in range(15 - p.swaps):
            p.tableColor[i] = '#000000'
    return render_template('table.html', puzzle = p.scrambledPuzzle, colors = p.states, swaps = p.swaps, draggable = p.draggable, numGreen = p.numGreen, official_puzzle = p.official_puzzle, moves = p.movesList, shown = p.shown, tableColor = p.tableColor)

# Solve page and show next steps
@app.route('/solveShow', methods = ['GET', 'POST'])
def solveShow():
    global p
    p.shown = 1
    p.solvable = 3
    newList = main(p.scrambledPuzzle, p.solvedPuzzle)
    swapsTemp = p.swaps
    # colorings for the table
    if p.numGreen == -5:
        newList = main(p.scrambledPuzzleUnmodified, p.solvedPuzzle)
        for i in range(10):
            p.movesList[i] = newList[i]
        return render_template('table.html', puzzle = p.scrambledPuzzle, colors = p.states, swaps = p.swaps, draggable = p.draggable, numGreen = p.numGreen, official_puzzle = p.official_puzzle, moves = p.movesList, shown = p.shown, tableColor = p.tableColor)
    p.tableColor = ['#6fb05c'] * 15
    for i in range(len(newList)):
        if (p.swaps - len(newList) < 0): 
            p.draggable = [["false"] * 5 for i in range(5)]
            p.numGreen = -1
            p.tableColor = ['#000000'] * 15
            for i in range(0, 5):
                for j in range(0, 5):
                    p.states[i][j] = ('#454747', '#FFFFFF')
            return render_template('table.html', puzzle = p.scrambledPuzzle, colors = p.states, swaps = p.swaps, draggable = p.draggable, numGreen = p.numGreen, official_puzzle = p.official_puzzle, moves = p.movesList, shown = p.shown, tableColor = p.tableColor)
        p.movesList[15 - swapsTemp] = newList[i]
        for i in range(15 - p.swaps):
            p.tableColor[i] = '#000000'
        swapsTemp = swapsTemp - 1
    if p.numGreen == 21:
        p.tableColor = ['#000000'] * 15
    return render_template('table.html', puzzle = p.scrambledPuzzle, colors = p.states, swaps = p.swaps, draggable = p.draggable, numGreen = p.numGreen, official_puzzle = p.official_puzzle, moves = p.movesList, shown = p.shown, tableColor = p.tableColor)

# Back arrow
@app.route('/back', methods = ['GET', 'POST'])
def back():
    global p
    if p.solvable == 1:
        return redirect(url_for('index'))
    elif p.solvable == 0:
        return render_template('Error.html', puzzle = p.scrambledPuzzle, colors = p.states, swaps = p.swaps, draggable = p.draggable, numGreen = p.numGreen, official_puzzle = p.official_puzzle, moves = p.movesList, shown = p.shown, tableColor = p.tableColor)
    elif p.solvable == 3:
        return render_template('table.html', puzzle = p.scrambledPuzzle, colors = p.states, swaps = p.swaps, draggable = p.draggable, numGreen = p.numGreen, official_puzzle = p.official_puzzle, moves = p.movesList, shown = p.shown, tableColor = p.tableColor)
    else:
        return render_template('ErrorShowBoard.html', puzzle = p.scrambledPuzzle, colors = p.states, swaps = p.swaps, draggable = p.draggable, numGreen = p.numGreen, official_puzzle = p.official_puzzle, moves = p.movesList, shown = p.shown, tableColor = p.tableColor)

# Shows the solution on the unsolvable boards with '?' filled into unknown slots
@app.route('/showSolution2', methods = ['GET', 'POST'])
def showSolution2():
    global p
    p.shown = 0
    p.movesList = [((' ', ' '), (' ', ' '))] * 15
    p.solvable = 2
    p.scrambledPuzzle = [row[:] for row in p.solvedPuzzle]
    p.states, p.draggable, p.numGreen = getStates(p.solvedPuzzle, p.scrambledPuzzle)
    for i in range(0, 5):
            for j in range(0, 5):
                if p.scrambledPuzzle[i][j] == '?':
                    p.states[i][j] = ('#FF0000', '#FFFFFF')
    return render_template('ErrorShowBoard.html', puzzle = p.solvedPuzzle, colors = p.states, swaps = p.swaps, draggable = p.draggable, numGreen = p.numGreen, official_puzzle = p.official_puzzle, moves = p.movesList, shown = p.shown, tableColor = p.tableColor)

# Scrapes the actual waffle and solves the puzzle (or tries to)
@app.route('/getActualWaffle', methods = ['GET', 'POST'])
def getActualWaffle():
    global p
    p.shown = 0
    p.movesList = [((' ', ' '), (' ', ' '))] * 15
    p.solvable = 1
    p.official_puzzle = 1
    p.swaps = 15
    p.scrambledPuzzle, p.states = scrapeWeb()
    p.scrambledPuzzleUnmodified = [row[:] for row in p.scrambledPuzzle]
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
    p.solvedPuzzle, trulySolved = solvePuzzle(p.scrambledPuzzle, p.states)
    if trulySolved:
        p.solvable = 1
    else:
        p.solvable = 0
    if not trulySolved:
        p.numGreen = 0
        p.draggable = [["false"] * 5 for i in range(5)]
        for i in range(0, 5):
            for j in range(0, 5):
                p.states[i][j] = ('#454747', '#FFFFFF')
        return render_template('Error.html', puzzle = p.scrambledPuzzle, colors = p.states, swaps = p.swaps, draggable = p.draggable, numGreen = p.numGreen, official_puzzle = p.official_puzzle, moves = p.movesList, shown = p.shown, tableColor = p.tableColor)
    p.states, p.draggable, p.numGreen = getStates(p.solvedPuzzle, p.scrambledPuzzle)
    return redirect(url_for('index'))
