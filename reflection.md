# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first time I ran the game, it appeared to be a number guessing game that asked me to guess a secret number between 1 and 100. It displayed the selected difficulty, my score, remaining attempts, and hints that were supposed to guide me. While testing the game, I noticed incorrect hints, problems with the attempt counter, and guesses outside the stated range being accepted. The New Game button also failed to start a playable new round.

### Bugs I Identified

1. **The hints were incorrect:** The hints did not consistently compare my guess to the secret number. During Easy mode, the secret number was 43, but a guess of 25 displayed “Go Lower” instead of “Go Higher.” During Hard mode, the secret number was 12, but guesses above 12 displayed “Go Higher” instead of “Go Lower.”

2. **The attempt counter was incorrect:** The game ended while the screen still showed one attempt remaining. During Hard mode, the attempt counter also unexpectedly changed from 2 attempts left to 12 attempts left after my fourth guess.

3. **Guesses outside the stated range were accepted:** The game instructed me to enter a number between 1 and 100. However, it accepted -10 as a guess instead of rejecting it or displaying an error.

4. **The New Game button did not properly reset the game:** The button responded when I clicked it, but a new playable round did not begin. The game continued to display the “Game over” message, and the attempts changed to one more than the selected difficulty’s starting amount. I still had to refresh the browser to start another game.

### Bug Reproduction Logs

| Input Used                                    | Expected Behavior                                                                        | Actual Behavior                                                                                                 | Console Error / Output                      |
| --------------------------------------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| Easy mode, secret number 43, guess 25         | The game should display “Go Higher.”                                                     | The game displayed “Go Lower.”                                                                                  | No console error; incorrect hint displayed. |
| Hard mode, secret number 12, guess 76         | The game should display “Go Lower.”                                                      | The game displayed “Go Higher.”                                                                                 | No console error; incorrect hint displayed. |
| Hard mode with 2 attempts left, then guess 92 | The attempt counter should decrease normally and end at the correct time.                | The attempt counter unexpectedly displayed 12, and the game ended.                                              | No console error; attempts displayed as 12. |
| Guess -10                                     | The game should reject the guess because it is outside the 1–100 range.                  | The game accepted the negative guess and continued.                                                             | No console error; invalid input accepted.   |
| Click the New Game button after a round       | The game should reset the secret number, score, and attempts and begin a playable round. | The game remained over, the attempts changed to the starting amount plus one, and the page had to be refreshed. | “Game over. Start a new game to try again.” |

---

## 2. How did you use AI as a teammate?

### AI Tools Used

I used Claude Code in VS Code to review, refactor, and test the project files. I also used ChatGPT to help me understand the instructions, review Claude’s proposed changes to decide what to test next.

### Correct AI Suggestion

Claude correctly explained that the New Game input problem was caused by Streamlit storing the keyed text box value in session state. Claude suggested using a reset flag that clears `guess_input` before the text box is created during the next rerun. I verified this by playing a complete Easy round, clicking New Game, and confirming that the previous guess disappeared while the score and attempts reset correctly. I also ran pytest and confirmed that all four tests passed.

### Incorrect or Misleading AI Suggestion

During the earlier refactor, Claude changed the guess box to use one stable key but did not initially clear that key when New Game was clicked. This caused my previous guess to remain in the box even though the rest of the game reset. I discovered the problem by manually testing the game after the refactor. I then asked Claude to explain the cause before editing the code, reviewed the proposed fix, and tested New Game again to confirm that the input box cleared.

---

## 3. Debugging and testing your fixes

I decided that a bug was fixed only after reviewing the code and testing the behavior myself. I tested different difficulties, valid and invalid guesses, the hint directions, the attempt counter, and the New Game button. I also confirmed that New Game cleared my previous guess and reset the attempts and score.

One automated test I used was `test_hint_directions_are_not_swapped`. It checks that a “Too Low” result displays “Go HIGHER!” and a “Too High” result displays “Go LOWER!” This showed that the hint messages were connected to the correct outcomes. I ran pytest after adding the test, and all four tests passed.

AI helped me understand how pytest checks the output of individual functions. Claude suggested the regression test, explained what each assertion verified, and ran the full test suite. I reviewed the test before approving it and also tested the same behavior in the live Streamlit game.

---

## 4. What did you learn about Streamlit and state?

Streamlit reruns the entire script from top to bottom whenever a user interacts with the app. Session state saves important values, such as the secret number, attempts, score, and input, so they are not lost during each rerun.

---

## 5. Looking ahead: your developer habits

- One habit I want to reuse is testing each feature manually and with pytest after making changes.
- Next time, I would keep each AI chat focused on one bug from the beginning. This would make the suggestions easier to follow and reduce the chance of unrelated changes being included.
- This project taught me that AI-generated code can be helpful, but it can also introduce new bugs. I should always understand, review, and test the code instead of assuming every suggestion is correct.
