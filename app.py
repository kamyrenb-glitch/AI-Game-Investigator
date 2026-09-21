import random
import streamlit as st

from logic_utils import (
    check_guess,
    get_attempt_limit,
    get_hint,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("A number guessing game, debugged.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

low, high = get_range_for_difficulty(difficulty)
attempt_limit = get_attempt_limit(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

def start_new_game():
    """Reset every piece of game state for a fresh round."""
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.difficulty = difficulty
    # The guess box is a keyed widget, so its value lives in session state and
    # survives this reset. Streamlit forbids writing to a widget's key after
    # the widget exists, so leave a note for the top of the next run instead.
    st.session_state.clear_guess_input = True


if "secret" not in st.session_state:
    start_new_game()

# Switching difficulty changes the range, so the old secret may no longer be
# reachable. Start a fresh round instead of leaving a stale secret behind.
if st.session_state.difficulty != difficulty:
    start_new_game()

# FIX: New Game left my last guess in the box. Claude diagnosed the keyed widget
# as session state the reset missed, and proposed this deferred clear.
# Runs before the text input is created, which is the only point where its
# stored value may be changed.
if st.session_state.get("clear_guess_input"):
    st.session_state.guess_input = ""
    st.session_state.clear_guess_input = False

st.subheader("Make a guess")

# These render now but are filled in at the bottom of the script, after this
# run's guess has been processed, so they never show stale counts.
attempts_slot = st.empty()
debug_slot = st.empty()

raw_guess = st.text_input("Enter your guess:", key="guess_input")

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    start_new_game()
    st.rerun()

if st.session_state.status == "playing" and submit:
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        # An invalid entry is not a guess, so it does not burn an attempt.
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        outcome = check_guess(guess_int, st.session_state.secret)

        if show_hint and outcome != "Win":
            st.warning(get_hint(outcome))

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"

if st.session_state.status == "won":
    st.success(
        f"You won! The secret was {st.session_state.secret}. "
        f"Final score: {st.session_state.score}"
    )
elif st.session_state.status == "lost":
    st.error(
        f"Out of attempts! "
        f"The secret was {st.session_state.secret}. "
        f"Score: {st.session_state.score}"
    )

attempts_left = max(attempt_limit - st.session_state.attempts, 0)
attempts_slot.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempts_left} | Score: {st.session_state.score}"
)

with debug_slot.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI. Debugged by a human.")
