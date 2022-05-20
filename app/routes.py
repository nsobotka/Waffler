from flask import render_template, request, redirect, url_for
from app import app
from waffleLogic import *

# Things to do: 
# fix bug on generating puzzle
# shuffle puzzle correct number of colors
# make it so it doesn't reload every time you make a move? if possible?
# moves counter
# end of game - win or lose
# todays waffle
# load custom
# solve board
# optimal solution to solve board
# display optimal solution somehow
# aesthetics - font sizes, placement, weird behavior on half screen, etc

solvedPuzzle = getPuzzle()
scrambledPuzzle = scramble(solvedPuzzle)
states = getStates(solvedPuzzle, scrambledPuzzle)

@app.route('/')
@app.route('/index', methods = ['GET'])

def index():
    return render_template('index.html', puzzle = scrambledPuzzle, colors = states)

@app.route('/newBoard', methods = ['POST'])
def newBoard():
    global states
    global scrambledPuzzle
    global solvedPuzzle
    solvedPuzzle = getPuzzle()
    scrambledPuzzle = scramble(solvedPuzzle)
    states = getStates(solvedPuzzle, scrambledPuzzle)
    return redirect(url_for('index'))

@app.route('/swap', methods = ['GET', 'POST'])
def swap():
    global states
    global scrambledPuzzle
    global solvedPuzzle
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
    states = getStates(solvedPuzzle, scrambledPuzzle)
    item = render_template('index.html', puzzle = scrambledPuzzle, colors = states)
    # print(item)
    return render_template('index.html', puzzle = scrambledPuzzle, colors = states)
