from logic_utils import check_guess, get_hint

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_hint_directions_are_not_swapped():
    # Regression: the original code paired "Too High" with "Go HIGHER!",
    # which pointed the player away from the secret instead of toward it.
    assert "Go HIGHER!" in get_hint("Too Low")
    assert "Go LOWER!" in get_hint("Too High")
