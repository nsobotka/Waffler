from flask import render_template, request, redirect, url_for
from app import app
from waffleLogic import *
from scrape import *
from viz import *
from boardGeneration import * 
from testBoards import *
from shortestPath import *

# Things to do: 
# aesthetics - tracking moves
# gereral aesthetics
# Delete unused code / make sure everything in routes is correct
# Nice readme
# Credits blurb
# clean up code
# Final bug checks
# clean up repository
# publish to website
# reach out to waffle man


# Global variables
solvedPuzzle = getPuzzle()
scrambledPuzzle = scramble(solvedPuzzle)
while(len(main(scrambledPuzzle, solvedPuzzle)) != 10):
        scrambledPuzzle = scramble(solvedPuzzle)
scrambledPuzzleUnmodified = [row[:] for row in scrambledPuzzle]
states, draggable, numGreen = getStates(solvedPuzzle, scrambledPuzzle)
swaps = 15
official_puzzle = 0
solvable = 1
movesList = [(('A', 'B'), ('', ''))] * 15

# Splash page
@app.route('/')

# Main page
@app.route('/index', methods = ['GET'])
def index():
    return render_template('index.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList)

# New board
@app.route('/newBoard', methods = ['POST'])
def newBoard():
    global states
    global scrambledPuzzle
    global scrambledPuzzleUnmodified
    global solvedPuzzle
    global swaps
    global draggable
    global numGreen
    global official_puzzle 
    global solvable
    global movesList
    movesList = [((' ', ' '), (' ', ' '))] * 15
    solvable = 1
    official_puzzle = 0
    solvedPuzzle = getPuzzle()
    scrambledPuzzle = scramble(solvedPuzzle)

    while(len(main(scrambledPuzzle, solvedPuzzle)) != 10):
        scrambledPuzzle = scramble(solvedPuzzle)

    scrambledPuzzleUnmodified = [row[:] for row in scrambledPuzzle]
    states, draggable, numGreen = getStates(solvedPuzzle, scrambledPuzzle)
    swaps = 15
    return redirect(url_for('index'))

# Swap two pieces
@app.route('/swap', methods = ['GET', 'POST'])
def swap():
    global states
    global scrambledPuzzle
    global solvedPuzzle
    global swaps
    global draggable
    global numGreen
    global movesList
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
    tempChar = scrambledPuzzle[math.floor(coord1 / 5)][coord1 % 5]
    scrambledPuzzle[math.floor(coord1 / 5)][coord1 % 5] = scrambledPuzzle[math.floor(coord2 / 5)][coord2 % 5]
    scrambledPuzzle[math.floor(coord2 / 5)][coord2 % 5] = tempChar
    states, draggable, numGreen = getStates(solvedPuzzle, scrambledPuzzle)
    movesList[15 - swaps] = (((coord1 + 1, scrambledPuzzle[math.floor(coord2 / 5)][coord2 % 5]), (coord2 + 1, scrambledPuzzle[math.floor(coord1 / 5)][coord1 % 5])))
    swaps = swaps - 1
    # lose condition
    if swaps == 0 and numGreen != 21:
        draggable = [["false"] * 5 for i in range(5)]
        for i in range(0, 5):
            for j in range(0, 5):
                states[i][j] = ('#454747', '#FFFFFF')
        return render_template('index.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList)
    # win condition
    elif numGreen == 21:
        return render_template('index.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList)
    return render_template('index.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList)

# Restart the board
@app.route('/reload', methods = ['GET', 'POST'])
def reload():
    global scrambledPuzzle
    global swaps
    global states
    global draggable
    global numGreen
    global movesList
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
    numGreen = 5
    return redirect(url_for('index'))

# About page
@app.route('/about', methods = ['GET', 'POST'])
def about():
    return render_template('about.html')

# Solve page
@app.route('/solve', methods = ['GET', 'POST'])
def solve():
    global solvable
    solvable = 3
    return render_template('table.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList)

# Solve page and show next steps
@app.route('/solveShow', methods = ['GET', 'POST'])
def solveShow():
    global solvable
    solvable = 3
    newList = main(scrambledPuzzle, solvedPuzzle)
    swapsTemp = swaps
    for i in range(len(newList)):
        movesList[15 - swapsTemp] = newList[i]
        swapsTemp = swapsTemp - 1
    return render_template('table.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList)

# Back arrow
@app.route('/back', methods = ['GET', 'POST'])
def back():
    if solvable == 1:
        return redirect(url_for('index'))
    elif solvable == 0:
        return render_template('Error.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList)
    elif solvable == 3:
        return render_template('table.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList)
    else:
        return render_template('ErrorShowBoard.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList)

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
    movesList = [((' ', ' '), (' ', ' '))] * 15
    solvable = 2
    scrambledPuzzle = [row[:] for row in solvedPuzzle]
    states, draggable, numGreen = getStates(solvedPuzzle, scrambledPuzzle)
    for i in range(0, 5):
            for j in range(0, 5):
                if scrambledPuzzle[i][j] == '?':
                    states[i][j] = ('#FF0000', '#FFFFFF')
    return render_template('ErrorShowBoard.html', puzzle = solvedPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList)

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
    # viz_swaps(main(scrambledPuzzle, solvedPuzzle))
    if not trulySolved:
        numGreen = 0
        draggable = [["false"] * 5 for i in range(5)]
        for i in range(0, 5):
            for j in range(0, 5):
                states[i][j] = ('#454747', '#FFFFFF')
        return render_template('Error.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen, official_puzzle = official_puzzle, moves = movesList)
    states, draggable, numGreen = getStates(solvedPuzzle, scrambledPuzzle)
    return redirect(url_for('index'))
