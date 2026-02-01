def permutation(possibilities):
    states = []
    for possibility in possibilities:
        states.extend([possibility+" ",possibility+"X",possibility+"O"])
    return states 
    
def game_state():
    # all game states in string format
    
    # Recurrence relation: (T = string of gamestates, n = number of moves made)
    # Base case: T(0) = ""
    # T(n) = T(n-1) + " "
    #      = T(n-1) + "X"
    #      = T(n-1) + "O"
    # We end at n = 9. So loop with 9 iterations
    # this will give us all possible combinations of X, O, and empty spaces in a 3x3 grid = (3 possibilities)^(9 positions) = 19683 states
    all_states = [""]
    for i in range(9):
        all_states = permutation(all_states)
    
    #remove all where (number of X) - (number of O) > 1 since we can only have alternating moves and X always starts
    remove_state = []
    for state in all_states:
        if state.count("X") - state.count("O") > 1 or state.count("O")>state.count("X"):
            remove_state.append(state)
    for state in remove_state:
        all_states.remove(state)

    #remove rotations and mirrored states. 
    # For this we pick a state one at a time, generate all its rotations and mirrored versions, and then check if any of those already exist in new_states. IF not we add them.
    unique_states = []
    index_map = [6,3,0,7,4,1,8,5,2] # 90 deg rotated indexes. we can repeat this rotation again and again for every rotation.
    mirror_y_map = [2,1,0,5,4,3,8,7,6] # mirrored indexes along y axis
    mirror_x_map = [6,7,8,3,4,5,0,1,2] # mirrored indexes along x axis
    for state in all_states:
        
        to_rotate = list(state)
        y_mirror = [state[mirror_y_map[i]] for i in range(9)]
        x_mirror = [state[mirror_x_map[i]] for i in range(9)]
        similar_states = [state,x_mirror,y_mirror]  #similar states contins all states equivalent to the selected state
        for i in range(3):
            rotated_state = [to_rotate[index_map[i]] for i in range(9)]
            to_rotate = list(rotated_state)
            similar_states.append(rotated_state)

        for item in similar_states:      
            if item in unique_states:
                break
        else:
            unique_states.append(state) #if none matches then for loop is not broken and the state is added

    #all game states in grid format
    sample_space = []
    for state in unique_states:
        grid = [[" " for i in range(3)] for j in range(3)]
        for i in range(9):
            grid[i // 3][i % 3] = state[i]
        sample_space.append(grid)

    
    return sample_space

    



def print_board(board: str):
    print(f"""
{board[0]} | {board[1]} | {board[2]}
---------
{board[3]} | {board[4]} | {board[5]}
---------
{board[6]} | {board[7]} | {board[8]}""")
    
def player_turn(board, player):
    while True:
        try:
            num = int(input(f"Player {player}, enter the cell number (0-8): "))
            if board[num] == " ":
                board = board[:num] + player + board[num+1:]
                return board, num
            else:
                print("That position is already taken. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter numbers between 0 and 8.")

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

def game_loop(board, player):
    print_board(board)
    board, move = player_turn(board, player)
    return board, move
    


if __name__ == "__main__":
    #game always starts with X
    
    board = " " * 9
    X_move_list = []
    O_move_list = []
    player = 1 # 1 = X, 0 = O
    while True:
        board, move = game_loop(board, "X" if player == 1 else "O")
        if player == 1:
            X_move_list.append(move)
        else:
            O_move_list.append(move)
        
        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"Player {winner} wins!")
            break
        
        
        player = 1 - player # Switch player