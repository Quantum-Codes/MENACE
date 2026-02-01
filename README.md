# MENACE
Self trained menace

Menace - Matchbox Educable Noughts and Crosses Engine
One of the first Reinforcement Learning algorithms made. This was used to play tic-tac-toe intelligently.

Also in this i will show some basic python too for the 1st year students. Others can just skip those parts.

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
> skim through this part if you already know basic python<br>

So first we will decide how to store the game - 2D lists seem like a natural choice because of the 3x3 board. We can also use a length 9 string (and that will be better as we figure out later). So we will use the string method but for a few functions i will also share the 2D list method (but not use it in the main code)

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

Let us first create the board and printing function:
```python
board = " " * 9  # This creates a string with 9 spaces representing an empty board

# this is a print board function for string version
def print_board(board: str):
    print(f"""
{board[0]} | {board[1]} | {board[2]}
---------
{board[3]} | {board[4]} | {board[5]}
---------
{board[6]} | {board[7]} | {board[8]}""")
```
For the 2D list version: (which we will not use in main code)
```python
board = [[" ", " ", " "] for _ in range(3)]
# This is list comprehension. This is the shorter version of:
board = []
for _ in range(3):
    board.append([" ", " ", " "])

def print_board(board):
    print()
    print(" | ".join(board[0]))
    print("-" * 9)
    print(" | ".join(board[1]))
    print("-" * 9)
    print(" | ".join(board[2]))
```

Now let us create a function to get user input (Standard tictactoe, no AI yet)
```python
def player_turn(board: str, player: str) -> tuple[str, int]: # string version
    # returns 2 values = updated board and position played
    while True:
        try:
            num = int(input(f"Player {player}, enter the cell number (0-8): "))
            if board[num] == " ": # check if cell is empty
                board = board[:num] + player + board[num+1:]
                return board, num
            else:
                print("That position is already taken. Try again.")
        except (ValueError, IndexError): # valueeerror= not an int, indexerror= not in 0-8
            print("Invalid input. Please enter numbers between 0 and 8.")
```
The 2D list version: (which we will not use in main code)
```python
def player_turn(board: list[list[str]], player: str) -> int:
    while True:
        try:
            num = int(input(f"Player {player}, enter the cell number (0-8): "))
            if board[num // 3][num % 3] == " ":
                board[num // 3][num % 3] = player
                return num # this function does changes in place on the list, so no need to return board
            else:
                print("That position is already taken. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter numbers between 0 and 8.")
```

## 2. Game loop and player switching logic
> skim if you already know basic python<br>

Now we will create a game loop function that will print the board, get user input and return the move played
```python
def game_loop(board, player):
    print_board(board)
    board, move = player_turn(board, player)
    return board, move



if __name__ == "__main__":
    # game always starts with X
    board = " " * 9
    player = 1 # 1 = X, 0 = O
    while True:
        board, move = game_loop(board, "X" if player == 1 else "O")     
        player = 1 - player # Switch player (1-1=0, 1-0=1)
```
Also these are equivalent if loops:
```python
if player == 1:
    symbol = "X"
else:
    symbol = "O"
board, move = game_loop(board, symbol)

# shortened:
symbol = "X" if player == 1 else "O"
board, move = game_loop(board, symbol)
```

### Checkpoint 1 
The code now should run a basic tictactoe game between 2 players. Next we will add win checking logic.
<details>
<summary>Full code until now (click this to reveal)</summary>

```python
def print_board(board: str):
    print(f"""
{board[0]} | {board[1]} | {board[2]}
---------
{board[3]} | {board[4]} | {board[5]}
---------
{board[6]} | {board[7]} | {board[8]}""")

def player_turn(board: str, player: str) -> tuple[str, int]:
    # returns 2 values = updated board and position played
    while True:
        try:
            num = int(input(f"Player {player}, enter the cell number (0-8): "))
            if board[num] == " ": # check if cell is empty
                board = board[:num] + player + board[num+1:]
                return board, num
            else:
                print("That position is already taken. Try again.")
        except (ValueError, IndexError): # valueeerror= not an int, indexerror= not in 0-8
            print("Invalid input. Please enter numbers between 0 and 8.")

def game_loop(board, player):
    print_board(board)
    board, move = player_turn(board, player)
    return board, move


if __name__ == "__main__":
    # game always starts with X
    board = " " * 9
    player = 1 # 1 = X, 0 = O
    while True:
        board, move = game_loop(board, "X" if player == 1 else "O")     
        player = 1 - player # Switch player (1-1=0, 1-0=1)
``` 

</details>

## 3. Win checking logic
> skim if you already know basic python<br>

[HERE PUT IMAGES FOR WINNING COMBINATIONS AND EXPLAIN WHY THE LOOP 3]

Now we will create a function to check if there is a winner after each move
```python
def check_winner(board):
```

2D list version: (which we will not use in main code)
```python
def check_winner(board):
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]
        
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    return None
```