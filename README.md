# MENACE
Self trained menace

Menace - Matchbox Educable Noughts and Crosses Engine
One of the first Reinforcement Learning algorithms made. This was used to play tic-tac-toe intelligently.

Also in this i will show some basic python too for the 1st year students. Others can just skip those parts.<br>
To the first years, there are some references to higher level topics too, don't get demotivated if you don't get it, it doesn't matter too much to code this up without knowing them fully. Send me doubts if needed

Created by:
- [@Quantum-Codes](https://github.com/Quantum-Codes) (Ankit Sinha, IIT Tirupati)
- [@AnmolSinha42](https://github.com/AnmolSinha42) (Anmol Sinha, NIT Puducherry)

## Behaviour
MENACE doesn't know the rules of Tic-Tac-Toe. It doesn't know that three-in-a-row wins. It only picks out of a learned whitelist moves from each game board possibility.
We need to teach it this whitelist (The ideal moves on every game board possible)

This is done by adding beads to a matchbox as it was done originally, and then pick a random bead corresponding to the move it needs to play (so there will be 9 coloured beads)
Each matchbox in the system represents a unique state of the Tic-Tac-Toe board.
The Memory: Inside each box are beads of different colours. Each colour corresponds to a potential move (an empty square) on the grid. There can be multiple beads of same colour indicating this move has been responsible for a lot of wins and the random picking will most likely pick that colour again.

- **On a Win**: MENACE is rewarded. Each matchbox used in that game receives 3 additional beads of the colour that was played. This makes it much more likely to repeat those winning moves in the future.

- **On a Draw**: It receives a small reward of 1 additional bead.

- **On a Loss**: It is punished. The beads used in that game are removed from their boxes. This decreases the chance of the machine making that losing mistake again.

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
<details>
<summary>For the 2D list version: (which we will not use in main code)</summary>

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
</details><br>

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
<details>
<summary>2D list version: (which we will not use in main code)</summary>

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
</details>

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
<details>
<summary>compressed if loops</summary>

These two code snippets are equivalent:
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
</details>

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

For checking the winner we need to check all possible winning combinations:
1. Line among rows (3 combinations)
2. Line among columns (3 combinations)
3. Line among diagonals (2 combinations)

Note: `index = row * 3 + col` <br>

So for 1, we can check on each row if all 3 cells are same <br>
On ith row, cells are: `i*3+0, i*3+1, i*3+2` and they all should be same. <br>

For 2, on ith column, cells are: `0*3+i, 1*3+i, 2*3+i` and they all should be same. <br>

Now we will create a function to check if there is a winner after each move
```python
def check_winner(board: str):
    # Check rows and columns
    for i in range(3):
        if board[i*3] == board[i*3+1] == board[i*3+2] != " ":
            return board[i*3]
        if board[i] == board[i+3] == board[i+6] != " ":
            return board[i]
        
    # Check diagonals
    if board[0] == board[4] == board[8] != " ":
        return board[0]
    if board[2] == board[4] == board[6] != " ":
        return board[2]
    return None
```
<details>
<summary>2D list version (which we will not use in main code)</summary>

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
</details>

<br>
2 player tictactoe game is now complete!!

Now we need to add the AI itself to play against us. (later against itself)

### Checkpoint 2
We have our 2 player tictactoe game completed!
This is how our main loop looks like now:
```python
if __name__ == "__main__":
    #game always starts with X
    
    board = " " * 9
    player = 1 # 1 = X, 0 = O
    while True:
        board, move = game_loop(board, "X" if player == 1 else "O")

        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"Player {winner} wins!")
            break
        
        player = 1 - player # Switch player
```


<br><br>

# Creating the MENACE AI
We will create a MENACE class that will handle all the logic for the AI. <br>
We need to do: 
1. We create an AI class for all the AI logic.
2. Save every move played in a game (to reward/punish later) using lists.
3. Create all possible board states and initialize matchboxes for them 
4. After each game, reward/punish the moves played based on win/draw/loss 
5. Integrate the AI to play against human 
6. Make the AI play against itself to train 

And somewhere in the middle we need a system to save whatever it learnt and load back on startup; also need to optimize the matchbox storage so that we dont store symmetric board states separately (since they are equivalent). 


We couldve created a class for the game too but i wanted to show both functional programming and object oriented programming. So now we use functional programming for the game and object oriented programming for the AI.

Added code: (for the 1 and 2 steps)
```python
class AI:
    def __init__(self):
        self.X_move_list = []
        self.O_move_list = []
        self.games_played = 0

    def save_move(self, move, player):
        if player == 1:
            self.X_move_list.append(move)
        else:
            self.O_move_list.append(move)
    
    def reset_game_state(self):
        self.X_move_list.clear()
        self.O_move_list.clear()
        self.games_played += 1

# main loop
if __name__ == "__main__":
    #game always starts with X

    ai = AI()
    board = " " * 9
    player = 1 # 1 = X, 0 = O
    while True:
        board, move = game_loop(board, "X" if player == 1 else "O")
        ai.save_move(move, player)
        
        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"Player {winner} wins!")
            break
        
        player = 1 - player # Switch player
```

## Generating all possible board states 
I will show 3 methods

Need to create all possible combinations of X, O, and empty spaces in a 3x3 grid = (3 possibilities)^(9 positions) = 19683 states

### Method 1: Iterative approach using loops
```python
def generate_all_boards():
    boards = []
    for i in range(3**9): # total 3^9 combinations
        # you remember how you did this modulus and floor division thingy to convert decimal to other bases? This is the same, we are converting i to base 3 and mapping 0->X, 1->O, 2->" "
        board = ""
        num = i
        for _ in range(9):
            rem = num % 3
            if rem == 0:
                board += "X"
            elif rem == 1:
                board += "O"
            else:
                board += " "
            num //= 3
        boards.append(board)
    return boards
```
### Method 2: Recursive approach
```python
def fill_board(board, index, boards):
    board = board.copy()
    if index == 9:
        return
    for symbol in ["X", "O", " "]:
        board[index] = symbol
        boards.append("".join(board))
        fill_board(board, index + 1, boards)

def generate_all_boards():
    boards = []
    board = [" "] * 9
    fill_board(board, 0, boards)
    return boards
```

### Method 3: Iterative using recursive relationships

```
Recurrence relation: (T = string of gamestates, n = number of moves made) 
Base case: T(0) = "" 
T(n) = T(n-1) + " " 
     = T(n-1) + "X" 
     = T(n-1) + "O" 
We end at n = 9. So loop with 9 iterations
```
Code: <br>
Technically this is recursion too, just another version that uses loops instead of function calls. Also more memory efficient than method 2.<br>

```python
def generator(possibilities):
    states = []
    for possibility in possibilities:
        states.extend([possibility + " ", possibility + "X", possibility + "O"])
    return states 

def generate_all_states():
    all_states = [""]
    for _ in range(9):
        all_states = generator(all_states)
    return all_states
```
<br>

## Removing invalid and symmetric states
Note that this is simply an optimization step to reduce the number of matchboxes we need to store and to make the AI learn a lot quicker. We can skip this step and just have MENACE learn all states but that would be inefficient. MENACE will anyway skip invalid boards since it will never encounter them.<br>
You can skip this section and still have the AI work, just slower.

### Invalid states
Out of these 3^9 states, there are many that we will never encounter. The following are invalid states:

1. States where the difference between number of X's and O's is more than 1 (since players alternate turns)
2. States where O has more X's than O's (since X always starts first)
3. States where both X and O have winning lines (impossible in a real game)
4. Already won. Nothing to learn in here and game stops at this.

Here are some examples of invalid states:

```
X | X | X      O | X | X
---------      ---------
  | O |          | O |  
---------      ---------
  |   |          |   | O
```

Condition 1 and 2 can be checked together by the condition: <br>`if ((count_X - count_O) > 1 OR (count_O > count_X)) then reject`<br>
Condition 3 can be checked by using the `check_winner` function modified to count how many conditions within it are met. Note that 2 of X or O winning lines are possible.<br>
BUT 2 of X parallel winning lines are impossible since the game would have ended on the first winning line. AND if you do that even then you have 6X and at max 3Os which anywaty violates condition 1.<br>
But if we simlpy implement condition 4 then we never had to think all this, nothing to learn in already won states. No double win needed to be considered.<br>

Code for 1 and 2:
```python
def filter_game_states():
    all_states = generate_all_states()
    #remove all where (number of X) - (number of O) > 1 since we can only have alternating moves and X always starts
    remove_state = [] # we have this list to avoid modifying the list while iterating over it
    for state in all_states:
        if state.count("X") - state.count("O") > 1 or state.count("O") > state.count("X"):
            remove_state.append(state)
    for state in remove_state:
        all_states.remove(state)
```

Code for 3 and 4:
I will just add this right below the `for states in all_states:` loop in the above code
```python
        if check_winner(state):
            continue
```

### How do we know this is right?
We do know that the original guy got 304 matchboxes after all this. Let us try to get that number after applying his extra conditions. Conditions he had that we did not implement:

1. Only X plays. (we added both X and O)
2. Ignore states where we only have 1 empty cell left (since game would end before that) [we didnt do this because we would anyway have only 1 bead in there so it wouldnt matter at all]

For 1, we say that after O plays, there is always equal number of Xs and Os.<br>
For 2, we can make sure that number of `" "` (blanks) are more than 1.<br>

We change 
```python
all_states = [state for state in all_states if state.count("X") - state.count("O") <= 1 and state.count("O") <= state.count("X")]
```
to
```python
all_states = [state for state in all_states if state.count("X") - state.count("O") == 0 and state.count(" ") > 1]
```

<details>
<summary>Full code for filtering invalid states with these 2 extra conditions (i will run this, you can run this too in a whole new file)</summary>

```python
def generator(possibilities):
    states = []
    for possibility in possibilities:
        states.extend([possibility + " ", possibility + "X", possibility + "O"])
    return states 

def generate_all_states():
    # all game states in string format
    
    # Recurrence relation: (T = string of gamestates, n = number of moves made)
    # Base case: T(0) = ""
    # T(n) = T(n-1) + " "
    #      = T(n-1) + "X"
    #      = T(n-1) + "O"
    # We end at n = 9. So loop with 9 iterations
    # this will give us all possible combinations of X, O, and empty spaces in a 3x3 grid = (3 possibilities)^(9 positions) = 19683 states
    all_states = [""]
    for _ in range(9):
        all_states = generator(all_states)
    
    return all_states

def check_winner(board: str):
    # Check rows and columns
    for i in range(3):
        if board[i*3] == board[i*3+1] == board[i*3+2] != " ":
            return board[i*3]
        if board[i] == board[i+3] == board[i+6] != " ":
            return board[i]
        
    # Check diagonals
    if board[0] == board[4] == board[8] != " ":
        return board[0]
    if board[2] == board[4] == board[6] != " ":
        return board[2]
    return None

def filter_game_states():
    all_states = generate_all_states()
    #remove all where (number of X) - (number of O) > 1 since we can only have alternating moves and X always starts
    # same as generating a new list with only valid states
    all_states = [state for state in all_states if state.count("X") - state.count("O") <= 1 and state.count("O") <= state.count("X")]

    #remove rotations and mirrored states. 
    # For this we pick a state one at a time, generate all its rotations and mirrored versions, and then check if any of those already exist in new_states. IF not we add them.
    unique_states = []
    index_map = [6,3,0,7,4,1,8,5,2] # 90 deg rotated indexes. we can repeat this rotation again and again for every rotation.
    mirror_y_map = [2,1,0,5,4,3,8,7,6] # mirrored indexes along y axis
    mirror_x_map = [6,7,8,3,4,5,0,1,2] # mirrored indexes along x axis

    for state in all_states:
        # If already won, skip. Dont waste processing time.
        if check_winner(state):
            continue
        
        # make mirror images
        y_mirror = ''.join([state[mirror_y_map[i]] for i in range(9)])
        x_mirror = ''.join([state[mirror_x_map[i]] for i in range(9)])
        similar_states = [state, x_mirror, y_mirror]

        # generate rotations (90 deg at a time)
        to_rotate = state
        to_rotate_y = y_mirror
        to_rotate_x = x_mirror
        for _ in range(3):
            to_rotate = ''.join([to_rotate[index_map[j]] for j in range(9)])
            to_rotate_y = ''.join([to_rotate_y[index_map[j]] for j in range(9)])
            to_rotate_x = ''.join([to_rotate_x[index_map[j]] for j in range(9)])
            similar_states.append(to_rotate)
            similar_states.append(to_rotate_y)
            similar_states.append(to_rotate_x)

        # check if any of the similar states already exist in unique_states
        for item in similar_states:  
            if item in unique_states:
                break
        else:
            unique_states.append(state) #if none matches then for loop is not broken and the state is added (for-else loop)
    
    return unique_states


if __name__ == "__main__":
    print(len(filter_game_states())) 
```
</details><br>
AND... The output:

```bash
(menace-py3.12) ankit@LAPTOP-T90NGO2F:~/python/MENACE$ python3 menace.py 
304
```
Yay!<br>
And actually removing condition 2 is pretty nice and i couldnt think about it before i went around searching why my count was `338` prior to this, so i will keep the condition 2, the blanks >1, (see the filtering code below to see) but then reintroduce both X and Os<br>

<details>
<summary>Here is my current code for filtering invalid states</summary>

```python
def filter_game_states():
    all_states = generate_all_states()
    #remove all where (number of X) - (number of O) > 1 since we can only have alternating moves and X always starts
    # same as generating a new list with only valid states
    all_states = [state for state in all_states if 0 <= state.count("X") - state.count("O") <= 1 and state.count(" ") > 1]

    #remove rotations and mirrored states. 
    # For this we pick a state one at a time, generate all its rotations and mirrored versions, and then check if any of those already exist in new_states. IF not we add them.
    unique_states = []
    index_map = [6,3,0,7,4,1,8,5,2] # 90 deg rotated indexes. we can repeat this rotation again and again for every rotation.
    mirror_y_map = [2,1,0,5,4,3,8,7,6] # mirrored indexes along y axis
    mirror_x_map = [6,7,8,3,4,5,0,1,2] # mirrored indexes along x axis

    for state in all_states:
        # If already won, skip. Dont waste processing time.
        if check_winner(state):
            continue
        
        # make mirror images
        y_mirror = ''.join([state[mirror_y_map[i]] for i in range(9)])
        x_mirror = ''.join([state[mirror_x_map[i]] for i in range(9)])
        similar_states = [state, x_mirror, y_mirror]

        # generate rotations (90 deg at a time)
        to_rotate = state
        to_rotate_y = y_mirror
        to_rotate_x = x_mirror
        for _ in range(3):
            to_rotate = ''.join([to_rotate[index_map[j]] for j in range(9)])
            to_rotate_y = ''.join([to_rotate_y[index_map[j]] for j in range(9)])
            to_rotate_x = ''.join([to_rotate_x[index_map[j]] for j in range(9)])
            similar_states.append(to_rotate)
            similar_states.append(to_rotate_y)
            similar_states.append(to_rotate_x)

        # check if any of the similar states already exist in unique_states
        for item in similar_states:  
            if item in unique_states:
                break
        else:
            unique_states.append(state) #if none matches then for loop is not broken and the state is added (for-else loop)
    
    return unique_states


if __name__ == "__main__":
    print(len(filter_game_states())) 
```

</details>


Now we need to map it to matchboxes and initialize beads in them.<br>
We can use a dictionary for this purpose. Also accessing a dictionary item is O(1) on average due to hashmaps (meaning fast regardless of number of items stored) unlike lists where searching is O(n) (meaning time taken increases linearly with number of items stored).<br>
Also rehashing cost does not negate the O(1) since we max only add approx 600 items and we access its items (membership check) more than that.<br>
If we want to exploit this speed in the filtering thing too then we could've made a dict rather than a list for unique_states and then just do `if item in unique_states_dict:`and also we would already have a dict so no need to convert to dict later; but since this is a one time operation and we have only 304 items, it doesnt matter much. I would do it but imagine spending 5 minutes on this optimisation that saves a few milliseconds once a while<br>

## TODO! converting to a dictionary of matchboxes and initializing beads
