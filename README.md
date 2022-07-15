# WAFFLE(R) (ADD LINK)
First and foremost, all ownership of the original game and design belongs to <a href="https://twitter.com/jamesjessian" style="color: #6fb05c;"  target="_blank">@JamesJessian</a>. <br><br>
Please check out the official <a href="https://wafflegame.net" style="color: #6fb05c;" target="_blank">Waffle</a> and twitter at <a href="https://twitter.com/thatwafflegame" style="color: #6fb05c;" target="_blank">@thatwafflegame</a>.

## About This Project
We are a team of two developers who, after enjoying the Waffle, questioned whether every board was truly solvable in 10 moves (as the game claims). <br><br>
We decided to implement the game and expand upon its features. This included adding in computer generated boards, optimal solutions, and move tracking, as some of the most important additions. <br><br>
Notably, you can also import and optimally solve / play the daily Waffle. In finding optimal paths, we had to algorithmically solve the board - one of the key challenges of the project. 

## Implementation
We begin each Waffle by selecting 6 words and assembling the solved puzzle. Then, we scamble our puzzle according to trends from the official game; i.e. greens in all corners and the center. 
Furthermore, we ensure that each puzzle is minimally solvable in exactly 10 moves. After the puzzle is scrambled, we compare to the solved puzzle to determine the color of each square. <br><br>
In addition to generating our own puzzles, we wanted to create a solver for any Waffle (including the daily Waffle). To do so, we created an algorithm which incorporates many heuristics, each of which narrows down the potential solutions based purely on the initial coloring of the board. We make use of all available data in the starting board to find a unique solution (if one exists, more on this later).<br><br>
By combining our solver and web scraping, we are able to import a fully playable copy of the daily Waffle. <br><br>
Finally, we designed an algorithm to solve each board in the minimum number of moves. This algorithm works by prioritizing moves that "correct" two squares in one swap, followed by three squares in two swaps, and so forth. This algorithm is used to ensure that our randomly generated boards are minimally solvable in exactly 10 moves, and to output solutions when the user requests them.
We can show optimal paths not only from the start, but from any point in the game (or output that the game is no longer solvable).

## About Us
Feel free to check out our websites: <a href="https://nsobotka.github.io" style="color: #6fb05c;" target="_blank">Nathan Sobotka</a> and <a href="http://avielresnick.com" style="color: #6fb05c;" target="_blank">Aviel Resnick</a>.

# File structure
- 5LetterWords.txt : word bank
- boardGeneration.py : creates new boards
- waffleLogic.py : solves boards
- shortestPath.py : finds optimal moves
- scrape.py : web scraping
- viz.py : visualizers for debugging
- testBoards.py : past official Waffles
