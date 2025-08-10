# JobExamples

Two small projects included in this repository. Both descriptions use the same structure and formatting for a clean, consistent look.

---

## Dice Roller (Python • Tkinter + Matplotlib)

### Overview
A small GUI app to roll custom dice sets. You can create multiple **sets**, choose how many **dice** each set has, pick the **number of sides** per die, and roll each set independently.  
For dice with **2–6 sides** the result is shown with traditional **pips**; for **>6** sides the **number** is shown.

### Features
- Multiple dice **sets**, each with its own settings
- Per‑set **color** for the die face and the number/pips
- **Roll** each set independently with one click
- Layout adapts to **smaller screens**

### Requirements
- **Python 3.12+** (tested on 3.12)
- Packages: `matplotlib`, `numpy`
- Tkinter (included with the standard Python installer on Windows/macOS)

### Getting Started
```bash
# 1) Clone / Download
git clone <your-repo-url>
cd <repo-folder>

# 2) (Optional) Create & activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 3) Install dependencies
pip install -r requirements.txt  # or: pip install matplotlib numpy

# 4) Run
python dice_en.py
```

---

## Hangman (C# • Console)

### Overview
A simple, classic **Hangman** game for the terminal. You pick a difficulty, the game pulls a random word from `words.txt`, and you guess one letter at a time while an ASCII figure slowly takes shape.

### Features
- **Difficulty levels**
  - Easy: 4–5 letters
  - Medium: 6–8 letters
  - Hard: 9+ letters
- **10 wrong attempts** allowed (the 11th wrong guess ends the game)
- **ASCII hangman** that grows with each mistake
- **Word list from file**: `words.txt` (one word per line)
- Case‑insensitive input, **no double‑counting** of repeated guesses
- Cross‑platform with **.NET 8** (Windows/macOS/Linux)

### Requirements
- **.NET SDK 8+**

### Getting Started
```bash
# 1) Clone / Download
git clone <your-repo-url>
cd <repo-folder>

# 2) Build & Run (from the Hangman project directory)
dotnet build
dotnet run
```

---

## Repository Notes

- `README.md` uses consistent headings, lists, and fenced code blocks so both project descriptions match in **layout** and **style**.
- Command examples use **bash** blocks for uniform syntax highlighting across platforms.
- Replace `<your-repo-url>` and adjust file paths if your project structure differs.
