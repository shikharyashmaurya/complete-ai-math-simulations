import sys
from pathlib import Path

import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from common.assets import load_lab  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="Cross-Entropy — Predicted vs Reality", layout="wide")


def render_cross_entropy_lab():
    html_code = load_lab("p59_cross_entropy")
    st.iframe(html_code, height=790)

def main():
    st.title("🌋 Page 59: Cross-Entropy — Predicted vs Reality")

    st.markdown(
        """
        In **Page 58: Entropy — Average Uncertainty**, we learned how to measure the **average uncertainty** ($H(P)$) of a real-world system. 
        But in Artificial Intelligence, we don't just sit back and watch reality. We make **predictions ($Q$)** using neural networks and cross-reference them with **reality ($P$)**.
        
        **Cross-Entropy ($H(P, Q)$)** is the ultimate penalty compass. It measures the **average surprise** you experience when you expect outcomes based on your prediction beliefs $Q$, but reality hits you with facts governed by $P$!
        """
    )
    safe_page_link("pages/58Entropy — Average Uncertainty.py", "Revisit Page 58: Entropy — Average Uncertainty", "↩️")

    st.divider()

    col1, col2 = st.columns([1.1, 0.9])

    with col1:
        st.subheader("The Mathematics of Surprise Mismatch 🧮")
        st.markdown(
            r"""
            For a target distribution $P$ (the true label probability) and predicted distribution $Q$ (the model's probabilities), the **Cross-Entropy** $H(P, Q)$ is defined as:
            
            $$H(P, Q) = -\sum_{i=1}^n P(x_i) \log_2(Q(x_i))$$
            
            * **Single-Label Classification (One-Hot):** If the true class is definitely a **Cat** (so $P(\text{Cat})=1$, and all others are $0$), the entire formula collapses down to exactly one term:
              $$H(P, Q) = -\log_2(Q(x_{\text{correct}}))$$
              This is exactly the **surprise of the correct class** under the model's prediction!
            * **Gibbs' Inequality:** Cross-Entropy is mathematically guaranteed to be **greater than or equal to** the Shannon Entropy of reality:
              $$H(P, Q) \ge H(P)$$
              The extra cost is called **Kullback-Leibler (KL) Divergence**:
              $$\underbrace{H(P, Q)}_{\text{Cross-Entropy}} = \underbrace{H(P)}_{\text{Inevitable Entropy}} + \underbrace{D_{KL}(P \parallel Q)}_{\text{Imperfect Coding Waste}}$$
            """
        )

    with col2:
        st.subheader("Interactive Lessons & Warnings 🌋")
        st.success("🎯 **The Optimal Ideal (No Waste):** When your predictions $Q$ align *perfectly* with reality $P$ ($Q = P$), the waste drops to exactly zero ($D_{KL} = 0$). The Cross-Entropy is minimized and matches $H(P)$!")
        st.info(r"🤷 **The Naive Ignorance baseline:** If a model initializes as a uniform split (33% each for 3 classes), its Cross-Entropy is a moderate, predictable $\log_2 3 \approx 1.585\text{ bits}$ regardless of the true label.")
        st.error(r"💥 **The Confident Wrong Penalty:** If you predict a class has near-zero probability (e.g. $Q(\text{Cat}) = 0.01\%$), but reality declares it is indeed a **Cat**, the surprise penalty $-\log_2(0.0001)$ is about **$13.29\text{ bits}$**. The interactive display floors smaller probabilities at 0.01%; without that numerical floor, the mathematical loss is infinite when a positive target probability is assigned $Q=0$.")

    st.divider()
    st.markdown("### 🧪 The Cross-Entropy Meltdown Laboratory")
    st.markdown(
        "Experiment with reality $P$ and prediction $Q$ live! "
        "Use **Reality Mode** to select standard one-hot label states (like pure Cat) or soft targets (Label Smoothing). "
        "Drag the **Q sliders** to adjust model predictions. Watch how the **waste (KL Divergence)** region grows on the dial as predictions deviate, "
        "and see a visual **Meltdown** alert when the model assigns very little probability to the true outcome!"
    )

    render_cross_entropy_lab()

    st.divider()
    st.subheader("🤖 Bridge to AI: Why Classifiers Love Cross-Entropy")
    st.markdown(
        r"""
        Cross-entropy is the standard loss function for training almost all deep learning classifiers (like ResNet, BERT, or GPT-4). Here is the deep engineering intuition:
        
        #### 1. Why Not Mean Squared Error (MSE) for Classification? 📉
        If we trained classifiers using squared error, when the network is confident and wrong, the derivatives of the sigmoid or softmax activation functions become extremely small (called **gradient saturation**). The model stops learning!
        
        Cross-entropy solves this. Suppose the model outputs $Q = \text{softmax}(z)$ from logits $z$, and measure the loss in **nats** (natural log, which is what deep-learning libraries use). Then the gradient with respect to each logit is:
        $$\frac{\partial H_{\text{nats}}(P, Q)}{\partial z_i} = Q(x_i) - P(x_i)$$
        The $\log$ in the loss exactly cancels the $\exp$ inside the softmax, so there is no saturating factor left over. When the model is confidently wrong ($Q(\text{correct}) \to 0$), the gradient on the correct logit stays close to $-1$: it is **bounded** (never larger than $1$ in magnitude), but it does **not vanish** the way the MSE gradient does.
        
        This page measures cross-entropy in **bits**. Since $H_{\text{bits}} = H_{\text{nats}} / \ln 2$, the base-2 gradient is the same vector rescaled: $\frac{\partial H_{\text{bits}}}{\partial z_i} = \frac{Q(x_i) - P(x_i)}{\ln 2}$. Either way, the gradient is simply the **prediction error** (prediction minus reality), so bigger mistakes get bigger corrections.
        
        #### 2. Label Smoothing: The Art of Preventative Humility 🐾
        In modern AI (e.g., training state-of-the-art vision models), we often prevent models from becoming overly confident by slightly "softening" target labels:
        $$P = [0.90, 0.05, 0.05] \quad \text{instead of} \quad [1.0, 0.0, 0.0]$$
        This is called **Label Smoothing**. As you saw in the laboratory, soft reality targets have an inherent entropy $H(P) > 0$. Because cross-entropy is minimized at $Q = P$, a soft target means the model is penalized if it drives its predictions $Q$ all the way to $100\%$ confidence. This acts as a regularizer that often improves calibration and generalization (it is not a guaranteed cure for overfitting).
        """
    )

    st.divider()
    st.markdown(
        '<div style="color:#94a3b8;font-size:0.95rem;">Page 59 — you\'ve mastered how Cross-Entropy penalizes the mismatch between reality and expectation, and how it drives classification gradients. But what happens when we isolate just the "excess waste" component of this mismatch? Next: we zoom into the core measure of the gap between probability distributions — <b>KL Divergence (Page 60)</b>!</div>',
        unsafe_allow_html=True,
    )
    safe_page_link("pages/60KL Divergence — Gap Between Distributions.py", "Continue to Page 60: KL Divergence — Gap Between Distributions", "➡️")

if __name__ == "__main__":
    main()
