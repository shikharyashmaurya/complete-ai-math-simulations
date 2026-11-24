import sys
from pathlib import Path

import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402

st.set_page_config(page_title="What is a Loss Function?", layout="wide")

def render_lab():
    st.iframe(load_lab("p50_loss_function"), height=660)

def main():
    st.title("🥊 Page 50: What is a Loss Function?")
    
    st.markdown(
        """
        Welcome to the **Penalty Box**! In AI, a model's job is to make predictions. But models aren't perfect—they make mistakes.
        
        The **Loss Function** is a mathematical way of saying: *"How bad did I mess up?"*
        It takes all the mistakes, crushes them down into a **single number**, and hands it to us as a score. Lower is better!
        """
    )
    
    st.divider()
    
    render_lab()
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📏 Mean Absolute Error (MAE)")
        st.latex(r"L = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|")
        st.markdown(
            """
            **The Intuition:** Just measure the distance from the point to the line. 
            If you're off by 5 units, the "penalty" is 5.
            
            - **Pros:** Easy to explain, robust to outliers.
            - **Cons:** The "V-shape" (absolute value) is hard to use with calculus because the tip isn't smooth.
            """
        )
        
    with col2:
        st.markdown("### ⬛ Mean Squared Error (MSE)")
        st.latex(r"L = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2")
        st.markdown(
            """
            **The Intuition:** Imagine drawing a **literal square** for every error. The total Loss is the total area of those squares.
            
            - **Pros:** Huge penalties for big misses! Calculus loves squares ($x^2 \\to 2x$ is smooth).
            - **Cons:** One single "outlier" (a very wrong point) can explode the loss.
            """
        )
        
    st.divider()
    st.markdown("### 🕵️ Why 'Squared'?")
    st.info(
        """
        In the lab above, switch to **MSE** and move a single point far away. Watch the "Loss Meter" skyrocket! 
        Because we square the error, being off by **10** costs you **100**, while being off by **2** only costs **4**. 
        
        This pushes the fit to prioritize fixing the "biggest" mistakes first. For a straight-line model like this one, MSE also turns the "Loss Landscape" (loss plotted against *w* and *b*) into a smooth bowl with a single bottom, which makes finding the bottom much easier. For deep neural networks the landscape is usually bumpier, even with MSE, as we'll see in the next few pages!
        """
    )

    st.markdown(
        '<div style="color:#94a3b8;font-size:0.95rem;">Page 50 — you now understand how we quantify failure. Next: we turn these failure scores into a 3D landscape of Hills and Valleys!</div>',
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
