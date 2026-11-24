import sys
from pathlib import Path

import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from common.assets import load_lab  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="KL Divergence — Gap Between Distributions", layout="wide")


def render_kl_divergence_lab():
    html_code = load_lab("p60_kl_divergence")
    st.iframe(html_code, height=830)

def main():
    st.title("🧩 Page 60: KL Divergence — Gap Between Distributions")

    st.markdown(
        """
        In **Page 59: Cross-Entropy — Predicted vs Reality**, we observed how **Cross-Entropy** penalizes a neural network's incorrect prediction.
        But mathematically, Cross-Entropy consists of two parts: the inevitable natural entropy of reality $H(P)$, and an **excess coding waste** when we approximate reality using our model's beliefs $Q$.
        
        This excess waste — the actual gap between two probability distributions — is quantified by the **Kullback-Leibler (KL) Divergence** ($D_{KL}$).
        It measures exactly how many **extra bits** of information we waste, on average, if we encode data events from a true distribution $P$ using an imperfect code optimized for a predicted distribution $Q$.
        """
    )
    safe_page_link("pages/59Cross-Entropy — Predicted vs Reality.py", "Revisit Page 59: Cross-Entropy — Predicted vs Reality", "↩️")

    st.divider()

    col1, col2 = st.columns([1.1, 0.9])

    with col1:
        st.subheader("The Mathematics of Information Gap 🧮")
        st.markdown(
            r"""
            For two probability distributions, $P(x)$ (the target label or reality) and $Q(x)$ (the approximation or model predictions):
            
            * **Discrete Case:**
              $$D_{KL}(P \parallel Q) = \sum_{x} P(x) \log_2 \left( \frac{P(x)}{Q(x)} \right) \text{ bits}$$
              
            * **Continuous Case:**
              $$D_{KL}(P \parallel Q) = \int_{-\infty}^{\infty} P(x) \log_2 \left( \frac{P(x)}{Q(x)} \right) dx \text{ bits}$$
              
            * **Closed-Form for two Gaussians:** In our visualizer, we model two normal bell curves $P \sim \mathcal{N}(\mu_P, \sigma_P^2)$ and $Q \sim \mathcal{N}(\mu_Q, \sigma_Q^2)$. The analytical divergence is calculated exactly as:
              $$D_{KL}(P \parallel Q) = \frac{1}{\ln 2} \left[ \ln\left(\frac{\sigma_Q}{\sigma_P}\right) + \frac{\sigma_P^2 + (\mu_P - \mu_Q)^2}{2\sigma_Q^2} - \frac{1}{2} \right] \text{ bits}$$
              
            * **Gibbs' Inequality:** The KL divergence is mathematically guaranteed to be **non-negative**:
              $$D_{KL}(P \parallel Q) \ge 0$$
              It equals exactly $0$ if and only if $P = Q$ (distributions match perfectly).
            """
        )

    with col2:
        st.subheader("Why the Direction Matters: Asymmetry ⚖️")
        st.markdown(
            r"""
            KL Divergence is **not a true distance metric** because it is asymmetric:
            $$D_{KL}(P \parallel Q) \neq D_{KL}(Q \parallel P)$$
            
            This directionality creates two radically different optimization behaviors in deep learning:
            
            1. **Forward KL ($D_{KL}(P \parallel Q)$) — Zero-Avoiding / Mean-Seeking:**
               If $P(x) > 0$, we *must* have $Q(x) > 0$. If $Q(x) \to 0$ in a region where reality exists, the fraction $\frac{P(x)}{Q(x)}$ explodes, and the penalty sweeps to **infinity** (exactly $Q(x) = 0$ where $P(x) > 0$ gives $D_{KL} = \infty$; for two Gaussians, as in the lab below, it stays finite but grows fast when $Q$ is too narrow). 
               Thus, a model optimizing Forward KL is forced to stretch and cover **every mode** of $P$, often producing fuzzy, averaged predictions.
               
            2. **Reverse KL ($D_{KL}(Q \parallel P)$) — Zero-Forcing / Mode-Seeking:**
               If reality has no data in a region ($P(x) \to 0$), the model $Q(x)$ is heavily penalized for placing any probability there. 
               To minimize this, $Q$ will shrink to zero wherever $P$ is zero. If $P$ has multiple well-separated modes, $Q$ tends to lock onto **one mode** and concentrate its density there, largely ignoring the others in exchange for a tight, sharp, high-confidence fit.
            """
        )

    st.divider()
    st.markdown("### 🧪 The KL Divergence Asymmetry & Sampling Laboratory")
    st.markdown(
        "Experiment with drifting normal distributions in real time! "
        r"Select presets or drag the sliders to change the means ($\mu$) and standard deviations ($\sigma$) of reality $P$ and model $Q$. "
        "Watch how the **asymmetry** is reflected in the twin liquid columns, witness a local **Surprise Penalty** ribbon, "
        "and toggle the **Interactive Monte Carlo Sampler** to drop particle samples: the running average of all samples so far "
        "approaches the exact value, and its ± standard error shrinks roughly like $1/\\sqrt{n}$ as more samples land."
    )

    render_kl_divergence_lab()

    st.divider()
    st.subheader("🤖 Bridge to AI: KL Divergence in Modern Deep Learning")
    st.markdown(
        r"""
        KL Divergence is a fundamental tool across the most advanced branches of modern Artificial Intelligence:
        
        #### 1. VAEs & Variational Inference: Reverse KL 🔍
        In **Variational Autoencoders (VAEs)**, we want to map complex input data (like high-resolution faces) into a simple, continuous latent space (usually standard Gaussians $\mathcal{N}(0, I)$). 
        To force the encoder network's output distribution $Q(z|x)$ to resemble standard noise, we add a KL Divergence penalty to our loss function:
        $$\text{Loss} = \text{Reconstruction Error} + D_{KL}(Q(z|x) \parallel \mathcal{N}(0, I))$$
        This regularizes the latent space, keeping it smooth and continuous, allowing us to generate completely new, realistic images by sampling coordinates!
        
        Note the direction: the **model** $Q$ comes first, so in this page's convention ($P$ = target, $Q$ = model) this is a **reverse KL**. Variational inference in general minimizes $D_{KL}(Q(z|x) \parallel P(z|x))$, also a reverse KL, which is why variational approximations tend to be mode-seeking and to under-estimate the spread of the true posterior.
        
        #### 2. Reinforcement Learning from Human Feedback (RLHF): Stable Policy Alignment 🛡️
        When fine-tuning Large Language Models with RLHF, we train a **Reward Model** based on human feedback and optimize the language policy network ($Q_\theta$) with a reinforcement-learning algorithm such as PPO. 
        However, if optimized aggressively, the model will find "hacks" in the reward function (called **reward hacking**), outputting gibberish or unsafe answers that exploit the evaluator.
        
        To limit this drift, engineers add a KL penalty between the policy being trained, $Q_\theta$, and a frozen **reference model** $P_{\text{ref}}$ (typically the supervised fine-tuned model the run started from). The policy comes first, so in this page's convention it is a **reverse KL**, $D_{KL}(Q_\theta \parallel P_{\text{ref}})$:
        $$\text{Objective}(\theta) = \mathbb{E}_{x \sim D}\Big[\, \mathbb{E}_{y \sim Q_\theta(\cdot|x)}[\text{Reward}(x, y)] - \beta \, D_{KL}\big(Q_\theta(\cdot|x) \parallel P_{\text{ref}}(\cdot|x)\big) \Big]$$
        Here prompts $x$ come from the dataset $D$, but responses $y$ are **sampled from the policy being trained**. This KL "anchor" acts as a leash: it penalizes the policy for drifting too far from the reference model's token distributions, which helps keep its outputs fluent and makes reward hacking harder. It does **not** by itself guarantee factual accuracy or safety — the model can only stay as truthful and safe as the reference model and the reward signal allow.
        """
    )

    st.divider()
    st.markdown(
        '<div style="color:#94a3b8;font-size:0.95rem;">Page 60 — you\'ve mastered how KL Divergence captures the information gap and asymmetry between probability distributions. By isolating excess surprise, you have met a quantity that shows up everywhere from VAE latents to keeping fine-tuned LLMs close to their reference model. Next: before plunging into advanced Linear Algebra, one more information-theory tool — <b>Mutual Information (Page 89)</b>, which uses KL Divergence to measure how much knowing one variable tells you about another!</div>',
        unsafe_allow_html=True,
    )
    safe_page_link("pages/89Mutual Information.py", "Next: 89 · Mutual Information", "➡️")

if __name__ == "__main__":
    main()
