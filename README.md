# Tic-Tac-Toe

A Tic-Tac-Toe game with two implementations: a terminal-based version built in Python, and a browser-based version built with HTML, CSS, and JavaScript. Both support Player vs Player and Player vs Computer modes, with Easy (random) and Hard (Minimax AI) difficulty levels.

---

## Project Structure

```
/
├── main.py              ← launcher: choose between terminal or browser
├── terminal/
│   └── game.py          ← terminal version (Python)
├── web/
│   ├── index.html       ← browser version structure
│   ├── style.css        ← styling
│   └── game.js          ← browser game logic
├── tests/
│   ├── __init__.py
│   └── test_game.py     ← unit tests for terminal game logic
├── .gitignore
└── README.md
```

---

## Requirements

- Python 3.x
- No external dependencies — everything uses the Python standard library

---

## How to Run

### Launcher (recommended)

From the project root:

```bash
python main.py
```

Choose option `1` to play in the terminal or `2` to open the browser version.

### Terminal only

```bash
python terminal/game.py
```

### Browser only

Open `web/index.html` directly in your browser, or use the Live Server extension in VS Code.

---

## How to Run Tests

From the project root:

```bash
python -m unittest tests.test_game -v
```

Tests cover: win conditions (rows, columns, diagonals), tie detection, invalid moves, computer behavior (random and Minimax), and player switching.

---

## Technical Justification

### 1. The three most important technical decisions

**Implementing Minimax for the Hard difficulty**

The challenge required at minimum a computer opponent that makes valid random moves, with Minimax as a bonus. Implementing Minimax was a deliberate choice to go beyond the minimum requirement. The algorithm explores all possible game states recursively, assigning +10 for a computer win, -10 for a player win, and 0 for a tie. Because Tic-Tac-Toe has a small state space (at most 9 moves), Minimax runs instantly without any optimization needed. The result is an unbeatable opponent on Hard mode.

**Separating `check_winner_minimax()` from the main win-checking logic**

The main `check_win()` function modifies global state — it sets `gameRunning` to False and prints to the screen. Using it inside the Minimax simulation would corrupt the game state during recursive calls. A separate `check_winner_minimax(player)` function was created to evaluate board states cleanly, returning only a boolean without side effects. This separation of concerns made the Minimax implementation reliable and testable.

**Two separate implementations (terminal and web) instead of one**

Rather than building a single interface, both a terminal and a browser version were developed. The terminal version was written from scratch in Python, which is my primary language. The web version was built with HTML, CSS, and JavaScript to provide a more intuitive and visual experience. This decision demonstrates separation of concerns at the architecture level: the core game logic lives in Python, while the web version reimplements that logic independently in JavaScript.

### 2. What I would do differently with more time

- **Add unit tests for the web version** — the current test suite only covers the Python terminal logic. Testing the JavaScript game logic with a framework like Jest would improve overall coverage.
- **Add depth penalty to Minimax** — currently, two moves that both lead to a win are treated as equal. Adding a depth parameter (e.g. `return 10 - depth` for a win) would make the computer prefer faster victories.
- **Improve input handling in the terminal** — the current `playerInput()` uses recursion for invalid input handling, which could cause issues with very deep recursion if a user enters many invalid inputs in a row. An iterative loop would be more robust.

### 3. How I used AI — and where I made different choices

AI (Claude) was used in the following areas:

- **Web interface**: The HTML, CSS, and JavaScript were generated with AI assistance. Web development is outside my current skill set, and the challenge explicitly permits and encourages the use of AI tools.
- **Minimax explanation and implementation**: The Minimax algorithm was explained conceptually by AI before implementation. The code structure was suggested by AI and then integrated and adapted into the existing codebase.
- **Debugging**: AI helped identify specific bugs, such as the missing `return False` in `check_columns()`, the `winner` variable not being updated after refactoring `check_win()`, and a logical error in the difficulty selection loop.

Where I made different choices from AI suggestions:

- **Terminal game logic**: The core terminal implementation was written independently, following a video tutorial, before AI assistance was involved.
- **Restart during gameplay**: The decision to allow mid-game restart via the `'r'` input in `playerInput()` was my own addition after noticing the challenge required it — and I identified and fixed a bug where the restart was switching the current player before the new game began.
- **`play_again()` return value**: AI's initial suggestion used an unclear break condition. I asked for clarification and the approach was revised to use an explicit `"quit"` return value, which is cleaner and easier to reason about.