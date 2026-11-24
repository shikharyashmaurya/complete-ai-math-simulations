import sys
from pathlib import Path

import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from common.assets import load_lab  # noqa: E402

st.set_page_config(page_title="Information & Surprise", layout="wide")

def render_surprise_lab():
    html_code = load_lab("p57_surprise")
    st.iframe(html_code, height=670)

def main():
    st.title("💡 Page 57: Information & Surprise")

    st.markdown(
        """
        Imagine you open the morning news and read:
        
        * **Headline A:** *"The Sun Rose this Morning!"*
        * **Headline B:** *"Snow Falls in the Sahara Desert!"*
        
        Which one catches your eye? Which one makes you double-check the source, text your friends, and scream *"No way!"*?
        
        Headline B, obviously. But why? Because **Headline A has a probability of about 99.999%** — it is practically certain and tells you almost nothing you didn't already know. **Headline B is extremely rare (say, 0.01%)** — it carries massive shock value.
        
        In 1948, the father of information theory, **Claude Shannon**, unlocked a beautiful mathematical truth that forms the bedrock of modern AI:
        
        $$\\text{less likely} \\;\\Longrightarrow\\; \\text{more surprise} \\;\\Longrightarrow\\; \\text{more information}$$
        
        Hearing that a 100% certain event occurred yields **zero information**. Hearing that a rare, low-probability event occurred yields **immense information**.
        """
    )

    st.divider()
    
    col1, col2 = st.columns([1.1, 0.9])
    
    with col1:
        st.subheader("The Math of Shock 🧮")
        st.markdown(
            """
            Shannon mathematically defined the self-information (or "surprise") of an event $x$ with probability $p$ as:
            
            $$I(p) = -\\log_2(p)$$
            
            * **Unit:** **Bits** (or Shannons) when the log is base 2. 1 bit represents the surprise of a perfect 50/50 choice. With the natural log ($\\ln$) the unit is the **nat**: $1\\text{ nat} = 1/\\ln 2 \\approx 1.443$ bits.
            * **Why the Negative?** Since $p \\le 1$, $\\log_2(p) \\le 0$. The negative sign flips it to a non-negative number, ensuring that lower probability equals higher surprise!
            * **Why a Logarithm?** 
              Suppose you flip a coin ($p_1 = 0.5$) and roll a die ($p_2 = 1/6$). Because the two events are **independent**, their joint probability is $p_1 \\times p_2 = 1/12$. 
              
              But intuitively, the surprise you feel should be the **sum** of the two surprises:
              
              $$I(\\text{both}) = I(\\text{coin}) + I(\\text{die}) = 1 + 2.585 = 3.585 \\text{ bits} = \\log_2 12$$
              
              Any continuous (or monotonic) function that turns multiplication of independent probabilities into addition of surprises must be of the form $c \\cdot \\log(p)$ — this is the classic Cauchy functional equation. Requiring "rarer ⇒ more surprising" makes $c$ negative, and choosing base 2 just fixes the unit (bits)!
              
              $$\\log(A \\cdot B) = \\log(A) + \\log(B)$$
            """
        )
        
    with col2:
        st.subheader("Properties of Surprise ⚡")
        st.info("🥱 **Certain Event ($p=1$):** $I(1) = -\\log_2(1) = 0$ bits of surprise.")
        st.success("🪙 **50/50 Event ($p=0.5$):** $I(0.5) = -\\log_2(0.5) = 1$ bit of surprise.")
        st.warning("🎲 **Rare Event ($p=0.01$):** $I(0.01) \\approx 6.64$ bits of surprise.")
        st.error("🤯 **Extreme Event ($p \\to 0$):** $I(p) \\to \\infty$ bits of surprise!")

    st.divider()
    st.markdown("### 🧪 Shannon's Shock-O-Meter Laboratory")
    st.markdown(
        "Click on a **preset event** below or drag the **probability slider** (log scale — each quarter of the track is a factor of 10) to see how surprise scales. "
        "Click **Trigger Event** to release sparks into the chamber. Notice how rare events generate massive kinetic energy and rattle the instruments!"
    )
    
    render_surprise_lab()

    st.divider()
    st.subheader("🤖 Bridge to AI: Why Neural Networks Hate Being Surprised")
    st.markdown(
        """
        In classification tasks (like teaching an AI to recognize Cats vs. Dogs), the model outputs a probability $p$ representing its confidence in the correct label.
        
        If the true image is a **Cat**:
        * **Scenario 1 (Confident & Correct):** The model predicts $p=0.99$ for Cat.
          $$\\text{Surprise} = -\\log_2(0.99) \\approx 0.014\\text{ bits}$$
          The model feels practically zero surprise. The loss is tiny.
          
        * **Scenario 2 (Confidently Wrong):** The model predicts $p=0.01$ for Cat (it was 99% sure it was a dog!).
          $$\\text{Surprise} = -\\log_2(0.01) \\approx 6.64\\text{ bits}$$
          The model is **shocked**! It got a massive shock penalty.
          
        For a single example with a one-hot (certain) label, this surprise **is** the **Cross-Entropy Loss** $-\\log p_{\\text{correct}}$. One caveat: deep-learning frameworks use the natural log, so they report it in **nats** — e.g. $-\\ln(0.01) \\approx 4.61$ nats $= 6.64$ bits (just a constant factor of $\\ln 2$). Training a neural network is quite literally the process of **minimizing the model's average surprise** on the training data.
        """
    )
    
    st.divider()
    st.markdown(
        '<div style="color:#94a3b8;font-size:0.95rem;">Page 57 — you\'ve experienced how single events spark surprise. But what is the <b>average</b> surprise across a whole landscape of possibilities? Next: we discover the core metric of uncertainty — <b>Entropy (Page 58)</b>!</div>',
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
