import sys

# Global variables
board = [0] * 9
flag = False

# Function definitions


def print_board():
    print("-------------")
    for i in range(3):
        print("| ", end="")
        for j in range(3):
            if board[3 * i + j]:
                if board[3 * i + j] == 1:
                    print("X | ", end="")
                else:
                    print("O | ", end="")
            else:
                print("  | ", end="")
        print("\n-------------")


def is_valid_move(row, col):
    return row <= 2 and col <= 2 and not board[3 * row + col]


def has_winner(player):
    for i in range(3):
        if player == board[3 * i] == board[3 * i + 1] == board[3 * i + 2]:
            return True
        if player == board[i] == board[i + 3] == board[i + 6]:
            return True
    return (
        player == board[0] == board[4] == board[8]
        or player == board[2] == board[4] == board[6]
    )


def is_board_full():
    return all(board)


def evaluate_board():
    if has_winner(1):
        return 10
    if has_winner(2):
        return -10
    return 0


def minimax(depth, is_maximizing):
    score = evaluate_board()
    if score:
        return score
    if is_board_full():
        return 0
    if is_maximizing:
        best_score = float("-inf")
        for i in range(3):
            for j in range(3):
                if not board[3 * i + j]:
                    board[3 * i + j] = 1
                    best_score = max(best_score, minimax(depth + 1, False))
                    board[3 * i + j] = 0
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if not board[3 * i + j]:
                    board[3 * i + j] = 2
                    best_score = min(best_score, minimax(depth + 1, True))
                    board[3 * i + j] = 0
        return best_score


def make_best_move():
    best_score = float("-inf")
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if not board[3 * i + j]:
                board[3 * i + j] = 1
                move_score = minimax(0, False)
                board[3 * i + j] = 0
                if move_score > best_score:
                    best_score = move_score
                    best_move = (i, j)
    if best_move != (-1, -1):
        board[3 * best_move[0] + best_move[1]] = 1


def main():
    global flag
    for i in range(3):
        for j in range(3):
            board[3 * i + j] = 0
    # make_best_move()
    while not has_winner(1) and not has_winner(2) and not is_board_full():
        print_board()
        row, col = map(
            int, input("Enter your move (row, column, 0 indexing): ").split()
        )
        if is_valid_move(row, col):
            board[3 * row + col] = 2
            if has_winner(2):
                print_board()
                print("You win!")
                flag = True
                print("It can't be...")
                print("BITSCTF{n0t_th4T_eZ}")
            elif is_board_full():
                print_board()
                print("It's a draw!")
                return
            make_best_move()
            if has_winner(1):
                print_board()
                print("AI wins (not really)!")
                return
            if is_board_full():
                print_board()
                print("It's a draw!")
                return
        else:
            print("Invalid move! Try again.")


if __name__ == "__main__":
    main()
