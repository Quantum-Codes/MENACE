def permutation(possibilities):
    for possibility in possibilities:
        return [possibility+" ",possibility+"X",possibility+"O"]

    
def game_state():
    all_states = [""]
    for i in range(9):
        all_states.extend(permutation(all_states))
    
    for string in all_states:
        grid = [[" " for i in range(3)] for j in range(3)]
        for i in range(9):
            grid[i // 3][i % 3] = string[i]



def print_board(board):
    print()
    print(" | ".join(board[0]))
    print("-" * 9)
    print(" | ".join(board[1]))
    print("-" * 9)
    print(" | ".join(board[2]))

def player_turn(board, player):
    while True:
        try:
            num = int(input(f"Player {player}, enter the cell number (0-8): "))
            if board[num // 3][num % 3] == " ":
                board[num // 3][num % 3] = player
                break
            else:
                print("That position is already taken. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter numbers between 0 and 2.")

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
    player_turn(board, player)
    winner = check_winner(board)

    if winner:
        print_board(board)
        print(f"Player {winner} wins!")
        exit()
    


if __name__ == "__main__":
    board = [[" ", " ", " "] for _ in range(3)]

    player = 1 # 1 = X, 0 = Y
    while True:
        game_loop(board, "X" if player == 1 else "O")
        player = 1 - player # Switch player