import streamlit as st
import sys
from pathlib import Path

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="Sample Space & Probability", layout="wide")

def render_sample_space_interactive():
    html_code = load_lab("p23_sample_space")
    st.iframe(html_code, height=460)

def render_venn_interactive():
    html_code = load_lab("p23_venn")
    st.iframe(html_code, height=560)

def render_2d_space_interactive():
    html_code = load_lab("p23_2d_space")
    st.iframe(html_code, height=660)

def main():
    st.title("🎲 Page 23: Sample Space & Basic Probability")
    st.markdown(
        r"""
        Probability begins with mapping out the universe. Before you can ask "how likely is it?", you must ask **"what is possible?"**
        
        That complete list of everything that could possibly happen is called the **Sample Space ($\Omega$)**. 
        For a single fair six-sided die, $\Omega = \{1, 2, 3, 4, 5, 6\}$. 

        An **Event (A)** is simply a subset of that universe. When all atoms in the universe are equally likely, finding the probability is just counting:
        $$ P(A) = \frac{|A|}{|\Omega|} = \frac{\text{Number of winning outcomes}}{\text{Total possible outcomes}} $$
        """
    )
    
    st.markdown("### 1) The Universe of Outcomes")
    st.markdown("Interact with the atoms below. Select an **Event** to watch the subset light up and see the probability calculated live.")
    
    render_sample_space_interactive()
    
    st.divider()

    st.markdown("### 2) Intersections, Unions & Complements (Venn Lab)")
    st.markdown(
        r"""
        Events can be combined using set theory operations:
        - **Complement ($A^c$)**: Everything NOT in A. The leftovers. $|A^c| = |\Omega| - |A|$.
        - **Intersection ($A \cap B$)**: The overlap. Outcomes that live in **both** A and B.
        - **Union ($A \cup B$)**: The merge. Outcomes that live in A, **or** B, **or both**.
        
        Play with the dropdowns to see how different events share atoms. Notice how $|A \cup B| = |A| + |B| - |A \cap B|$.
        """
    )
    
    render_venn_interactive()
    
    st.divider()

    st.markdown("### 3) 2D Sample Space: Rolling Two Dice")
    st.markdown(
        """
        When you roll **two dice**, the universe expands. It is no longer 6 atoms, it is the **Cartesian Product**: a 6x6 grid of **36 ordered pairs**.
        
        Use the slider to highlight a target sum. See how sums like **7** carve out a long diagonal with 6 different ways to win, while extreme sums like **2** or **12** have only 1 way to win.
        """
    )
    
    render_2d_space_interactive()
    
    st.warning(
        r"""
        **Counting trap:** the *sums* $\{2, 3, \dots, 12\}$ are 11 possible results, but they are **not** equally likely,
        so $P(\text{sum}=7) \neq \frac{1}{11}$. Counting only works on the 36 equally likely ordered pairs:
        $P(\text{sum}=7) = \frac{6}{36} = \frac{1}{6}$, while $P(\text{sum}=2) = \frac{1}{36}$.
        Always count in a sample space whose atoms really are equally likely.
        """
    )
    
    st.info(
        """
        ### Recap
        - **Sample Space (Ω):** The absolute truth of all possible outcomes.
        - **Events:** Subsets of Ω that we care about.
        - **Set operations:** complement, intersection and union combine events — and $|A \\cup B| = |A| + |B| - |A \\cap B|$.
        - **Counting is Probability:** If outcomes are equally likely, math reduces to simply counting glowing orbs.
        
        **Next up (Page 24):** *Complement, Union & Intersection* — combine events with NOT, AND and OR, and count overlaps without double-counting.
        """
    )
    safe_page_link("pages/24Complement, Union & Intersection.py", "Next: 24 · Complement, Union & Intersection", icon="➡️")

if __name__ == "__main__":
    main()
