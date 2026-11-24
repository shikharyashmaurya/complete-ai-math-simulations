import streamlit as st
import sys
from pathlib import Path

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402

st.set_page_config(page_title="Independence", page_icon="🎲", layout="wide")

st.title("🎲 Page 26: Independence — The Tale of Two Spinners")
st.markdown("### When knowing one thing tells you *nothing* about the other.")

st.info("""
**The Setup:** Imagine we have two separate spinners.
- **Spinner A** decides the Weather.
- **Spinner B** decides the Outfit.

**The Question:** Does knowing the result of Spinner A help you predict Spinner B?
""")

html_code = load_lab("p26_two_spinners")

st.iframe(html_code, height=1040)

st.markdown("---")
st.markdown("### 🧠 The Core Insight")
st.markdown(r"""
**Definition.** Events $A$ and $B$ are **independent** when

$$ P(A \cap B) = P(A)\,P(B) \quad\Longleftrightarrow\quad P(B \mid A) = P(B) \;\; (\text{when } P(A) > 0). $$

In the lab: independent means $P(\text{T-Shirt} \mid \text{Sunny}) = P(\text{T-Shirt} \mid \text{Rainy}) = P(\text{T-Shirt})$,
and the green card's $P(\text{Sunny} \cap \text{T-Shirt})$ matches $P(\text{Sunny}) \cdot P(\text{T-Shirt})$.

- **Independent Events:** Knowing one outcome tells you nothing about the other. The probabilities stay exactly the same.
  - *Example in AI:* Dropout flips a separate coin for every neuron. Whether neuron 3 was dropped tells you nothing about whether neuron 7 was dropped.
- **Dependent Events:** Knowing one outcome changes the probabilities of the other: the conditional probability $P(B \mid A)$ differs from $P(B)$.
  - *Example in AI:* Words in a sentence are highly dependent! If the previous word was "Eiffel", the next word is highly likely to be "Tower". This dependence is what makes Language Models work!
""")

st.success("""
**💡 Notice what happens in the lab:**
- In **Independent Mode** (theory: 50% / 50% / 50%), `P(T-Shirt | Sunny)` and `P(T-Shirt | Rainy)` land close to the overall `P(T-Shirt)` — the gap shrinks as you spin more (try **1000x**). Spinner A's result gives you no advantage in predicting Spinner B.
- In **Dependent Mode** (theory: 90% if Sunny, 10% if Rainy, 58% overall), the conditional probabilities diverge sharply from the overall probability. Spinner A *directly informs* you about Spinner B!
- Switching modes **resets the stats**, so each experiment only contains spins from one rule set.
""")
