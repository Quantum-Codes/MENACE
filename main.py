from menace import AI


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

def game_loop(board, player):
    print_board(board)
    board, move = player_turn(board, player)
    return board, move
    


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