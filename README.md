# Quoridor Strategic Game AI

This repository contains a Python implementation of the **Quoridor board game** along with an AI agent capable of playing against a human opponent. Developed as a course project for *CS246: Artificial Intelligence* at the American University of Armenia, this project demonstrates the use of classical AI algorithms to navigate adversarial and pathfinding challenges.

---

## Project Overview

Quoridor is a strategic board game where players race to reach the opposite side of a 9x9 grid while placing walls to block opponents. This AI agent leverages **Minimax with alpha-beta pruning** and heuristic functions to make optimal moves and strategically place walls to hinder its opponent. The game environment was built using **PyGame**, allowing for interactive play between human users and the AI agent.

---

## Features

- **AI Agent:** Implements Minimax with alpha-beta pruning for decision making.
- **Heuristic Functions:** Balances pathfinding and opponent obstruction strategies.
- **Adaptive Strategies:** Dynamically adjusts between movement and wall placement based on the game stage.
- **PyGame Interface:** Interactive graphical interface for playing against the AI.

---

## Project Structure

```
Quoridor_Strategic_Game/
├── src/                    # Source code
│   └── main.py
├── assets/                 # Images (e.g., quoridor.png)
├── docs/                   # Documentation
│   ├── Quoridor_Report.pdf
│   ├── Quoridor.tex
│   └── Slides-Presentation.pdf
├── README.md               # Project description
```

---

## How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/Quoridor-Strategic-Game.git
   cd Quoridor-Strategic-Game/src
   ```

2. **Install dependencies:**
   ```bash
   pip install pygame
   ```

3. **Run the game:**
   ```bash
   python main.py
   ```

4. **Controls:**
   - Move player: `↑ ↓ ← →`
   - Place wall: Press `W`, move with arrows, rotate with `Space`, confirm with `Enter`
   - Cancel wall placement: Press `M`

---

## Technologies

- Python 3.x
- PyGame
- Minimax Algorithm with Alpha-Beta Pruning

---

## Authors

This project was developed as part of *CS246: Artificial Intelligence*.

- Narek Khachikyan
- Kima Badalyan
- Ruben Galoyan
