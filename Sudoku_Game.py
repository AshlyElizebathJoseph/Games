import random
import tkinter as tk
from tkinter import messagebox

# Function to generate a random, solvable Sudoku puzzle
def generate_sudoku():
    base = 3  # Size of the subgrid (3x3)
    side = base * base  # Size of the entire grid (9x9)

    # Generating a basic grid pattern for a Sudoku puzzle
    def pattern(row, col): return (base * (row % base) + row // base + col) % side

    # Randomly shuffle rows, columns, and numbers for puzzle generation
    def shuffle(s): return random.sample(s, len(s))

    rows = [g * base + r for g in shuffle(range(base)) for r in shuffle(range(base))]
    cols = [g * base + c for g in shuffle(range(base)) for c in shuffle(range(base))]
    nums = shuffle(range(1, side + 1))

    # Create a randomized Sudoku grid
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    # Remove random numbers from the grid to create a puzzle
    squares = side * side
    empties = squares * 3 // 4  # Remove about 75% of the numbers
    for _ in range(empties):
        row = random.randint(0, side - 1)
        col = random.randint(0, side - 1)
        board[row][col] = 0

    return board

# Function to check if a number can be placed in a specific cell
def is_valid_move(board, row, col, num):
    #checking the row
    if num in board[row]:
        return False
    # Checking the column
    if num in [board[r][col] for r in range(9)]:
        return False
    # Check the 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False
    return True

# Backtracking algorithm to solve the Sudoku puzzle
def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid_move(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

# Checking if the current board is solved
def is_solved(board):
    return all(board[row][col] != 0 for row in range(9) for col in range(9))

# Function to display a new Sudoku puzzle
def new_game():
    global puzzle, original_puzzle
    puzzle = generate_sudoku()
    original_puzzle = [row[:] for row in puzzle]
    update_grid()

# Updating the grid display based on the current puzzle state
def update_grid():
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] != 0:
                entries[row][col].delete(0, tk.END)
                entries[row][col].insert(0, str(puzzle[row][col]))
                entries[row][col].config(state='disabled', disabledforeground='black')
            else:
                entries[row][col].delete(0, tk.END)
                entries[row][col].config(state='normal')

# Checking the user's move
def check_move(row, col):
    try:
        user_input = int(entries[row][col].get())
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter a number between 1 and 9.")
        return

    if not (1 <= user_input <= 9):
        messagebox.showwarning("Invalid Input", "Please enter a number between 1 and 9.")
        return

    if original_puzzle[row][col] != 0:
        messagebox.showwarning("Invalid Move", "You cannot change the original numbers.")
        entries[row][col].delete(0, tk.END)
        entries[row][col].insert(0, str(original_puzzle[row][col]))
        return

    if is_valid_move(puzzle, row, col, user_input):
        puzzle[row][col] = user_input
        if is_solved(puzzle):
            messagebox.showinfo("Congratulations!", "You solved the Sudoku puzzle!")
            play_again = messagebox.askyesno("Play Again?", "Do you want to play another Sudoku puzzle?")
            if play_again:
                new_game()
            else:
                app.quit()
    else:
        messagebox.showwarning("Incorrect Move", "This move is not valid.")
        entries[row][col].delete(0, tk.END)

# Create the main application window
app = tk.Tk()
app.title("Sudoku")

# Initializing the puzzle board
puzzle = generate_sudoku()
original_puzzle = [row[:] for row in puzzle]
entries = [[None for _ in range(9)] for _ in range(9)]

# Create a 9x9 grid of entry widgets
for row in range(9):
    for col in range(9):
        entry = tk.Entry(app, width=3, font=("Arial", 18), justify="center")
        entry.grid(row=row, column=col)
        entry.bind("<FocusOut>", lambda e, r=row, c=col: check_move(r, c))
        entries[row][col] = entry

# Add a "New Game" button to start a new puzzle
new_game_button = tk.Button(app, text="New Game", font=("Arial", 14), command=new_game)
new_game_button.grid(row=9, column=0, columnspan=9)

# Display the initial puzzle
update_grid()

# Run the GUI event loop
app.mainloop()
