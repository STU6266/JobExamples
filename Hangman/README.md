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
