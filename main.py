import subprocess
import webbrowser
import os

print("Welcome to Tic-Tac-Toe!")
print("1 - Play in terminal")
print("2 - Play in browser\n")

choice = ""
while choice not in ("1", "2"):
    choice = input("Enter 1 or 2: ")
    if choice == "1":
        subprocess.run(["python", "terminal/game.py"])
    elif choice == "2":
        path = os.path.abspath("web/index.html")
        webbrowser.open(f"file://{path}")
        print("Opening game in your browser...")
    else:
        print("Invalid choice. Try again.\n")