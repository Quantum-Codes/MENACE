class AI:
    def __init__(self,player):
        self.X_move_list = []
        self.O_move_list = []
        self.player = player   
        self.unique_states = filter_game_states() 
        self.games_played = 0

    def save_move(self, move, player):
        if player == 1:
            self.X_move_list.append(move)
        else:
            self.O_move_list.append(move)
    
    def reset_game_state(self, winner):
        
        
        if winner == "X" and self.player == 1 or winner == "O" and self.player == 0:
            win = 1
        elif winner == "X" and self.player == 0 or winner == "O" and self.player == 1:
            win = -1
        else:
            win = 0
        played_states, played_indexes = generate_played_states(self.X_move_list, self.O_move_list, self.unique_states)[0], generate_played_states(self.X_move_list, self.O_move_list, self.unique_states)[1]
        self.unique_states = update_beads(played_states,played_indexes,self.unique_states,win)



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
    
    if board.count(" ")==0:
        return "draw"
    
    return None

def filter_game_states():
    all_states = generate_all_states()
    #remove all where (number of X) - (number of O) > 1 since we can only have alternating moves and X always starts
    # same as generating a new list with only valid states
    new_all_states = []
    for state in all_states:
        if 0 <= (state.count("X") - state.count("O")) <= 1 and state.count(" ") > 1:
            new_all_states.append(state)

    all_states = new_all_states
    
    #remove rotations and mirrored states. 
    # For this we pick a state one at a time, generate all its rotations and mirrored versions, and then check if any of those already exist in new_states. IF not we add them.
    unique_states = {}
    index_map = [6,3,0,7,4,1,8,5,2] # 90 deg rotated indexes. we can repeat this rotation again and again for every rotation.
    mirror_y_map = [2,1,0,5,4,3,8,7,6] # mirrored indexes along y axis
    mirror_x_map = [6,7,8,3,4,5,0,1,2] # mirrored indexes along x axis

    for state in all_states:
        # If already won, skip. Dont waste processing time.
        if check_winner(state):
            continue
        
        # make mirror images
        y_mirror = ''.join([state[index] for index in mirror_y_map])
        x_mirror = ''.join([state[index] for index in mirror_x_map])
        similar_states = [state, x_mirror, y_mirror]

        # generate rotations (90 deg at a time)
        to_rotate = state
        to_rotate_y = y_mirror
        to_rotate_x = x_mirror
        for _ in range(3):
            to_rotate = ''.join([to_rotate[index] for index in index_map])
            to_rotate_y = ''.join([to_rotate_y[index] for index in index_map])
            to_rotate_x = ''.join([to_rotate_x[index] for index in index_map])
            similar_states.append(to_rotate)
            similar_states.append(to_rotate_y)
            similar_states.append(to_rotate_x)

        # check if any of the similar states already exist in unique_states
        for item in similar_states:  
            if item in unique_states:
                break
        else:
            #add the initial beads to each state
            #the number of beads is stored in a list of 9 items (corresponding to 9 boxes) and every possible move(" ") will get 1 bead while others get 0.
            beads = [int(" "==state[i]) for i in range(9)]
            unique_states[state] = beads #if none matches then for loop is not broken and the state is added (for-else loop)

    return unique_states

def generate_played_states(X_moves, O_moves, unique_states):#generate all board positions that happend
    played_states = ["         "] #the first state
    prev_order = "012345678"
    state = [" " for j in range(9)]
    idx = []
    x_idx = o_idx = 0
    while x_idx<=len(X_moves): #X and O are put in same iteration. So, x_idx is checked as it starts first
        if x_idx==o_idx:
            state[X_moves[x_idx]] = "X"
            added_idx = X_moves[x_idx]
            x_idx+=1
            
        else:
            state[O_moves[o_idx]] = "O"
            added_idx = O_moves[o_idx]
            o_idx+=1
            
        winner = check_winner("".join(state))
        if winner==None and state.count(" ")>1:
            idx.append(prev_order.index(str(added_idx)))
            present_state, prev_order = find_similar_states("".join(state),unique_states)[0], find_similar_states("".join(state),unique_states)[1] 
            played_states.append(present_state)
            
        else:
            idx.append(prev_order.index(str(added_idx)))
            break #The winning states are not stored in the unique states.
            
    return (played_states,idx)


def find_similar_states(state, unique_states):
    index_map = [6,3,0,7,4,1,8,5,2]
    mirror_y_map = [2,1,0,5,4,3,8,7,6]
    mirror_x_map = [6,7,8,3,4,5,0,1,2]
    # make mirror images
    y_mirror = ''.join([state[index] for index in mirror_y_map])
    x_mirror = ''.join([state[index] for index in mirror_x_map])
    similar_states = [state, x_mirror, y_mirror]

    # generate rotations (90 deg at a time)
    to_rotate = state
    to_rotate_y = y_mirror
    to_rotate_x = x_mirror
    for _ in range(3):
        to_rotate = ''.join([to_rotate[index] for index in index_map])
        to_rotate_y = ''.join([to_rotate_y[index] for index in index_map])
        to_rotate_x = ''.join([to_rotate_x[index] for index in index_map])
        similar_states.append(to_rotate)
        similar_states.append(to_rotate_y)
        similar_states.append(to_rotate_x)
    idx = ["0123456789",
            "678345012",
            "210543876",
            "630741852",
            "852741630",
            "036147258",
            "876543210",
            "678345012",
            "210543876",
            "258147036",
            "036147258",
            "852741630"]
    
    count = 0
    for item in similar_states:  #it is guaranteed that one of the similar states exist as all possible unique board is stored
        if item in unique_states:
            return (item,idx[count])
        count+=1

    

   
def update_beads(played_states,played_indexes,unique_states,win): #win=1 if the ai wins, win=0 if it draws and win=-1 for a loss
    #played states is the list of states played in the position
    

    for i in range(len(played_states)):
        beads = unique_states[played_states[i]]
        if beads[played_indexes[i]]!=0:
            beads[played_indexes[i]] = ((win//2)+1)*(beads[played_indexes[i]] + win*2+1)  # if win=1 => +3; win=0 => +1; win=-1 => remove all
        unique_states[played_states[i]] = beads
    return unique_states
                


if __name__ == "__main__":
    import time
    start_time = time.time()
    print(len(filter_game_states())) 
    print(f"Time taken: {time.time() - start_time} seconds")
