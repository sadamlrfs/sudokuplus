import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (540, 540)
CELL_SIZE = 60
GRID_SIZE = 9
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (196, 220, 255)
DARK_BLUE = (0, 0, 128)

# Set up the window
window = pygame.display.set_mode(WINDOW_SIZE)
icon = pygame.image.load('Sudoku.ico')
pygame.display.set_icon(icon)
pygame.display.set_caption("Sudoku Solver")

# Load font
font = pygame.font.Font(None, 48)

# Example Sudoku board
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

# Variables for animation
current_row = -1
current_col = -1

# Function to draw the Sudoku grid
def draw_grid():
    window.fill(WHITE)
    for i in range(GRID_SIZE + 1):
        for j in range(GRID_SIZE + 1):
            if i % 3 == 0:
                pygame.draw.line(window, BLACK, (0, i * CELL_SIZE), (GRID_SIZE * CELL_SIZE, i * CELL_SIZE), 3)
                pygame.draw.line(window, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, GRID_SIZE * CELL_SIZE), 3)
            else:
                pygame.draw.line(window, BLACK, (0, i * CELL_SIZE), (GRID_SIZE * CELL_SIZE, i * CELL_SIZE), 1)
                pygame.draw.line(window, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, GRID_SIZE * CELL_SIZE), 1)

            if i == j or i + j == GRID_SIZE - 1:  # Check if the current cell is on the diagonal
                pygame.draw.rect(window, LIGHT_BLUE, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Function to draw the numbers on the Sudoku grid
def draw_numbers():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] != 0:
                text = font.render(str(board[i][j]), True, DARK_BLUE)
                window.blit(text, (j * CELL_SIZE + 20, i * CELL_SIZE + 15))

# Function to find an empty cell in the Sudoku board
def find_empty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return (row, col)
    return None

# Function to check if a number is valid in a given position
def is_valid(board, num, pos):
    # Check row
    for i in range(9):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
        
    # Check column
    for i in range(9):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check 3x3 box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    # Check diagonal from top left to bottom right
    if pos[0] == pos[1]:
        for i in range(9):
            if board[i][i] == num and (i, i) != pos:
                return False

    # Check diagonal from top right to bottom left
    if pos[0] + pos[1] == 8:
        for i in range(9):
            if board[i][8 - i] == num and (i, 8 - i) != pos:
                return False

    return True

# Function to solve the Sudoku recursively
def solve_sudoku(board):
    global current_row, current_col
    empty = find_empty(board)

    if not empty:
        return True
    else:
        row, col = empty

    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num

            # Update the current cell for animation
            current_row = row
            current_col = col

            # Update the display
            draw_grid()
            draw_numbers()
            pygame.display.update()
            pygame.time.wait(1)  # Delay for animation

            if solve_sudoku(board):
                return True

            # Reset the current cell for animation
            current_row = -1
            current_col = -1

            board[row][col] = 0

            # Update the display
            draw_grid()
            draw_numbers()
            pygame.display.update()
            pygame.time.wait(1)  # Delay for animation

    return False

# Function to solve the Sudoku using the solve_sudoku function from the previous example
def solve():
    solve_sudoku(board)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                solve()

    # Draw grid and numbers
    draw_grid()
    draw_numbers()

    # Highlight the current cell
    if current_row != -1 and current_col != -1:
        pygame.draw.rect(window, (255, 0, 0), (current_col * CELL_SIZE, current_row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

    # Update the display
    pygame.display.update()
    
