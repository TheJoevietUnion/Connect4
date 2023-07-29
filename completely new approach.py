import tkinter as tk
import pygame
import time

#the grid haha
ROWS = 6
COLS = 7
CELL_SIZE = 100

#list of list of string (virtual board)
grid = [['empty' for _ in range(COLS)] for _ in range(ROWS)]

# Function to update a cell in the grid with a color
def update_cell(row, col, color):
    grid[row][col] = color
    draw_grid()
    if check_winner(row, col):
        show_winner(grid[row][col])
        update_scoreboard(grid[row][col])
        stop_game()
    else:
        show_current_player()

# Function to check if a player has won
def check_winner(row, col):
    directions = [(-1, 0), (0, -1), (-1, -1), (-1, 1)]
    for dr, dc in directions:
        count = 1
        for i in range(1, 4):
            r, c = row + i * dr, col + i * dc
            if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c] == grid[row][col]:
                count += 1
            else:
                break
        for i in range(1, 4):
            r, c = row - i * dr, col - i * dc
            if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c] == grid[row][col]:
                count += 1
            else:
                break
        if count >= 4:
            return True
    return False

# Function to show a message indicating the winner
def show_winner(color):
    winner_label.config(text=f"{color.capitalize()} player won!")
    winner_label.pack()

# Function to update the scoreboard
def update_scoreboard(winner_color):
    global red_wins, yellow_wins
    if winner_color == 'red':
        red_wins += 1
    else:
        yellow_wins += 1
    red_score_label.config(text=f"Red Wins: {red_wins}")
    yellow_score_label.config(text=f"Yellow Wins: {yellow_wins}")

# Function to show the current player's turn in the sidebar
def show_current_player():
    current_player_label.config(text=f" Current turn: {current_player.capitalize()}")
    current_player_label.pack()

# Function to stop the game after a win
def stop_game():
    canvas.unbind('<Button-1>')
    reset_button.pack()

# Function to reset the game board
def reset_board():
    global grid, current_player
    grid = [['empty' for _ in range(COLS)] for _ in range(ROWS)]
    draw_grid()
    canvas.bind('<Button-1>', on_column_click)
    reset_button.pack_forget()
    winner_label.pack_forget()
    current_player_label.pack_forget()
    current_player = 'red'
    show_current_player()

# Function to handle column click event
def on_column_click(event):
    col = event.x // CELL_SIZE
    if 0 <= col < COLS and grid[0][col] == 'empty':
        drop_piece(col)

# Function to drop a piece in the selected column
def drop_piece(column):
    row = 0
    while row < ROWS - 1 and grid[row + 1][column] == 'empty':
        row += 1

    animate_drop(row, column, current_player)

# Function to animate the dropping of a piece
def animate_drop(row, column, color):
    start_y = -CELL_SIZE
    end_y = row * CELL_SIZE
    drop_speed = 20  # Adjust this value to control the animation speed

    for y in range(start_y, end_y, drop_speed):
        draw_grid()  # Redraw the entire grid with the current state
        draw_piece(column, y, color)
        window.update()
        time.sleep(0.01)

    update_cell(row, column, color)
    toggle_player()

# Function to toggle the current player
def toggle_player():
    global current_player
    if current_player == 'red':
        current_player = 'yellow'
    else:
        current_player = 'red'
    show_current_player()

# Function to draw the grid in the GUI window
def draw_grid():
    canvas.delete("piece")  # Clear all previous pieces before redrawing the grid
    for row in range(ROWS):
        for col in range(COLS):
            color = grid[row][col]
            cell_color = '#cdcae3' if color == 'empty' else color
            canvas.itemconfig(cells[row][col], fill=cell_color)

# Function to draw a game piece
def draw_piece(column, y, color):
    x = column * CELL_SIZE + 10
    canvas.create_oval(x, y, x + CELL_SIZE - 20, y + CELL_SIZE - 20, fill=color, tags="piece")

# Initialize Pygame
pygame.init()

# Create the main window
window = tk.Tk()
window.title('Connect 4 Board')

# Create a frame for the sidebar
sidebar = tk.Frame(window, bg='lightgray')
sidebar.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)

# Create the canvas to display the grid
canvas = tk.Canvas(window, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE, bg='#0000ff')  # Use a dark blue background
canvas.pack(side=tk.LEFT)

# Bind the column click event to the canvas
canvas.bind('<Button-1>', on_column_click)

# Create the cells in the grid
cells = [[canvas.create_oval(col*CELL_SIZE + 10, row*CELL_SIZE + 10, (col+1)*CELL_SIZE - 10, (row+1)*CELL_SIZE - 10, fill='#cdcae3')
          for col in range(COLS)] for row in range(ROWS)]  # Use a light blue color for the game pieces

# Create a label to display the winner
winner_label = tk.Label(sidebar, text="", font=("Century Gothic", 24))

# Create a reset button
reset_button = tk.Button(sidebar, text="Reset", command=reset_board)

# Create a label to show the current player's turn
current_player_label = tk.Label(sidebar, text="", font=("Century Gothic", 18))

# Create labels for the scoreboard
red_wins = 0
yellow_wins = 0
red_score_label = tk.Label(sidebar, text=f"Red Wins: {red_wins}", font=("Century Gothic", 14))
yellow_score_label = tk.Label(sidebar, text=f"Yellow Wins: {yellow_wins}", font=("Century Gothic", 14))

# Set initial player to red and show the current player's turn
current_player = 'red'
show_current_player()

# Pack the labels for the scoreboard
red_score_label.pack()
yellow_score_label.pack()

# Start the GUI event loop
window.mainloop()
