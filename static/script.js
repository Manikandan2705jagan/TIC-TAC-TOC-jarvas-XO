/* Tic-Tac-Toe AI — frontend logic. The heavy lifting (minimax + alpha-beta)
   happens server-side in Python via /api/move; this file handles rendering,
   human input, and the outcome UI. */

"use strict";

const HUMAN = "X";
const AI_PLAYER = "O";
const EMPTY = null;

const LINES = [
  [0, 1, 2], [3, 4, 5], [6, 7, 8],   // rows
  [0, 3, 6], [1, 4, 7], [2, 5, 8],   // columns
  [0, 4, 8], [2, 4, 6],              // diagonals
];

const SCORE_KEY = "tictactoe-ai-scores-v1";

const boardEl = document.getElementById("board");
const winLineEl = document.getElementById("win-line");
const statusEl = document.getElementById("status");
const thinkingEl = document.getElementById("thinking-dots");
const scoreEls = {
  human: document.getElementById("score-you"),
  draw: document.getElementById("score-draw"),
  ai: document.getElementById("score-ai"),
};

const statEls = {
  plain: document.getElementById("stat-plain"),
  pruned: document.getElementById("stat-pruned"),
  saved: document.getElementById("stat-saved"),
  move: document.getElementById("stat-move"),
  note: document.getElementById("stats-note"),
};

let board = Array(9).fill(EMPTY);
let turn = HUMAN;
let over = false;
let winCells = [];
let firstPlayer = AI_PLAYER; // who moves first in the next/current game

let scores = loadScores();

function loadScores() {
  try {
    const raw = localStorage.getItem(SCORE_KEY);
    const data = raw ? JSON.parse(raw) : {};
    return {
      human: data.human || 0,
      draw: data.draw || 0,
      ai: data.ai || 0,
    };
  } catch {
    return { human: 0, draw: 0, ai: 0 };
  }
}

function saveScores() {
  localStorage.setItem(SCORE_KEY, JSON.stringify(scores));
}

/* ------------------------------- rendering ------------------------------ */

function markSVG(player) {
  if (player === "X") {
    return `
      <svg class="mark pop" viewBox="0 0 100 100" aria-hidden="true">
        <g class="draw x-draw">
          <line class="path" pathLength="100" x1="24" y1="24" x2="76" y2="76"/>
          <line class="path" pathLength="100" x1="76" y1="24" x2="24" y2="76"/>
        </g>
      </svg>`;
  }
  return `
      <svg class="mark pop" viewBox="0 0 100 100" aria-hidden="true">
        <g class="draw o-draw">
          <circle class="path" pathLength="100" cx="50" cy="50" r="25"/>
        </g>
      </svg>`;
}

function render() {
  boardEl.innerHTML = "";
  for (let i = 0; i < 9; i++) {
    const cell = document.createElement("button");
    cell.className = "cell";
    cell.dataset.index = i;
    cell.setAttribute("role", "gridcell");
    cell.setAttribute("aria-label", "Cell " + (i + 1));
    if (board[i] !== EMPTY) {
      cell.classList.add("taken");
      cell.innerHTML = markSVG(board[i]);
    } else {
      cell.innerHTML = "";
    }
    cell.addEventListener("click", () => onCellClick(i));
    boardEl.appendChild(cell);
  }
}

function refreshScoreboard() {
  scoreEls.human.textContent = scores.human;
  scoreEls.draw.textContent = scores.draw;
  scoreEls.ai.textContent = scores.ai;
}

function setStatus(text) {
  statusEl.textContent = text;
  thinkingEl.hidden = true;
}

function setThinking(thinking) {
  thinkingEl.hidden = !thinking;
  statusEl.textContent = thinking ? "JARVIS XO is thinking" : statusEl.textContent;
}

/* ------------------------------- game flow ------------------------------ */

function startGame(playerWhoStarts) {
  firstPlayer = playerWhoStarts;
  board = Array(9).fill(EMPTY);
  turn = HUMAN;
  over = false;
  winCells = [];

  winLineEl.classList.remove("show");
  document.querySelectorAll(".cell.win-cell").forEach((c) => c.classList.remove("win-cell"));

  render();
  setStatus(firstPlayer === HUMAN ? "Your turn" : "AI starts");
  updateTurnButtons();

  if (firstPlayer === AI_PLAYER) {
    aiTurn();
  }
}

function onCellClick(index) {
  if (over || turn !== HUMAN || board[index] !== EMPTY) return;
  placeMark(index, HUMAN);
  if (!over) aiTurn();
}

async function aiTurn() {
  setThinking(true);
  const payload = { board, ai_player: AI_PLAYER };

  // small delay so the "thinking" state is visible
  await new Promise((r) => setTimeout(r, 450));

  try {
    const res = await fetch("/api/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "AI request failed");

    await new Promise((r) => setTimeout(r, 250));
    placeMark(data.move, AI_PLAYER);
    updateStats(data.stats, data.move);
  } catch (err) {
    setStatus("Something went wrong: " + err.message);
  }
}

function placeMark(index, player) {
  if (board[index] !== EMPTY || over) return;
  board[index] = player;
  turn = player === HUMAN ? AI_PLAYER : HUMAN;

  const cells = boardEl.children;
  if (cells[index]) {
    cells[index].classList.add("taken");
    cells[index].innerHTML = markSVG(player);
  }

  const result = evaluate();
  if (result) {
    finishGame(result);
  } else {
    setStatus(turn === HUMAN ? "Your turn" : "JARVIS XO is thinking");
    // if AI somehow starts and human never moved, loop:
    if (turn === AI_PLAYER && !over) aiTurn();
  }
}

function evaluate() {
  for (let l = 0; l < LINES.length; l++) {
    const [a, b, c] = LINES[l];
    if (board[a] !== EMPTY && board[a] === board[b] && board[a] === board[c]) {
      return { player: board[a], winLine: l + 1, cells: [a, b, c] };
    }
  }
  if (board.every((cell) => cell !== EMPTY)) {
    return { player: null, winLine: 0, cells: [] }; // draw
  }
  return null;
}

function finishGame(result) {
  over = true;
  winCells = result.cells;

  if (result.player === HUMAN) {
    scores.human += 1;
    setStatus("You win! Can you do it again?");
  } else if (result.player === AI_PLAYER) {
    scores.ai += 1;
    setStatus("JARVIS XO wins. Minimax never sleeps.");
  } else {
    scores.draw += 1;
    setStatus("It's a draw. JARVIS XO is unbeatable!");
  }
  saveScores();
  refreshScoreboard();

  if (result.winLine > 0) {
    const line = document.getElementById("win-line-" + result.winLine);
    if (line) line.style.setProperty("animation-delay", "0.3s");
    winLineEl.classList.remove("show");
    void winLineEl.offsetWidth; // restart animation
    winLineEl.classList.add("show");
    result.cells.forEach((i) => {
      const cell = boardEl.children[i];
      if (cell) cell.classList.add("win-cell");
    });
  }
}

/* -------------------------------- stats --------------------------------- */

function updateStats(stats, move) {
  const saved = stats.plain_nodes - stats.pruned_nodes;
  statEls.plain.textContent = stats.plain_nodes;
  statEls.pruned.textContent = stats.pruned_nodes;
  statEls.saved.textContent = saved;
  statEls.move.textContent = move;
  statEls.note.textContent =
    "Last JARVIS XO move on this board: minimax explored " + stats.plain_nodes +
    " nodes, alpha-beta only " + stats.pruned_nodes +
    " (" + saved + " pruned, SAME optimal move).";
}

/* ------------------------------ controls -------------------------------- */

function updateTurnButtons() {
  document.querySelectorAll(".turn-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.first === (firstPlayer === HUMAN ? "human" : "ai"));
  });
}

document.getElementById("new-game-btn").addEventListener("click", () => startGame(firstPlayer));

document.querySelectorAll(".turn-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    startGame(btn.dataset.first === "human" ? HUMAN : AI_PLAYER);
  });
});

document.getElementById("logout-btn").addEventListener("click", async () => {
  await fetch("/logout", { method: "POST" });
  window.location = "/login";
});

/* --------------------------------- init --------------------------------- */

function init() {
  refreshScoreboard();
  updateTurnButtons();
  startGame(firstPlayer);
}

init();