# Complete AI Math Simulations

Interactive Streamlit simulations that teach the mathematics behind AI and machine learning.
About 100 pages, each focused on one idea, with sliders, plots, embedded labs and a short quiz.

| Section | Pages |
| --- | --- |
| Vectors & Matrices | 1–18, 76–78 |
| Functions | 19–22 |
| Probability & Statistics | 23–43, 84–88 |
| Calculus | 44–49, 79–83 |
| Optimization | 50–56, 90–92 |
| Information Theory | 57–60, 89 |
| Eigenvectors & PCA | 61–63 |
| Neural Networks & ML | 64–75, 93–98 |

Lessons added after the original 1–75 sequence (they fill gaps or extend a section):

- **Vectors & Matrices:** 76 Span, Basis & Rank · 77 Projections · 78 SVD
- **Probability & Statistics:** 24 Complement, Union & Intersection · 39 Quantiles, IQR & Outliers ·
  43 Residuals & Least Squares · 84 Joint & Marginal Distributions · 85 Poisson & Exponential ·
  86 Beta Distribution · 87 Maximum Likelihood Estimation · 88 Confidence Intervals & Hypothesis Tests
- **Calculus:** 79 Limits & Continuity · 80 Product & Quotient Rules · 81 Taylor Series ·
  82 Jacobian & Hessian · 83 Automatic Differentiation
- **Optimization:** 55 Convex Functions · 90 Momentum · 91 RMSProp & Adam · 92 Learning-Rate Schedules
- **Information Theory:** 89 Mutual Information
- **Neural Networks & ML:** 66 Stacking Linear Layers Collapses · 72 Train, Validation & Test Splits ·
  93 Weight Initialization · 94 Dropout · 95 Batch Normalization · 96 Convolution · 97 Embeddings · 98 Attention

Each page ends with Previous/Next links that follow the learning path through these
additions (e.g. 18 → 76, 49 → 79, 56 → 90, 60 → 89, 75 → 93).

`app.py` opens on a **Home** page with a curriculum map and groups the sidebar into
these sections. Lessons are discovered automatically from `pages/`: a file named
`NNTitle.py` appears as "NN · Title" in its section, at the URL path `/pNN-title`.
Each section lists explicit page numbers (`SECTIONS` in `app.py`), so later lessons
such as 76–78 are listed after the section's original block; a page whose number is
not in any section appears under "More Lessons".

## Quizzes

Every lesson ends with a "🧠 Check your understanding" quiz that `app.py` renders below
the page (pages do not call it themselves; see `common/quiz.py`). Pick an answer for each
question, press **Check answers** to see ✅/❌ with an explanation per question and your
score, and **Try again** to reset. A quiz counts as passed at 75 % or better; the Home
curriculum map shows passed/total quizzes per section and the sidebar shows the overall
total. Progress lives in the Streamlit session state, so it is per browser session and
resets when the session ends.

To add a quiz for page `NN`, create `quizzes/pNN.json` (two-digit number, UTF-8):

```json
{"page": 24, "questions": [
  {"q": "Markdown question (LaTeX via $...$ allowed)", "options": ["A", "B", "C", "D"], "answer": 1,
   "explain": "Why the correct option is right (and the common trap)."}
]}
```

- 3–4 questions, each with 3–4 unique options; `answer` is the 0-based index of the correct one.
- `page` must equal the number in the file name, and a page with that number must exist.
- Escape backslashes in JSON (`"$\\frac{a}{b}$"`).
- A missing quiz file simply shows no quiz; a malformed one shows a short warning caption
  instead of crashing. `tests/test_quizzes.py` validates every quiz file.

## Setup

Requires Python 3.11+ (Streamlit 1.67 does not support older versions).

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Development

```bash
pip install -r requirements-dev.txt
ruff check .
pytest                  # full suite, including the slow widget fuzz (several minutes)
pytest -m "not slow"    # skip the fuzz for a quick check (about a minute)
pytest -n auto          # run in parallel (pytest-xdist)
```

Ruff and pytest are configured in `pyproject.toml`. The test suite in `tests/`:

- `test_pages_smoke.py`: every page runs without an exception under Streamlit's `AppTest`;
  `app.py` renders the Home page, and every page is registered in its navigation and
  runs when selected.
- `test_pages_fuzz.py` (marked `slow`): each page is re-run with every slider at its
  min/max, every number input at min/max/0, every selectbox/radio option, every button
  clicked and every checkbox/toggle flipped; no combination may raise.
- `test_static.py`: pages compile with no `SyntaxWarning` (invalid escape sequences),
  contain none of the banned patterns listed under *Contributing conventions*, have
  unique, cleanly named page-number prefixes, use `pNN_`-prefixed widget and
  session-state keys matching their own page number, and only reference existing files
  (`load_lab("name")` → `assets/labs/name.html`, `safe_page_link("pages/…")` → a page file).
- `test_quizzes.py`: every page has a `quizzes/pNN.json`, every quiz file matches the
  schema and belongs to an existing page; `app.py` renders a quiz below its page, grades
  it and records progress.
- `test_common.py`: unit tests for the helpers in `common/`.

CI (`.github/workflows/ci.yml`) runs `ruff check .` and the full `pytest -q` suite on
every push and pull request, on Python 3.12 and 3.13.

## Project structure

```
app.py                  # entry point: Home page + st.navigation sections
pages/                  # one file per lesson, prefixed with its page number (e.g. 37Softmax.py)
quizzes/                # one quiz per lesson (pNN.json), rendered below the page by app.py
assets/labs/            # self-contained HTML/JS labs (pNN_name.html), loaded via common.assets.load_lab
common/                 # shared helpers (math, matrix display, navigation, lab loading, quiz engine)
.streamlit/config.toml  # theme (dark) and Streamlit settings
requirements.txt        # runtime dependencies
requirements-dev.txt    # runtime + dev tools (pytest, pytest-xdist, ruff)
pyproject.toml          # ruff and pytest configuration
tests/                  # test suite
```

## Contributing conventions

- **Session state keys** are page-prefixed (`pNN_name`, e.g. `p28_seed`) so pages never collide.
- **LaTeX** goes in raw strings (`r"\frac{a}{b}"`) to avoid invalid escape sequences.
- Use `width="stretch"` instead of the deprecated `use_container_width=True`.
- Embed HTML labs with `st.iframe`, not `streamlit.components.v1.html`. Larger labs live in
  `assets/labs/pNN_name.html` and are loaded with `common.assets.load_lab("pNN_name", **values)`
  (`$placeholder` substitution via `string.Template`; write `$$` for a literal `$`).
- Link to other lessons with `common.nav.safe_page_link("pages/<exact file name>.py", label)`.
- No external fonts, scripts or CDNs unless pinned with Subresource Integrity (SRI).
- Randomness is deterministic: use a seeded generator stored in session state and
  provide an explicit "Resample" button to draw new data.
- Close matplotlib figures after rendering (`st.pyplot(fig)` then `plt.close(fig)`).
