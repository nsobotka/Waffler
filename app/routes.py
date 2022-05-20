from flask import render_template, session, request, redirect, url_for
from app import app
from waffleLogic import *

solvedPuzzle = getPuzzle()
scrambledPuzzle = scramble(solvedPuzzle)
states = getStates(solvedPuzzle, scrambledPuzzle)

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html', puzzle = scrambledPuzzle, colors = states)

@app.route('/swap', methods = ['POST'])
def swap():
    global states
    global scrambledPuzzle
    global solvedPuzzle
    box1 = request.form['box1']
    box2 = request.form['box2']
    coord1 = int(box1[3]) - 1
    coord2 = int(box2[3]) - 1
    tempChar = scrambledPuzzle[math.floor(coord1 / 5)][coord1 % 5]
    scrambledPuzzle[math.floor(coord1 / 5)][coord1 % 5] = scrambledPuzzle[math.floor(coord2 / 5)][coord2 % 5]
    scrambledPuzzle[math.floor(coord2 / 5)][coord2 % 5] = tempChar
    states = getStates(solvedPuzzle, scrambledPuzzle)
    return render_template('index.html', puzzle = scrambledPuzzle, colors = states)
