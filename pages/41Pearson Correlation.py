import streamlit as st
import sys
from pathlib import Path

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402

st.set_page_config(page_title="Pearson Correlation", layout="wide")

def render_correlation_lab():
    html_code = load_lab("p41_correlation_lab")
    st.iframe(html_code, height=680)


def render_nonlinear_gotcha():
    html_code = load_lab("p41_nonlinear_gotcha")
    st.iframe(html_code, height=370)


def main():
    st.title("📏 Page 41: Pearson Correlation — Covariance, Normalized.")
    
    st.markdown(
        """
        On the last page, we saw that **Covariance** tells us if two variables move together. But there's a fatal flaw: 
        its value depends on the *units* of the data. Measure height in millimeters instead of meters, and the covariance skyrockets, 
        even though the relationship is exactly the same!
        
        **Pearson Correlation (r)** fixes this by squashing the relationship into a perfect, universal scale from **-1.0 to +1.0**.
        """
    )
    
    st.divider()

    st.markdown("### 1) The Correlation Morph")
    st.markdown("Drag the slider to shift the correlation. Watch how the data cloud transforms from pure randomness (0) into perfect mathematical harmony (+1 or -1).")
    
    render_correlation_lab()
    
    st.info(
        "**Visual Intuition:** As you move towards `1.0` or `-1.0`, the 'noise' vanishes. In AI, when features have a correlation of `1.0`, they are completely redundant—the neural network only needs one of them!"
    )
    
    st.divider()
    
    st.markdown("### 2) The Mathematical Squasher")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(
            """
            How does the math squeeze Covariance into a perfect box? It divides by the spread (Standard Deviation, $\\sigma$) of both variables.
            
            **The Formula:**
            $$ r = \\frac{\\text{Covariance}(X, Y)}{\\sigma_X \\sigma_Y} $$
            
            By dividing out the scale, we strip away the units. What is left is the pure, naked truth of how tightly they are bound together.
            
            *Fine print:* use the same convention (divide by $n-1$, or by $n$) in the covariance and in both $\\sigma$'s; the factor then cancels. If either variable is constant ($\\sigma = 0$), $r$ is **undefined** (0 ÷ 0), not zero.
            """
        )
        
    with col2:
        st.markdown(
            """
            **The Scale** (rough rules of thumb; the lab above uses the same bands):
            * **$r = \\pm 1$**: Perfect line. (e.g. Temperature in °C vs Temperature in °F gives $r = 1$)
            * **$0.7 \\le |r| < 1$**: Strong trend. (e.g. Height vs Arm span)
            * **$0.3 \\le |r| < 0.7$**: Moderate trend. (e.g. Height vs Weight)
            * **$0.1 \\le |r| < 0.3$**: Weak trend.
            * **$|r| < 0.1$**: Little or no *linear* relationship.
            * The sign gives the direction: e.g. Outdoor temperature vs Home heating bill is negative.
            """
        )
        
    st.divider()
    
    st.markdown("### 3) The Gotcha: Correlation is not everything")
    st.markdown("It is tempting to think that `r = 0` means two variables are completely independent. But remember its full name: the **Pearson product-moment correlation coefficient**, and that it only measures *linear* association.")
    
    render_nonlinear_gotcha()
    
    st.divider()
    st.markdown(
        """
        <div style="color:#94a3b8; font-size:0.95rem;">
        Page 41 — you just learned how to measure the pure strength of a linear relationship. Up next: what happens when we try to draw the "best" line through these clouds of data? Welcome to Scatter Plots & Lines of Best Fit!
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
