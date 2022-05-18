from flask import render_template, session
from app import app
from waffleLogic import *

@app.route('/')
@app.route('/index')

def index():
    solvedPuzzle = getPuzzle()
    scrambledPuzzle = scramble(solvedPuzzle)
    states = getStates(solvedPuzzle, scrambledPuzzle)
    return render_template('index.html', puzzle = scrambledPuzzle, colors = states)