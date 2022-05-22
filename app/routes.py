from flask import render_template, request, redirect, url_for
from app import app
from waffleLogic import *

# Things to do: 
# scramble puzzle correct number of colors
# make it so it doesn't reload every time you make a move? if possible?
# end of game - win or lose -> base on moves counter
# todays waffle - scrape, let person solve on their own, solve for them (or show them how)
# load custom
# solve board
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
    return render_template('index.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable)

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
    print(numGreen)
    swaps = swaps - 1
    # lose condition
    if swaps == 0 and numGreen != 21:
        draggable = [["false"] * 5 for i in range(5)]
        return render_template('index.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable)
        youLose()
    # win condition
    elif numGreen == 21:
        return render_template('index.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable)
        youWin()
    return render_template('index.html', puzzle = scrambledPuzzle, colors = states, swaps = swaps, draggable = draggable)

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
