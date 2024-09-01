"""DON'T USE AS A MODULE"""
import re as regex

print(f"Running on {__name__}")

GRID_SIZE: int = 3
GRID_DATA: dict[tuple[int, int], int] = {}
LOCATION_REGEX: str = r"(\d+)x(\d+)"

CHECK_MATRIX: list[list[tuple[int, int]]] = [
    [ (0, 0), (1, 0), (2, 0) ], # ROW 1
    [ (0, 1), (1, 1), (2, 1) ], # ROW 2
    [ (0, 2), (1, 2), (2, 2) ], # ROW 3

    [ (0, 0), (0, 1), (0, 2) ], # COL 1
    [ (1, 0), (1, 1), (1, 2) ], # COL 2
    [ (2, 0), (2, 1), (2, 2) ], # COL 3

    [ (0, 0), (1, 1), (2, 2) ], # DIAGONAL
    [ (2, 0), (1, 1), (0, 2) ], # ANTI DIAGONAL
]

PLAYER_KEYS: dict[int, str] = {
    0: "O",
    1: "X"
}

# TicTacToe Board
#  O | X | O    0 0
# ---|---|---   ~ 1
#  X | O | X    1 2
# ---|---|---   ~ 3
#  O | X | X    2 4

def generate_board_line() -> str:
    """Generates the board's board for a row

    Returns
        str: The board line
    """
    buffer: str = ""
    chars: int = GRID_SIZE * 4
    for i in range(1, chars):
        is_hor = i % 4 == 0 and i != 0
        buffer += "|" if is_hor else "-"
    return buffer

def generate_row(y: int) -> str:
    """Generates a row (based on the `GRID_DATA`) for `render_board`

    Args
        y (int): The row axis

    Returns:
        str: A row from `GRID_DATA` represented in a string
    """
    buffer: str = ""
    for x in range(GRID_SIZE):
        slot: int | None = GRID_DATA.get((x, y), None)
        player_name: str = " " if slot is None else PLAYER_KEYS[slot]
        sub_buf = f" {player_name} "
        if x != GRID_SIZE - 1:
            sub_buf += "|"
        buffer += sub_buf
    return buffer

def render_board() -> str:
    """Renders the board inside a string

    Returns
        str: The board represented in a string
    """
    total_rows = GRID_SIZE + 2
    buffer: list[str] = []
    line_str: str = generate_board_line()

    for row in range(0, total_rows):
        is_line: bool = row % 2 == 1

        if not is_line:
            buffer.append(generate_row(row // 2))
        else:
            buffer.append(line_str)
    return "\n".join(buffer)

def input_location() -> tuple[int, int]:
    """
    Gets the input for the TicTacToe board.

    Returns
          tuple[int, int]: The grid location
    """
    input_str: str = input("Pick a location, e.g. 1x1: ")
    regex_match = regex.search(LOCATION_REGEX, input_str)
    if regex_match is None:
        print("Can't be validated, please try again...")
        return input_location()

    x, y = int(regex_match.group(1)) - 1, int(regex_match.group(2)) - 1
    if not is_board_location_valid((x, y)):
        print("This location can't be placed, please try again...")
        return input_location()
    return x, y

def use_check_matrix() -> int | None:
    """Uses the `CHECK_MATRIX` to check of a winner

    Returns
        int | None: The winner's ID
    """
    winner: int | None = None

    for _, check_set in enumerate(CHECK_MATRIX):
        first: int | None = GRID_DATA.get(check_set[0], None)
        success: bool = True
        if first is None:
            continue
        for i in range(1, GRID_SIZE):
            x, y = check_set[i]
            claimed_by: int | None = GRID_DATA.get((x, y), None)
            if claimed_by != first:
                success = False
                break
        if success:
            winner = first

    return winner

def is_board_location_valid(at: tuple[int, int]) -> bool:
    """Checks if a location is valid. Checking:
    • In range,
    • Is the node taken

    Args:
        at (tuple[int, int]): The location of the check

    Returns
        bool: Is the location valid
    """
    x, y = at[0], at[1]

    x_in_range = 0 <= x < GRID_SIZE
    y_in_range = 0 <= y < GRID_SIZE

    if not x_in_range or not y_in_range:
        return False

    node: int | None = GRID_DATA.get(at, None)

    return node is None

def award_winner(winner: int):
    """Awards the winner, with cake and coke(-a-cola)

    Args:
        winner (int): The winner's ID
    """
    player_name: str = PLAYER_KEYS[winner]
    print(f"🥤🎂 Player {player_name} won!!! 🎂🥤")

def on_draw():
    """You both lost. You don't actually lose System32.
    """
    print("Deleting System32")

def game_loop():
    """The TicTacToe's boards main game loop"""
    i: int = 0

    while True:
        current_player: int = i % 2
        player_name: str = PLAYER_KEYS[current_player]

        print(f"It is {player_name} turn!")
        location: tuple[int, int] = input_location()

        GRID_DATA[location] = current_player

        print(render_board())

        winner: int | None = use_check_matrix()
        if winner is not None:
            award_winner(winner)
            break
        if i + 1 >= GRID_SIZE * GRID_SIZE:
            on_draw()
            break
        i += 1

if __name__ == "__main__":
    print("Ready!")
    game_loop()
    input("Press Enter to Exit") # yielding the game until enter
else:
    raise NameError(f"Wrong file name, {__name__}")
