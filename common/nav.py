"""Navigation helpers."""

import streamlit as st
from streamlit.errors import StreamlitPageNotFoundError


def safe_page_link(path, label, icon=None):
    """st.page_link that degrades to a caption when the target page is not registered
    (the page was launched on its own instead of via app.py)."""
    try:
        st.page_link(path, label=label, icon=icon)
    except StreamlitPageNotFoundError:
        st.caption(f"{icon} {label}" if icon else label)
