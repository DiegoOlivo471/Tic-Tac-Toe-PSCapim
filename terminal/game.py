# Game process:
#
# 1. Print the game board (#)
# 2. Receive player input
# 3. Check for win or tie
# 4. Switch players
# 5. Repeat

import time

# Defining main variables
board = ["-", "-", "-",
         "-", "-", "-",
         "-", "-", "-"]
currentPlayer = "X"       # Every game starts with the X player
winner = None
gameRunning = True

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

# Checking for wins
def check_rows():
    """
    Checks if there is a horizontal line (row) of "X"s or "O"s.
    """
    global winner
    if board[0] == board[1] == board[2] and board[0] != '-':
        winner = board[0]
        return True
    elif board[3] == board[4] == board[5] and board[3] != "-":
        winner = board[3]
        return True
    elif board[6] == board[7] == board[8] and board[6] != "-":
        winner = board[6]
        return True
    return False

def check_columns():
    """
    Checks if there is a vertical line (column) of "X"s or "O"s.
    """
    global winner
    if board[0] == board[3] == board[6] and board[0] != '-':
        winner = board[0]
        return True
    elif board[1] == board[4] == board[7] and board[1] != '-':
        winner = board[1]
        return True
    elif board[2] == board[5] == board[8] and board[2] != '-':
        winner = board[2]
        return True
    return False

def check_diagonals():
    """
    Checks if there is a diagonal line of "X"s or "O"s.
    """
    global winner
    if board[0] == board[4] == board[8] and board[0] != "-":
        winner = board[0]
        return True
    elif board[6] == board[4] == board[2] and board[6] != "-":
        winner = board[6]
        return True
    return False

def check_tie():
    """
    Checks if there is any possible moves left.
    """
    global gameRunning
    if "-" not in board and gameRunning:
        print_board()
        print("It's a tie!")
        gameRunning = False

def check_win():
    """
    Calls all check functions and checks 
    """
    global gameRunning
    if check_rows() or check_columns() or check_diagonals():
        gameRunning = False
        print_board()
        print(f"The winner is {winner}!")

def switch_players():
    """
    Changes the turn for the next player.
    """
    global currentPlayer
    if currentPlayer == "X":
        currentPlayer = "O"
    elif currentPlayer == "O":
        currentPlayer = "X"

explain_board()
while gameRunning:
    print_board()
    playerInput()

    check_win()
    check_tie()

    if gameRunning:
        switch_players()