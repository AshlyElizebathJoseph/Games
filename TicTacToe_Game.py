import tkinter as tk
from tkinter import messagebox

# Initializing the main application window
app = tk.Tk()
app.title("Tic Tac Toe")

# Global variables
current_player = "X"
board = [["" for _ in range(3)] for _ in range(3)]

# Reseting the game board
def reset_game():
    global current_player, board
    current_player = "X"
    board = [["" for _ in range(3)] for _ in range(3)]
    for button in buttons:
        button.config(text="", state="normal")

# Check for a win or a draw
def check_winner():
    global current_player
    # Check rows, columns, and diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return True
        if board[0][i] == board[1][i] == board[2][i] != "":
            return True
    if board[0][0] == board[1][1] == board[2][2] != "":
        return True
    if board[0][2] == board[1][1] == board[2][0] != "":
        return True
    # Check for a draw
    if all(board[row][col] != "" for row in range(3) for col in range(3)):
        messagebox.showinfo("Tic Tac Toe", "It's a draw!")
        reset_game()
    return False

# Handle a button click
def button_click(row, col):
    global current_player
    if board[row][col] == "":
        board[row][col] = current_player
        buttons[row * 3 + col].config(text=current_player)
        # Check for a win
        if check_winner():
            messagebox.showinfo("Tic Tac Toe", f"Player {current_player} wins!")
            reset_game()
        else:
            # Switch player
            current_player = "O" if current_player == "X" else "X"

# Create the game board
buttons = []
for row in range(3):
    for col in range(3):
        button = tk.Button(app, text="", font=("Arial", 24), width=5, height=2,
                           command=lambda r=row, c=col: button_click(r, c))
        button.grid(row=row, column=col)
        buttons.append(button)

# Add a reset button
reset_button = tk.Button(app, text="Reset", font=("Arial", 14), command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3)

# Start the GUI event loop
app.mainloop()
