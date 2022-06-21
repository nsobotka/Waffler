from flask import render_template, request, redirect, url_for
from app import app
from waffleLogic import *
from scrape import *

# Things to do: 
# change names of buttons
# scramble puzzle correct number of colors
# make it so it doesn't reload every time you make a move? if possible?
# load custom
# solve board and link this to the getRealWaffle so that the real waffle can be played
# optimal solution to solve board
# display optimal solution somehow
# aesthetics - font sizes, placement, weird behavior on half screen, etc

solvedPuzzle = getPuzzle()
scrambledPuzzle = scramble(solvedPuzzle)
scrambledPuzzleUnmodified = [row[:] for row in scrambledPuzzle]
states, draggable, numGreen = getStates(solvedPuzzle, scrambledPuzzle)
swaps = 15

@app.route('/')
@app.route('/index', methods = ['GET'])

def index():
    return render_template('index.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen)

@app.route('/newBoard', methods = ['POST'])
def newBoard():
    global states
    global scrambledPuzzle
    global scrambledPuzzleUnmodified
    global solvedPuzzle
    global swaps
    global draggable
    global numGreen
    solvedPuzzle = getPuzzle()
    scrambledPuzzle = scramble(solvedPuzzle)
    scrambledPuzzleUnmodified = [row[:] for row in scrambledPuzzle]
    states, draggable, numGreen = getStates(solvedPuzzle, scrambledPuzzle)
    swaps = 15
    return redirect(url_for('index'))

@app.route('/swap', methods = ['GET', 'POST'])
def swap():
    global states
    global scrambledPuzzle
    global solvedPuzzle
    global swaps
    global draggable
    global numGreen
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
    swaps = swaps - 1
    # lose condition
    if swaps == 0 and numGreen != 21:
        draggable = [["false"] * 5 for i in range(5)]
        for i in range(0, 5):
            for j in range(0, 5):
                states[i][j] = ('#454747', '#FFFFFF')
        return render_template('index.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen)
    # win condition
    elif numGreen == 21:
        return render_template('index.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen)
    return render_template('index.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen)

@app.route('/reload', methods = ['GET', 'POST'])
def reload():
    global scrambledPuzzle
    global swaps
    global states
    global draggable
    global numGreen
    swaps = 15
    scrambledPuzzle = [row[:] for row in scrambledPuzzleUnmodified]
    states, draggable, numGreen = getStates(solvedPuzzle, scrambledPuzzle)
    return redirect(url_for('index'))

@app.route('/showSolution', methods = ['GET', 'POST'])
def showSolution():
    global scrambledPuzzle
    global swaps
    global states
    global draggable
    global numGreen
    scrambledPuzzle = [row[:] for row in solvedPuzzle]
    states, draggable, numGreen = getStates(solvedPuzzle, scrambledPuzzle)
    return render_template('index.html', puzzle = solvedPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen)

@app.route('/getActualWaffle', methods = ['GET', 'POST'])
def getActualWaffle():
    global scrambledPuzzle
    global swaps
    global states
    global draggable
    global numGreen
    scrambledPuzzle, states = scrapeWeb()
    # solved puzzle = ????
    # states, draggable, numGreen = getStates(solvedPuzzle, scrambledPuzzle)
    return render_template('index.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable, numGreen = numGreen)
