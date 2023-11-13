from game_functions import generate_secret_code
from game_functions import guess_code
from game_functions import check_guess
from game_functions import is_win
from game_functions import display_board
from colorama import init, Fore, Style
from version_info import VER, VER_DATE

# GAME CONSTANTS
PINS = 4  # amount of pins used for the secret code
MAX_TRIES = 12  # maximum tries for guessing the code
init(autoreset=True)  # Initializes colorama


def game(max_tries: int = MAX_TRIES):
    """ Function with game loop. Returns None. """

    board = []  # represents players guesses
    pins_score = []  # represents red and white pins (red is correct spot, white is correct color
    win = False
    guesses = 0  # represents the amount of guesses of the player

    print(f"\nMASTERMIND v {VER} {VER_DATE}\n")

    code = generate_secret_code()

    while guesses < max_tries and not win:

        guesses += 1

        # prints the guess number
        text = f"Guess {guesses}"
        print(text)
        print("-" * len(text))

        new_guess = guess_code()  # Lets player guess the code

        # check the players guess for red and white pins. returns tuple with amount of red and white pins.
        red_pins, white_pins = check_guess(code, new_guess[:])

        # append player guess to the board list
        board.append(new_guess)

        # append pin results (white & red pins score) to the pins list
        pins_score.append(Style.BRIGHT + Fore.RED + f"\t{red_pins}" + Fore.WHITE + f"\t{white_pins}")

        # display the game board in the interpreter (player guesses and pins)
        display_board(board, pins_score)

        # check if the player guess results in a win situation
        win = is_win(red_pins)

    placeholder = 'try' if guesses == 1 else 'tries'

    if win:
        print(f"\033[3;33mCongratulations!\033[0;0m You have guessed the secret code in {guesses} {placeholder}!")
    else:
        print(f"Too bad! You did not guess the secret code within {max_tries} tries!")

    print("The secret code was:", code, "\n")

    while True:
        play_again = input("Play again (y/n): ")
        if play_again.lower().startswith("y"):
            game()

        elif play_again.lower().startswith("n"):
            quit()


if __name__ == "__main__":
    game()
