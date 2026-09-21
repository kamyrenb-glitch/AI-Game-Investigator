# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- **Game purpose:** Glitchy Guesser is a numeric guessing game where users follow hints to find a secret number within a limited number of attempts. 
- **Bugs found:** I found incorrect higher and lower hints, invalid guesses affecting the game, an inaccurate attempt counter, and the previous guess remaining after starting a new game. 
- **Fixes applied:** I corrected the hint logic, improved input validation and attempt tracking, moved the core game logic into `logic_utils.py`, fixed the New Game reset behavior, and added a regression test to verify the hints.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. The user selects Easy, Normal, or Hard difficulty to set the number range and attempt limit.
2. The user enters a number within the displayed range and clicks “Submit Guess.”
3. The game responds with “Go HIGHER!” or “Go LOWER!” and updates the attempts and score.
4. The user follows the hints and continues guessing until they find the correct number or run out of attempts.
5. After the game ends, the user can click “New Game” to generate a new secret number, reset the score and attempts, and clear the previous guess.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# pytest tests/ -v
# ============================= 4 passed in 0.03s =============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
