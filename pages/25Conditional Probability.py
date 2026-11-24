import json

import streamlit as st
import sys
from pathlib import Path

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="Conditional Probability: P(A|B)", layout="wide")

TOTAL_STUDENTS = 40
# Each scenario splits the same 40 students into the four regions of the Venn diagram.
SCENARIOS = {
    "Club A: the clue matters (dependent)": {"ab": 12, "a-only": 4, "b-only": 8, "none": 16},
    "Club B: the clue changes nothing (independent)": {"ab": 8, "a-only": 8, "b-only": 12, "none": 12},
}

def render_conditional_probability_interactive(counts):
    config = [{"type": t, "count": counts[t]} for t in ("ab", "a-only", "b-only", "none")]
    html_code = load_lab("p25_conditional_probability")
    st.iframe(html_code.replace("__CONFIG_JSON__", json.dumps(config)), height=720)

def main():
    st.title("🎯 Page 25: Conditional Probability - P(A|B)")
    st.markdown(
        r"""
        Welcome to the world of **shifting perspectives**. 
        
        Normally, probability is measured against the **entire universe (Ω)**. But what happens if you receive a clue? If someone whispers, *"Hey, event B already happened"*, your entire universe instantly shrinks. You no longer care about the full sample space—you only care about the **B** outcomes.
        
        Conditional probability asks:
        $$ P(A \mid B) = \frac{P(A \cap B)}{P(B)} $$
        
        Read it simply as: *"Out of the new universe where **B** is true, what fraction also satisfies **A**?"*
        """
    )
    
    st.markdown("### 1) The Shrinking Universe")
    st.markdown("Pick a club, then interact with the simulation below. Watch how knowing a condition drops irrelevant outcomes and changes the denominator.")

    scenario = st.radio(
        "Which club of 40 students?",
        list(SCENARIOS),
        horizontal=True,
        key="p25_scenario",
    )
    counts = SCENARIOS[scenario]
    
    render_conditional_probability_interactive(counts)
    
    st.divider()

    n_ab = counts["ab"]
    n_a = n_ab + counts["a-only"]
    n_b = n_ab + counts["b-only"]
    p_a = n_a / TOTAL_STUDENTS
    p_b = n_b / TOTAL_STUDENTS
    p_a_given_b = n_ab / n_b
    p_b_given_a = n_ab / n_a

    if abs(p_a_given_b - p_a) < 1e-9:
        clue_verdict = (
            f"Here $P(A \\mid B) = P(A) = {p_a:.2f}$: learning that the student is in the AI Club told you **nothing** "
            "new about whether they like Math. That special situation is called **independence** — the topic of the next page."
        )
    else:
        direction = "raised" if p_a_given_b > p_a else "lowered"
        clue_verdict = (
            f"The clue **{direction}** the chance of liking Math from ${p_a:.2f}$ to ${p_a_given_b:.2f}$. "
            "Conditioning on B genuinely changed what we believe about A."
        )

    st.markdown("### 2) The Story Challenge 🧠")
    st.markdown(
        f"""
        Think about the numbers in the simulation above (**{scenario}**):
        - Let **A = Student likes Math** (Blue)
        - Let **B = Student is in AI Club** (Pink)

        Compare the three numbers:
        - $P(A) = {n_a}/{TOTAL_STUDENTS} = {p_a:.2f}$ (If you pick a random student, there's a {p_a:.0%} chance they like Math).
        - $P(A \\mid B) = {n_ab}/{n_b} = {p_a_given_b:.2f}$ (If you pick from the AI Club, there's a {p_a_given_b:.0%} chance they like Math).
        - $P(B \\mid A) = {n_ab}/{n_a} = {p_b_given_a:.2f}$ (If you pick from the Math lovers, there's a {p_b_given_a:.0%} chance they are in the AI Club).

        {clue_verdict}
        """
    )
    st.markdown(
        r"""
        **The Direction Matters!**
        $P(A \mid B)$ is usually different from $P(B \mid A)$. Both share the same numerator $P(A \cap B)$ but divide by
        different denominators ($P(B)$ vs. $P(A)$), so they only agree when $P(A) = P(B)$.
        - E.g., $P(\text{has a steering wheel} \mid \text{is a car})$ is nearly $1.00$. 
        - But $P(\text{is a car} \mid \text{has a steering wheel})$ is lower (it could be a boat, a bus, or a golf cart).

        **When you condition, always ask yourself: "What is my new denominator?"**
        """
    )
    st.caption(f"Check: P(A ∩ B) = {n_ab}/{TOTAL_STUDENTS} = {n_ab / TOTAL_STUDENTS:.2f} and P(B) = {n_b}/{TOTAL_STUDENTS} = {p_b:.2f}, so P(A ∩ B) / P(B) = {p_a_given_b:.2f}.")
    
    st.info(
        """
        ### Recap
        - **Conditioning shrinks the sample space.** You throw away everything that contradicts the given condition.
        - The new denominator is the number of outcomes in the condition.
        - The numerator is the overlap (the outcomes that satisfy both the new universe and the target event).
        
        **Next up:** *Independence* — what happens when knowing B tells you absolutely *nothing* about A? (Club B above is a sneak preview.)
        """
    )
    prev_col, next_col = st.columns(2)
    with prev_col:
        safe_page_link("pages/24Complement, Union & Intersection.py", "Previous: 24 · Complement, Union & Intersection", icon="⬅️")
    with next_col:
        safe_page_link("pages/26Independence.py", "Next: 26 · Independence", icon="➡️")

if __name__ == "__main__":
    main()
