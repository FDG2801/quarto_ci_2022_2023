from .objects import Quarto


def possible_actions(state: Quarto) -> list:
    return [index for index, value in enumerate(state.get_board_status()) if value == -1]
