import tkinter as tk
import random

def create_board():
  """Creates an empty 3x3 Tic Tac Toe board."""
  return [[" " for _ in range(3)] for _ in range(3)]

def get_ai_move(board, difficulty):
  """Gets a move for the AI opponent based on the difficulty level."""
  available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]

  if difficulty == "Easy":
    return random.choice(available_moves)
  elif difficulty == "Medium":
    # Try to block player's winning move or make a random move
    for i in range(3):
      for j in range(3):
        if board[i][j] == " ":
          board[i][j] = "X"  # Temporarily assume player's move
          if check_win(board, "X"):
            return i, j  # Block the winning move
          board[i][j] = " "  # Reset the board
    return random.choice(available_moves)
  else:  # Hard difficulty
    # Implement a more strategic algorithm here (e.g., Minimax)
    # For now, let's keep it random for demonstration
    return random.choice(available_moves)

def check_win(board, player):
  """Checks if the given player has won the game."""
  # Check rows, columns, and diagonals
  for i in range(3):
    if all(board[i][j] == player for j in range(3)) or \
       all(board[j][i] == player for j in range(3)):
      return True
  if all(board[i][i] == player for i in range(3)) or \
     all(board[i][2 - i] == player for i in range(3)):
    return True
  return False

def is_board_full(board):
  """Checks if the board is full (a tie)."""
  return all(board[i][j] != " " for i in range(3) for j in range(3))

def on_button_click(row, col):
  """Handles button clicks."""
  global current_player, board

  if board[row][col] == " " and current_player == "X":
    buttons[row][col].config(text="X", fg="red") 
    board[row][col] = "X"

    if check_win(board, current_player):
      label.config(text=f"Player {current_player} wins!")
      disable_buttons()
    elif is_board_full(board):
      label.config(text="It's a tie!")
      disable_buttons()
    else:
      current_player = "O"
      label.config(text="AI's turn...")
      window.after(1000, lambda: ai_move(difficulty.get())) 

def ai_move(difficulty):
  """AI makes a move based on the selected difficulty."""
  global current_player, board

  row, col = get_ai_move(board, difficulty)
  buttons[row][col].config(text="O", fg="blue") 
  board[row][col] = "O"

  if check_win(board, current_player):
    label.config(text=f"Player {current_player} wins!")
    disable_buttons()
  elif is_board_full(board):
    label.config(text="It's a tie!")
    disable_buttons()
  else:
    current_player = "X"
    label.config(text="Your turn!")

def disable_buttons():
  """Disables all buttons after the game ends."""
  for row in buttons:
    for button in row:
      button.config(state=tk.DISABLED)

def reset_game():
  """Resets the game board and enables buttons."""
  global current_player, board
  board = create_board()
  current_player = "X"
  label.config(text="Your turn!")

  for i in range(3):
    for j in range(3):
      buttons[i][j].config(text=" ", state=tk.NORMAL)

# Create the main window
window = tk.Tk()
window.title("Tic Tac Toe")

# Create buttons for the game board
buttons = []
for i in range(3):
  row = []
  for j in range(3):
    button = tk.Button(window, text=" ", font=('normal', 20), width=5, height=2,
                       command=lambda row=i, col=j: on_button_click(row, col))
    button.grid(row=i, column=j)
    row.append(button)
  buttons.append(row)

# Create a label to display game status
label = tk.Label(window, text="Your turn!", font=('normal', 14))
label.grid(row=3, column=0, columnspan=3)

# Create a reset button
reset_button = tk.Button(window, text="Reset", font=('normal', 12), command=reset_game)
reset_button.grid(row=4, column=0, columnspan=3)

# Create a dropdown to select difficulty
difficulty = tk.StringVar(value="Medium")
difficulty_dropdown = tk.OptionMenu(window, difficulty, "Easy", "Medium", "Hard")
difficulty_dropdown.grid(row=5, column=0, columnspan=3)

# Initialize game variables
current_player = "X"
board = create_board()

window.mainloop()