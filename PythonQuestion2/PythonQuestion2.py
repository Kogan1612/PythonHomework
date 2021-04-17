
MATRIX_LENGTH = 3  # The size of a line of the game's board
WIN_LENGTH = 3  # The length of a series a player needs to have to win


def check_horizontal_win(game_board):
    """The function receives the game's board and checks if someone won horizontally
    The function returns 0 if no one won, 1 if the first player won and 2 if the second player won
    """
    for y in range(0,MATRIX_LENGTH):
        count = 0
        for x in range(0, MATRIX_LENGTH):
            # We need to check that the previous number is equal to the current number and that it's not an empty square
            # which means it belongs to one of the players
            if count == 0 or (game_board[y][x] == game_board[y][x-1] and game_board[y][x] != 0):
                count += 1
                if count == WIN_LENGTH:
                    return game_board[y][x]
            else:
                count = 0
    return 0

def check_vertical_win(game_board):
    """The function receives the game's board and checks if someone won vertically
    The function returns 0 if no one won, 1 if the first player won and 2 if the second player won
    """
    for x in range(0,MATRIX_LENGTH):
        count = 0
        for y in range(0, MATRIX_LENGTH):
            # We need to check that the previous number is equal to the current number and that it's not an empty square
            # which means it belongs to one of the players
            if count == 0 or (game_board[y][x] == game_board[y-1][x] and game_board[y][x] != 0):
                count += 1
                if count == WIN_LENGTH:
                    return game_board[y][x]
            else:
                count = 0
    return 0

def check_diagonal_win(game_board):
    """The function receives the game's board and checks if someone won diagonally
    The function returns 0 if no one won, 1 if the first player won and 2 if the second player won
    """
    # Check the main diagonal
    x = 0
    y = 0
    count = 0
    while x != MATRIX_LENGTH:  # It doesn't matter if we are checking x or y - the game's board is a square
        # We need to check that the previous number is equal to the current number and that it's not an empty square
        # which means it belongs to one of the players
        if count == 0 or (game_board[y][x] == game_board[y-1][x-1] and game_board[y][x] != 0):
            count += 1
            if count == WIN_LENGTH:
                return game_board[y][x]
        else:
            count = 0
        x += 1
        y += 1

    # Check the antidiagonal
    x = 0
    y = MATRIX_LENGTH - 1
    count = 0
    while x != MATRIX_LENGTH:  # It doesn't matter if we are checking x or y - the game's board is a square
        # We need to check that the previous number is equal to the current number and that it's not an empty square
        # which means it belongs to one of the players
        if count == 0 or (game_board[y][x] == game_board[y+1][x-1] and game_board[y][x] != 0):
            count += 1
            if count == WIN_LENGTH:
                return game_board[y][x]
        else:
            count = 0
        x += 1
        y -= 1

    return 0


def check_win(game_board):
    """The function gets a game board of a tic tac toe game and prints a message suitable message
    if a player won or if it's a tie"""
    result = check_horizontal_win(game_board)
    if result == 0:
        result = check_vertical_win(game_board)
        if result == 0:
            result = check_diagonal_win(game_board)

    if result == 0:
        print("This is a tie!")
    elif result == 1:
        print("Player one won")
    else:
        print("Player two won")


def main():
    game = [[1, 2, 0],
            [2, 1, 0],
            [2, 1, 1]]
    check_win(game)

if __name__ == "__main__":
    main()
