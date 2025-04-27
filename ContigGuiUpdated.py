# Import necessary modules
import tkinter as tk
import random

# --- Window Setup ---
root = tk.Tk()
root.title("Contig Game")

# Center the window on screen
window_width = 850
window_height = 880
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.resizable(False, False)

# --- Globals ---
player1_initials = ""
player2_initials = ""
player1_score = 0
player2_score = 0
current_player = ""
current_roll = []
timer_label = None
timer_seconds = None
timer_id = None

move_history = []  # Track moves

# Initial values of the 8x8 game board with perfect squares
squares = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16",
    "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32",
    "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "44", "45", "48", "50", "54", "55",
    "60", "64", "66", "72", "75", "80", "90", "96", "100", "108", "120", "125", "144", "150", "180", "216"
]

# --- UI Frames ---
name_frame = tk.Frame(root)
game_frame = tk.Frame(root)

# --- Name Input Screen ---
tk.Label(name_frame, text="Enter Player Names", font=("Helvetica", 20, "bold")).pack(pady=20)

# Player 1 input
p1_label = tk.Label(name_frame, text="Player 1 Name (Max 5 chars):", font=("Helvetica", 14))
p1_label.pack(pady=5)
p1_entry = tk.Entry(name_frame, font=("Helvetica", 14))
p1_entry.pack()

# Player 2 input
p2_label = tk.Label(name_frame, text="Player 2 Name (Max 5 chars):", font=("Helvetica", 14))
p2_label.pack(pady=5)
p2_entry = tk.Entry(name_frame, font=("Helvetica", 14))
p2_entry.pack()

# Error message label
error_label = tk.Label(name_frame, text="", font=("Helvetica", 12), fg="red")
error_label.pack()

# Start button
start_button = tk.Button(name_frame, text="Start Game", font=("Helvetica", 14), command=lambda: start_game())
start_button.pack(pady=20)


# --- Start Game ---
def start_game():
    global player1_initials, player2_initials, current_player

    player1_initials = p1_entry.get().strip().upper()[:5] or "P1"
    player2_initials = p2_entry.get().strip().upper()[:5] or "P2"

    # Error if initials match a square number
    if player1_initials in squares or player2_initials in squares:
        error_label.config(text="Player names cannot match a square number! Please choose different names.")
        return

    error_label.config(text="")
    current_player = player1_initials
    name_frame.pack_forget()
    game_frame.pack()
    setup_game()
    open_history_window()


# --- Game UI Setup ---
def setup_game():
    global board_frame, score_frame, turn_label, input_frame, guess_entry, submit_button, play_again_button, timer_label

    tk.Label(game_frame, text="CONTIG", font=("Helvetica", 28, "bold"), fg="darkblue").pack(pady=10)

    board_frame = tk.Frame(game_frame)
    board_frame.pack(pady=10)

    score_frame = tk.Frame(game_frame)
    score_frame.pack(pady=10)

    global player1_label, player2_label
    player1_label = tk.Label(score_frame, text=f"{player1_initials}'s Score: 0", font=("Helvetica", 14), fg="darkblue")
    player1_label.pack(side="left", padx=50)
    player2_label = tk.Label(score_frame, text=f"{player2_initials}'s Score: 0", font=("Helvetica", 14), fg="darkblue")
    player2_label.pack(side="right", padx=50)

    turn_label = tk.Label(game_frame, text="", font=("Helvetica", 16))
    turn_label.pack(pady=5)

    input_frame = tk.Frame(game_frame)
    input_frame.pack(pady=20)

    # Input for guesses
    guess_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=30)
    guess_entry.pack(side="left", padx=10)

    # Submit button
    submit_button = tk.Button(input_frame, text="Submit", font=("Helvetica", 12), command=submit_guess)
    submit_button.pack(side="left")

    guess_entry.bind("<Return>", lambda event: submit_guess())

    # Play Again button
    play_again_button = tk.Button(game_frame, text="Play Again", font=("Helvetica", 12), command=reset_game)
    play_again_button.pack(pady=10)
    play_again_button.pack_forget()

    # Timer label
    timer_label = tk.Label(game_frame, text="", font=("Helvetica", 12), fg="red")
    timer_label.place(relx=1.0, rely=1.0, anchor="se", x=-40, y=-25)

    display_board()
    prompt_ready()


# --- Board Rendering ---
def display_board():
    for widget in board_frame.winfo_children():
        widget.destroy()

    for i in range(8):
        row = tk.Frame(board_frame)
        row.pack()
        for j in range(8):
            index = i * 8 + j
            if index < len(squares):
                value = squares[index]
                bg_color = "white"
                if value == player1_initials:
                    bg_color = "#add8e6"  # Blue for Player 1
                elif value == player2_initials:
                    bg_color = "#90ee90"  # Green for Player 2

                tk.Label(row, text=value, width=8, height=3,
                         relief="solid", borderwidth=1, bg=bg_color,
                         font=("Helvetica", 14, "bold")).grid(row=0, column=j, padx=1, pady=1)


# --- Score Collection ---
def find_index(val):
    try:
        return squares.index(val)
    except ValueError:
        return -1


def collect_points(player, index):
    global player1_score, player2_score
    score = 0
    row, col = divmod(index, 8)  # Convert linear index to 2D row/col
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip center
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                i = r * 8 + c  # Convert back to linear index
                if squares[i] in (player1_initials, player2_initials):
                    score += 1

    # Update score and return it
    if player == player1_initials:
        player1_score += score
        player1_label.config(text=f"{player1_initials}'s Score: {player1_score}")
        return score, player1_score
    else:
        player2_score += score
        player2_label.config(text=f"{player2_initials}'s Score: {player2_score}")
        return score, player2_score


# --- Win Check ---
def check_winner():
    if player1_score >= 25:
        turn_label.config(text=f"{player1_initials} wins!")
    elif player2_score >= 25:
        turn_label.config(text=f"{player2_initials} wins!")
    else:
        return False

    # Disable input
    guess_entry.config(state="disabled")
    submit_button.config(state="disabled")
    play_again_button.pack()
    return True


# --- Turn Management ---
def switch_player():
    global current_player
    current_player = player2_initials if current_player == player1_initials else player1_initials
    prompt_ready()


def start_turn():
    global current_roll
    current_roll = [random.randint(1, 6) for _ in range(3)]
    turn_label.config(
        text=f"{current_player}'s Turn | Numbers: {current_roll[0]}, {current_roll[1]}, {current_roll[2]}")
    start_timer()


def prompt_ready():
    turn_label.config(text=f"{current_player}, are you ready? Press Enter to roll your numbers.")
    guess_entry.delete(0, tk.END)
    guess_entry.bind("<Return>", lambda event: confirm_ready())


def confirm_ready():
    guess_entry.unbind("<Return>")
    guess_entry.bind("<Return>", lambda event: submit_guess())
    start_turn()


# --- Timer ---
def update_timer():
    global timer_seconds, timer_id
    timer_label.config(text=f"Time left: {timer_seconds}s")
    if timer_seconds > 0:
        timer_seconds -= 1
        timer_id = root.after(1000, update_timer)
    else:
        turn_label.config(text=f"Time's up! Turn skipped.")
        switch_player()


def start_timer():
    global timer_seconds, timer_id
    stop_timer()
    timer_seconds = 60
    update_timer()


def stop_timer():
    global timer_id
    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None


# --- Submit Guess ---
# --- Proof Time Popup ---
def show_proof_popup(guess, idx):
    popup = tk.Toplevel(root)
    popup.title("Proof Time")
    popup.geometry("400x200")
    popup.grab_set()  # Focus on popup only

    tk.Label(popup, text="Proof Time!", font=("Helvetica", 18, "bold")).pack(pady=10)
    tk.Label(popup, text="Double check your proof.\nIs the guess valid?", font=("Helvetica", 14)).pack(pady=10)

    def on_valid():
        popup.destroy()
        points, total_score = collect_points(current_player, idx)
        squares[idx] = current_player
        move_history.append(f"{current_player} placed on {guess} (+{points} points) | Total: {total_score}")
        update_history_window()
        display_board()
        if not check_winner():
            switch_player()

    def on_invalid():
        popup.destroy()
        turn_label.config(
            text=f"Resubmit your guess.\n{current_player}'s Turn | Numbers: {current_roll[0]}, {current_roll[1]}, {current_roll[2]}")
        start_timer()

    button_frame = tk.Frame(popup)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Valid", font=("Helvetica", 12), width=10, command=on_valid).pack(side="left", padx=10)
    tk.Button(button_frame, text="Invalid", font=("Helvetica", 12), width=10, command=on_invalid).pack(side="right", padx=10)

def submit_guess():
    guess = guess_entry.get().strip()
    guess_entry.delete(0, tk.END)
    stop_timer()

    if guess.lower() == "skip":
        switch_player()
        return

    if guess == player1_initials or guess == player2_initials:
        turn_label.config(
            text=f"That square is already taken! Try again.\n{current_player}'s Turn | Numbers: {current_roll[0]}, {current_roll[1]}, {current_roll[2]}")
        return

    if guess in squares:
        idx = find_index(guess)
        if idx != -1:
            show_proof_popup(guess, idx) # Triggers Proof Time 
            return

    turn_label.config(
        text=f"Invalid guess! Try again.\n{current_player}'s Turn | Numbers: {current_roll[0]}, {current_roll[1]}, {current_roll[2]}")
def reset_game():
    global player1_score, player2_score, squares, current_player, move_history
    squares = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16",
        "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32",
        "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "44", "45", "48", "50", "54", "55",
        "60", "64", "66", "72", "75", "80", "90", "96", "100", "108", "120", "125", "144", "150", "180", "216"
    ]
    player1_score = 0
    player2_score = 0
    current_player = player1_initials
    move_history = []

    player1_label.config(text=f"{player1_initials}'s Score: 0")
    player2_label.config(text=f"{player2_initials}'s Score: 0")
    guess_entry.config(state="normal")
    submit_button.config(state="normal")
    play_again_button.pack_forget()

    display_board()
    start_turn()
    stop_timer()
    timer_label.config(text="")


# --- Move History Window ---
history_window = None
history_listbox = None


def open_history_window():
    global history_window, history_listbox
    history_window = tk.Toplevel(root)
    history_window.title("Move History")
    history_window.geometry("300x400")

    tk.Label(history_window, text="Move History", font=("Helvetica", 16, "bold")).pack(pady=10)

    history_listbox = tk.Listbox(history_window, font=("Helvetica", 12), width=30, height=15)
    history_listbox.pack()

    update_history_window()


def update_history_window():
    global history_listbox
    if history_listbox:
        history_listbox.delete(0, tk.END)
        for move in move_history:
            history_listbox.insert(tk.END, move)


# --- Start Game Loop ---
name_frame.pack()
root.mainloop()