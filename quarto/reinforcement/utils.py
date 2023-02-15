import numpy as np

def cook_status(game, board: np.ndarray) -> dict:
    status = dict()

    high_values = [
        elem for elem in board.ravel() if elem >= 0 and game.get_piece_charachteristics(elem).HIGH
    ]
    coloured_values = [
        elem for elem in board.ravel() if elem >= 0 and game.get_piece_charachteristics(elem).COLOURED
    ]
    solid_values = [
        elem for elem in board.ravel() if elem >= 0 and game.get_piece_charachteristics(elem).SOLID
    ]
    square_values = [
        elem for elem in board.ravel() if elem >= 0 and game.get_piece_charachteristics(elem).SQUARE
    ]
    low_values = [
        elem for elem in board.ravel() if elem >= 0 and not game.get_piece_charachteristics(elem).HIGH
    ]
    noncolor_values = [
        elem for elem in board.ravel() if elem >= 0 and not game.get_piece_charachteristics(elem).COLOURED
    ]
    hollow_values = [
        elem for elem in board.ravel() if elem >= 0 and not game.get_piece_charachteristics(elem).SOLID
    ]
    circle_values = [
        elem for elem in board.ravel() if elem >= 0 and not game.get_piece_charachteristics(elem).SQUARE
    ]

    elements_per_type = [(len(high_values), 8), (len(coloured_values), 4), (len(solid_values), 2),
                         (len(square_values), 1),
                         (len(low_values), 0), (len(noncolor_values), 0), (len(hollow_values), 0),
                         (len(circle_values), 0)]

    rows_at_risk = list()
    columns_at_risk = list()
    diagonals_at_risk = list()
    for i in range(5):
        rows_at_risk.append(list())
        columns_at_risk.append(list())

    # 0 empty cells -> risk is 0
    # 1 empty cells -> risk is 4
    # 2 empty cells -> risk is 3
    # 3 empty cells -> risk is 2
    # 4 empty cells -> risk is 1
    for i in range(4):
        rows_at_risk[abs(list(board[i]).count(-1) - 5) % 5].append(i)
        columns_at_risk[abs(list(np.array(board).T[i]).count(-1) - 5) % 5].append(i)

    holes_count_main = 0
    holes_count_secondary = 0
    for i in range(4):
        if board[i][i] == -1:
            holes_count_main += 1
        if board[i][4 - i - 1] == -1:
            holes_count_secondary += 1

    if holes_count_main == 1:
        diagonals_at_risk.append(1)  # at this point the main diagonal is at risk
    if holes_count_secondary == 1:
        diagonals_at_risk.append(2)  # at this point the secondary diagonal is at risk

    status["elements_per_type"] = elements_per_type
    status["rows_at_risk"] = rows_at_risk
    status["columns_at_risk"] = columns_at_risk
    status["diagonals_at_risk"] = diagonals_at_risk

    return status

