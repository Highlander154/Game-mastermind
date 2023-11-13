import pygame
import game_functions
from version_info import VER, VER_DATE
from pygame.locals import *
from colors import *
from random import choice

PAWNS = 6  # Game supports 1 to 10 pawns
ROWS = 10  # Game supports 1 to 12 rows

WIN_SIZE = [1280, 800]  # Window width, Window height
FPS = 60  # Frames per second
PAWN_SIZE = (25, 25)  # image size for pawns

BOARD_WIDTH = 3 * PAWNS * PAWN_SIZE[0] + 6 * PAWN_SIZE[0]  # Dynamic board width
BOARD_HEIGHT = 2 * ROWS * PAWN_SIZE[0] + 3 * PAWN_SIZE[0]  # Dynamic board height

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption(f'Crack the code game v{VER} ({VER_DATE})')
pygame.display.set_icon(pygame.image.load('img/2.png'))

# Welcome screen image
welcome_screen_img = pygame.transform.scale(pygame.image.load('img/mastermind.jpg'), (1280, 800)).convert_alpha()

# Load the pawn images
red_pawn = pygame.transform.scale(pygame.image.load('img/1.png'), PAWN_SIZE).convert_alpha()
green_pawn = pygame.transform.scale(pygame.image.load('img/2.png'), PAWN_SIZE).convert_alpha()
orange_pawn = pygame.transform.scale(pygame.image.load('img/3.png'), PAWN_SIZE).convert_alpha()
purple_pawn = pygame.transform.scale(pygame.image.load('img/4.png'), PAWN_SIZE).convert_alpha()
blue_pawn = pygame.transform.scale(pygame.image.load('img/5.png'), PAWN_SIZE).convert_alpha()
yellow_pawn = pygame.transform.scale(pygame.image.load('img/6.png'), PAWN_SIZE).convert_alpha()

# load the empty hole image
hole = pygame.transform.scale(pygame.image.load('img/Hole.png'), PAWN_SIZE).convert_alpha()
small_hole = pygame.transform.scale(pygame.image.load('img/Hole_10pct.png'), PAWN_SIZE).convert_alpha()

# load the pin images
red_pin = pygame.transform.scale(pygame.image.load('img/red_50pct.png'), PAWN_SIZE).convert_alpha()
white_pin = pygame.transform.scale(pygame.image.load('img/white_50pct.png'), PAWN_SIZE).convert_alpha()

# dictionaries for storing pawns and pins
pawns = {'R': red_pawn, 'G': green_pawn, 'O': orange_pawn, 'P': purple_pawn, 'B': blue_pawn, 'Y': yellow_pawn}
pins = {'r': red_pin, 'w': white_pin}

secret_code = []  # Secret code
player_board = []  # Player pawns
score_pins = []  # player scores
guess_placeholder = ['' for _ in range(PAWNS)]  # placeholder for current players guess

# Game music
pygame.mixer.music.load('music/Modern Castle Atmosphere.mp3')
pygame.mixer.music.play(-1)


def render_welcome_screen():
    window.blit(welcome_screen_img, (0, 0))
    mus_font = pygame.font.SysFont('Consolas', 10, True)
    welcome_font = pygame.font.SysFont('Consolas', 28, True)

    mus_txt = mus_font.render("music 'Modern Castle Atmosphere' by Bogart VGM https://www.facebook.com/BogartVGM/",
                              True, WHITE)
    mus_rect = mus_txt.get_rect(center=(1000, 775))
    window.blit(mus_txt, mus_rect)

    for i in range(255):
        start = welcome_font.render('- Press SPACE to start -', True, (i, i, i))
        start_rect = start.get_rect(center=(1000, 750))
        window.blit(start, start_rect)
        pygame.display.update()
        clock.tick()


def render_player_board(player_pawns, player_score):
    pawn_start_x = 200
    pawn_start_y = 100
    score_pin_start_x = pawn_start_x + 2 * PAWNS * PAWN_SIZE[0] + 2 * PAWN_SIZE[0]
    score_pin_start_y = 100
    spacing_pin_x = 25
    spacing_pawn = spacing_pin_y = 50

    # render the board
    pygame.draw.rect(window, GREY, (pawn_start_x - 50, pawn_start_y - 50, BOARD_WIDTH, BOARD_HEIGHT), 0, 25)
    pygame.draw.rect(window, DARK_GREY,
                     (pawn_start_x - 25, pawn_start_y - 25, 2 * PAWNS * PAWN_SIZE[0] + PAWN_SIZE[0],
                      BOARD_HEIGHT - 50), 2, 20)
    pygame.draw.rect(window, DARK_GREY,
                     (score_pin_start_x - 25, score_pin_start_y - 25, PAWNS * PAWN_SIZE[0] + 2 * PAWN_SIZE[0],
                      BOARD_HEIGHT - 50), 2, 20)

    # Render the holes
    for i in range(ROWS):
        for j in range(PAWNS):
            window.blit(hole, (pawn_start_x + j * spacing_pawn, pawn_start_y + i * spacing_pawn))
            window.blit(small_hole, (score_pin_start_x + j * spacing_pin_x, score_pin_start_y + i * spacing_pin_y))

    # render board from board data
    for i, row in enumerate(player_pawns):
        for j, pawn in enumerate(row):
            if pawn != '':
                window.blit(pawns[pawn], (pawn_start_x + j * spacing_pawn, pawn_start_y + i * spacing_pawn))

    # render score pins from score_pins data
    for i, row in enumerate(player_score):
        for j, pin in enumerate(row):
            if pin != '':
                window.blit(pins[pin], (score_pin_start_x + j * spacing_pin_x, score_pin_start_y + i * spacing_pin_y))

    # render column selection text (numbers)
    column_font = pygame.font.SysFont('Consolas', 14, True)
    for i in range(PAWNS):
        if len(player_board) != ROWS and not win:
            column_text = column_font.render(f'{i+1}', True, DARK_GREY)
            column_text_rect = column_text.get_rect(midtop=(pawn_start_x + PAWN_SIZE[0]/2 + 2*i*PAWN_SIZE[0],
                                                            pawn_start_y + PAWN_SIZE[0] +
                                                            len(player_pawns)*2*PAWN_SIZE[0] - 20))
            window.blit(column_text, column_text_rect)


def render_selected_slot(slot_choice: int = 1):
    if slot_choice > 0 and len(player_board) < ROWS and not win:
        pawn_start_x = 200 + (slot_choice-1)*2*PAWN_SIZE[0]
        pawn_start_y = 100 + len(player_board)*2*PAWN_SIZE[0]
        center = (pawn_start_x + PAWN_SIZE[0]/2 + 1, pawn_start_y + PAWN_SIZE[0]/2 + 1)
        pygame.draw.circle(window, RED, center, PAWN_SIZE[0]/2 + 8, 3)


def render_color_options(slot_choice: int = 0, color_index=0):
    if slot_choice > 0 and color_index:
        pawn_color = ''
        idx: int = slot_choice-1
        pawn_start_x = 200 + (slot_choice-1)*2*PAWN_SIZE[0]
        pawn_start_y = 100 + len(player_board)*2*PAWN_SIZE[0]
        image = pygame.transform.scale(pygame.image.load(f'img/{color_index}.png'), PAWN_SIZE).convert_alpha()
        window.blit(image, (pawn_start_x, pawn_start_y))
        if color_index == 1: pawn_color = 'R'
        elif color_index == 2: pawn_color = 'G'
        elif color_index == 3: pawn_color = 'O'
        elif color_index == 4: pawn_color = 'P'
        elif color_index == 5: pawn_color = 'B'
        elif color_index == 6: pawn_color = 'Y'
        guess_placeholder[idx] = pawn_color


def render_player_guess(player_guess=None):
    if player_guess is None:
        player_guess = guess_placeholder

    spacing_pawn = 50

    for idx, pawn in enumerate(player_guess):
        if pawn != '':
            pawn_start_x = 200 + idx * spacing_pawn
            pawn_start_y = 100 + len(player_board) * 2 * PAWN_SIZE[0]
            window.blit(pawns[pawn], (pawn_start_x, pawn_start_y))


def render_player_wins():
    win_font = pygame.font.SysFont('Consolas', 28, True)

    render_secret_code()

    for i in range(255):
        win_txt = win_font.render('Congratulations! You Won!', True, (i, i, i))
        win_rect = win_txt.get_rect(center=(3*(WIN_SIZE[0]/4), 500))
        window.blit(win_txt, win_rect)
        pygame.display.update()
        clock.tick()


def render_player_loses():
    lose_font = pygame.font.SysFont('Consolas', 28, True)

    render_secret_code()

    for i in range(255):
        lose_txt = lose_font.render('Sad! You lost!', True, (i, i, i))
        lose_rect = lose_txt.get_rect(center=(3*(WIN_SIZE[0]/4), 500))
        window.blit(lose_txt, lose_rect)
        pygame.display.update()
        clock.tick()


def render_secret_code(code=None):
    if code is None:
        code = secret_code

    spacing_pawn = 75

    code_font = pygame.font.SysFont('Consolas', 28, True)
    code_txt = code_font.render('The secret code was', True, WHITE)
    code_rect = code_txt.get_rect(center=(3*(WIN_SIZE[0]/4), 350))
    window.blit(code_txt, code_rect)

    for idx, pawn in enumerate(code):
        if pawn != '':
            pawn_start_x = 840 + idx * spacing_pawn
            pawn_start_y = 400
            window.blit(pawns[pawn], (pawn_start_x, pawn_start_y))


game_running = True
game_state = 'welcome_screen'
selected_slot = 1
pawn_index = 0
win = False


while game_running:

    for event in pygame.event.get():
        if event.type == QUIT:
            game_running = False

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if game_state == 'welcome_screen':
                    game_state = 'game'
                    temp_pawn = choice(list(pawns.values()))
                    secret_code = game_functions.generate_secret_code(PAWNS)
                    # print("Secret Code:", secret_code)
                    player_board = []  # Player pawns
                    score_pins = []  # player scores
                    guess_placeholder = ['' for _ in range(PAWNS)]  # placeholder for current players guess
                    win = False
                else:
                    game_state = 'welcome_screen'

            if game_state == 'game' and len(player_board) != ROWS and not win:

                # Number keys represent the slots
                if event.key == K_1 and PAWNS >= 1: selected_slot = 1
                if event.key == K_2 and PAWNS >= 2: selected_slot = 2
                if event.key == K_3 and PAWNS >= 3: selected_slot = 3
                if event.key == K_4 and PAWNS >= 4: selected_slot = 4
                if event.key == K_5 and PAWNS >= 5: selected_slot = 5
                if event.key == K_6 and PAWNS >= 6: selected_slot = 6
                if event.key == K_7 and PAWNS >= 7: selected_slot = 7
                if event.key == K_8 and PAWNS >= 8: selected_slot = 8
                if event.key == K_9 and PAWNS >= 9: selected_slot = 9
                if event.key == K_0 and PAWNS == 10: selected_slot = 10

                # Arrow left and right move through slots
                if event.key == K_RIGHT and selected_slot < PAWNS:
                    selected_slot += 1
                    pawn_index = 0
                if event.key == K_LEFT and selected_slot > 1:
                    selected_slot -= 1
                    pawn_index = 0

                # Arrow up and down select color options (continuous loop through available colors)
                if event.key == K_UP and pawn_index < len(pawns): pawn_index += 1
                elif event.key == K_UP and pawn_index == len(pawns): pawn_index = 1
                if event.key == K_DOWN and pawn_index > 0: pawn_index -= 1
                if event.key == K_DOWN and pawn_index == 0: pawn_index = len(pawns)

                # Hit enter to accept user input, add it to the board and check the result
                if event.key == K_RETURN and '' not in guess_placeholder:
                    # print("Guess placeholder:", guess_placeholder)
                    player_board.append(guess_placeholder)
                    # print("Player board:", player_board)
                    result_check = game_functions.check_guess(secret_code=secret_code, player_guess=guess_placeholder, num_pins=PAWNS)
                    # print("Result check:", result_check)
                    result_pins = game_functions.convert_score(result_check[0], result_check[1])
                    # print("Result pins:", result_pins)
                    score_pins.append(result_pins)
                    # print("Pins board:", score_pins)
                    guess_placeholder = ['' for _ in range(PAWNS)]
                    pawn_index = 0
                    selected_slot = 1
                    win = game_functions.is_win(red_pins=result_check[0], num_pins=PAWNS)

    if game_state == 'welcome_screen':
        window.fill(WHITE)
        render_welcome_screen()

    elif game_state == 'game':
        window.fill(BLACK)
        render_player_board(player_board, score_pins)
        render_selected_slot(selected_slot)
        render_color_options(selected_slot, pawn_index)
        render_player_guess()
        if win:
            render_player_wins()
        if len(score_pins) == 12 and not win:
            render_player_loses()
    clock.tick(FPS)
    pygame.display.update()
