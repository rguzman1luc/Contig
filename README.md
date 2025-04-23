# Contig 

A two-player math strategy game in Python.

## 🎮 How to Play
- Roll 3 dice per turn.
- Form a math expression using the dice.
- If your result matches an unclaimed number on the board, you can claim it.
- Gain 1 point for each adjacent tile you own.
- First to 25 points wins!

## 📌 Mission Statement
Our mission is to remake the original Java based Contig game by adding new features and improving gameplay through a fresh implementation in a new programming language. We aim to enhance the user experience with some improvements that weren't originally implemented due to time constraints of the original projects. Through this process, we seek to deepen our understanding of software development practices and the nature of open-source projects.
## 🗂️ Project Outline & Progress

## Our plans / timeline of the project:

### ✅ 1. Analyze Original Code
- Reviewed the original implementation.
- Cleaned up code. 
- Identified a base for the project. 

### 💡 2. Brainstorm Improvements
- Discussed improvements:
  - GUI version (Tkinter? Pyqt5?)✅
  - Player turn timer✅
  - Move History tab
  - Proof Time tab
  - Arithmetic validation helper🟥
  - Sound effects or animations 🟥
  - Save/load game state🟥

### 🐍 3. Choose Language: Python
- Selected Python for readability and rapid GUI development (via `tkinter`).

### 🔧 4. Rebuilt Base Game in Python (Text-based)
- Re-implemented original terminal version in Python.
- Preserved all core functionality (e.g., score system, board layout, dice logic).

### 🗺️ 5. Begin GUI Planning
- Drafted initial window layout.
- Determined components needed:
  - Game board 
  - Display a way for the numbers rolled 
  - Input field number obtained
  - Score tracker
  - Turn indicator

### ⚙️ 6. GUI Implementation
- Integrated GUI with original Python logic.
- Opened in a new window instead of terminal
- Achieved putting everything into a simple game window instead of multiple dialog boxes. 

### 🧼 7. Final Polish + New Features
- Refactored code for clarity and modularity.
- Added a **turn timer** for each player.
