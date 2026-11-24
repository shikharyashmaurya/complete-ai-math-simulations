import sys
from pathlib import Path

import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from common.assets import load_lab  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="Entropy — Average Uncertainty", layout="wide")

def render_entropy_lab():
    html_code = load_lab("p58_entropy")
    st.iframe(html_code, height=670)


def main():
    st.title("🌀 Page 58: Entropy — Average Uncertainty")

    st.markdown(
        """
        In **Page 57: Information & Surprise**, we explored **surprise** ($I(p) = -\\log_2(p)$) — a concept that measures the shock of a *single* event occurring. 
        """
    )
    safe_page_link("pages/57Information & Surprise.py", "Revisit Page 57: Information & Surprise", "💡")
    st.markdown(
        """
        But what if you are looking at a system with **multiple possible outcomes** (like forecasting the weather or predicting the next token in a ChatGPT generation)? How do you measure the **overall predictability or average uncertainty** of the entire system?
        
        This is where **Shannon Entropy ($H$)** comes in! Entropy is simply the **expected value (average)** of surprise across all possible outcomes.
        """
    )

    st.divider()
    
    col1, col2 = st.columns([1.1, 0.9])
    
    with col1:
        st.subheader("The Mathematics of Average Uncertainty 🧮")
        st.markdown(
            r"""
            For a system $X$ with $n$ possible outcomes, each with probability $p_i$, the overall entropy $H(X)$ is defined as:
            
            $$H(X) = \sum_{i=1}^n p_i I(p_i) = -\sum_{i=1}^n p_i \log_2(p_i)$$
            
            * **Unit:** **Bits** (or Shannons) because we use $\log_2$. A system with $1\text{ bit}$ of entropy has the same uncertainty as a perfect 50/50 coin flip. (With the natural log, as ML libraries use, the unit is the **nat**; $1\text{ nat} \approx 1.443$ bits.)
            * **Convention $0 \cdot \log 0 = 0$:** An outcome with $p_i = 0$ never happens, so it adds nothing to the average (since $p \log p \to 0$ as $p \to 0$).
            * **The Weighted Average:** Notice how we multiply the surprise $-\log_2(p_i)$ by its probability $p_i$. A highly rare event has massive surprise, but because it happens so rarely, it contributes very little to the **average** surprise!
            * **Bounds:** $0 \le H(X) \le \log_2 n$. The maximum $\log_2 n$ is reached only by the uniform distribution — $1$ bit for a coin, $\log_2 4 = 2$ bits for the 4-state weather lab below.
            * **Binary Entropy (2-State):** If there are only two outcomes (Heads with probability $p$, and Tails with $1-p$), the formula simplifies to:
              $$H(p) = -p \log_2(p) - (1-p) \log_2(1-p)$$
            """
        )
        
    with col2:
        st.subheader("Interactive Insights 💡")
        st.info(r"🤷 **Maximum Entropy ($H = \log_2 n$):** Occurs when all outcomes are equally likely (uniform distribution). No outcome is favoured, so the best possible guess is right only $1/n$ of the time — no better than chance.")
        st.success(r"🎯 **Minimum Entropy ($H=0$):** Occurs when one outcome is 100% guaranteed. There is zero uncertainty, meaning the system is completely predictable.")
        st.warning(r"📉 **The Curve shape:** For binary outcomes, the curve peaks precisely at $p=0.5$ ($H = 1\text{ bit}$) and drops down to $0$ on both sides. Adding certainty drops entropy!")

    st.divider()
    st.markdown("### 🧪 Shannon's Entropy Laboratory Sandbox")
    st.markdown(
        "Choose a mode below to experiment with average uncertainty! Drag the **sliders** to adjust the probabilities live. "
        "Click **Toss Coin** / **Generate Weather** (or toggle **AUTO**) to simulate draws and observe how the running average surprise (green) **smooths out and converges** to the theoretical entropy (dashed purple) via the Law of Large Numbers! "
        "Changing any probability restarts the running average, because convergence only holds for a fixed distribution."
    )
    
    render_entropy_lab()

    st.divider()
    st.subheader("🤖 Bridge to AI: Why Neural Networks Love Low Entropy")
    st.markdown(
        r"""
        In machine learning, entropy is the ultimate compass. Here is why it rules the AI landscape:
        
        #### 1. Information Gain in Decision Trees 🌳
        When a Decision Tree (like ID3) decides how to split your dataset (e.g. splitting email by "Has Link" to detect Spam), it calculates the **Information Gain**:
        $$\text{Information Gain} = H(\text{Parent}) - \sum_{k} \frac{|S_k|}{|S|}\, H(S_k)$$
        where $S_k$ is the subset of the $|S|$ parent samples that lands in child $k$ — the children's entropies are **weighted by their size**.
        The tree chooses the split that **maximizes Information Gain** — which is just a fancy way of saying it wants to **reduce entropy (uncertainty)** as much as possible, splitting data into clean, predictable categories!
        
        #### 2. Entropy Regularization in Reinforcement Learning 🤖
        When training an RL agent (like a robot learning to walk), we don't want it to lock into one strategy too early and get stuck. 
        We add an **entropy bonus** to its loss function:
        $$\text{Loss} = \text{Policy Loss} - \alpha \cdot H(\pi)$$
        This penalizes the agent for being too certain too quickly, forcing it to keep exploring new actions because **higher entropy = more exploratory freedom**!
        
        #### 3. The Core of Cross-Entropy Loss 🎯
        When training classifiers, the **Cross-Entropy** $H(p, q) = -\sum_i p_i \log q_i$ compares the true distribution $p$ with the model's predicted distribution $q$. It decomposes as $H(p, q) = H(p) + D_{\text{KL}}(p \,\|\, q)$, so minimizing it drives $q$ toward $p$ (the KL divergence toward $0$). With a one-hot label ($H(p) = 0$) that means pushing the prediction toward certainty on the correct class; with soft labels (e.g. label smoothing) the optimum is $q = p$, which is **not** zero-entropy. (Libraries use $\ln$, so the loss is reported in nats.)
        """
    )
    
    st.divider()
    st.markdown(
        '<div style="color:#94a3b8;font-size:0.95rem;">Page 58 — you\'ve mastered how entropy gauges average uncertainty across a system. But what happens when we compare a predicted distribution against real-world labels? Next: we discover the cornerstone penalty of classifier training — <b>Cross-Entropy (Page 59)</b>!</div>',
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
