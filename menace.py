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


def filter_game_state():
    all_states = generate_all_states()
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


def fill_board(board, index, boards):
    board = board.copy()
    if index == 9:
        boards.append("".join(board))
        return
    for symbol in ["X", "O", " "]:
        board[index] = symbol
        fill_board(board, index + 1, boards)

def generate_all_boards():
    boards = []
    board = [" "] * 9
    fill_board(board, 0, boards)
    return boards

if __name__ == "__main__":
    print(len(generate_all_boards()))  #prints 765 unique game states after removing invalid and symmetric states