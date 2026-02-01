def permutation(possibilities):
    for possibility in possibilities:
        return [possibility+" ",possibility+"X",possibility+"O"]

    
def game_state():
    solutions = [""]
    for i in range(9):
        solutions.extend(permutation(solutions))
    
    for string in solutions:
        grid = [["" for i in range(3)] for j in range(3)]
        for i in range(9):
            grid[i//3][i%3] = 1



def print_board(board):
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


def game_loop(board):
    print_board(board)
    player_turn(board, "X")
    


if __name__ == "__main__":
    board = [[" ", " ", " "] for _ in range(3)]

    player = 1 # 1 = X, 0 = Y
    while True:
        game_loop(board)