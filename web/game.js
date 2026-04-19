// --- Game state ---
let board = Array(9).fill("");
let currentPlayer = "X";
let gameMode = null;
let difficultyLevel = null;
let gameRunning = false;

const WINNING_COMBOS = [
  [0,1,2],[3,4,5],[6,7,8],  // rows
  [0,3,6],[1,4,7],[2,5,8],  // columns
  [0,4,8],[2,4,6]           // diagonals
];

// --- Menu ---
function selectMode(mode) {
  gameMode = mode;
  difficultyLevel = null;
  document.getElementById("btn-pvp").classList.toggle("selected", mode === "pvp");
  document.getElementById("btn-pvc").classList.toggle("selected", mode === "pvc");

  const diffSection = document.getElementById("difficulty-section");
  if (mode === "pvc") {
    diffSection.classList.add("visible");
    document.getElementById("start-btn").disabled = true;
  } else {
    diffSection.classList.remove("visible");
    document.getElementById("btn-easy").classList.remove("selected");
    document.getElementById("btn-hard").classList.remove("selected");
    document.getElementById("start-btn").disabled = false;
  }
}

function selectDifficulty(level) {
  difficultyLevel = level;
  document.getElementById("btn-easy").classList.toggle("selected", level === "easy");
  document.getElementById("btn-hard").classList.toggle("selected", level === "hard");
  document.getElementById("start-btn").disabled = false;
}

function startGame() {
  board = Array(9).fill("");
  currentPlayer = "X";
  gameRunning = true;
  showScreen("screen-game");
  renderBoard();
  updateStatus();
}

function restartGame() {
  board = Array(9).fill("");
  currentPlayer = "X";
  gameRunning = true;
  renderBoard();
  updateStatus();
}

function goToMenu() {
  gameMode = null;
  difficultyLevel = null;
  document.querySelectorAll(".menu-btn").forEach(b => b.classList.remove("selected"));
  document.getElementById("difficulty-section").classList.remove("visible");
  document.getElementById("start-btn").disabled = true;
  showScreen("screen-menu");
}

function showScreen(id) {
  document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
  document.getElementById(id).classList.add("active");
}

// --- Core game logic ---
function checkWinner(b, player) {
  return WINNING_COMBOS.some(([a, c, d]) => b[a] === player && b[c] === player && b[d] === player);
}

function getWinningCombo(b, player) {
  return WINNING_COMBOS.find(([a, c, d]) => b[a] === player && b[c] === player && b[d] === player);
}

function isBoardFull(b) {
  return b.every(cell => cell !== "");
}

function handleCellClick(index) {
  if (!gameRunning || board[index] !== "" || (gameMode === "pvc" && currentPlayer === "O")) return;
  makeMove(index, currentPlayer);
}

function makeMove(index, player) {
  board[index] = player;
  renderBoard();

  if (checkWinner(board, player)) {
    highlightWin(player);
    updateStatus(`${player} wins!`);
    gameRunning = false;
    return;
  }

  if (isBoardFull(board)) {
    updateStatus("It's a tie!");
    gameRunning = false;
    return;
  }

  currentPlayer = currentPlayer === "X" ? "O" : "X";
  updateStatus();

  if (gameMode === "pvc" && currentPlayer === "O" && gameRunning) {
    setTimeout(computerMove, 400);
  }
}

// --- Computer moves ---
function computerMove() {
  if (!gameRunning) return;
  const move = difficultyLevel === "hard" ? bestMoveMinimax() : randomMove();
  makeMove(move, "O");
}

function randomMove() {
  const available = board.map((v, i) => v === "" ? i : null).filter(v => v !== null);
  return available[Math.floor(Math.random() * available.length)];
}

function bestMoveMinimax() {
  let bestScore = -Infinity;
  let bestMove = null;
  board.forEach((cell, i) => {
    if (cell === "") {
      board[i] = "O";
      const score = minimax(board, false);
      board[i] = "";
      if (score > bestScore) { bestScore = score; bestMove = i; }
    }
  });
  return bestMove;
}

function minimax(b, isMaximizing) {
  if (checkWinner(b, "O")) return 10;
  if (checkWinner(b, "X")) return -10;
  if (isBoardFull(b)) return 0;

  if (isMaximizing) {
    let best = -Infinity;
    b.forEach((cell, i) => {
      if (cell === "") {
        b[i] = "O";
        best = Math.max(best, minimax(b, false));
        b[i] = "";
      }
    });
    return best;
  } else {
    let best = Infinity;
    b.forEach((cell, i) => {
      if (cell === "") {
        b[i] = "X";
        best = Math.min(best, minimax(b, true));
        b[i] = "";
      }
    });
    return best;
  }
}

// --- Rendering ---
function renderBoard() {
  const boardEl = document.getElementById("board");
  boardEl.innerHTML = "";
  board.forEach((cell, i) => {
    const div = document.createElement("div");
    div.className = "cell" + (cell ? " taken" : "");
    div.textContent = cell;
    div.onclick = () => handleCellClick(i);
    boardEl.appendChild(div);
  });
}

function highlightWin(player) {
  const combo = getWinningCombo(board, player);
  if (!combo) return;
  const cells = document.querySelectorAll(".cell");
  combo.forEach(i => cells[i].classList.add("win"));
}

function updateStatus(message) {
  const statusEl = document.getElementById("status");
  if (message) {
    statusEl.textContent = message;
  } else {
    const isComputer = gameMode === "pvc" && currentPlayer === "O";
    statusEl.textContent = isComputer ? "Computer is thinking..." : `Player ${currentPlayer}'s turn`;
  }
}
