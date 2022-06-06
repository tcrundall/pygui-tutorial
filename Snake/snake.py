from dataclasses import dataclass
from typing import Tuple
import PySimpleGUI as sg
from time import time
import random


@dataclass
class Direction:
    name: str
    offset: Tuple[int, int]
    opposite: str


# game constants
FIELD_SIZE = 400
GRID_SIZE = 10
CELL_SIZE = FIELD_SIZE / GRID_SIZE
NAPPLES = 5
CLOCK = 0.3    # seconds

DIRECS = {
    'left': Direction('left', (-1, 0), 'right'),
    'up': Direction('up', (0, 1), 'down'),
    'right': Direction('right', (1, 0), 'left'),
    'down': Direction('down', (0, -1), 'up'),
}


def draw_square(i, j, field, color='blue'):
    topleft = (i * CELL_SIZE, (j + 1) * CELL_SIZE)
    botright = ((i + 1) * CELL_SIZE, j * CELL_SIZE)
    field.draw_rectangle(top_left=topleft, bottom_right=botright,
                         fill_color=color)


def move_snake(snake, direction, ate_apple):
    head_cell = snake[-1]
    offset = direction.offset
    next_cell = (
        head_cell[0] + offset[0],
        head_cell[1] + offset[1],
    )

    if not ate_apple:
        snake.pop(0)

    snake.append(next_cell)

    if next_cell in snake[:-1]:
        return False

    return 0 <= next_cell[0] < GRID_SIZE and 0 <= next_cell[1] < GRID_SIZE


def place_apple(snake, apples):
    ncells = GRID_SIZE * GRID_SIZE
    snake_size = len(snake)
    n_apples = len(apples)
    if ncells == snake_size + n_apples:
        return

    while True:
        apple_pos = (
            random.randint(0, GRID_SIZE - 1),
            random.randint(0, GRID_SIZE - 1)
        )
        if apple_pos not in snake and apple_pos not in apples:
            break

    apples.append(apple_pos)


def init_game():
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    snake = [(2, 3), (3, 3), (4, 3), (5, 3)]
    snake_dir = DIRECS['right']

    apples = []
    for _ in range(NAPPLES):
        place_apple(snake, apples)

    return grid, snake, snake_dir, apples


sg.theme('Green')
field = sg.Graph(
    canvas_size=(FIELD_SIZE, FIELD_SIZE),
    graph_bottom_left=(0, 0),
    graph_top_right=(FIELD_SIZE, FIELD_SIZE),
    background_color='black',
)
layout = [[field]]

window = sg.Window("Snake", layout=layout, finalize=True)

window.bind('<Left>', 'left')
window.bind('<Right>', 'right')
window.bind('<Up>', 'up')
window.bind('<Down>', 'down')
window.bind('<space>', 'space')

grid, snake, snake_dir, apples = init_game()
dir_buffer = []
ate_apple = False

last_tick = time() 
running = True
while True:
    event, values = window.read(timeout=10)

    # draw snake
    print(event)
    if event == sg.WIN_CLOSED:
        break

    if event in DIRECS and len(dir_buffer) < 2:
        new_dir = DIRECS[event]
        if dir_buffer:
            last_queued_dir = dir_buffer[-1]
        else:
            last_queued_dir = snake_dir
        if last_queued_dir.name != new_dir.opposite:
            dir_buffer.append(new_dir)

    if event == 'space' and not running:
        grid, snake, snake_dir, apples = init_game()
        dir_buffer = []
        ate_apple = False

        last_tick = time() 
        running = True

    # mimic clock
    if running and time() - last_tick > CLOCK:
        # reset last tick
        last_tick = time()

        # update position
        if dir_buffer:
            snake_dir = dir_buffer.pop(0)

        valid_move = move_snake(snake, snake_dir, ate_apple)
        if not valid_move:
            running = False
            continue

        ate_apple = False

        # handle "game logic"
        if snake[-1] in apples:
            apples.remove(snake[-1])
            place_apple(snake, apples)
            ate_apple = True

        # redraw field
        field.erase()
        for apple_pos in apples:
            draw_square(*apple_pos, field, color='red')  # apples

        for cell in snake[:-1]:
            draw_square(*cell, field)                    # snake body
        draw_square(*snake[-1], field, color='yellow')   # snake head

window.close()
