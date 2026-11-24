"""Helpers shared by several lesson pages.

Pages import from here as ``from common.<module> import ...``. Each importing page puts the repo
root on ``sys.path`` first, so the imports work via ``streamlit run app.py``, when a page is run
on its own (``streamlit run "pages/<page>.py"``) and under ``AppTest.from_file``.
"""
