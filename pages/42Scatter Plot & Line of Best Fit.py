import streamlit as st
import sys
from pathlib import Path

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="Scatter Plot & Line of Best Fit", layout="wide")

def render_regression_lab():
    html_code = load_lab("p42_regression_lab")
    st.iframe(html_code, height=760)


def main():
    st.title("📈 Page 42: Scatter Plot & Line of Best Fit")
    
    st.markdown(
        """
        ### What is a Scatter Plot?
        A **Scatter Plot** is a simple but powerful graph that plots the values of two different variables along two axes, representing each piece of data as a single dot. 
        It allows us to instantly, visually see the relationship (or lack thereof) between two things—like *hours studied* versus *test scores*, or *square footage* versus *house price*.
        
        We know how to measure *if* two things are correlated in a scatter plot (Pearson $r$), but how do we actually **use** that relationship? 
        If we have a cloud of data points, how do we draw a line through them that best captures the trend?
        
        Welcome to **Linear Regression**. This is the first algorithm in our journey to AI. We are trying to build a tiny "model" 
        (a straight line) that summarizes the data.
        """
    )
    
    st.divider()

    st.markdown("### 1) The Interactive Scatter Plot Lab")
    st.markdown(
        "Drop some data points and watch the **Line of Best Fit** instantly recalculate to chase your points. "
        "Try making a straight line, a messy cloud, or putting an outlier far away."
    )
    
    render_regression_lab()
    
    st.info(
        "**Try This:** Turn on **'Show Errors'**. Notice those red vertical lines? Those are called **Residuals**. "
        "The line is placed so that the **sum of the squared lengths** of those red lines is as small as possible (that's what *least squares* means) — not the plain total length."
    )
    
    st.divider()
    
    st.markdown("### 2) How does the Line know where to go?")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(
            """
            The line doesn't have a brain. It uses pure mathematics. 
            
            It evaluates itself using a **Loss Function**. In this case, it uses **Mean Squared Error (MSE)**. 
            For every point, it measures the vertical distance to the line (the error), squares that distance, and averages them.
            
            **The Goal:** Find the Slope ($m$) and Intercept ($b$) that give the absolute lowest possible MSE.
            """
        )
        
    with col2:
        st.markdown(
            """
            **Why Square the Errors?**
            1. **No cancelling out:** If we just added them, a +5 error above the line and a -5 error below the line would sum to 0. Squaring makes everything positive (absolute values would too, giving a different "least absolute deviations" line).
            2. **Punish big mistakes:** Squaring means an error of 1 is just 1, but an error of 5 becomes 25. The line gets heavily penalized for ignoring points completely!
            3. **Smooth & solvable:** The squared loss is a smooth bowl, so calculus gives an exact formula for the best $m$ and $b$ (and gradient descent works nicely). It is also the natural choice when the noise is Gaussian.
            """
        )
        
    st.divider()
    
    st.markdown("### 3) Bridge to AI")
    st.markdown(
        """
        In Machine Learning, we call this **Training a Model**. 
        - The **Data Points** are our Training Data.
        - The **Line ($y = mx + b$)** is our Model.
        - The **Slope ($m$)** is our Weight.
        - The **Intercept ($b$)** is our Bias.
        
        When a Neural Network "learns", it is doing the same kind of thing: adjusting its weights and biases to minimize a loss over the data. The difference is that a network can't jump straight to the answer with a formula — it takes many small gradient-descent steps on a much bumpier loss landscape.
        """
    )
    
    st.divider()
    
    st.markdown("### 4) The Danger of Outliers")
    st.markdown(
        """
        Because we use **Mean Squared Error (MSE)** to evaluate the line, *large* errors are squared and become *massive* penalties. 
        
        **Try it yourself in the lab above:** 
        1. Create a nice, tight diagonal line of data points.
        2. Drop a single point extremely far away in the opposite corner.
        
        Watch how the line violently swings to accommodate that one rogue point! This is why outliers are so dangerous in Machine Learning—models will often destroy a perfectly good trend just to avoid the massive MSE penalty of a single outlier.
        """
    )
    
    st.divider()
    st.markdown(
        """
        <div style="color:#94a3b8; font-size:0.95rem;">
        Page 42 — you just trained your first model and learned about the danger of outliers. Up next: Page 43 opens the hood on that line — residuals, the exact least-squares formula, and how a single high-leverage outlier can drag the whole line.
        </div>
        """,
        unsafe_allow_html=True,
    )
    safe_page_link("pages/43Residuals & Least Squares.py", "Next: 43 · Residuals & Least Squares", icon="➡️")

if __name__ == "__main__":
    main()
