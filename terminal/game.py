# Game process:
#
# 1. Print the game board (#)
# 2. Receive player input
# 3. Check for win or tie
# 4. Switch players
# 5. Repeat

import time
import random

# Defining main variables
board = ["-", "-", "-",
         "-", "-", "-",
         "-", "-", "-"]
currentPlayer = "X"       # Every game starts with the X player
gameRunning = True
gameMode = None
difficultyLevel = None

def select_game_mode():
    """
    Asks the player to choose between the PlayerVSPlayer (PvP) or PlayerVSComputer (PvC) modes.
    """
    global gameMode
    global difficultyLevel
    print("Select game mode:")
    print("1 - Player VS Player")
    print("2 - Player VS Computer\n")
    choice = input("Enter 1 or 2: ")

    if choice == "1":
        gameMode = "pvp"
        print("You selected the Player VS Player mode!\n")
        time.sleep(1)
    elif choice == "2":
        gameMode = "pvc"
        print("You selected the Player VS Computer mode!\n")
        time.sleep(1)

        print("Select your difficulty level: ")
        print("1 - Easy Mode")
        print("2 - Hard Mode\n")
        while difficultyLevel != "easy" and difficultyLevel != "hard":
            computer_mode = input("Enter 1 or 2: ")
            if computer_mode == "1":
                difficultyLevel = "easy"
            elif computer_mode == "2":
                difficultyLevel = "hard"
            else:
                print("Please, insert a valid option.\n")
                time.sleep(0.5)
    else:
        print("Invalid choice. Choose again.\n")
        time.sleep(1)
        select_game_mode()

def print_board():
    print("-------------")
    print("| " + board[0] + " | " + board[1] + " | " + board[2] + " |")
    print("| " + board[3] + " | " + board[4] + " | " + board[5] + " |")
    print("| " + board[6] + " | " + board[7] + " | " + board[8] + " |")
    print("-------------\n")

def explain_board():
    """
    Gives a quick explanation of the logic behind the game board.
    """
    print("Let the board be a 3x3 grid. Each square is represented by a number.")
    print("-------------")
    print("| " + "1" + " | " + "2" + " | " + "3" + " |")
    print("| " + "4" + " | " + "5" + " | " + "6" + " |")
    print("| " + "7" + " | " + "8" + " | " + "9" + " |")
    print("-------------\n")

    # Gives 3 seconds for the user to read before running the next lines of code
    time.sleep(3)

def playerInput():
    """
    Receives a player input and updates the game board, recursively.
    """
    inp = int(input("Enter a value between 1-9: "))
    if inp >= 1 and inp <= 9 and board[inp-1] == "-":
        board[inp-1] = currentPlayer
        return
    
    print("Value cannot be used. Insert another one, please.")
    playerInput()

# Checking for wins or ties
def check_win():
    """
    Checks for winning patterns in the rows, columns and diagonals.
    """
    global gameRunning
    combos = [
        [0,1,2],[3,4,5],[6,7,8],  # rows
        [0,3,6],[1,4,7],[2,5,8],  # columns
        [0,4,8],[2,4,6]           # diagonals
    ]
    if any(board[a] == board[b] == board[c] == currentPlayer for a,b,c in combos):
        gameRunning = False
        print_board()
        print(f"The winner is {currentPlayer}!")

def check_tie():
    """
    Checks if there is any possible moves left.
    """
    global gameRunning
    if "-" not in board and gameRunning:
        print_board()
        print("It's a tie!")
        gameRunning = False

def switch_players():
    """
    Changes the turn for the next player.
    """
    global currentPlayer
    if currentPlayer == "X":
        currentPlayer = "O"
    elif currentPlayer == "O":
        currentPlayer = "X"

def computer_move_random():
    """
    Randomly selects an available position on the board.
    Computer plays as "O".
    """
    available = [i for i, spot in enumerate(board) if spot == "-"]
    choice = random.choice(available)
    board[choice] = currentPlayer

# Separate function for the minimax algorithm
def check_winner_minimax(player):
    """
    Returns True if the given player has won. Used internally by minimax.
    """
    combos = [
        [0,1,2],[3,4,5],[6,7,8],  # rows
        [0,3,6],[1,4,7],[2,5,8],  # columns
        [0,4,8],[2,4,6]           # diagonals
    ]
    return any(board[a] == board[b] == board[c] == player for a,b,c in combos)

# Minimax AI algorithm implementation
def minimax(is_maximizing):
    """
    Recursively evaluates all possible moves and returns the best score.
    """
    # Base cases: check terminal states
    if check_winner_minimax("O"):
        return 10
    if check_winner_minimax("X"):
        return -10
    if "-" not in board:
        return 0

    if is_maximizing:
        best_score = -1000
        for i in range(9):
            if board[i] == "-":
                board[i] = "O"
                score = minimax(False)
                board[i] = "-"
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for i in range(9):
            if board[i] == "-":
                board[i] = "X"
                score = minimax(True)
                board[i] = "-"
                best_score = min(score, best_score)
        return best_score

def computer_move_smart():
    """
    Uses minimax to select the best available position on the board.
    """
    best_score = -1000
    best_move = None
    for i in range(9):
        if board[i] == "-":
            board[i] = "O"
            score = minimax(False)
            board[i] = "-"
            if score > best_score:
                best_score = score
                best_move = i
    board[best_move] = "O"

explain_board()
select_game_mode()
while gameRunning:
    print_board()

    if gameMode == "pvc" and currentPlayer == "O":
        print("Computer is thinking...\n")
        time.sleep(1)
        if difficultyLevel == "easy":
            computer_move_random()
        elif difficultyLevel == "hard":
            computer_move_smart()
    else:
        playerInput()

    check_win()
    check_tie()

    if gameRunning:
        switch_players()