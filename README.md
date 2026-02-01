# MENACE
Self trained menace

Menace - Matchbox Educable Noughts and Crosses Engine
One of the first Reinforcement Learning algorithms made. This was used to play tic-tac-toe intelligently.

## Behaviour
MENACE doesn't know the rules of Tic-Tac-Toe. It doesn't know that three-in-a-row wins. It only picks out of a learned whitelist moves from each game board possibility.
We need to teach it this whitelist (The ideal moves on every game board possible)

This is done by adding beads to a matchbox as it was done originally, and then pick a random bead corresponding to the move it needs to play (so there will be 9 coloured beads)
Each matchbox in the system represents a unique state of the Tic-Tac-Toe board.
The Memory: Inside each box are beads of different colours. Each colour corresponds to a potential move (an empty square) on the grid. There can be multiple beads of same colour indicating this move has been responsible for a lot of wins and the random picking will most likely pick that colour again.

On a Win: MENACE is rewarded. Each matchbox used in that game receives 3 additional beads of the colour that was played. This makes it much more likely to repeat those winning moves in the future.

On a Draw: It receives a small reward of 1 additional bead.

On a Loss: It is punished. The beads used in that game are removed from their boxes. This decreases the chance of the machine making that losing mistake again.

There is a possibility that a box empties itself in the process - this means that the game state always leads to a loss and there is no way to recover OR it was in early game and the bot had too much of a skill issue to win (and so we might either have to restart training or make sure each early game state always has 1 of each bead, we will decide which to choose later)

Also typically we always let the bot start so it only learns X's moves or Y's moves (these are disjoint to one another). I would want them to play against each other and improve each other, and due to this disjoint property I can just use the same set of matchboxes and in the end have a singular model that can play both X and O.

<br>

# Creating the tictactoe game itself
We need to create a standard tictactoe game first and then put this system on it.

## 1. Storing the game state
So first we will decide how to store the game - 2D lists seem like a natural choice because of the 3x3 board. We can also use a length 9 string (and that will be better as we figure out later) but we will stick to 2D lists since this is a beginner blog

If you are using strings then this is how you index: "012345678" and that corresponds to: <br>

<table>
  <thead>
    <tr>
      <th></th>
      <th><b>col0</b></th>
      <th><b>col1</b></th>
      <th><b>col2</b></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>row0</b></td>
      <td>0</td>
      <td>1</td>
      <td>2</td>
    </tr>
    <tr>
      <td><b>row1</b></td>
      <td>3</td>
      <td>4</td>
      <td>5</td>
    </tr>
    <tr>
      <td><b>row2</b></td>
      <td>6</td>
      <td>7</td>
      <td>8</td>
    </tr>
  </tbody>
</table>

You can see that <br>
`index = row * 3 + col` <br>
`col = index % 3`<br>
`row = index // 3`

Also we will fill the table with X, O and " " (a space for empty cell)

Let us first create the board (2d list)
```python
board = [[" ", " ", " "] for _ in range(3)]
# This is list comprehension. This is the shorter version of:
board = []
for _ in range(3):
    board.append([" ", " ", " "])

# the string guys would just do board = " "*9
```