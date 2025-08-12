

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

