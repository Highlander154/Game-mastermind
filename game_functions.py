# ----------------
# -- MASTERMIND --
# ----------------

from random import choice
from colorama import init, Fore, Style

# GAME CONSTANTS
VER = '0.1.1'  # current version of this game
VER_DATE = '03.02.2022'  # date current version

PINS = 4   # amount of pins used for the secret code
MAX_TRIES = 12  # maximum tries for guessing the code
init(autoreset=True)  # Initializes colorama


def generate_secret_code(num_pins: int = PINS):
    """ Function creates a random secret code for the specified amount of pins.
    The colors will be randomly picked from the colors list. Colors may appear
    more than once in the secret code. """

    colors = ["Y", "O", "R", "P", "B", "G"]
    secret_code = [choice(colors) for _ in range(num_pins)]
    # print("Secret code:", secret_code)
    return secret_code


def guess_code(num_pins: int = PINS):
    """ Function asks for user input to guess the secret code for the specified
    amount of pins and returns the list with colors specified by the user."""

    print("Colors: (Y)ellow, (O)range, (R)ed, (P)urple, (B)lue or (G)reen")
    guess = [input(f"color {i + 1}: ").upper() for i in range(num_pins)]
    return guess


def check_guess(secret_code: list, player_guess: list, num_pins: int = PINS):
    """ Function checks the guess of the user against the secret code and returns
    True or False when the player has won or not.
    The total of white and red pins will be printed out as a hint for the user.
    White pins represent a correct color but wrong position
    Red pins represent a correct color on a correct position"""

    player_guess_copy = player_guess[:]
    red_pins = 0
    correct_colors = 0

    # First check - correct colors in correct spots (red pins)
    for idx in range(num_pins):
        if secret_code[idx] == player_guess_copy[idx]:
            red_pins += 1

    # Second check - correct colors in incorrect spots (white pins)
    for color in secret_code:
        if color in player_guess_copy:
            correct_colors += 1
            player_guess_copy.remove(color)

    white_pins = correct_colors - red_pins
    return red_pins, white_pins


def convert_score(red_pins, white_pins):
    rp = ['r' for _ in range(red_pins)]
    wp = ['w' for _ in range(white_pins)]
    return rp + wp


def is_win(red_pins, num_pins: int = PINS):
    if red_pins == num_pins:
        return True
    return False


def display_board(board, pins):
    """ Function displays the mastermind board with player pins and score indication. Returns None. """

    color = 0
    print("\nBoard:")
    for idx, row in enumerate(board):
        for i in range(PINS):
            if row[i] == 'Y': color = Style.BRIGHT + Fore.LIGHTYELLOW_EX
            elif row[i] == 'R': color = Style.BRIGHT + Fore.RED
            elif row[i] == 'G': color = Style.BRIGHT + Fore.GREEN
            elif row[i] == 'B': color = Style.BRIGHT + Fore.BLUE
            elif row[i] == 'P': color = Style.BRIGHT + Fore.MAGENTA
            elif row[i] == 'O': color = Style.BRIGHT + Fore.YELLOW
            print(color + "∎", end=' ')
        print(pins[idx])
    print()
