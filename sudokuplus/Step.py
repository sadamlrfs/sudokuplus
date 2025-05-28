import pygame
import sys

pygame.init()

WINDOW_SIZE = (540, 540)
CELL_SIZE = 60
GRID_SIZE = 9
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (196, 220, 255)
RED = (255, 0, 0)

window = pygame.display.set_mode(WINDOW_SIZE)
icon = pygame.image.load('sudokuplus.ico')
pygame.display.set_icon(icon)
pygame.display.set_caption("Sudoku Plus")

font = pygame.font.Font(None, 48)

board = [
    [3, 4, 0,   8, 7, 0,    0, 0, 0],
    [0, 9, 0,   0, 0, 0,    0, 7, 0],
    [0, 0, 0,   3, 9, 0,    0, 0, 0],
    [0, 0, 4,   0, 6, 3,    7, 0, 0],
    [1, 2, 0,   7, 8, 9,    0, 4, 3],
    [0, 0, 7,   4, 2, 0,    5, 0, 0],
    [0, 0, 0,   0, 3, 8,    0, 0, 0],
    [0, 5, 0,   0, 0, 0,    0, 6, 0],
    [0, 0, 0,   0, 5, 4,    0, 3, 7]
]

current_cell = (-1, -1)

def draw_grid():
    window.fill(WHITE)
    for i in range(GRID_SIZE + 1):
        width = 3 if i % 3 == 0 else 1
        pygame.draw.line(window, BLACK, (0, i * CELL_SIZE), (GRID_SIZE * CELL_SIZE, i * CELL_SIZE), width)
        pygame.draw.line(window, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, GRID_SIZE * CELL_SIZE), width)
        # Highlight diagonals
        if i < GRID_SIZE:
            pygame.draw.rect(window, LIGHT_BLUE, (i * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(window, LIGHT_BLUE, ((GRID_SIZE - 1 - i) * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_numbers():
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] != 0:
                text = font.render(str(board[r][c]), True, RED)
                window.blit(text, (c * CELL_SIZE + 20, r * CELL_SIZE + 15))

def find_empty():
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == 0:
                return r, c
    return None

def is_valid(num, pos):
    r, c = pos
    if any(board[r][i] == num for i in range(GRID_SIZE) if i != c):
        return False
    if any(board[i][c] == num for i in range(GRID_SIZE) if i != r):
        return False
    box_r, box_c = (r // 3) * 3, (c // 3) * 3
    for i in range(box_r, box_r + 3):
        for j in range(box_c, box_c + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    if r == c and any(board[i][i] == num and i != r for i in range(GRID_SIZE)):
        return False
    if r + c == GRID_SIZE - 1 and any(board[i][GRID_SIZE - 1 - i] == num and i != r for i in range(GRID_SIZE)):
        return False
    return True

def solve_sudoku():
    global current_cell
    empty = find_empty()
    if not empty:
        return True
    r, c = empty
    for num in range(1, 10):
        if is_valid(num, (r, c)):
            board[r][c] = num
            current_cell = (r, c)
            draw_grid()
            draw_numbers()
            pygame.draw.rect(window, RED, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
            pygame.display.update()
            pygame.time.wait(1)
            if solve_sudoku():
                return True
            board[r][c] = 0
            draw_grid()
            draw_numbers()
            pygame.display.update()
            pygame.time.wait(1)
    current_cell = (-1, -1)
    return False

def solve():
    solve_sudoku()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            solve()

    draw_grid()
    draw_numbers()

    if current_cell != (-1, -1):
        r, c = current_cell
        pygame.draw.rect(window, RED, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

    pygame.display.update()
