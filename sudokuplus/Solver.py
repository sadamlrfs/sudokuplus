import pygame
import sys

pygame.init()

WINDOW_SIZE = 540
CELL_SIZE = 60
GRID_SIZE = 9
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (196, 220, 255)
RED = (255, 0, 0)

window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Sudoku Plus")
pygame.display.set_icon(pygame.image.load('sudokuplus.ico'))
font = pygame.font.Font(None, 48)

board = [
    [3, 4, 0, 8, 7, 0, 0, 0, 0],
    [0, 9, 0, 0, 0, 0, 0, 7, 0],
    [0, 0, 0, 3, 9, 0, 0, 0, 0],
    [0, 0, 4, 0, 6, 3, 7, 0, 0],
    [1, 2, 0, 7, 8, 9, 0, 4, 3],
    [0, 0, 7, 4, 2, 0, 5, 0, 0],
    [0, 0, 0, 0, 3, 8, 0, 0, 0],
    [0, 5, 0, 0, 0, 0, 0, 6, 0],
    [0, 0, 0, 0, 5, 4, 0, 3, 7]
]

def draw_grid():
    window.fill(WHITE)
    for i in range(GRID_SIZE + 1):
        width = 3 if i % 3 == 0 else 1
        pygame.draw.line(window, BLACK, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE), width)
        pygame.draw.line(window, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE), width)
        for j in range(GRID_SIZE):
            if i == j or i + j == GRID_SIZE - 1:
                pygame.draw.rect(window, LIGHT_BLUE, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_numbers():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j]:
                text = font.render(str(board[i][j]), True, RED)
                window.blit(text, (j * CELL_SIZE + 20, i * CELL_SIZE + 15))

def find_empty():
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def is_valid(num, pos):
    r, c = pos
    if any(board[r][j] == num and j != c for j in range(9)): return False
    if any(board[i][c] == num and i != r for i in range(9)): return False
    box_x, box_y = c // 3 * 3, r // 3 * 3
    for i in range(box_y, box_y + 3):
        for j in range(box_x, box_x + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    if r == c and any(board[i][i] == num and (i, i) != pos for i in range(9)): return False
    if r + c == 8 and any(board[i][8 - i] == num and (i, 8 - i) != pos for i in range(9)): return False
    return True

def solve():
    empty = find_empty()
    if not empty: return True
    r, c = empty
    for num in range(1, 10):
        if is_valid(num, (r, c)):
            board[r][c] = num
            if solve(): return True
            board[r][c] = 0
    return False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            solve()

    draw_grid()
    draw_numbers()
    pygame.display.update()
