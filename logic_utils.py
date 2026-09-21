"""Pure game logic for the number guessing game.

Nothing in here imports Streamlit, so every function can be called directly
from pytest without spinning up the app.
"""

# Each difficulty gets its own range and attempt budget. The budget is at least
# log2(range size) so a player using binary search can always win.
DIFFICULTY_SETTINGS = {
    "Easy": {"range": (1, 20), "attempts": 6},
    "Normal": {"range": (1, 100), "attempts": 8},
    "Hard": {"range": (1, 200), "attempts": 8},
}

DEFAULT_DIFFICULTY = "Normal"

# FIX: The original code paired "Too High" with "Go HIGHER!". I had Claude trace
# check_guess -> get_hint and replay my logged cases to confirm this pairing.
HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}


def _settings_for(difficulty: str):
    return DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS[DEFAULT_DIFFICULTY])


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    return _settings_for(difficulty)["range"]


def get_attempt_limit(difficulty: str):
    """Return how many guesses the player gets on a given difficulty."""
    return _settings_for(difficulty)["attempts"]


def parse_guess(raw: str, low=None, high=None):
    """
    Parse user input into an int guess.

    When low and high are given, the guess must fall inside that inclusive
    range. Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    text = raw.strip()
    if text == "":
        return False, None, "Enter a guess."

    try:
        value = int(text)
    except ValueError:
        return False, None, "That is not a whole number."

    if low is not None and high is not None and not low <= value <= high:
        return False, None, f"Enter a number between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    outcome is one of: "Win", "Too High", "Too Low"
    """
    guess = int(guess)
    secret = int(secret)

    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def get_hint(outcome: str):
    """Return the player-facing message for an outcome from check_guess."""
    return HINT_MESSAGES.get(outcome, "")


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number.

    A win is worth more the earlier it happens (100 on the first attempt,
    10 points less per attempt after that, floored at 10). Every wrong guess
    costs 5 points, whichever direction it missed by.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        return current_score + max(points, 10)

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
