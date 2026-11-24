import streamlit as st
import sys
from pathlib import Path

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="Mean, Median, Mode", layout="wide", page_icon="📊")

st.title("📊 38. Mean, Median, Mode")
st.markdown("### The Three Sisters of Statistics")
st.write("When we have a bunch of numbers, we often want to summarize them with a single value. But 'the center' can mean different things! **Drag the data points on the number line below** and watch how each metric responds live.")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("**Mean (The Balance Point)**\n\nThe mathematical average. Imagine the number line is a seesaw; the mean is where you'd place the fulcrum to balance it perfectly. It's highly sensitive to outliers. *Try dragging the rightmost point (19) out to 30 and watch the mean chase it!*")
   
with col2:
    st.info("**Median (The Middle Child)**\n\nThe exact middle value when you line up all the numbers in order. Half the numbers are bigger, half are smaller. It is robust to extreme outliers. *Drag that same point to 30: the median doesn't move at all.* Use **+ Add point** to get an even count and see the median become the average of the two middle values.")
   
with col3:
    st.info("**Mode (The Popular Vote)**\n\nThe most frequent value in the dataset. It's visually the highest stack of dots. There can be more than one mode (ties are all shown), or no mode at all if every number is unique.")

html_code = load_lab("p38_mean_median_mode")

st.iframe(html_code, height=700)

st.markdown(
    "**Next up:** the center is only half the story — *Quantiles, IQR & Outliers* measure the **spread** "
    "with the same robustness as the median, and give a rule for flagging outliers."
)
safe_page_link("pages/39Quantiles, IQR & Outliers.py", "Next: 39 · Quantiles, IQR & Outliers", icon="➡️")
