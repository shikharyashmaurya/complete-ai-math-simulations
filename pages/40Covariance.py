import streamlit as st
import sys
from pathlib import Path

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="Covariance", layout="wide", page_icon="📈")

st.title("📈 40. Covariance")
st.markdown("### How Do Two Variables Move Together?")
st.write("Covariance measures the **joint variability** of two variables. It tells us whether they tend to move in the same direction, opposite directions, or have zero linear co-variation. Zero covariance alone does not imply independence.")
st.markdown("#### The Formula")
st.markdown("**Population Covariance:**")
st.latex(r"\text{Cov}(X, Y) = \frac{1}{N} \sum_{i=1}^{N} (x_i - \mu_X)(y_i - \mu_Y)")

st.markdown("**Sample Covariance:**")
st.latex(r"\text{Cov}(X, Y) = \frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})")

st.markdown("#### Visualizing the Formula")
st.markdown("""
- **Green Zones (+):** When $X$ and $Y$ are both above average, or both below average, their product is positive. These points **increase** covariance.
- **Red Zones (-):** When one is above average and the other is below, their product is negative. These points **decrease** covariance.
""")
st.write("**Rotate the point cloud below** to see how changing the shape of the data impacts the balance between these zones, resulting in positive, negative, or zero covariance!")

html_code = load_lab("p40_covariance")

st.iframe(html_code, height=740)

st.caption(
    "The dashboard shows the **sample** covariance (divide by n − 1). The **population** version (divide by n) is shown underneath. "
    "Switch X to centimetres or millimetres: the cloud and r stay exactly the same, but the covariance grows ×100 or ×1000. "
    "Covariance's size depends on units, which is why the next page normalizes it into the correlation r. "
    "The dashed line is the least-squares regression of Y on X. For nearly vertical clouds it is visibly flatter than the cloud's long axis (regression dilution)."
)

prev_col, next_col = st.columns(2)
with prev_col:
    safe_page_link("pages/39Quantiles, IQR & Outliers.py", "Previous: 39 · Quantiles, IQR & Outliers", icon="⬅️")
with next_col:
    safe_page_link("pages/41Pearson Correlation.py", "Next: 41 · Pearson Correlation", icon="➡️")
