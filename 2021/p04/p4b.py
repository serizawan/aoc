import sys
import copy


def is_completed(board):
    for line in board:
        if sum(line) == -5:
            return True

    for i in range(len(board[0])):
        column_sum = 0
        for j in range(len(board)):
            column_sum += board[j][i]
        if column_sum == -5:
            return True
    return False


def set_drawn(drawn, board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == drawn:
                board[i][j] = -1
    return board


def get_last_drawn_and_last_winning_board(draws, boards):
    last_winning_board = None
    while boards:
        drawn = draws.pop(0)
        boards = [set_drawn(drawn, board) for board in boards]
        remaining_boards = []
        for board in boards:
            if is_completed(board):
                last_winning_board = board
            else:
                remaining_boards.append(board)
        boards = remaining_boards
    return drawn, last_winning_board


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    draws = [int(i) for i in lines[0].split(',')]

    board = []
    boards = []
    for line in lines[2:]:
        if line == '':
            boards.append(board)
            board = []
            continue
        board.append([int(i) for i in line.strip().split()])
    boards.append(board)

    drawn, board = get_last_drawn_and_last_winning_board(draws, boards)

    lx = len(board)
    ly = len(board[0])
    score = drawn * sum([board[i][j] if board[i][j] != -1 else 0 for i in range(lx) for j in range(ly)])

    print(score)
