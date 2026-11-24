# Review fixes — change log & UI verification guide

Branch: `fix/review-improvements` (based on `456a99a`). This branch implements the **"What needs to improve"** list from the
full line-by-line review of all 70 pages. New content (missing pages 24/39/43/55/66/72, new topics) is **not** part of this branch.

## How to verify

```powershell
pip install -r requirements-dev.txt
streamlit run app.py          # then follow the "UI differences to verify" bullets below
ruff check .                  # lint: must say "All checks passed!"
pytest -n auto                # 375 tests: static checks, smoke run of every page, widget fuzz, unit tests
```

## App-wide changes (visible everywhere)

- **Dark theme** is now fixed via `.streamlit/config.toml` (previously followed your OS setting, and some headers were invisible on one of the two themes).
- **Sidebar navigation** is grouped into 8 sections with clean titles (`37 · Softmax`) plus a new **Home** page with a curriculum map. URLs changed (e.g. `/p37-softmax`); old bookmarks break.
- **Page 64 duplicate removed**: `64A Single Neuron2.py` merged into `64A Single Neuron.py` (new "Case Study: Build a Cat Detector" section).
- **No crashes** when widgets are pushed to extremes (page 10 rows/cols = 1, page 32 returning with old results, etc.).
- Deprecated APIs migrated: `use_container_width` → `width="stretch"`, `components.html` → `st.iframe` (embedded labs may have slightly different heights).
- All widget/session keys are page-prefixed (`pNN_`), so values no longer leak between pages (e.g. page 5's `x2` showing up as Gravity=3.0 on page 67).
- Random data is deterministic by default, with explicit "New / Resample" buttons.
- No Google Fonts / external font requests; broken `file:///d:/…` links replaced by in-app page links.
- LaTeX rendering fixes (invalid escapes / `\t` turning into TAB) on pages 23, 49, 57–61, 74.

## Files changed

Summary: 94 files changed (93 below + this `REVIEW_CHANGES.md`). Line counts: `git diff --stat 456a99a`.

| Change | File |
|---|---|
| Deleted | `.agents/skills/developing-with-streamlit` |
| Deleted | `.claude/skills/developing-with-streamlit` |
| Added | `.github/workflows/ci.yml` |
| Modified | `.gitignore` |
| Added | `.streamlit/config.toml` |
| Added | `README.md` |
| Modified | `app.py` |
| Added | `common/__init__.py` |
| Added | `common/linalg2d.py` |
| Added | `common/mathutils.py` |
| Added | `common/matrix_display.py` |
| Added | `common/nav.py` |
| Modified | `pages/10What is a Matrix.py` |
| Modified | `pages/11Matrix Addition & Scalar Multiplication.py` |
| Modified | `pages/12Matrix × Vector.py` |
| Modified | `pages/13Matrix × Matrix.py` |
| Modified | `pages/14Matrix as a Transformation.py` |
| Modified | `pages/15Transpose.py` |
| Modified | `pages/16Identity Matrix.py` |
| Modified | `pages/17Determinant — Area Scaling.py` |
| Modified | `pages/18Matrix Inverse — Undoing a Transform.py` |
| Modified | `pages/19Functions as Machines.py` |
| Modified | `pages/1From Number to Arrow to List.py` |
| Modified | `pages/20Linear Functions.py` |
| Modified | `pages/21Why Non-linearity.py` |
| Modified | `pages/22Piecewise Functions.py` |
| Modified | `pages/23Sample Space & Basic Probability.py` |
| Modified | `pages/25Conditional Probability.py` |
| Modified | `pages/26Independence.py` |
| Modified | `pages/27Bayes' Theorem.py` |
| Modified | `pages/28Random Variables.py` |
| Modified | `pages/29Expected Value.py` |
| Modified | `pages/2Adding & Subtracting Vectors.py` |
| Modified | `pages/30Variance & Standard Deviation.py` |
| Modified | `pages/31Bernoulli Distribution.py` |
| Modified | `pages/32Binomial Distribution.py` |
| Modified | `pages/33Uniform Distribution.py` |
| Modified | `pages/34Normal (Gaussian) Distribution.py` |
| Modified | `pages/35Z-Scores & Standardization.py` |
| Modified | `pages/36Central Limit Theorem.py` |
| Renamed | `pages/37Softmax .py → pages/37Softmax.py` |
| Modified | `pages/38Mean, Median, Mode.py` |
| Modified | `pages/3Scalar Multiplication.py` |
| Modified | `pages/40Covariance.py` |
| Modified | `pages/41Pearson Correlation.py` |
| Modified | `pages/42Scatter Plot & Line of Best Fit.py` |
| Modified | `pages/44What is a Derivative.py` |
| Modified | `pages/45Derivative Rules (Power & Constant).py` |
| Modified | `pages/46Chain Rule — Derivative Through Layers.py` |
| Modified | `pages/47Partial Derivatives.py` |
| Modified | `pages/48The Gradient — Steepest Climb.py` |
| Modified | `pages/49Integral as Area.py` |
| Modified | `pages/4Magnitude — How Long is the Arrow.py` |
| Modified | `pages/50What is a Loss Function.py` |
| Modified | `pages/51Loss Landscape — Hills and Valleys.py` |
| Modified | `pages/52Gradient Descent.py` |
| Modified | `pages/53Learning Rate.py` |
| Modified | `pages/54Local vs Global Minimum.py` |
| Modified | `pages/56Stochastic Gradient Descent.py` |
| Modified | `pages/57Information & Surprise.py` |
| Modified | `pages/58Entropy — Average Uncertainty.py` |
| Modified | `pages/59Cross-Entropy — Predicted vs Reality.py` |
| Modified | `pages/5Unit Vectors & Normalization.py` |
| Modified | `pages/60KL Divergence — Gap Between Distributions.py` |
| Modified | `pages/61Eigenvectors — Vectors That Don't Rotate.py` |
| Modified | `pages/62Eigenvalues — How Much Do They Stretch.py` |
| Modified | `pages/63PCA Intuition — Finding the Best Angle.py` |
| Modified | `pages/64A Single Neuron.py` |
| Deleted | `pages/64A Single Neuron2.py` |
| Modified | `pages/65Activation Functions Compared.py` |
| Modified | `pages/67Neural Network as Matrix Layers.py` |
| Modified | `pages/68MSE Loss — For Regression.py` |
| Modified | `pages/69Cross-Entropy Loss — For Classification.py` |
| Modified | `pages/6Dot Product — Geometric View.py` |
| Modified | `pages/70Backpropagation — Chain Rule Backward.py` |
| Modified | `pages/71Overfitting Underfitting.py` |
| Modified | `pages/73Bias-Variance Tradeoff.py` |
| Modified | `pages/74L1 & L2 Regularization.py` |
| Modified | `pages/75Learning Curves.py` |
| Modified | `pages/7Dot Product — Algebraic View.py` |
| Modified | `pages/8Cosine Similarity.py` |
| Modified | `pages/9Data as Vectors.py` |
| Deleted | `pages/__pycache__/62Eigenvalues — How Much Do They Stretch.cpython-39.pyc` |
| Deleted | `pages/__pycache__/63PCA Intuition — Finding the Best Angle.cpython-39.pyc` |
| Deleted | `pages/__pycache__/64A Single Neuron.cpython-39.pyc` |
| Added | `pyproject.toml` |
| Added | `requirements-dev.txt` |
| Modified | `requirements.txt` |
| Added | `tests/conftest.py` |
| Added | `tests/test_common.py` |
| Added | `tests/test_pages_fuzz.py` |
| Added | `tests/test_pages_smoke.py` |
| Added | `tests/test_static.py` |

## Detailed changes and UI checks per area

Each section lists, per file: **Fixes** (original issue → fix), **UI differences to verify** (concrete click-paths), and **Not fixed** (with reason).


---

## Project setup (requirements, theme, README, symlinks)


### Files
- **requirements.txt** (modified): compatible-release pins. `streamlit>=1.67,<2` (needed for `st.iframe` and `width="stretch"`), `numpy>=2.0,<3`, `matplotlib>=3.8,<4`, `plotly>=5.0,<8`, `scikit-learn>=1.3,<2` (page 9 uses sklearn PCA), `scipy>=1.11,<2` (pages 28,30,32,34,35,36), `pandas>=2.0,<4` (pages 20,32,37,69,75). **seaborn dropped**: only imported (unused, no `sns.` calls) by page 10. All pins verified against installed versions; `pip install --dry-run -r requirements.txt` resolves.
- **requirements-dev.txt** (new): `-r requirements.txt`, `pytest`, `ruff`.
- **.agents/skills/developing-with-streamlit**, **.claude/skills/developing-with-streamlit** (removed from index via `git rm --cached`; still on disk): symlinks into a developer's `.venv`, broken on other machines.
- **.gitignore** (modified): appended `.agents/` and `.claude/` (`.vscode/` kept).
- **.streamlit/config.toml** (new): `[theme] base="dark"`, `primaryColor="#38bdf8"` to match the dark-styled embedded labs.
- **pyproject.toml** (new): ruff only (`target-version="py310"`, `line-length=200`, select F/E9/W605/B/PLE, ignore B905/B007/E501) + `[tool.pytest.ini_options] testpaths=["tests"]`. Verified ruff picks it up (`ruff check app.py` passes, settings path = pyproject.toml).
- **README.md** (new): description, sections table, setup, dev commands, structure, contributing conventions.

### Dependencies (resolved)
- Page 10's unused `import seaborn as sns` was removed (pages 1–13 work), so dropping seaborn from requirements.txt is safe.
- `tests/` directory does not exist yet; `pytest` will report "no tests ran" until one is added.

### UI differences to verify
- App always renders in dark theme regardless of OS/browser light/dark setting (users can still switch in Settings menu).
- Primary accent (sliders, buttons, active widgets, links) is sky blue `#38bdf8` instead of Streamlit red.
- Matplotlib pages (3,4,7,8,10,14,16,17,18,21) with white figure backgrounds will now sit on a dark page — check contrast/appearance.
- Plotly charts use Streamlit's theme by default and should adopt dark styling automatically.
- Sidebar/navigation unchanged (no new pages or widgets).


---

## Navigation, Home page & rename


### Files changed
- `app.py` — rewritten. `st.set_page_config(page_title="Complete AI Math Simulations", layout="wide")`,
  then lessons are discovered by globbing `pages\*.py` (leading number parsed, sorted numerically) and
  registered with `st.navigation` in 8 sections (+ a "Start" section holding Home; any future page whose
  number falls outside the ranges lands in "More Lessons"). Each page: title `"NN · Title"`, section icon,
  explicit `url_path` `pNN-<ascii-slug>` (e.g. `p37-softmax`). Home is a function page (`default=True`)
  with title, intro, "How to use", and a curriculum map (2 columns of expanders with `st.page_link`s).
- `README.md` — section table renamed "Eigen & PCA" → "Eigenvectors & PCA"; added paragraph on Home
  page / sidebar sections / auto-discovery / URL paths; project-structure comments updated.

### Renamed
- `pages\37Softmax .py` → `pages\37Softmax.py` (`git mv`; uncommitted modifications kept, status `RM`).
  No references to the old filename existed in pages, README, or app.py.

### Removed from git index (files kept on disk)
- `pages/__pycache__/62Eigenvalues — How Much Do They Stretch.cpython-39.pyc`
- `pages/__pycache__/63PCA Intuition — Finding the Best Angle.cpython-39.pyc`
- `pages/__pycache__/64A Single Neuron.cpython-39.pyc`

### Verification
- ruff check app.py: clean; `python -W error::SyntaxWarning -m py_compile app.py`: OK.
- AppTest: home renders (69 page_links, no exceptions); `switch_page` to every one of the 69 pages: 0 exceptions.
- page_links in pages 58/59/60 resolve to real links (no caption fallback).
- `streamlit run app.py` on :8599 — `/`, `/p37-softmax`, `/p58-entropy-average-uncertainty` all HTTP 200.

### UI differences to verify
- Sidebar is now grouped into 8 section headers (plus "Start" → Home) with clean titles such as
  "37 · Softmax" instead of raw filenames ("37Softmax ") in Streamlit's default lexical order.
- Pages are ordered numerically (1, 2, …, 10) instead of the old string sort (1, 10, 11, …, 2).
- New default Home page with intro, how-to-use, and curriculum map (expanders; first two expanded).
- URL paths changed: old auto-generated paths (e.g. `/Softmax_`, `/Matrix_×_Vector`) no longer exist;
  new ones are `/pNN-slug` (e.g. `/p12-matrix-vector`). Old bookmarks will fall back to Home / 404 page.
- Each page still calls its own `st.set_page_config`, so the browser tab title switches to the
  page's own title on lesson pages; Home uses "Complete AI Math Simulations".
- Sidebar entries carry per-section emoji icons.


---

## Shared `common/` helpers


Todo id: `shared-helpers`. Scope: new package `common\`; pages 11–18, 58, 59, 60, 64, 65, 67.
`app.py`, `README.md` and `pages\37Softmax.py` were handled by the navigation work.

### New files

| File | Contents |
|---|---|
| `common\__init__.py` | Docstring only. Explains the import convention and the run modes. |
| `common\matrix_display.py` | `matrix_html(matrix, title, highlight=None, color="#38bdf8", *, precision=2, font_size=18, cell_padding="7px 10px", min_width=42, theme="slate"\|"lab", cell_style="bold"\|"fill"\|"plain", title_color=None, text_color=None, margin_bottom=None)`. This one function covers every page variant. The title goes through `html.escape`. NaN renders as an italic, faded "?". -0.0 renders as 0. Also: `vector_html` (a column vector, highlighted by index), `format_entry`, `row_major_cells(step, rows, cols)` (the step-order helper) and `partial_matrix(full, cells)` (fills unrevealed cells with NaN, which renders as "?"). |
| `common\linalg2d.py` | `rotation_matrix`, `unit_square`, `transform_points` (accepts (n, 2+) points), `det2` |
| `common\mathutils.py` | `sigmoid` (stable with no clipping: `np.where` on the sign of z with `e = exp(-\|z\|)`, so it cannot overflow; returns a NumPy scalar for scalar input), `softmax(z, axis=-1)` (subtracts the max first), `fmt_num`, `fmt_factor` (puts negatives in parentheses), `fmt_signed(x, prec)` → `"- 1.50"` / `"+ 1.50"`, `close_enough` (wraps `np.isclose` with the same defaults and returns a plain bool for scalars) |
| `common\nav.py` | `safe_page_link(path, label, icon=None)`: calls `st.page_link` and falls back to `st.caption(f"{icon} {label}")` on `StreamlitPageNotFoundError`. This is the exact old behaviour. |

#### Import shim (every importing page)
```python
import sys
from pathlib import Path
...
# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from common.... import ...  # noqa: E402
```
The shim is needed. With `streamlit run "pages\X.py"` and with AppTest, Streamlit only adds the page's own folder (`pages\`) to `sys.path`. The `if` guard prevents duplicate entries. Streamlit's own `modified_sys_path` removes its entry by value, so the two do not interfere. Streamlit sets `__file__` to the page path in all three modes, including `st.navigation` (see `streamlit\navigation\page.py`).

### Per-page replacements

| Page | Removed | Now uses |
|---|---|---|
| 11 | `matrix_to_html`, `num`, `paren`, `plus`, `step_coordinates`, two inline `np.full_like(..., nan)` reveal loops, `np.isclose` ×2 | `matrix_to_html = functools.partial(matrix_html, theme="lab", cell_style="fill", precision=1, font_size=20, cell_padding="8px 12px", min_width=46)`, `fmt_num/fmt_factor/fmt_signed(x, 1)`, `row_major_cells`, `partial_matrix`, `close_enough` |
| 12 | `cell_html`, `matrix_html`, `vector_html`, `fmt_factor` | Two 1-line wrappers that call `matrix_display.matrix_html/vector_html` with `CARD_STYLE` (lab/fill, 19px, 8px 12px). They keep the page's two default colours and the 42 vs 72 px widths. Also uses `fmt_factor`. (`row_dot_product_steps` is vector-specific and stays.) |
| 13 | `cell_html`, `matrix_html`, `fmt_factor`, `solve_order`, inline reveal loop | `functools.partial(matrix_html, theme="lab", cell_style="fill", font_size=18, ...)`, `fmt_factor`, `row_major_cells`, `partial_matrix` |
| 14 | `rotation_matrix`, `transform_points`, `unit_square`, `matrix_html` | `common.linalg2d` + `partial(matrix_html, theme="slate", cell_style="plain", cell_padding="7px 14px", min_width=48, title_color="#e2e8f0", text_color="#f8fafc", margin_bottom="12px")` |
| 15, 16 | `matrix_html` | Direct import. slate/bold are the shared defaults, and every call site already passes `precision=0` (checked by grep). |
| 17 | `det2`, `unit_square`, `transform_points`, `matrix_html`, inline "Rotate 25°" rotation | `common.linalg2d` (incl. `rotation_matrix(25.0)`, which is bit-identical) + `partial(matrix_html, theme="slate", cell_style="plain", cell_padding="7px 14px", min_width=48)` |
| 18 | `det2`, `unit_square`, `transform_points`, `matrix_html`, inline "Rotate 40°" rotation | Same as 17 (`rotation_matrix(40.0)`) |
| 58 | Inline `try: st.page_link … except StreamlitPageNotFoundError: st.caption(...)` | `safe_page_link(...)` |
| 59, 60 | Local `nav_link` (2 calls each) | `safe_page_link(...)` |
| 64 | Inline scalar `math.exp` stable logistic in `neuron_forward` | `a = float(sigmoid(z))` (`math` is still used for `tanh`) |
| 65 | `sigmoid` (tanh form) | `from common.mathutils import sigmoid`. `sigmoid_derivative` etc. stay on the page. |
| 67 | `sigmoid` (tanh form), `softmax(z, axis=0)` | Imported. The call site `softmax(Z2)` is now `softmax(Z2, axis=0)`, because the shared default axis is -1. The batched call already passed `axis=0`. |

### Verification evidence

- **Ruff:** `ruff check common pages --no-cache` reports "All checks passed!" The repo's `pyproject.toml` rules (F, E9, W605, B, PLE) apply.
- **Compile:** `python -W error::SyntaxWarning` compile of `common\*.py` and all 14 touched pages succeeds.
- **Old vs new equivalence** (`files\equiv_shared_helpers.py`): the script AST-extracts the old helpers from snapshot copies in `files\shared_helpers_orig\` and the new page-level wrappers from the edited pages, then compares them. All checks passed:
  - **Rendered HTML is byte-identical** for p11 (46,800 inputs), p12 matrix (46,800), p12 vector (2,600), p13 (46,800), p14/p17/p18 (78 each), and p15/p16 (159,250 each). Inputs: shapes 1–5×1–5 (2×2 for 14/17/18); int, float and NaN-partial matrices; highlight sets None / [] / first cell / half / all / row / column; 5 colours; 13 real page titles (incl. `M⁻¹ — the rewind`, `A + B (partial, ? = not solved yet)`); precision 0–3. The only differences are the -0.0 cases described below.
  - `row_major_cells` equals p11 `step_coordinates` and p13 `solve_order` for every (rows, cols, step), including step > rows×cols. `partial_matrix` equals the inline `np.full_like` loop (NaN-aware equality).
  - Over 2,810 values: `fmt_num/fmt_factor/fmt_signed(x, 1)` equal p11 `num/paren/plus`, and `fmt_factor(x, 2)` equals the p12/p13 `fmt_factor`. Also `fmt_signed(-1.5, 2) == "- 1.50"`. `close_enough` equals `np.isclose` on the p11 scalar slider grid.
  - `unit_square`, `transform_points` (3,000 random cases for each of 14/17/18), `det2`, `rotation_matrix` (−180…180) and the 25°/40° presets all match bitwise.
  - **sigmoid** (old tanh form vs new `np.where` form), on 200,036 points with |z| ≤ 1e4 (incl. ±50, ±709, ±745):
    - Max absolute difference is 2.2e-16. Max relative difference is 4e-14 wherever sigmoid > 1e-3.
    - Larger relative differences occur only deep in the left tail. There the old form loses relative precision, e.g. it returns 0.0 at z = −50 while the new form returns 1.9e-22.
    - No overflow/invalid/divide FP errors at ±1e308.
  - **Page 65:** the displayed strings are identical over its real input grids:
    - `f(z)` and `f′(z)` at `.4f` for z ∈ [−6, 6] in steps of 0.01.
    - Backprop `clean_format` / `pct_format` / `.3f` for z1, z2, z3 ∈ [−5, 5] in steps of 0.5 (9,261 combos) × grad ∈ {1, 10, 20}.
    - The saturation and vanished/severe threshold verdicts, and the "chain at 4" `.1e` text.
  - **Page 64:** `float(sigmoid(z))` is bitwise equal to the old `math` form at all 100,007 z values in [−50, 50] (plus ±700, ±1000). The other activations are unchanged.
  - **Page 67:** `softmax` is bitwise equal (axis=0 and 1-D). Across 1,500 random slider-grid networks with sigmoid hidden layers, Y% at `.1f` is identical and the 60×60 decision grid has 0 class mismatches.
- **AppTest, mode (c):**
  - `files\fuzz_shared_helpers.py` (adapted from `fuzz_pages.py`, touched pages only) moves every slider and number_input to its extremes and tries every radio and selectbox option, every button and every checkbox. All 14 pages are ok, with no exceptions.
  - `files\apptest_base_shared_helpers.py` runs as if from the repo root with `AppTest.from_file("pages/X.py")` relative paths. It asserts the repo root is not on `sys.path` first, so the shim is what makes the imports work. It adds base runs plus every select_slider extreme combination (rows/cols etc.) with all sliders at max. ALL OK.
  - 58/59/60 show the caption fallbacks with exactly the old text (e.g. `💡 Revisit Page 57: Information & Surprise`).
- **Mode (b), `streamlit run "pages\X.py"`:**
  - Pages 13, 18, 59 and 65 were each started headless on spare ports 86xx; `curl` of `/` returned 200 and `/_stcore/health` returned ok.
  - `files\ws_probe.py` then drove a real script run over `/_stcore/stream`. Every run finished successfully (`script_finished=0`) with no exception elements, and the matrix cards and nav captions were present.
  - The servers were stopped afterwards.
- **Mode (a), `streamlit run app.py`** (port 8700, using the app.py in its current state with the nav-rename edits):
  - The probe ran the main script and all 14 touched pages via their page hashes. All finished successfully with no exceptions.
  - Pages 58/59/60 rendered real `page_link` elements, which exercises the success path of `safe_page_link`.
  - The server was stopped afterwards.

### UI differences to verify

There is one deliberate cosmetic difference: an exact `-0.0` matrix entry now shows as `0.00` instead of `-0.00`, on pages 14–18. Pages 11–13 already did this. Where it is visible:
- **Page 18:** in "Matrices side by side", the **M⁻¹ — the rewind** card for the *Identity (nothing to undo)* preset used to show `-0.00` in both off-diagonal cells, because −b/det = −0.0. It now shows `0.00`. The same applies to any slider setting with b = 0 or c = 0.
- **Pages 14/17:** only if an entry is exactly −0.0, which the sliders and presets don't normally produce.
- **Pages 15/16:** the integer matrices never contain −0.0 (`I @ A` sums to +0.0), so nothing visible changes.

Tiny negatives such as −1e-17 still print as `-0.00`, as before. No other visible change: all other HTML strings are byte-identical, and the numeric output differences are below display precision. Pages 64/65/67 render the same digits and the same verdicts.

### Duplication intentionally left

- **Large inline CSS/JS/HTML in the iframe labs** (58/59/60 `st.iframe` documents, 64 JS neuron lab incl. its JS `sigmoid`, the 65/67 `<style>` blocks and SVG builders, 67 `html_vector_2d/html_matrix_3x2/...`). They are JavaScript or page-specific markup in a different language and style system. Sharing them would require a templating layer, which is out of scope and riskier than the gain.
- **Page 67 `render_html` and the 3×2/2×3 HTML helpers**: their glassmorphic styling differs from the matrix pages' cards, and they would need different knobs.
- **Page 65 derivative/activation helpers** (`sigmoid_derivative`, `tanh_derivative`, `relu*`, `leaky_relu*`): they are only used on page 65.
- **Page 12 `row_dot_product_steps`**: reveals rows of a vector rather than cells of a matrix, and is used once.
- **Pages 17/18 `preset_matrix` / wild-card generators and `style_axes`/matplotlib scene code**: these are page-specific content, not shared logic.
- **The 5-line `sys.path` shim on each importing page**: it is bootstrap code that has to run before `common` can be imported, so it cannot itself live in `common`.


---

## Tests & CI


### Files
Added:
- `tests/conftest.py` – page discovery (pathlib, sorted by numeric prefix), `pytest_generate_tests` parametrizes any `page_path` test with file-stem ids; fixtures `repo_root`, `app_file`, `all_pages`.
- `tests/test_pages_smoke.py` – every page runs under `AppTest.from_file(..., default_timeout=60)` with no exception (messages + stack traces in failure); `app.py` Home renders; every page reachable via `at.switch_page("pages/<file>")` from app.py (switch_page raises ValueError for unregistered pages; also asserts Home title not shown).
- `tests/test_pages_fuzz.py` – port of `fuzz_pages.py` as one `@pytest.mark.slow` test per page (sliders min/max, number_input min/max/0, all selectbox/radio options, button clicks, checkbox/toggle flips; page exceptions and harness errors both fail).
- `tests/test_common.py` – mathutils (sigmoid ±1000 no overflow/warnings, symmetry; softmax sums to 1 on both axes, shift invariance ±1000; fmt_signed incl. -0.0 and precision; close_enough scalar bool / array), matrix_display (title HTML-escaped; NaN cells via partial_matrix/row_major_cells render "?" with MISSING_CSS), linalg2d.det2.
- `tests/test_static.py` – SyntaxWarning-as-error compile of app.py + every page; banned patterns (`use_container_width`, `components.html(`, `fonts.googleapis`, `file:///`, `np.random.seed(`) in app.py + pages; no stray whitespace in stems; number prefix present; unique page numbers; ast check that every literal `key=` value AND session_state literal key (`ss["k"]`, `.get/.setdefault/.pop("k")`, `"k" in ss`; f-strings by leading literal) starts with the page's own `pNN_` prefix (stricter than `p\d{2}_`).
- `.github/workflows/ci.yml` – push/pull_request, ubuntu-latest, Python 3.12 & 3.13 (Streamlit 1.67 Requires-Python >=3.11), setup-python pip cache, `pip install -r requirements-dev.txt`, `ruff check .`, `pytest -q`.

Changed:
- `pyproject.toml` – `[tool.pytest.ini_options]` only: `pythonpath = ["."]`, registered `slow` marker.
- `README.md` – Development section (smoke/fuzz/slow marker/static/common tests, CI); Setup now says Python 3.11+ (Streamlit 1.67 requires >=3.11; previously said 3.10+).

### How to run
```
pip install -r requirements-dev.txt
ruff check .
pytest -q                  # everything incl. fuzz
pytest -q -m "not slow"    # skip fuzz
pytest -q -n auto          # if pytest-xdist installed (not a dev requirement)
```

### Results (local, Windows, Python 3.15.2, streamlit 1.67.0)
- `ruff check .` → All checks passed!
- `python -m pytest -q -n auto` (16 workers) → **375 passed in 206.33s** (69 fuzz + 306 others). Slowest fuzz: page 10 (85s), 18 (79s), 17 (63s).
- `python -m pytest -q -m "not slow"` (serial) → 306 passed, 69 deselected in 66.92s.
- Serial full run (as in CI) estimated ~15–25 min (sum of fuzz durations).

### Allowlisted keys
None – all literal widget/session_state keys already use their own page's `pNN_` prefix; `KEY_PREFIX_ALLOWLIST` is empty. Non-literal keys (e.g. page 67 `W1_KEYS[...]`) are not checked.

### UI differences
None – no page or app code changed.


---

## Pages 01–13


Verification run: ruff (`F,E9,W605,B,PLE`, ignore B905) clean; `python -W error::SyntaxWarning` compile clean;
AppTest fuzz (all sliders min/max, radios, selectboxes, buttons) on all 13 pages → no exceptions; plus targeted
AppTest checks listed per page. All widget/session keys now use a `pNN_` prefix. No `use_container_width` left.
No `np.random.seed`/global RNG use left (all seeded `default_rng` + explicit "New …" buttons).

---

### 1From Number to Arrow to List.py
**Fixes**
- Smiley image got fresh random noise on every rerun (numbers changed while dragging the unroll slider) → noise now from `default_rng(28)`, identical every rerun.
- `st.code(f"v = {list(n_dim_vector)}")` printed `np.int64(12)` on numpy 2 → uses `.tolist()`.
- "Generate Random 15-Dim Vector" result vanished on the next rerun → stored in `st.session_state.p01_n_dim_vector`; seeded draws; added "Reset to Example Vector" button.
- Unused `reshaped_for_viewing` removed.
- Text: 1D vector "has a direction" ignored the zero vector; scalar text said "magnitude… It's a point" → reworded (scalar = how much + sign, drawn as a dot; non-zero 1D vector has direction; `[0]` has none). Zero value now draws no stray arrowhead and the label reads "Zero vector [0] (no direction)". Same for the 2D zero vector.
- Unroll slider (10..784 step 10) could not reach 784 → 28..784 step 28 (one image row per step) + caption "first N of 28 rows"; "..." suffix dropped when all 784 are shown.
- `use_container_width` → `width="stretch"/"content"`; slider keys prefixed `p01_`.

**UI differences to verify**
- Page 1 load: Step 4 code box shows `v = [12, -4, 33, ...]` (plain ints, no `np.int64`).
- Click "🎲 Generate Random 15-Dim Vector", then move "Pick a number" → the random vector stays. "↩️ Reset to Example Vector" restores the original.
- Set "Pick a number" = 0 → no arrow, cyan label "Zero vector [0] (no direction)".
- Step 2: X=0, Y=0 → a cyan dot labelled "zero vector" instead of an arrow.
- Step 5: drag the unroll slider → the smiley pixels and listed numbers no longer change; slider reaches 784 and shows "# all 784 values".

**Not fixed**: none.

### 2Adding & Subtracting Vectors.py
**Fixes**
- Resultant shown only when `time_step == 1.0` → tolerance compare.
- Zero resultant (e.g. A − B with A = B) drew a stray arrowhead → shows a green circle "Resultant = zero vector".
- Pedagogy: added the second picture of subtraction (faint green arrow from tip of B to tip of A, labelled "A - B (tip of B → tip of A)") and mentioned it in the tip text.
- Ignored `width=700` removed; `use_container_width` → `width="stretch"`; keys `ax/ay/bx/by` → `p02_*` (+ radio/slider keys).

**UI differences to verify**
- Choose Subtraction, scrub the timeline to 1.0 → green resultant plus the faint "A - B (tip of B → tip of A)" arrow.
- Subtraction with B = A (e.g. A=(3,4), B=(3,4)), timeline 1.0 → circle labelled "Resultant = zero vector", no arrowhead.

**Not fixed**: the figure keeps its white plot background (self-contained, readable in dark theme).

### 3Scalar Multiplication.py
**Fixes**
- Wrong text: intro said the arrow stays on the same line "unless the number is negative"; the explanation said scaling doesn't change "basic direction" → both rewritten (always same line; negative k reverses direction; k=0 → zero vector). Bullet list adds k = 1 and the shrink/stretch cases for negative k.
- Axes fixed at ±6 while k·v reaches ±12 → limits grow with the vectors.
- Figure never closed → `plt.close(fig)`.
- k = 1 hid the blue arrow → k·v drawn wider underneath, v thinner on top; k = 0 shows an orange dot "k·v = 0 (zero vector)".
- Keys `p03_*`.

**UI differences to verify**
- k = 3, x = 4, y = 4 → the orange arrow fits inside the plot (axes extend to about ±14).
- k = 1 → blue arrow visible inside the orange one; k = 0 → orange dot at origin with its legend entry.

**Not fixed**: none.

### 4Magnitude — How Long is the Arrow.py
**Fixes**
- Unused `from mpl_toolkits.mplot3d import Axes3D` removed.
- Negative squares rendered as `-3.00^2` (reads as −9) → helper `sq()` renders `(-3.00)^2` in the 2D, 3D and N-D formulas.
- "New Random Vector" button was not rendered on first load (`'rand_vec' not in st.session_state or st.button(...)` short-circuit) → button always rendered; vector drawn from seeded `default_rng(draw_no)` and kept in `p04_rand_vec`.
- Duplicate 3D dashed segment removed; x/y text labels formatted `.1f`; vector shown with `.tolist()`.
- Wording: "length … can mean … the confidence of a prediction" replaced with "how large a model's weights have grown".
- Keys `x2,y2,x3,y3,z3` → `p04_*` (this collided with pages 5/65/67: page 67's `x2` slider showed page 5's value). Text input, number input and buttons keyed too.

**UI differences to verify**
- First load: the Fun Challenge shows both "New Random Vector" and "Check My Guess".
- x component = −3 → formula shows `\sqrt{(-3.00)^2 + 4.00^2}`.
- Section 3: enter `-3, 4, 0` → `(-3.00)^2 + 4.00^2 + 0.00^2 = 5.00`.
- Visit page 4, move sliders, then open page 5 or page 67 → their sliders keep their own defaults.

**Not fixed**: none.

### 5Unit Vectors & Normalization.py
**Fixes**
- Unused `import math` removed.
- Negative squares `-0.60^2` → `(-0.60)^2` (Step 1, Step 3, 3D and N-D formulas).
- N-D: the 1e-9 threshold called `1e-10, 0` a "zero vector", and `1e-200` underflowed to length 0 → only the exact zero vector is rejected; norm computed after rescaling by the max entry; very small/large values formatted with `.3g`.
- "Already 1.00" band (0.95–1.05) said e.g. 0.99 was exactly 1 → `np.isclose(mag, 1, atol=5e-3)`, otherwise shrink/stretch.
- Challenge: unseeded `np.random`; a length of exactly 1 counted as "stretch"; challenge vectors were almost always > 1 → seeded draws; 40% of draws are short vectors; length ≈ 1 gets a "Trick question" message; zero vector impossible.
- LayerNorm claim was misleading (LayerNorm standardises, it is not L2 normalisation) → reworded.
- Keys `x2 … step3` → `p05_*`; session `rand_norm_vec` → `p05_rand_norm_vec`.

**UI differences to verify**
- x = −0.6, y = 0.8 → Step 1 shows `(-0.60)^2 + 0.80^2`; message "Length is already 1.00 … unit vector".
- Section 3: `1e-10, 0` → unit vector `[1.0, 0.0]` (no warning); `0, 0` → zero-vector warning.
- Fun Challenge: press "New Random Vector" a few times → some short vectors (e.g. `[0.26, -0.3]`) where "Stretch" is correct.

**Not fixed**: the 2D/3D sliders keep the 1e-9 zero check (0.1-step sliders, so only exact 0 hits it).

### 6Dot Product — Geometric View.py
**Fixes**
- Agreement meter used the exact sign of the dot product: the "Sideways strangers" preset (dot = 1.8e-15) showed green "same direction energy" → meter colour/label and the success/error/warning message share `SIDEWAYS_TOL = 0.01` on cos θ. Meter title now says "cos(θ)".
- Presets silently overrode the sliders → the preset radio is replaced by preset buttons (+ "Reset to start") that write into the slider keys via `on_click`, so the sliders always show what is drawn.
- The "right-angle" ticks lay on the dotted line itself → a real right-angle square at the foot of the perpendicular (uses the formerly unused `rejection_vector`, size scales with the axes).
- Placeholder-less f-strings with a single-space line break (lines merged) → plain strings with a proper `"  \n"` break.
- Shadow length can be negative → labelled "signed shadow length" with a help tooltip; no-op `round()` removed.
- `use_container_width` → `width="stretch"`; keys `p06_*`.

**UI differences to verify**
- Sidebar: the "Quick presets" radio is now a set of buttons. Click "Sideways strangers" → Angle of A slider jumps to 90, Angle of B to 0; the meter is amber "perfect sideways" and the message says "Near zero dot product".
- After a preset, drag any slider → the picture follows the slider (no stuck preset). "Reset to start" → 6.0 / 35° / 5.0 / 0°.
- A small right-angle square marks where the dotted "missed sideways part" meets B.
- "Shadow story" tab: each of the three columns shows the bold heading and the sentence on separate lines.

**Not fixed**: the zero-norm guards in `build_vector_figure` stay as defensive code (sliders start at 0.5).

### 7Dot Product — Algebraic View.py
**Fixes**
- False statement "zero dot product … do not agree in any coordinate direction" → explains cancellation with the (1,1)·(1,−1) example; quick rules say "for non-zero vectors" and add the zero-vector case.
- Figure never closed → `plt.close(fig)`.
- Negative factors printed `2 × -3` and `= 2 + -6` → `2 × (-3)` and `= 2 - 6`.
- Projection was "b onto a" while page 6 projects A onto B → now projects a onto b; label and explanation updated.
- Slider keys `p07_*`.

**UI differences to verify**
- Set b₁ = −3 → steps read `2 × (-3) + 1 × 2` and `= -6 + 2`.
- Set a₂ = −2 (a = (2, −2), b = (1, 2)) → `= 2 - 4`.
- Plot legend reads "projection (shadow) of a onto b", with the dashed line from the shadow to a's tip.
- "What the numbers mean" mentions (1, 1) · (1, -1) = 0.

**Not fixed**: none.

### 8Cosine Similarity.py
**Fixes**
- No `set_page_config` → added (wide layout).
- Only unit vectors and no division, so it never showed that cosine ignores length → added "Length of Vector 1/2" sliders (0.5–3; no zero vector possible), full formula `dot / (|v1||v2|)`, and two metrics (dot product changes with length, cosine does not). The formula with the current numbers is shown below the plot.
- Plot limits follow the lengths; angle arc radius 0.4; figure placed in a half-width column so the wide layout doesn't blow it up.
- Keys `p08_*`.

**UI differences to verify**
- Angle 60°, change "Length of Vector 1" from 1 to 3 → "Dot product" goes 0.500 → 1.500 while "Cosine similarity" stays 0.500.
- The plot rescales so both arrows stay visible.

**Not fixed**: the page is still short (kept the original single-concept design).

### 9Data as Vectors.py
**Fixes**
- `np.random.seed(42)` reseeded the process-wide RNG (affected all sessions/pages) → local `default_rng(42)` inside a cached builder.
- Pure random data plus the claim "similar items cluster together" was false, and per-dataset PCA with min-max scaling put three unrelated spaces on shared PC axes → synthetic but structured data (action vs romance raters; word topic prototypes: animals/actions/feelings/royalty/fruit; vertical vs horizontal bar images). One PCA per dataset, chosen with a radio, coloured by group, no min-max squashing, explained-variance caption. An info box explains why datasets aren't mixed.
- No `set_page_config`; no caching → both added (`st.cache_data`).
- Text updated (synthetic-data disclaimer; concrete cluster examples).

**UI differences to verify**
- The page now has a radio "Pick a dataset to explore". Movies: red action vs blue romance points are clearly separated (caption "PC1 96%").
- Words: "king" next to "queen", "cat" next to "dog", etc. Images: vertical-bar vs horizontal-bar groups separated.

**Not fixed**: the data is still synthetic (no real dataset download, by design); this is stated on the page.

### 10What is a Matrix.py
**Fixes**
- **Crash:** Rows = 1 or Columns = 1 made the "Select Row/Column" slider min == max (`StreamlitInvalidMinMaxError`) → the slider is replaced by a caption "Only one row, so i = 1" when there is a single row/column.
- The random matrix changed on every widget move (selected element changed while selecting) → seeded by `[seed, rows, cols]`, with a "🎲 New random numbers" button. The 4×4 image uses its own seed and a "🎲 New random image" button.
- Concept boxes: bullet lists directly after `<div>` rendered as run-on text → blank line after the opening `<div>` (Parts 2 and 3, Key Takeaways). Added CSS so text inside the light box is always dark (readable in dark theme). Section title colour `#A23B72` (low contrast on dark) → `#D63384`.
- Inventory figure: row labels were one squashed text block and the column labels were centred on column 1 → one label per row/column, title centred, tighter limits.
- Chessboard `RdGy` had two dark colours → classic light/dark board colours, with a1 dark.
- Column-vector figure (2×6) was stretched very tall → 2.6×5 at `width="content"`, centred so the title isn't clipped.
- `A ∈ ℝ^(3×3)` with a literal caret → LaTeX `$A \in \mathbb{R}^{3 \times 3}$`.
- Unused `matplotlib.patches as patches`, `seaborn as sns`, `im`, `text` removed. Typos: "a 8×8" → "an 8×8"; "Alaska" (a state) → "Anchorage"; fun fact now mentions 3 colour channels (6,220,800 numbers).
- `use_container_width` → `width`; keys `rows/cols/sel_row/sel_col` → `p10_*`, plus the colour selectbox key.

**UI differences to verify**
- Part 2: set Rows = 1 → no crash; Part 3 shows "Only one row, so i = 1" and the single-row matrix with A[1,j] highlighted. Same with Columns = 1, and with 1×1.
- Change "Color Theme" or move "Select Row" → matrix numbers stay the same; "🎲 New random numbers" changes them.
- Parts 2/3 and Key Takeaways boxes show real bullet lists and dark text on the light-blue box in the dark theme.
- Part 1 inventory: "Store A/B/C" aligned with rows; "Red/Blue/Green" under the columns.
- Game Board tab: beige/brown chessboard. Column-vector figure is compact.
- Notation line renders as ℝ with superscript 3×3.

**Not fixed**: the Section 2/3 figures keep their matplotlib white backgrounds (self-contained images).

### 11Matrix Addition & Scalar Multiplication.py
**Fixes**
- Unrevealed result cells displayed as `0.0` (indistinguishable from real zeros) → shown as an italic, faded `?`; titles say "? = not solved yet".
- Meaning text: "flips sign + stretches" for −1 < k < 0 and "stretches/shrinks" for k = 0 → exact cases (squashes to 0 / unchanged / flips same size / shrinks / stretches / flips + shrink or stretch).
- `-0.0` shown for negative k × 0 → normalised to 0.0; success messages use `3.0 - 3.0` instead of `3.0 + -3.0` and `×` with parenthesised negatives.
- Unseeded random matrices, generic `A_matrix/B_matrix/shape` session keys, redundant double init → seeded `default_rng([seed, rows, cols, i])` with `p11_seed`; keys `p11_*` for all widgets and state.
- Highlighted cells now use dark text (readable on bright fills in the dark theme); box background is theme-neutral.

**UI differences to verify**
- Load: the "A + B (partial…)" grid shows `?` in unsolved cells; dragging the step slider replaces `?` one by one.
- k = 0 → "squashes every cell to 0"; k = −0.5 → "flips sign + shrinks"; k = −1 → "flips every sign (same sizes)".
- Highlighted cells are readable in the dark theme.
- "Generate new random matrices" changes the numbers; reloading or moving other sliders does not.

**Not fixed**: none.

### 12Matrix × Vector.py
**Fixes**
- Success text `(1.00*2.00) + (3.00*4.00)` lost its `*` to Markdown italics → `(1.00 × 2.00) + (3.00 × (-4.00))`; code rule uses `×`.
- Unsolved output entries displayed as 0.00 → `?`.
- Shape story always said "match!" and never showed a mismatch → added the expander "🚫 What if x had n+1 entries…" showing NumPy's real error and an explanation. Unused `x` parameter and duplicate `y` computation removed; `-0.00` normalised.
- Unseeded random A/x and `mxv_*` keys → seeded, `p12_*` keys (sliders, button, state). Highlight text colour fixed for the dark theme.

**UI differences to verify**
- Success box shows `×` between factors (no italics), with negatives in parentheses.
- The output vector shows `?` for rows not yet revealed.
- Section 2: open "🚫 What if x had 4 entries instead of 3?" → red "NumPy refuses: matmul: … mismatch …" message.

**Not fixed**: none.

### 13Matrix × Matrix.py
**Fixes**
- The shape gate could never fail (B always built with n rows) → new sidebar control "Rows of B (must equal Cols of A — try a mismatch!)". On a mismatch, an explained "Access denied" message plus A and B side by side (a row of A vs a column of B highlighted), and the rest of the page stops as designed.
- Success text `*` swallowed as italics → `×` with parenthesised negatives; cell explorer terms use `×`.
- Unsolved C cells displayed as 0.00 → `?`.
- At step 0, row 1 / column 1 were spotlighted although nothing was solved → no spotlight at step 0.
- Unseeded matrices and `mxm_*` keys → seeded, `p13_*` keys for all widgets/state; `-0.00` normalised; highlight text colour for the dark theme.

**UI differences to verify**
- Sidebar: set "Rows of B" = 4 while "Cols of A" = 3 → red "Access denied…" explanation plus both matrices shown; Section 2/3 hidden. Set Cols of A = 4 → "Access granted" and everything returns.
- Factory slider at 0 → no green row / purple column highlights; C shows only `?`.
- Success box: `(3.00 × (-4.00)) + …`.

**Not fixed (at this step)**: the HTML table helpers were still duplicated across pages 11–13. Later resolved by the shared `common/` module (see "Shared `common/` helpers").

---

### Cross-cutting notes
- Shared-key collision (`x2`, `z3` with pages 65/67): fixed on both sides — pages 65/67 now use `p65_`/`p67_` keys too.
- No `components.html` / JS or Google Fonts / `file:///` links existed in these 13 pages.


---

## Pages 14–21


Verification (all pass): ruff `F,E9,W605,B,PLE` clean; `python -W error::SyntaxWarning` compile OK; AppTest fuzz (sliders min/max, every radio/select option, buttons, toggles) → 0 exceptions on all 8 pages; targeted AppTest checks listed per file; no "default value + Session State API" warnings logged. JS in p19/p20 re-read; brackets/parens/backticks balanced. Line endings kept CRLF (working-tree convention).

App-wide conventions applied to every file: `use_container_width` → `width="stretch"/"content"`; `components.html` → `st.iframe`; all session_state / widget keys prefixed `p14_`…`p21_` (old `d14_/d17_/d18_/d19_/df_/transpose_` keys renamed); all figures still closed after `st.pyplot`.

---

### 14Matrix as a Transformation.py
**Fixes**
- "Shear Only" matrix `[[1, shx], [shy, 1]]` was not a shear (det = 1 − shx·shy, could collapse/flip) → now a genuine product of two shears `[[1,shx],[0,1]] @ [[1,0],[shy,1]]` (det always 1).
- Composition `M = h @ r @ s` order was never explained → added `st.latex(M = H R S)` + caption "right-to-left: scaled first, then rotated, then sheared"; recap bullet added.
- Switching "Build matrix from" mode reset the preset radio + hand-tuned entries (and geometric sliders) → all widgets keyed (`p14_*`) and a `keep_widget_state()` re-assignment preserves them across mode switches.
- "Space-Time Grid Warp" (no time involved) → "Grid Warp".
- Recap "det(M) tells you the area scaling factor" → "|det(M)| … negative sign = flip".
- Rotation 45° preset now reuses `rotation_matrix` (duplicate code removed).

**UI differences to verify**
- Geometric mode → "Shear Only" → Shear X = 2.0, Shear Y = 0.5 → det card shows 1.000 (previously 0 / collapsed). Caption about right-to-left order appears under the controls.
- Direct Entries → pick "Shear X" → drag c to 0.5 → switch to Geometric → switch back: preset still "Shear X" and c still 0.5. Geometric sliders also keep their values.
- Plot title reads "Grid Warp".

**Not fixed**
- Off-step preset entries (cos 45° = 0.7071 on a 0.01 slider) — they display fine and snap only if dragged; rounding would distort the rotation.
- `matrix_html` / `unit_square` / `transform_points` duplication across p12–p18: later resolved by the shared `common/` module (see "Shared `common/` helpers").

### 15Transpose.py
**Fixes**
- Unseeded `np.random.randint` → `np.random.default_rng(seed)`; seed in `p15_seed` (deterministic; "Generate new matrix" increments it; shape change regenerates deterministically).
- Tautological checks (`if np.allclose(row_vals, col_vals)` and the impossible "Something is off" `st.error`) removed → plain explanatory `st.success` messages.
- Inconsistent precision ("3.0" vs "3") → row/column panels use `precision=0`; code panel prints ints.
- Highlighted cells (bright green/purple background) now use dark bold text (readable on dark theme).
- Sidebar claimed "transpose twice gives original" but never showed it → new section "4) Flip Twice = Back Home" showing A, Aᵀ, (Aᵀ)ᵀ.
- Index number_inputs keyed per shape (`p15_i_<rows>`, `p15_j_<cols>`) so a shrinking shape can't leave an out-of-range value.

**UI differences to verify**
- Reload the page twice → same matrix A both times; click "Generate new matrix" → A changes.
- Section 2 highlighted cells: dark text on green/purple; values without ".0".
- New section 4 with three matrices at the bottom.

**Not fixed**: none.

### 16Identity Matrix.py
**Fixes**
- Recap/sidebar claimed `AI = IA = A` but only `I·v` was shown → new section "3) Identity Is the Number 1 for Matrices" with a seeded random A (button "New random A"), `I @ A`, `A @ I` and a check.
- Vector lab ignored components beyond 3 (n = 4–6 had no controls) → one slider per component (`p16_v1..v6`); caption explains the plot shows only the first 2 components.
- Radar "Scoreboard" was hard-coded `[1,1,1,1,1]` → scores computed live from `v` vs `I @ v` (position, direction, length, angle, components).
- LaTeX `1*v1` → `1\cdot v_{1}`.
- Dead `else` branch ("Increase matrix size…", n is always ≥ 2) removed.
- Highlighted cells use dark bold text (dark theme readability).
- Sections renumbered 1–5.

**UI differences to verify**
- Sidebar dimension = 6 → six v-sliders appear; code panel shows 6 entries; caption under plot.
- Section 3: three matrices; "New random A" changes A; green success line.
- Section 4 LaTeX shows `1·v₁ + 0·v₂ …`.
- Section 5 radar still full; success "100% unchanged".

**Not fixed**: none.

### 17Determinant — Area Scaling.py
**Fixes**
- Axes `set_xlim(-0.15, lim)` clipped every parallelogram with negative coordinates (Mirror world, Rotate 25°, negative sliders) → symmetric limits.
- "Near-singular" preset was exactly singular (0.95² = 0.9025 → det 0) → `[[1, 0.95], [0.95, 0.91]]`, det = 0.0075.
- Story metric "Pure stretch/shear" for any det > 0 (also rotations) → "Orientation kept"; new "Almost flat" state for |det| < 0.05.
- "Wild card" always returned the same seeded matrix → seed in `p17_wild_seed` + "🎲 New wild card" button; values rounded to the 0.01 slider step.
- Playground (rendered first) was titled "4)" → unnumbered "Playground"; Micro-challenge renumbered "4)"; sidebar text updated.
- Unused slider return values → M built from them directly.
- Recap: det = 0 may collapse to a point as well; added near-singular bullet.

**UI differences to verify**
- Preset "Mirror world (flip)" → the whole orange parallelogram, including the part below the x-axis, is visible; "Rotate 25°" → left part visible; story = "Orientation kept".
- Preset "Near-singular" → det 0.0075, story "Almost flat" (not "Collapsed!").
- Preset "Wild card" → button "🎲 New wild card" appears; clicking it changes the sliders.

**Not fixed**: Rotate 25° entries are off the 0.01 step (see p14 note).

### 18Matrix Inverse — Undoing a Transform.py
**Fixes**
- Singular message "(essentially) zero" conflated numerics with math → names the `SINGULAR_TOL = 1e-8` tolerance explicitly.
- No warning for ill-conditioned but invertible matrices → "Fragile undo" warning when |det| < 0.05 (shows largest M⁻¹ entry and condition number).
- "Wild card" fixed seed → `p18_wild_seed` + "🎲 New wild card" button; rounded to slider step.
- Arrow centroids biased by the duplicated closing vertex → `centroid()` ignores it.
- Metric label "‖M·M⁻¹ − I‖∞" (wrong norm name) → "max |M·M⁻¹ − I| (entrywise)".
- Unused `inv_pack`, `a, b, c, dd`, `err` removed; sliders' return values used to build M.

**UI differences to verify**
- Set a=1, b=0.99, c=1, d=1 → yellow "Fragile undo" warning with large M⁻¹ entries.
- Set b=1 → red "No inverse today… |det| < 1e-08…" + collapsed plot.
- Preset "Wild card" → "🎲 New wild card" button re-rolls the sliders.

**Not fixed**: Rotate 40° off-step entries (see p14 note).

### 19Functions as Machines.py
**Fixes**
- `components.html` (removal date passed) → `st.iframe`; components import removed.
- DIY labels "0.80x + -1.50" and "Mega-Machine … + (-3.5)" → `fmt_affine()` gives "0.80x - 1.50".
- `ys_f` computed but never shown → dashed orange f(x) trace added beside g(f(x)) + caption + horizontal legend.
- Garbled tagline "Nonlinear first acts —" → "The first machine bends the input (x²) — …".
- Machine names HTML-escaped before injection into the iframe (defensive).
- Keys `d19_*` → `p19_*`; preset radio keyed.

**UI differences to verify**
- Assembly-line tab: conveyor animation still plays; graph shows dashed orange f(x) + yellow g(f(x)) with legend.
- DIY tab: set b = -1.0, d = -1.5 → machine label "0.80x - 1.00"/"2.00z - 1.50"; green box "g(f(x)) = 1.60·x - 3.50".

**Not fixed**: none.

### 20Linear Functions.py
**Fixes**
- `tubeMat`/`glowMat` were never attached (`new THREE.Mesh()` defaults to opaque white) → line rendered as a thick white tube hiding the intercept sphere → meshes now use the blue tube + translucent glow materials.
- Endless 60 fps `requestAnimationFrame` loop + never-removed resize listener → render-on-demand loop: wakes on slider input / orbit drag / pointer move / resize, idles after 6 s, pauses on `visibilitychange`, and on `pagehide` stops, removes listeners and disposes controls/renderer.
- No fallback if the CDN (SRI kept) or WebGL fails (loader text stuck forever) → visible amber fallback message pointing to the table.
- GridHelper lay in the XZ floor while the line lives in XY → grid rotated into the XY plane (graph paper behind the line).
- Title says "Linear" but `y = wx + b` is affine → added "Linear vs affine" paragraph in the intro.
- Neuron cartoon "+  [+ b]" double plus → "→".
- Table float noise (0.8999999) → rounded to 2 dp; note that table sliders are separate from the 3D sliders.
- `components.html` ×2 → `st.iframe`; `st.dataframe(use_container_width)` → `width="stretch"`; keys `df_*` → `p20_*`; "60FPS" claim removed.

**UI differences to verify**
- 3D scene: line is light blue with a soft glow; pink intercept ball visible at (0, b); grid now stands behind the line (XY plane) instead of a floor.
- Leave the scene untouched ~6 s → probe glow stops pulsing (loop idle); move mouse/drag/slider → it resumes.
- Block unpkg.com (DevTools → Network → block request URL) and reload → amber message "Could not load the 3D engine…".
- Neuron cartoon shows `x → [× w] → [+ b] → y`.

**Not fixed**
- Three.js stays on the unpkg CDN (per convention, SRI hashes verified to match).
- `pandas` import kept (now declared in requirements.txt).
- 3D sliders and table sliders remain independent (now labelled).

### 21Why Non-linearity.py
**Fixes**
- Wrong math: "the best single line still leaves **2** wrong" on XOR → **1** (cut off one corner); micro-proof extended with "at least 1, and 1 is achievable".
- Grid search was a half-degree/continuous-bias search whose result was then truncated (`int(rad2deg)`) and rounded off the slider step, so the reported best could disagree with the metric (seeds 7, 42) and on XOR it picked a degenerate line through two points → `best_line_bruteforce` now searches exactly the slider grid (integer degrees × 0.05 bias), vectorised per angle, tie-break by largest margin; result reproduced exactly by the sliders.
- Stale ring "best line" message after changing the seed → stored with its seed and dropped when the seed changes.
- Half-plane colours were inverted (+ side painted pink, − side navy) → + side navy (blue team), − side maroon (pink team).
- Proof used `\( … \)` (not rendered by Streamlit) → `$ … $`; `>` vs `>=` made consistent with `predict_linear`.
- Sliders passed a default *and* were set via session_state (Streamlit warning) → defaults via `setdefault`, sliders without `value`.
- `draw_classifier_panel`'s returned error count now used (duplicate prediction code removed); placeholder-less f-strings → plain strings; "pink halos" → "red halos" (they are rose-red).

**UI differences to verify**
- XOR tab: info box says best line leaves **1** wrong; click "Best straight line (grid search)" → sliders jump to θ = -45°, b = -0.35, metric "1 / 4", success message "1 mistake(s)"; the line passes between points (no point on the line).
- XOR: blue points sit on the navy half-plane, pink points on the maroon half-plane when classified correctly.
- Rings tab: click best line → warning count equals the "Misclassified samples" metric; change the seed → the warning disappears.
- Recap tab → expand "Optional micro-proof": formulas render as math.

**Not fixed**: none.


---

## Pages 22–27


Validation run: ruff (`F,E9,W605,B,PLE`, ignore B905) clean · `python -W error::SyntaxWarning` compile OK for all 5 ·
AppTest base run + fuzz (slider min/max, radio options) → 0 exceptions · p27 all 8 slider-corner combos × 3 timeline steps → 0 exceptions ·
every embedded `<script>` parsed with esprima (ES2017) → no syntax errors.

---

### pages/22Piecewise Functions.py

#### Fixes
- `components.html` → `st.iframe` (3×); removed `streamlit.components.v1` import.
- **b₃ slider default out of range** (`min=-5`, `value=-6.0` → clamped to -5, default curve was discontinuous at gate b): intercept sliders b₁/b₂/b₃ now `min=-20 max=20 step=0.01`; default -6 is in range, so the default curve is continuous (both jumps 0.00).
- **Continuity often unreachable** (0.1 intercept steps / ±5 range vs. 0.01-resolution m·a products): 0.01 steps + new **“🧵 Snap continuous (solve b₂, b₃)”** button that solves `b2=(m1−m2)a+b1`, `b3=(m2−m3)b+b2`, with a note when the needed value exceeds ±20.
- **Jump readout hid the sign** (`Math.abs`): now signed “right − left” (`+1.00` / `−1.00`), labels say “(right − left)”.
- **Tolerance mismatch** (green at <0.05 but text said “exactly 0.00”): green iff |jump| < 0.005, i.e. exactly when it displays `0.00`; st.info text updated and explains sign + snap formulas.
- three.js r128 + OrbitControls CDN scripts now have `integrity="sha384-…"` (computed from the exact URLs) + `crossorigin="anonymous"`; JS wrapped in an IIFE that shows a visible red **load-error** banner if `THREE`/`OrbitControls` is missing.
- Gate color typo `0xebbf24` → `0xfbbf24`.
- ReLU widget: “dead” output stayed blue after a positive input (inline color overrode `.dead-val`) → inline color cleared in the dead branch.
- XOR lab formulas: “+ -0.5” → “- 0.5”; output renamed `out = …` (no clash with input coordinate `y`).
- Removed unused CSS (`.graph`, `.line-segment`).
- Universal-approximation overclaim (“any curve imaginable”) → “any *continuous* function on a bounded range … given enough pieces”.
- “enforces sparsity” → “produces sparse activations”.
- XOR text: “bend the decision boundary” → accurate “band between two parallel kinks” description + note on the small ±0.1 margins.
- Footer: placeholder-less f-string removed; `**random**` inside an HTML block (rendered literally) → `<b>`.

#### UI differences to verify
1. Section 1 on load: right panel shows b₁ `2.00`, b₂ `-1.00`, b₃ `-6.00`; “Jump at a/b (right − left)” both green `0.00`.
2. Drag b₃ right → Jump at b turns red with a `+` sign; drag left of -6 → `−` sign.
3. Set m₂ = 0.3, then click **Snap continuous** → both jumps return to green `0.00`; note under button shows the snapped b₂, b₃. Move any slider → note resets to the tip.
4. Set Gate b = 8, m₂ = -3, m₃ = 3, click Snap → note says the needed intercept is outside ±20.
5. Gate lines are amber (#fbbf24) like the gate value labels.
6. Block `cdnjs.cloudflare.com` (DevTools → Network request blocking) and reload → red banner “The 3D library (three.js) could not be loaded…”, sliders dimmed.
7. Section 2 (ReLU): move x to +2, then to -2 → output shows red struck-through `0.0` (was blue before).
8. Section 3: formula lines read e.g. `h₁ = max(0, 1.0x + 1.0y - 0.5)` and `out = 1.0h₁ - 3.0h₂ - 0.1`.
9. Footer: “random”/“deterministic” bold, no literal asterisks.

#### Not fixed (intentionally)
- File size (three inline HTML docs) — moving them to static files is a structural refactor beyond targeted fixes.
- “Force Linear (Fails)” still uses a ReLU unit (its *boundary* is a single line, which is the point); left as is.
- a ∈ [-8, 0], b ∈ [0, 8] slider domains kept (design choice).

---

### pages/23Sample Space & Basic Probability.py

#### Fixes
- Invalid escape sequences (`\O`, `\{`, `\}`, `\c` at old lines 475–498) → both LaTeX markdown strings are raw strings; `\\frac`/`\\text` normalised.
- `components.html` → `st.iframe` (heights 450→460, 520→560, 600→660 to avoid clipping); removed components import.
- **Venn bug**: “A only”/“B only” slots 0 and 2 were drawn inside the other circle (lens), e.g. A=Even/B=Odd showed 2 and 6 in the overlap while |A∩B|=0 → new slots `(-98,±50), (-110,0)` (mirrored for B), verified inside own circle and outside the other.
- 2-D dice grid: axis label colours/names were swapped (“Die 1 (Coral)” drawn cyan) → “Die 1 (rows, blue) →”, “Die 2 (columns, pink) →”; removed `rotate(180deg)` so the row arrow points down.
- Heatmap coloured by sum value (2 darkest, 12 lightest) → coloured by number of ways (sums equidistant from 7 share a colour; 7 brightest) + caption line explaining it.
- Probability stat shows the fraction: `6/36 = 16.67%`.
- Added a **“Counting trap”** `st.warning` (sums 2..12 are 11 outcomes but not equally likely; P(7)=6/36≠1/11) — addresses the “counting rule only shown with equally-likely atoms” finding.
- Recap “Next up: Complement, Union, Intersection” (already covered on this page; page 24 doesn't exist) → recap bullet for set operations + “Next up (Page 25): Conditional Probability”.

#### UI differences to verify
1. Section 2 default (Even vs Odd): 2/4/6 all sit in the left-only crescent, 1/3/5 in the right-only crescent, nothing in the overlap; choose A=Prime, B=Prime → 2,3,5 in the overlap.
2. Section 3: left axis reads top-to-bottom “Die 1 (rows, blue) →” in blue; top axis “Die 2 (columns, pink) →” in pink.
3. Grid colours symmetric around the 7-diagonal (2 and 12 same dark colour, 7 brightest).
4. Slider at 2 → Probability box `1/36 = 2.78%`.
5. Amber “Counting trap” box under the grid; LaTeX renders.
6. Blue recap box ends with “Next up (Page 25): Conditional Probability …”.

#### Not fixed (intentionally)
- No Ω rectangle around the Venn circles (cosmetic). Page 24 not created (out of scope per instructions).

---

### pages/25Conditional Probability.py

#### Fixes
- **Example was secretly independent** (P(A)=P(A|B)=0.40 while text said “profound difference”) → new `st.radio` (key `p25_scenario`) with two 40-student clubs: **Club A (dependent, default)** ab=12/a-only=4/b-only=8/none=16 → P(A)=0.40, P(A|B)=0.60, P(B|A)=0.75; **Club B (independent)** = original counts. Counts are injected into the JS (`__CONFIG_JSON__`).
- “Story Challenge” numbers are now computed from the chosen club, with a verdict sentence (clue raised/lowered the probability vs. “that's independence — next page”). “Direction matters” explains why P(A|B)≠P(B|A) (same numerator, different denominators).
- Math panel shows the probability form under the fraction, e.g. `= P(A ∩ B) / P(B) = (12/40) ÷ (20/40)`; caption verifies the formula numerically.
- LaTeX intro string → raw string; `components.html` → `st.iframe` (650→720, panel now 2 rows); math-panel `box-sizing: border-box`.
- Recap “Next up” mentions Club B as a sneak preview of independence.

#### UI differences to verify
1. Radio “Which club of 40 students?” above the orb lab; default Club A.
2. Click “2. Given Student in AI Club” → `12/20 = 0.60` and the line `= P(A ∩ B) / P(B) = (12/40) ÷ (20/40)`.
3. Switch to Club B → lab reloads; same button gives `8/20 = 0.40`; Story Challenge says P(A|B)=P(A)=0.40 → independence.
4. Club A Story Challenge: “The clue **raised** the chance … from 0.40 to 0.60”.

#### Not fixed (intentionally)
- “violently shrinks” wording kept (tone, not an error).

---

### pages/26Independence.py

#### Fixes
- **Mode switch mixed regimes** (stats kept accumulating across Independent/Dependent) → toggling now calls `resetStats()` (also cancels pending spin timeouts) and logs “Stats were reset so the two rule sets don't mix.”
- **Sampling noise with ≤100 spins** (~33% chance of a >10-pt gap under independence) → new **Spin 1000x** button, every observed card shows `xx.x% ±m` (rough 95% margin), a **Theory** line per card, and an explanatory note.
- **No definition of independence** → “Core Insight” now states $P(A\cap B)=P(A)P(B) \Leftrightarrow P(B\mid A)=P(B)$; new 4th green card **P(Sunny ∩ T-Shirt)** vs **P(Sunny)·P(T-Shirt)** (theory 30.0 vs 30.0 independent; 54.0 vs 34.8 dependent).
- Dependent-mode legend said “T-Shirt (50%)” → shows “T-Shirt: 90% if Sunny, 10% if Rainy” until a spin, then “T-Shirt (90% given Sunny)”; fast spins/reset restore that legend.
- Dead stats `coat`, `sun_coat`, `rain_coat` removed; magic numbers → `P_SUN`, `DEP_TSHIRT_IF_SUN/RAIN` constants.
- Mode toggle is keyboard-accessible (`role="button"`, `tabindex="0"`, `aria-pressed`, Enter/Space, focus ring) and ignored while a spin is running.
- Pixel “might be completely independent” example (pixels are correlated) → dropout coin flips for different neurons; “sample space morphs” → “P(B|A) differs from P(B)”.
- Title now “Page 26: …” like sibling pages; `components.html(..., scrolling=False)` → `st.iframe(html, height=1040)`; stat cards wrap (`flex: 1 1 200px`), value font 46→32px.

#### UI differences to verify
1. Controls row: Independent toggle, Spin 1x/10x/100x/**1000x**, Reset.
2. On load, cards show `--%` and “Theory: 50%”; green card “Theory: 30.0% vs 30.0% (= → independent)”.
3. Spin 1000x → three orange/yellow/blue cards ≈50% with `±3`-ish margins; green card ≈30% vs ≈30%.
4. Click the toggle → log is cleared and says stats were reset; cards back to `--%`; Theory lines become 58% / 90% / 10% and green card “54.0% vs 34.8% (≠ → dependent)”; Spinner B legend reads “T-Shirt: 90% if Sunny, 10% if Rainy”.
5. Spin 1x in dependent mode → legend becomes “T-Shirt (90% given Sunny)” or “(10% given Rainy)”.
6. Tab to the toggle and press Enter/Space → toggles; during an animated spin it does nothing.
7. Core Insight shows the independence formula (KaTeX) and the dropout example.

#### Not fixed (intentionally)
- Page not wrapped in `main()` (module-level script works the same; structural only).

---

### pages/27Bayes' Theorem.py

#### Fixes
- **Posterior from rounded counts** (up to 0.8-pt error, half-to-even rounding) → posterior computed with the exact formula `sens·prior / (sens·prior + fpr·(1−prior))`; counts (now half-up rounded) only drive the picture/natural-frequency caption; a caption appears in Phase 3 whenever the count ratio differs from the exact value by ≥0.05 pt.
- **Wrong explanation** (“The high prevalence makes the positive result…” even at 2% prevalence with 0.5% FPR) → message compares expected true vs false positives and says it's the *balance* of prevalence and FPR.
- **P(Positive) described as “TP + FP”** → added law of total probability, P(Positive|Healthy)=FPR (=1−specificity), full Bayes denominator; `st.latex` now substitutes the actual numbers (e.g. `0.90×0.020 / (0.90×0.020 + 0.090×0.980) ≈ 16.9%`) plus a natural-frequency caption.
- **10,000 heavy divs, ~4,300 px tall grid** → `st.html` grid of 6-px `<i>` dots (2 classes per dot; timeline step is one class on the container) ≈180 KB instead of ~500 KB and ≈700 px tall; legend line added under the grid. CSS classes namespaced (`.bt-grid`) instead of generic `.highlight/.dimmed`.
- Dead `else: posterior_prob = 0.0` / `if total_positives > 0` guards removed (slider minimums make P(Positive) > 0).
- Widget keys `p27_prevalence`, `p27_sensitivity`, `p27_fpr`, `p27_step`; FPR help mentions specificity.
- `{sensitivity_pct}%` printed “90.0%” → `:.0f`; result card background now red when result is red; intro mentions the false positive rate; “aura” → “ring”.
- LaTeX markdown → raw string.

#### UI differences to verify
1. Grid is compact (≈ 85 rows of small dots) with a legend line “Each dot is one of 10,000 people…”.
2. Timeline 2 → positives get yellow rings, negatives fade; Timeline 3 → negatives almost invisible, positives enlarged.
3. Defaults (2%, 90%, 9%) → Phase 3 shows **16.9%** (exact `0.018/(0.018+0.0882)`) and green box; LaTeX line shows numeric substitution.
4. Sidebar: prevalence 0.1%, sensitivity 65%, FPR 0.5% → Phase 3 shows 11.5% and a caption “Counting whole people gives 7 / 57 ≈ 12.3% …”.
5. Prevalence 2%, FPR 0.5% → amber warning talks about ~180 true vs ~49 false positives and the *balance* of prevalence and FPR (no “high prevalence” claim).
6. Result card is red-tinted (not green) when posterior ≥ 50%.

#### Not fixed (intentionally)
- Population stays 10,000 (so 0.1% prevalence still yields visible sick people); grid still re-sent on rerun (~180 KB) — acceptable after the 3× reduction.


---

## Pages 28–34


All 7 files: `use_container_width=True` → `width="stretch"` (plotly charts and buttons).
Verification: ruff (F,E9,W605,B,PLE) clean; `python -W error::SyntaxWarning` compile OK; AppTest fuzz
(sliders min/max, radios, number inputs, buttons, checkboxes) plus targeted edge-case runs → no exceptions.
No `components.html`, Google Fonts, `np.random.seed` or matplotlib in these files.

---

### pages\28Random Variables.py
**(a) Fixes**
- `<div class='concept-box'>` opened/closed in separate `st.markdown` calls (rendered as an empty dark box, wrapped nothing) → replaced with `st.container(border=True)` in all 3 sections; the now-unused `.concept-box` CSS was removed.
- "Bridge" histogram: the 0.1 cm bucket (labelled "Continuous") was the *noisiest* (65 % max relative error with 10k samples), contradicting the lesson → now 2,000,000 cached samples (`@st.cache_data`, seeded); max error at 0.1 cm ≈ 7 %, median ≈ 0.9 %. Option relabelled "0.1 cm (Nearly continuous)" and a note explains the sample count.
- "probability of getting exactly 170.0000000 cm is essentially zero" → "is zero".

**(b) UI differences to verify**
- Sections 1–3: the controls now sit in a bordered box; there is no stray empty dark rectangle above the sliders.
- Section 3: slide "Measurement Precision" to "0.1 cm (Nearly continuous)" → the blue bars should hug the red dashed curve smoothly (not jagged). First load of the page may take ~0.1 s longer (cached afterwards).

**(c) Not fixed**
- `scipy` import kept (now declared in requirements.txt).

---

### pages\29Expected Value.py
**(a) Fixes**
- Split `concept-box` divs → `st.container(border=True)` (balance beam controls, casino controls, casino results).
- Fair games mislabelled: floating-point noise (e.g. cost 1, prize 20, 5 %) gave ±1e-16 → "Positive/Negative EV" with "$0.00". EV within 1e-9 is now snapped to 0.
- Sign formatting: `+$-40`, `$-10`, `$-4.50` → new `fmt_money()` gives `-$40`, `-$10`, `-$4.50`, `+$90`.
- Zero-EV message "Nobody makes money in the long run" (wrong) → explains average is zero but individuals still win/lose.
- "See who really wins in the long run" had no simulation → added a deterministic 1,000-play running-total chart vs the expected line n·E[X], with a "🎲 Simulate again" button (`p29_casino_seed`, key `p29_resample_casino`). `$` signs in the caption are escaped so Markdown doesn't treat them as LaTeX.
- AI section: "final answer is often just the Expected Value" → regression (squared error) predicts the mean; classifiers pick the most likely class. "Loss is literally an Expected Value" → empirical average estimating the expected error.
- f-string without placeholders removed (`f"<br>**Calculated Expected Value:**"`).

**(b) UI differences to verify**
- Casino: set Cost=50, Prize=10 → cards show `-$40` / `-$50` / `-$49.50` (no `+$-40`).
- Casino: Cost=1, Prize=20, Win=5 % → grey "⚖️ Zero EV!" info box, EV card `$0.00`.
- Casino: new chart "Who wins in the long run?" below the cards; click "🎲 Simulate again" → the blue line changes, the orange dashed line stays; caption shows `Simulation #2`.
- Section 3 bullet text for Loss Functions / Probabilistic Models is reworded.

**(c) Not fixed**
- None of note.

---

### pages\30Variance & Standard Deviation.py
**(a) Fixes**
- `.section-header` text was `#1e293b` (invisible on the dark theme) → `#e2e8f0`.
- The page showed population and sample formulas but never applied them to the plotted dots, and the fixed seed meant the dots only rescaled → under the chart: metrics for sample mean x̄, variance ÷N, variance ÷(n−1), and true σ², plus a caption on s vs σ and the n−1 correction. A "🎲 Draw a new sample" button (`p30_resample`, state `p30_sample_seed`) redraws the dots; default stays deterministic.
- Stat card formula `E[X] = ∑(x·P(x))` (discrete) next to a continuous Normal → `E[X] = ∫ x·f(x) dx`.
- Band label "68% of data" → "≈68.3% of the distribution".
- Feature scaling text: standardizing = subtract the mean **and** divide by σ (mean 0, σ 1).

**(b) UI differences to verify**
- Section headers ("🎛️ Control the Spread", "📐 Mathematical Definitions", "🤖 Why Spread Matters in AI") are readable on the dark background.
- Below the bell chart: 4 metrics + caption + "🎲 Draw a new sample" button; click it → yellow dots and the first 3 metrics change, "True σ²" doesn't.
- Change σ → the "Var ÷N" / "Var ÷(n−1)" values scale with σ².

**(c) Not fixed**
- Duplication with page 34 (identical μ/σ slider block): it's a content/curriculum decision, so I left it. Page 30 is now differentiated by the sample-statistics panel.

---

### pages\31Bernoulli Distribution.py
**(a) Fixes**
- Generic, app-wide session keys `sim_results/sim_p/sim_n` removed. The simulation is now deterministic from `p31_flip_seed` and always matches the current p and n (previously stale results from an old p persisted). The button is "🪙 Flip Again (new random flips)" (key `p31_flip_again`). Flips use `rng.random(n) < p`, so moving p reuses the same random stream.
- Heads/Tails % used `int()` truncation (e.g. p=0.29 → 28 % + 71 %) → `round()`, with tails = 100 − heads.
- Fixed "Error from True p" threshold of 0.05 regardless of n → colour now uses 2·√(p(1−p)/n), shown in the card, with a ✅/⚠️ caption.
- p=0 / p=1: coin label "Always Tails/Heads" and a sidebar "Deterministic" message (was "Heavily biased … 100 %"). Float equality on p now uses `math.isclose`.
- Wording: classifiers predict the Bernoulli *parameter*; dropout uses its own drop rate r (not this page's p); "more flips bring us closer on average (not monotonically)".
- Takeaway no longer promises non-existent logistic-regression/dropout pages (mentions the Binomial next page and the cross-entropy pages, which exist).
- Removed the unused `make_subplots` import, the dead `.bar-heads/.bar-tails` CSS and the unused `p` parameter of `render_special_cases`. Dim `#64748b` axis/label text → `#94a3b8` for contrast on dark.

**(b) UI differences to verify**
- Sidebar p=0.29 → coin bar shows "Heads: 29%" / "Tails: 71%".
- Sidebar p=0.00 → coin label "Always Tails"; sidebar shows "🔒 Deterministic …".
- The "Simulate Many Flips" section shows results immediately (no click needed). "🪙 Flip Again" changes the counts and the running-frequency line. Moving the p slider updates the simulation to the new p (no stale "True p").
- Set the number of flips to 10 → the error card is usually green with "typical ≤ ~0.32"; at 10,000 the tolerance is ~0.01.

**(c) Not fixed**
- The global `html, body, [class*="css"]` font override was kept (cosmetic, same on sibling pages).

---

### pages\32Binomial Distribution.py
**(a) Fixes**
- **High — IndexError crash** (`empirical_pmf[k]`, index 25 out of bounds) when stored results came from a larger n. This happened because widgets reset to defaults after navigating away/back without firing `on_change`. Now (n, p) is stored in `p32_params` and the data is reset whenever it differs. The histogram uses `np.bincount` with out-of-range values filtered, so pandas is no longer imported.
- Session keys renamed `binom_*` → `p32_results`, `p32_total_trials`, `p32_params`, `p32_rng`; all widgets get `p32_` keys.
- Randomness: a seeded generator (`np.random.default_rng(0)`) is stored in session state and reset on "Reset Data" or a parameter change → the same click sequence gives the same results (no global `np.random`).
- Blocking `time.sleep` loops: the 1-trial coin reveal is now optional (checkbox "Animate single-trial coin flips") and takes 0.02 s per coin (≤0.8 s, was ≤2 s). "Animate 100 Trials" is now 10 frames × 10 trials with a 0.05 s pause (was 20 × 0.1 s).
- "perfectly molds" → "gets closer and closer (small random wiggles remain)"; CLT note adds "fastest when p is near 0.5".
- Formula breakdown: `p^k` = the probability that the k chosen flips are all heads (was "probability of getting k heads").
- Reset button uses `on_click=reset_sim` (no `st.rerun`); f-string without placeholders fixed; title "32." → "Page 32:" to match the other pages.

**(b) UI differences to verify**
- Set n=50, click "🚀 100 Trials", navigate to another page and back → the page loads (no red IndexError), n=10, and the trial count is 0.
- New checkbox "Animate single-trial coin flips" under the Animate button. Click "🎲 1 Trial" with it on → coins appear quickly one by one; with it off → all coins appear at once.
- "🎬 Animate 100 Trials" finishes in about 1 s and the trial count increases by 100.
- Change the n or p slider → the histogram clears (as before).

**(c) Not fixed**
- Stored trials are reset (not preserved) when you leave and return to the page, because widget values reset to defaults. Preserving them would need persistent widget state, which other pages don't do either.

---

### pages\33Uniform Distribution.py
**(a) Fixes**
- The sample histogram disappeared on any rerun (it was drawn only inside `if st.button`) → it is always drawn from a deterministic seed (`p33_sample_seed`). "🚀 Draw New Samples!" (key `p33_draw_new`) changes the seed; a caption shows the sample set number.
- Continuous histogram bins (`nbinsx=30`, Plotly "nice" bins) straddled a and b, making the edge bars too short → `xbins` aligned exactly to [a, b] in 30 equal bins.
- Example values "could be {a+0.12345} or {b−0.98765}" fell outside [a, b] for narrow ranges (e.g. −0.48765 for [0, 0.5]) → now a + 0.123456·(b−a) and a + 0.987654·(b−a).
- The spinner caption claimed the wheel "stops uniformly" (it spins forever and is unrelated to the samples) → reworded as a decorative illustration.
- Discrete mean card said `E[X] = (a+b)/2` → `(n+1)/2`.
- The annotation printed float noise (`1/0.19999999999999998`) → `1/(b−a) = 5`. Continuous stat cards use `.4g` (small ranges no longer show 0.00). The PDF rectangle is drawn with exact vertical edges.
- Hyperparameter text: learning rates are sampled log-uniformly. Hero: "within its range" added.
- Discrete frequency loop → `np.bincount`. Unused `make_subplots` and `time` imports removed.

**(b) UI differences to verify**
- Discrete mode: the simulation chart is visible immediately. Move the "Number of Samples" slider → the chart updates and does not vanish. Click "Draw New Samples!" → the bars change and the caption says "Sample set #2".
- Continuous mode with a=0.3, b=7.1, 50000 samples → the outer bars are as tall as the inner ones and line up with the red dashed rectangle.
- Continuous mode a=0, b=0.5 → the text examples are 0.06173 and 0.49383 (both inside the range).
- The discrete "Expected Value" card shows `E[X] = (n+1)/2`.

**(c) Not fixed**
- The spinner stays a CSS-only decorative animation; tying it to the samples would need custom JS.
- The vague takeaway ("total neutrality … fairness") was left as is (Low).

---

### pages\34Normal (Gaussian) Distribution.py
**(a) Fixes**
- `.section-header` `#1e293b` (invisible on dark) → `#e2e8f0`.
- Empirical-rule labels "68.2 %" (incorrectly rounded) → "≈68.3 %", and all three bands are marked ≈ (checkboxes and legend).
- `$x$` / `$\mu$` inside a raw HTML block rendered literally → `<i>x</i>` / μ.
- The exponent card `e^{-(distance)²}` dropped the ½ and σ → `e^{−½((x−μ)/σ)²}`, with a sentence on σ-scaled distance.
- No sampling demo and no takeaway → new checkbox "Overlay 1,000 random samples" (key `p34_show_samples`) draws a deterministic density histogram (bins of σ/4) behind the curve, with "🎲 Draw new samples" (`p34_resample`, state `p34_sample_seed`). The y-axis stays 0–1 unless a noisy bar would exceed it. Added a takeaway pointing to the existing CLT (36) and Z-Scores (35) pages.
- The curve had `hoverinfo='skip'` → hover now shows x and f(x).
- AI text: "Midjourney and DALL-E" → "Stable Diffusion and DALL·E 2/3"; VAE latent space is *pushed toward* N(0, I) by a penalty.

**(b) UI differences to verify**
- Section headers "🎛️ Shape the Bell", "📏 The Empirical Rule", etc. are readable.
- Checkbox labels read "Show 1σ Area (≈68.3%)" etc.
- Tick "Overlay 1,000 random samples" → grey bars appear under the blue curve and a "🎲 Draw new samples" button shows up. Clicking it changes the bars; moving μ/σ moves the histogram with the curve.
- Hover over the blue curve → tooltip `x = …, f(x) = …`.
- "The Distance" card shows italic x and μ (no `$` signs). A 💡 Takeaway box sits at the bottom of the page.

**(c) Not fixed**
- The prior finding "y-axis max 1.0 clips the PDF for small σ" was WRONG (the peak at σ=0.5 is 0.798), so there was nothing to fix. The fixed axis is intentional, to show the curve flattening as σ grows.
- Duplication with page 30 is left (see page 30, section c).


---

## Pages 35–42


Applies to all of them: `ruff check --select F,E9,W605,B,PLE --ignore B905` is clean, `python -W error::SyntaxWarning` compile passes, and the AppTest fuzz (each slider/select-slider/radio/button at its extremes, plus targeted combos) produces no exceptions. I extracted the embedded HTML/JS of 38, 40, 41 and 42 and ran it in headless Edge (`--dump-dom` showed the computed values, and I took screenshots at 760px and 1000–1100px wide, including edge-case variants). No widget keys collide; all keys and session_state entries use the page prefix. There are no `use_container_width` or `components.html` calls, no `Math.random`, and no Google Fonts or `file:///` links.

---

### pages/35Z-Scores & Standardization.py
#### (a) Fixes
- **Med – percentile didn't say it assumes Normal data** (`norm.cdf` → "higher than X% of values"): the label now reads "Percentile *if the data are Normal*: … of a Normal population lies below x". The insight box adds a caveat: you can compute a z-score for any data, but Φ(z) is only a valid percentile for Normal data, and standardizing skewed data does not make it Normal.
- **Med – near-black section headers on the dark theme** (`.section-header color:#1e293b`) → `#c7d2fe`.
- **Low – extreme percentiles printed "100.0%"**: new `format_percent()` shows `>99.99%` / `<0.01%`, and 2 decimal places in the tails.
- **Low – coarse spiky curve at extreme z**: the number of curve points now scales with the axis width (`curve_points()`, ~100 per σ, between 500 and 20000).
- **Low – σ-ruler silently stopped at 6σ**: an amber annotation now says "… ruler stops at 6σ (x is Nσ away)".
- **Low – duplicate tick labels drawn at y=-0.02**: removed. The axis uses `dtick=1` while the range is ≤16σ.
- **Low – "exactly" next to a rounded number**: removed. "Nice round bowl" softened to note that correlated features can still tilt the bowl.
- Widget keys renamed `z_*` → `p35_mean`, `p35_sigma`, `p35_x_val`. Unused loop variable `i` → `_`.
#### (b) UI differences to verify
1. Default view: the left card reads "Percentile *if the data are Normal*: 93.3%". The insight box under the tabs has a **Caveat** paragraph.
2. Set μ=0, σ=1, x=160. The card shows ">99.99%". On the 🌎 tab an amber note reads "… ruler stops at 6σ (x is 160.0σ away)". On the 🔬 tab the bell curve is smooth, and there are no duplicate numbers under the x-axis.
3. Section headers ("⚖️ The Visual Ruler", "🧮 The Formula…", "🤖 Why…") are clearly readable (light indigo) on the dark theme.
#### (c) Not fixed
- Nothing deliberately skipped. The scipy import stays; scipy is now declared in requirements.txt.

---

### pages/36Central Limit Theorem.py
#### (a) Fixes
- **Med – misleading "extremes cancel / regression to the mean creates the peak"**: rewritten as counting (with 10 dice there is one way to roll 10 but about 4.4 million ways to roll exactly 35, which I verified) plus the σ/√n shrinking of the mean.
- **Med – the formula is about means but the simulation plotted only sums, and the SD was hidden**: added a radio "Plot the… Sum / Mean of the dice (X̄)" (`p36_statistic`). In mean mode the bins have width 1/n centred on each attainable mean, so density bars and the Normal pdf stay comparable. The stat card now shows expected vs. observed mean and theoretical vs. observed SD, with the √n vs. 1/√n note.
- **Med – weight-init card claimed weights are drawn Normal *because of* the CLT**: rewritten. The pre-activation is approximately Normal whether the weights are Normal or Uniform; what keeps the network stable is variance scaling (Xavier/He).
- **Med – deprecated `use_container_width=True`** → `width="stretch"`.
- **Low – overclaims in the Noise and SGD cards** → "approximately Normal", for large batches with finite variance.
- **Low – fixed seed with no re-roll**: the seed lives in `st.session_state["p36_seed"]` (default 42). The "🎲 Re-roll the dice" button (`p36_reroll`) increments it, so results are deterministic by default.
- **Low – `<p><ul>` invalid HTML** → `<div>`. The CSS selector was extended to `.insight-box > div`.
- **Med – near-black section headers on the dark theme** → `#a7f3d0`.
- Keys: `p36_n_dice`, `p36_n_rolls`, `p36_statistic`, `p36_reroll`, `p36_seed`.
#### (b) UI differences to verify
1. Left column: there is a new radio "Sum of the dice / Mean of the dice (X̄)" and a "🎲 Re-roll the dice" button. The blue card says "Sum of 1 dice: theory vs. experiment" with expected 3.50 vs. observed, and SD theory 1.71 vs. observed.
2. Set n=30 and switch to **Mean**. The x-axis spans 1–6, the histogram becomes narrow, and the SD reads about 0.312. Switch back to **Sum**: it becomes wide, with SD about 9.35.
3. Click Re-roll: the histogram and observed numbers change. Moving a slider afterwards does not re-randomize.
4. "Why does this happen?" card: the counting explanation, with no "regression to the mean". AI cards: the reworded Weight-Init, Noise and SGD text.
#### (c) Not fixed
- The Normal overlay was kept for n=1 and 2 on purpose. The existing caption already says it is only an approximation for few dice, and the mismatch is part of the lesson.

---

### pages/37Softmax .py  (file not renamed, as instructed)
#### (a) Fixes
- **Med (confirmed) – no max-subtraction**: probabilities now come from `exp(z/T − max)`. The table adds the "z/T − max" and "e^(z/T − max)" columns. A new section "🛡️ Numerical Stability: Subtract the Max First" explains shift-invariance (LaTeX identity), and that e^1000 would overflow to inf and give nan.
- **Med – "tweaking the Softmax function denominator" was wrong**: it now says T divides every logit before the exponential, which changes both numerator and denominator. It also explains that T only matters when *sampling* (greedy decoding ignores it), so "creativity" is in quotes as the popular description.
- **Med – 47-character numbers** at T=0.1: bar labels and table use `{:.3g}` (e.g. `2.69e+43`); logits use `{:+.2f}`.
- **Med – deprecated `use_container_width`** (×4) → `width="stretch"`.
- **Low – `temperature == 1.0` float comparisons** → `np.isclose`. T is displayed as `{:.1f}`.
- **Low – help text "High T makes probabilities uniform"** → "closer to uniform". The badge reads "🔥 High: Soft & closer to uniform".
- **Low – "divide by sum" could also be a division by zero** (e.g. 2 and −2): now mentioned.
- **Low – unused CSS** `.math-font` and `.tooltip`: removed.
- Keys: `p37_logit_cat`, `p37_logit_dog`, `p37_logit_car`, `p37_temperature`.
#### (b) UI differences to verify
1. Defaults: chart labels read 7.39 / 0.368 / 1.65. The table has the extra "z − max" and "e^(z − max)" columns.
2. Sidebar: set T=0.1 and Cat=10. The Step-2 chart and the table show `2.69e+43` (no huge strings), and the probabilities are still correct.
3. A new "🛡️ Numerical Stability" section appears below the normalization box. The temperature paragraph mentions dividing the logits and sampling.
4. The badge shows "Current T: 1.0 ⚖️ Standard Softmax" exactly at T=1.0.
#### (c) Not fixed
- The light-coloured `.highlight-box` / `.insight-box` (black text on light background) and the `plotly_white` charts were kept. They are readable on the dark theme, and restyling would change the page's design.

---

### pages/38Mean, Median, Mode.py
#### (a) Fixes
- **Med – outlier demo capped at 20**: the axis now runs 0–30 (labels every 5), leaving room to drag the 19 out to 30. The info text tells you to do exactly that and notes the median doesn't move.
- **Med – even-count median branch was unreachable** (always 11 points): added **+ Add point** (adds at the current median), **− Remove point**, and **↺ Reset**, with 2–20 points. The median card's subtitle says "n=12 (even): avg of a & b" or "n=11 (odd): value #6 in order".
- **Low – median label overlapped the "Dataset" box**: the median-marker height is computed from the real height of the dataset box, including when it wraps.
- **Low – mean triangle covered tick labels**: the triangle is now 12px and the "Mean" label sits below the tick numbers.
- **Low – tall stacks ran under the dashboard**: stack spacing shrinks to fit the available height. Mode highlight heights follow it.
- **Low – the dragged dot reserved a stack slot** (floating gap): dragged dots are skipped when stacking.
- **Low – no keyboard access**: dots are focusable (`tabindex=0`, `role=slider`, `aria-*`). ←/→/↑/↓ move the focused dot by 1.
- **Low – `\n` soft breaks in `st.info`** → `\n\n`.
- Mode highlights: there is now one per possible tie (10 for 20 points). The mode subtitle reads "appears k× (m-way tie)", and the font shrinks when many modes are tied.
- `components.html(…, 620)` → `st.iframe(html_code, height=700)`. App height 580 → 640 to fit the button row. The unused `components` import is removed.
#### (b) UI differences to verify
1. The page loads with the dataset [2…19]: Mean 10.3 ("113 ÷ 11"), Median 8 ("n=11 (odd): value #6 in order"), Mode 18 ("appears 3×"). The axis runs 0–30.
2. Drag the dot at 19 to 30. The mean rises to about 11.3; the median stays at 8.
3. Click **+ Add point**. n=12, and the median subtitle shows "(even): avg of 8 & 8"-style text. Click **− Remove point** to go back. Buttons disable at 20 and at 2 points.
4. Click a dot, then press → several times. It moves along with the stats; a yellow focus ring is visible.
5. Add points until one value has a tall stack. Dots compress and stay below the "Dataset:" box, and the "Median" label never overlaps that box.
#### (c) Not fixed
- Values remain integers (snapped), which is by design for a stacking dot plot.
- The prior "only 5 mode highlights" finding was WRONG for 11 points, but the count now scales anyway.

---

### pages/40Covariance.py
#### (a) Fixes
- **Med (confirmed) – unlabeled N−1 covariance**: the card is titled "Sample Covariance (÷ n−1)", with the subtitle "population (÷ n): …". A caption under the iframe explains both.
- **Med – fixed ±0.5 threshold on a unit-dependent value**: "Relationship" is now Positive/Negative by sign, or "≈ Zero" when the unit-free |r| < 0.1 (the same band as p41). The subtitle shows "unit-free correlation r = …".
- **Med – p41 claims covariance's unit dependence was shown here**: added a "Measure X in: metres / centimetres / millimetres" select. Covariance scales ×100/×1000 while the cloud and r stay the same.
- **Med – unlabeled regression line, hidden when |cov|≤0.5**: always drawn (when Var X > 0) and labelled "- - least-squares line (Y on X)" on the canvas. It is dimmed when |r| < 0.1. The caption explains why it is flatter than near-vertical clouds.
- **Low – points off-canvas at 90°**: the scale is fitted to the largest point radius (rotation-invariant), so every point is always visible.
- **Low – quadrant shading at the means vs. axes at the origin**: dashed amber lines at x̄ / ȳ, labelled.
- **Low – misleading "purplish" comment**: replaced. Alpha now depends on |r|.
- **Low – unseeded `Math.random`**: mulberry32 seeded PRNG, plus a "🎲 New random sample" button.
- Canvas is responsive (`max-width:96%`). `components.html(…,650)` → `st.iframe(html_code, height=740)`. The components import is removed.
#### (b) UI differences to verify
1. Default (45°): "SAMPLE COVARIANCE (÷ N−1) +2.03", "population (÷ n): +2.02 · X in metres", Relationship "Positive", "r = +0.93". The dashed white line has a label at the bottom-left, and dashed amber x̄ / ȳ lines are visible.
2. Change "Measure X in" to millimetres. Covariance becomes about +2026 while the picture and r are unchanged.
3. Rotate to 90°. All points stay inside the canvas, Relationship shows "≈ Zero" (grey), and the regression line is dimmed.
4. Rotate to 80°. The line is visibly flatter than the cloud (as the caption explains).
5. "New random sample" changes the cloud. Reloading the page gives the same first cloud.
#### (c) Not fixed
- Canvas is not HiDPI-scaled (it can look slightly soft on retina screens). That is cosmetic and would need devicePixelRatio handling across the drawing code.

---

### pages/41Pearson Correlation.py
#### (a) Fixes
- **Med (confirmed) – measured sample r not displayed**: there is a new "Measured sample r" row, computed from the 400 drawn points. It shows "undefined" if either variance is 0.
- **Med – gotcha fit line drawn at y=0 instead of ȳ**: r, ȳ and the least-squares line are now computed from the plotted points. The dashed line is drawn through (x̄, ȳ) with the computed slope (about 0) and labelled "ȳ = …". The "0.00" in the text is the computed value (with −0.00 guarded).
- **Med – inconsistent thresholds** (JS 0.8/0.3 vs. markdown 0.5; r=0.29 labelled "Zero"): one set of bands everywhere. Perfect ≥0.999, Strong ≥0.7, Moderate ≥0.3, Weak ≥0.1, otherwise "≈ No linear correlation". The markdown scale was rewritten to match and marked as rules of thumb.
- **Med – clipping on narrow screens**: flex columns use `min-width:0`, the canvas uses `max-width:100%; height:auto`, and a compact `@media (max-width:900px)` block was added. Iframe height 580 → 680.
- **Partly – NaN / zero variance**: the formula section now says to use the same n or n−1 convention in both places and that r is *undefined* when σ=0. The JS r helper returns NaN, shown as "undefined".
- **Low**: seeded PRNG (mulberry32) plus a "🎲 New random sample" button. Firefox `::-moz-range-thumb` styling added. Initial status text unified. `render_anscombe_gotcha` renamed to `render_nonlinear_gotcha`. "Pearson Linear Correlation Coefficient" → "Pearson product-moment correlation coefficient". The "Study time vs Video game time" example → "Outdoor temperature vs Home heating bill". Unneeded `f"""` removed. `Math.sqrt(Math.max(0, 1-r²))`. `components.html` → `st.iframe`.
#### (b) UI differences to verify
1. Lab: under the slider you see "Measured sample r −0.03" (yellow) and a "🎲 New random sample" button. Move the slider to 0.5: the status reads "Moderate Positive…", and the measured r is close to but not exactly 0.50.
2. Slider at 0.25: "Weak Positive" (previously "Zero Correlation"). At ±1: "Perfect …" and measured r is ±1.00.
3. Narrow the browser or open the sidebar (about 760px content). The equation box "y = …x + … × noise" is still visible and the canvas shrinks.
4. Section 2: the fine-print paragraph about n/n−1 and σ=0; the scale bullets use the 0.7 / 0.3 / 0.1 bands.
5. Gotcha: the dashed pink line sits *below* the x-axis at "ȳ = −0.47" (not on the axis), and the "r = 0.00" heading appears inside the top of the U.
#### (c) Not fixed
- The colour of each lab point still uses x·y relative to the population means (0,0) rather than the sample means. The difference is invisible at n=400.

---

### pages/42Scatter Plot & Line of Best Fit.py
#### (a) Fixes
- **High – "keep the total length of those red lines as small as possible"** → "the **sum of the squared lengths** … (least squares) — not the plain total length".
- **Med (confirmed) – "minimize the total error (residuals)"** → "minimize the **sum of squared vertical residuals** (least squares)".
- **Med – "Total Error (MSE)" label** → "Mean Squared Error (MSE)".
- **Med (confirmed) – identical x forced slope 0**: when Σ(x−x̄)² < 1e-9, the status is `vertical`. Slope shows "undefined", intercept and MSE show "—", the equation box shows "x = c", a grey dashed vertical line is drawn, residuals are not drawn, and an explanatory note is shown.
- **Med/Low – a single point drew a horizontal line**: n=1 now shows "Need ≥ 2 points" and "One point fits infinitely many lines", with no line drawn. With 0 points it says "Click the canvas to add points".
- **Med – buttons clipped on narrow screens**: responsive flex (`min-width:0`, canvas `max-width:100%; height:auto`) plus a compact `@media (max-width:900px)` block. Click coordinates are now mapped from CSS pixels to canvas pixels (`cvs.width/rect.width`), including the remove-point hit radius. Iframe height 600 → 760.
- **Low**: dead `sumXY/sumXX` removed. Slope and intercept use a sign-aware formatter (no "−0.00"). The "Why square" list mentions absolute deviations and adds a third reason (smooth, closed-form solution, Gaussian noise). "Exact same thing" is qualified: neural networks use iterative gradient descent on bumpier losses. Unneeded `f"""` removed. `components.html` → `st.iframe`.
#### (b) UI differences to verify
1. Default lab: the description mentions "sum of squared vertical residuals". Stats show Slope +0.70, Intercept +0.18, "Mean Squared Error (MSE) 0.64".
2. Click **Clear Points**, then click once. You see "Need ≥ 2 points", dashes in the stats, and no line.
3. Click a second point directly above the first (same column). You see "Slope undefined", "x = …", and a grey dashed vertical line. Add a point elsewhere and the yellow fit line returns.
4. Toggle **Show Errors**: the red residuals appear only when a fit exists.
5. Narrow window (about 760px): the canvas shrinks, the Show Errors and Clear buttons and the instruction stay visible, and clicking still drops points exactly under the cursor.
6. Blue info box under the lab: the "sum of the squared lengths" wording.
#### (c) Not fixed
- **No keyboard way to add points on the canvas** (mouse/touch only). It would need a separate input UI. The Clear and Show Errors buttons are keyboard-accessible.
- The footer "Page 42 & 43" was kept: page 43's content (MSE and outliers) lives in this page, and renaming or renumbering pages is out of scope.


---

## Pages 44–49


Applies to every file: `components.html(...)` → `st.iframe(html, height=H)` (the unused `streamlit.components.v1` import was removed), f-strings without placeholders were dropped, CRLF line endings were kept, and Google Fonts `@import` was replaced by a system font stack (p47–p49).
Verification:
- ruff (`F,E9,W605,B,PLE`, ignoring B905) is clean, and the files compile under `python -W error::SyntaxWarning`.
- AppTest base run of each page raised no exceptions.
- Each lab's HTML was run in headless Edge with scripted clicks: no JS errors, and the numbers matched hand and Python results (listed per page below).
- Screenshots were checked at 1200 px and 900 px iframe widths.

---

### pages/44What is a Derivative.py
**(a) Fixes**
- *(Med, PARTLY in review)* When h < 0.02 the page quietly swapped in a forward difference with h = 0.001, yet labelled it "Derivative" and showed literal "dy"/"dx". The tangent state (|h| < 0.02) now shows the exact `f'(x) = 0.4x` and is labelled "Limit h → 0: Instantaneous Rate (Derivative)". Rise, run and h read "→ 0".
- *(Med)* The 0/0 wording at the old lines 300–302 and "The moment they merge…" at old line 309 were rewritten. The derivative is now explained as a limit; h is never set to 0.
- *(Med)* "Zero slope = valley or hill" was rewritten to mention flat points that are not extrema (x³ at 0).
- *(Med)* The second point used to go off-canvas (x + h could reach 12). h is now clamped so x + h stays within ±6.5, and the slider value is written back.
- *(Low)* The h slider now runs from −6 to 6 so learners can approach from the left too. Auto-shrink keeps the sign of h.
- *(Low)* `$h$` showed as literal text in the iframe; it is now `<i>h</i>`, and the curve `f(x) = 0.2x² − 2` is shown in the description.
- *(Low)* Dragging h now stops auto-shrink, and the interval is also cleared on `pagehide`.
- *(Low)* Removed the unused `rangeY` (which had a wrong comment), the dead `slopeValDisp` code, and an f-string without placeholders. The `lim` bullet is now worded precisely.
- iframe height went from 800 to 860, because the bottom was clipped at 900 px width.

**(b) UI differences to verify**
1. Set x = 2 and drag h to −1. The status reads "Average Rate of Change (Secant)" and the slope is **0.60**.
2. Drag h to about 0.01. The status turns teal: "Limit h → 0…". The equation reads `f'(x) = lim Δy/Δx = 0.4x = 0.80`, and Rise/Run/h show "→ 0".
3. Set x = 6, then drag h to the maximum. The h slider snaps back to **0.50** and the yellow point stays on screen.
4. Set h = −3 and click **Auto-Shrink**. h shrinks toward 0 from the negative side and ends in the teal tangent state.
5. Grabbing the h slider during auto-shrink stops it, and the button label resets.

**(c) Not fixed**
- I did not refactor the duplicated canvas helpers shared with p45 and p46, because that would be a larger change.
- The canvas is still a fixed 480 px and has no high-DPI handling (Low; design kept).

---

### pages/45Derivative Rules (Power & Constant).py
**(a) Fixes**
- *(Med)* The button said `Quadratic (y = 0.5x²)` and the initial `f(x) = 0.5x²`, but the plotted function was `0.5x² − 2`. All labels now say `0.5x² − 2`.
- *(Med)* The text claimed "Quadratic (x²) → 2x, Cubic (x³) → 3x²", which doesn't match the lab. It now describes the lab's actual functions, and a new section "🧩 Two Helper Rules" covers the Constant Multiple and Sum rules with the lab's coefficients (0.5·2x = x, 0.1·3x² = 0.3x², −2 → 0, 1.5x → 1.5).
- *(Med)* Auto-sweep pushed and sorted a new trace point every 20 ms with no limit. Traces are now a `Map` keyed by x (rounded to the slider step), so it holds at most 153 points. Verified: 153 after a 9-second sweep.
- *(Med)* Points went off-canvas for |x| > 3.9 (quadratic and cubic) and |x| > 4.47 (cubic derivative). The slider range and auto-sweep are now limited to ±3.8, where every f and f′ stays inside the ±6 window.
- *(Low)* Click handlers use `e.currentTarget`. Switching function now resets `lastX` and seeds the trace with the current point.
- *(Low)* Auto-sweep is cleared on `pagehide` and always starts rightward.
- *(Low)* Removed a leftover comment and an f-string without placeholders. The MSE note now says `2·(Prediction − Reality)` is the slope with respect to the *prediction*, and that the chain rule carries it back to the weights.
- *(Low)* The description said "drag the point", but the point is moved with the slider; reworded.
- iframe height went from 750 to 800.

**(b) UI differences to verify**
1. The function card and the quadratic button both read `0.5x² − 2`.
2. Click **Cubic** and drag x to the right end. The slider stops at 3.80, the derivative shows **4.33**, and both dots stay on screen.
3. Run **Auto-Sweep** for 30 seconds or more. The bottom trail stays smooth and the page stays responsive.
4. Below the lab there is a new "🧩 Two Helper Rules" section.

**(c) Not fixed**
- The canvas window is still a fixed ±7 × ±6. I chose to limit x rather than rescale each function.

---

### pages/46Chain Rule — Derivative Through Layers.py
**(a) Fixes**
- *(Med)* In Wave mode the outer f(g) point left the canvas when |x| > 3, because g = 2x reaches ±8 while the axis only went to ±6. Power mode went past y = 5 when |x| > 3.74, and in Gauss mode g left the axis when |x| > 3.46. Each function now has a window per canvas (`views`, applied with `setView`), so all three points and tangents stay visible over x ∈ [−4, 4].
- *(Low)* The `m=…` slope labels flip inward near the right and top edges.
- *(Low)* The auto-sweep step is now 0.05, matching the slider step (0.03 was silently snapped up to 0.05).
- *(Low)* `drawFunction` now uses an index loop instead of accumulating floats.
- *(Low)* "3 × 2 = 6x" now reads "6 times".
- *(Low)* The backprop paragraph now mentions that contributions are added across paths.
- *(Low)* Removed an f-string without placeholders.
- iframe height went from 750 to 800, because the bottom was clipped at 900 px width.
- Formulas are unchanged and were re-verified: at x = 4 in Wave, g′ = 2, f′ = 3cos 8 = −0.44, df/dx = −0.87. At x = −4 in Power, −4 × 2.4 = −9.60. At x = 1.5 in Gauss, −1.5 × 1.30 = −1.95.

**(b) UI differences to verify**
1. Click **Wave** and drag x to 4. The yellow dot on the "Outer f(g)" canvas stays visible. The readouts are 2.00, −0.44 and −0.87.
2. Click **Power** and set x = −4. All three dots are visible, and the composite slope is −9.60.
3. The grid density now differs between canvases and functions, because each window is scaled to its own range.

**(c) Not fixed**
- Canvas and slider code is still duplicated with p44 and p45 (Low).

---

### pages/47Partial Derivatives.py
**(a) Fixes**
- *(High)* The displayed formula `f(x,y) = 0.25x² + 0.25y²` left out the `− 1.5` that is in the code. It now reads `… − 1.5`, so the readout of −1.00 at (1,1) is consistent.
- *(Med)* The buttons said `x²+y²` and `x²−y²`, which suggests ∂f/∂x = 2x, but the readout showed 0.5x. They now read `¼(x²+y²) − 1.5`, `¼(x² − y²)` and `1.5(sin x + cos y)`.
- *(Med)* The 3D view clipped the bowl's back corner (py = −45), and the wave's front corner went below the canvas. The projection is now SCALE 46, YSCALE 30, OY 243, with the canvas at 640×460. I checked numerically that all three surfaces stay within py ∈ [15, 444].
- *(Low)* In the 2D slices, the y = 0 axis is drawn only when 0 is in range, and the formerly unused `label` parameter now draws an "x →"/"y →" axis label.
- *(Low)* Click handlers use `e.currentTarget`. The auto-sweep step is now 0.05, matching the slider step.
- *(Low)* Footer: "slice … in any direction" became "along each axis".
- *(Low)* Removed the Google Fonts import.
- iframe height went from 780 to 800, using `st.iframe`.

**(b) UI differences to verify**
1. The Bowl readout reads `f(x,y) = 0.25x² + 0.25y² − 1.5 = -1.00` at (1,1).
2. The 3D surface is a little smaller, and the bowl's top corners are no longer cut off. Choose Wave and set X = Y = −3: the front corner is fully visible.
3. Each slice chart shows an "x →" or "y →" label in its bottom-right corner.

**(c) Not fixed**
- Slice curves and the point are still drawn on top of the whole surface, so they can show through hills. Proper hidden-line occlusion would need a z-buffer-style rewrite.

---

### pages/48The Gradient — Steepest Climb.py
**(a) Fixes**
- *(Med)* One button secretly toggled between ascent and descent, and the climber stopped without saying why. There are now explicit **⬆ ASCEND (+∇f)** and **⬇ DESCEND (−∇f)** buttons and a status line:
  - The status reports when the climber reaches a flat point (|∇f| < 0.005). A numerical-Hessian second-derivative test classifies the point as **MINIMUM**, **MAXIMUM** or **SADDLE**.
  - It also reports when the next step would leave the map, or when the 500-step limit is reached.
  - The trail is pink for ascent and green for descent, and the legend says which.
- *(Med)* The legend height used `climbDir?72:58`, which was always true. It now uses `trail.length>0`.
- *(Med)* Field arrows saturated once |∇f| ≥ 0.583, which contradicted "length = how steep". Arrows are now proportional to |∇f| (the longest is 0.45 units per surface), and the description says so.
- *(Med)* Axes were scaled unequally (93.75 vs 81.25 px per unit), so ∇f did not look perpendicular to the contours. The canvas is now 600×600, giving equal scales.
- *(Med)* The heatmap and contours (about 35k rects) were redrawn on every animation frame. They are now cached in an offscreen canvas once per surface. Contour dots now also detect vertical crossings.
- *(Med)* The Key Intuitions now note that ∇f = 0 at a saddle point as well.
- *(Low)* Readouts and the white dot used the slider value, which is snapped and clamped to ±3. They now use the exact point (`ptX`/`ptY`), and the sliders cover ±3.2, matching the map.
- *(Low)* The arrow grid was asymmetric (it ended at 2.55); it is now −3..3 in steps of 0.5.
- *(Low)* The ∇f arrow at the point is capped so it stays on the map. Components and their sum share the same scale.
- *(Low)* "Climber" mode only hid the arrows; it is renamed **🧗 Clean Map**, and switching overlay no longer stops a climb.
- *(Low)* The wave button label is now `2·sin x·cos y`.
- *(Low)* Removed the Google Fonts import; canvas text uses the system font.
- iframe height went from 750 to 800.
- Headless Edge results matched a Python simulation:
  - Saddle at (0.5, 0), Descend: saddle after 130 steps.
  - Bowl Ascend: left the map after 47 steps.
  - Bowl Descend: minimum after 139 steps.
  - Wave Ascend: maximum at (1.57, 0) after 157 steps.

**(b) UI differences to verify**
1. Under the sliders there are two buttons, ⬆ ASCEND (pink) and ⬇ DESCEND (green), with a status line below them.
2. Choose Saddle, set X = 0.5 and Y = 0, then click ⬇ DESCEND. The status ends with "a SADDLE point (∇f = 0, but neither a min nor a max!)".
3. Choose Bowl and click ⬆ ASCEND. The status reads "the next step would leave the map".
4. Field arrows near the bowl's centre are short and get longer toward the edges. The bowl's contours look like circles, not ellipses.
5. The legend box only grows to show the trail entry after a climb.
6. Clicking **🧗 Clean Map** during a climb hides the arrows without stopping it.

**(c) Not fixed**
- The learning rate stays a fixed 0.02 on the unnormalised gradient. That is deliberate: it is plain gradient descent, and the reasons for stopping are now shown.

---

### pages/49Integral as Area.py
**(a) Fixes**
- *(High)* The Gaussian's `F` returned `null`, so `if (f.F)` was truthy and `null − null = 0` was shown as "Calculus Exact", with an error of about 176%. `F` is now `(√π/2)·erf(x)`, using a high-accuracy erf series with all-positive terms (max error against Python's `math.erf` is 1.2e-15 on [−6, 6]). The fallback is now guarded with `typeof f.F === 'function'`. The exact value on [−2, 2] is 1.7642.
- *(Med)* Only the midpoint rule was available, and it was unlabelled. There is now a **Left / Midpoint / Right** selector, and the sum label shows the method.
  - Checked for x² on [−2, 2] with n = 10: midpoint 5.2800, left 5.4400, right 5.4400, exact 5.3333.
- *(Med)* `(trueI || 1)` turned the absolute error into a fake percentage. The display now shows `Error: p% (|Δ| = …)`, or `|Error| = … (exact value is 0, so % is undefined)` when the exact value is 0.
- *(Low/Med)* New function **y = sin(x) (signed area)**. Rectangles below the axis are drawn in rose, and the text explains negative area. Checked on [−3, 1]: exact −1.5303.
- *(Low)* `import numpy` was unused and has been removed.
- *(Low)* Invalid `"\i"` escape: that line is now a raw string, and the `\n` breaks in the sidebar boxes are now `\n\n`.
- *(Low)* The canvas is now absolutely positioned inside its wrapper and sized from its `clientWidth/Height`. This removes the risk of the wrapper growing on each window resize.
- *(Low)* The resize listener is re-added on `pageshow` after a back/forward-cache restore.
- *(Low)* The grid loop now uses an index, so the top line is no longer skipped.
- *(Low)* The error badge label is now consistent.
- *(Low)* The sigmoid antiderivative now uses an overflow-safe softplus.
- *(Low)* Entropy notation changed from `H(P)` with `P(x)` to `H(p) = −∫ p log p dx`.
- *(Low)* Removed the Google Fonts import.
- Layout: `.outer` height went from 650 to 760 to fit the new controls, and the iframe from 700 to 800.

**(b) UI differences to verify**
1. Click **Gaussian (Bell)**. The exact value shows **1.7642** instead of 0.0000, and the error is about 0.05%.
2. Click **Left**, then **Right**. The label changes to "RIEMANN SUM (LEFT/RIGHT)" and the sums differ from the midpoint sum.
3. Click **y = sin(x) (signed area)** and set a = −2, b = 2. The rose rectangles on the left cancel the cyan ones. Sum 0.0000, exact 0.0000, and the badge shows "|Error| = … (exact value is 0…)".
4. Resizing the browser window several times does not slowly grow the chart or push the "PRO TIP" off the bottom.
5. In the sidebar, the info, success and warning boxes have the bold title on its own line, and the ∫ renders.

**(c) Not fixed**
- The page title is still a raw centred `<h1>` rather than `st.title`. I kept it to preserve the page's design; it's a Low item.


---

## Pages 50–56


These conventions apply to all 6 files:
- `components.html(...)` was replaced by `st.iframe(html, height=H)`, and the `streamlit.components.v1` import was removed.
- The Google Fonts `@import`s were removed in favour of a system font stack.
- `$...$` was removed inside iframes.
- Header CSS classes are page-prefixed (`p51-header`, `p52-header`, `p53-…`) and unused CSS was deleted.
- Mouse handlers were replaced by pointer events (touch/pen).
- No page uses `session_state` or widgets.

### Verification

- **Lint and compile:** ruff (`F,E9,W605,B,PLE`) is clean, `python -W error::SyntaxWarning` compiles all 6 files, and an AppTest base run raised no exceptions (none of the pages have Streamlit widgets).
- **JS in headless Edge:** I extracted each iframe's HTML (scratch copies, never in the repo), clicked through it with scripts and took screenshots. No JS errors.
  - p50: MAE fit 11 px vs MSE fit 206 px², and all points are on the canvas.
  - p51: Complex loss at (1.5, 1.5) = 1.06, which matches Python.
  - p52: Lumpy run converges in 10 steps to a local dip (loss 0.825) and the toast says so. `.col-r` is now a child of `.row`.
  - p53: CHAOS gives DIVERGED after 5 steps; η = 1 gives BOUNCING FOREVER after 12 steps.
  - p54: Secret plus a click near the well gives GLOBAL; Twins at η = 0.3 gives "Bouncing…".
  - p56: after 3 s, batch loss is 2.400 (stuck) and SGD loss is 0.879 (escaped); 4 dots are lit; pills show 0.08 / 0.50 / 4.
- **Math in Python:** see the per-page notes below.

---

### pages/50What is a Loss Function.py

#### (a) Fixes
- **Switching MSE/MAE didn't redraw (Med).** Both toggles now call `render()`.
- **"Perfect Fit" always used least squares (Med).** It is now "✨ Best Fit".
  - In MAE mode it finds the exact least-absolute-error line by checking every line through two data points (an L1-optimal line always passes through two points).
  - In MSE mode it stays OLS.
  - Slider precision is now w step 0.01 and b step 0.1, with b range ±200. Values are clamped to the slider range.
- **Points generated off-canvas (Med).** The slope is limited to the canvas size, the noisy y is clamped to [12, height−12] and the bias range is reduced.
- **Random data with no seed (Low).** A seeded PRNG (mulberry32, seed 7) gives the same first dataset on every load; "Reset Data" moves to the next seed.
- **Dragged points could leave the canvas; mouse-only (Low).** Drags are clamped to the canvas and use pointer events with pointer capture. The window-level mouse handlers were removed.
- **"Smooth bowl" overgeneralised (Med).** The text now says this holds for straight-line models, and that deep networks are bumpier even with MSE.
- Grammar fix ("handed" → "hands"). The meter label now states units (pixels² / pixels).
- Iframe height changed from 550 to 660. The controls column was clipped before; checked by screenshot.

#### (b) UI differences to verify
1. Open Page 50 and click **MAE (Absolute)**. The meter number and the drawing switch at once from red squares to dashed bars. Click **MSE** and they switch back.
2. In MAE mode click **✨ Best Fit**. The line passes exactly through two points and the hint explains this. Switch to MSE and click Best Fit again; the line changes to least squares.
3. Reload the page. The first dataset is identical each time and slopes upward. **Reset Data** gives new data, always inside the canvas.
4. Drag a point past the canvas edge. It stops at the edge. Touch-drag also works.

#### (c) Not fixed
- The colour of the meter fill (gradient replaced by solid colours) is unchanged; it's cosmetic.

### pages/51Loss Landscape — Hills and Valleys.py

#### (a) Fixes
- **Animation loop always running (Med).** The idle `requestAnimationFrame` loop and the ball "pulse" are gone. A coalesced `requestDraw()` redraws only on slider input, drag, zoom, mode switch or resize.
- **3D draw order reversed (Med).** Polygons are now sorted far-to-near, and the w2 axis is mirrored so the camera is above the surface and the top-down view matches a map (w1 → right, w2 → up). Rotation comments were corrected.
- **3D view clipped / overflowing.** The surface is auto-fitted into the canvas every draw and offset right of the control card when the canvas is wider than 760 px. Ctrl+wheel zoom is now a multiplier (0.4–2.5×).
- **`$w_1$` shown literally in the iframe (Med).** Now `<i>w</i><sub>1</sub>`.
- **"Complex" differed from page 52's "Lumpy Terrain" (Med).** Both pages now use the same surface:
  `f = 0.2(x²+y²) + 0.5·sin3x·cos3y + 0.3·cos1.5x + 0.25`.
  Its minimum is ≈ 0.016 at (−0.548, 0), checked numerically. Convex is now `0.3(x²+y²)`, with a minimum of 0.
- **Wheel zoom trapped page scrolling (Low).** Zoom now only reacts to Ctrl/⌘ + wheel (or pinch); the hint text was updated.
- Unused `.info-card` and `.highlight` CSS and the unloaded 'Outfit' font were removed. The GPT-4 parameter claim was replaced with "billions — often hundreds of billions".

#### (b) UI differences to verify
1. Page 51, Convex: you see the whole bowl, with the near rim in front of the inside, as seen from above. Before, the top was cut off and the draw order was reversed.
2. Click **Complex**: the lumpy surface is fully visible, and peaks hide the valleys behind them. At w1 = w2 = 1.5 the loss reads **1.06** (it used to read 1.85 / 1.35 for convex).
3. Plain mouse-wheel over the 3D view scrolls the Streamlit page; **Ctrl + wheel** zooms.
4. The slider labels show subscripts w₁ and w₂, not `$w_1$`.
5. The ball no longer pulses. CPU is idle when you aren't interacting.

#### (c) Not fixed
- The ball is still drawn on top of everything, even when it's behind a hill. Kept on purpose so it stays visible.

### pages/52Gradient Descent.py

#### (a) Fixes
- **Unclosed `<div class="sep">` broke the layout (Med).** Closed. The controls and the two canvases are now side by side again (checked in the DOM: `.col-r` is a child of `.row`). Iframe height changed from 900 to 640.
- **Loss offset `+1.5` (CONFIRMED).** Both surfaces now have a true minimum of about 0 (bowl `0.3r²`; lumpy surface shared with p51), so the readout shows the raw `f`. The heat-map colour range was shifted to match.
- **3D draw order reversed (Med).** Same camera fix as p51. The 3D view is auto-fitted to the canvas (about 18% of vertices used to be off-canvas). The label "3D Perspective View" became "3D View (drag to rotate)".
- **"Always seeks the deepest blue" (Med).** Rewritten: the bowl always reaches the bottom, while Lumpy Terrain often stops in the nearest dip.
- **"Guaranteed downhill" (PARTLY).** Now says it is guaranteed for a small enough step size (true here, since η = 0.15 < 2/L ≈ 0.37) and only leads to *a* nearby dip.
- **Legend mismatch, "Yellow / Teal / Orange arrow" (Med).**
  - The text now describes what is actually drawn: orange dashed ∇f, green arrow −∇f, white contour lines.
  - The readout labels ∇f = [∂f/∂w1, ∂f/∂w2].
  - Unused highlight CSS was removed.
- **"TARGET REACHED" at local minima (Med).** The toast now says "GLOBAL MINIMUM REACHED! 🎯" or "STOPPED IN A LOCAL DIP 🕳️", based on distance to the known global minimum. A second dip at (1.51, 0) has loss 0.022, so a value-based test would not work.
- **Double animation loop on quick Pause→Play (Low).** The frame id is stored and cancelled.
- **Invisible contours (Low).** Real contour lines are drawn every 0.5 loss units (cell-edge band crossings).
- Text: "hardest challenge" now notes saddles and flat regions; "exactly how ChatGPT…" now says modern models use refined variants (mini-batches, Adam). Pointer events; teleport clamps to the map.
- Not changed: the divergence guard (WRONG in the review — η is fixed and stable).

#### (b) UI differences to verify
1. Page 52 at normal width: the controls are on the left and the Topo Map and 3D View are side by side on the right. Nothing is cut off at the bottom.
2. Convex Bowl, **START TRAINING**: Loss counts down to about 0.000 and the toast says **GLOBAL MINIMUM REACHED**.
3. Lumpy Terrain, START: the ball stops after about 10 steps at loss **0.825**, and the toast says **STOPPED IN A LOCAL DIP**.
4. Click near (−0.5, 0), left of the map centre, then START: the toast says GLOBAL.
5. Rotate the 3D view to nearly top-down: the picture matches the topo map's orientation and peaks are drawn over valleys.
6. Contour lines are visible on the map. Rapidly click Pause/Play: the speed doesn't double.

#### (c) Not fixed
- The bowl looks tall and narrow in 3D because heights are shown at true scale. Kept honest.

### pages/53Learning Rate.py

#### (a) Fixes
- **"η = 0.15 (Optimal)" was wrong (High).** It now reads "Good". The text explains that η = 0.5 is optimal for x² (one jump).
  - New presets: 🎯 ONE JUMP (0.5) and 🏓 BOUNCY (0.9), giving 5 presets in total.
  - A hint under the slider gives λ = 2 and η < 2/λ = 1.
- **Wrong description of Adam (High).** It now describes running averages of gradients and squared gradients, with each weight's step divided by its typical gradient size.
- **The stat-card `<div>` wrappers rendered as empty boxes (Med).** Replaced with `st.container(border=True)`; the CSS was removed and the tag classes prefixed.
- **Slow preset mismatch (0.02 vs 0.01) and "thousands of steps" (Med).** Now η = 0.02, "about 220 steps here (vs about 25 for 0.15)", which matches the computed values.
- **η < 2/λmax with no assumptions (CONFIRMED).** Now worked through x² explicitly: (1−2η)x, λ = 2, η < 1. It is stated as a *local* rule with λmax = largest Hessian eigenvalue, exact only for quadratics.
- **η = 1 runs forever (PARTLY).**
  - Detects |x| not shrinking for 12 steps and shows "BOUNCING FOREVER 🏓 (η = 2/λ = 1)".
  - Adds a cap of 500 steps per run ("STOPPED: not converged…").
  - Divergence now triggers when the ball leaves the chart (|x| > 6) and also checks `isFinite`.
- **The arrow ignored η (Low).** It now shows the actual next step (η·slope) with an arrowhead, plus a dashed ring where the ball will land. The legend was updated.
- Float-accumulating loop replaced with an integer loop. Fonts removed. Iframe height changed from 600 to 700 (stats were clipped).

#### (b) UI differences to verify
1. Page 53 shows 5 preset buttons. Pick **🎯 ONE JUMP** and START: CONVERGED after 2 steps.
2. Pick **🏓 BOUNCY**: the ball zig-zags but converges.
3. Pick **💥 CHAOS**: DIVERGED (left the chart) after about 5 steps.
4. Drag the slider to exactly **1.000** and START: after 12 steps you see "BOUNCING FOREVER". Press START again and it re-checks (the per-run counter resets).
5. The blue arrow's length changes when you move the η slider. The dashed ring marks the landing spot.
6. Below the lab, the three cards are bordered containers with no empty boxes. They read "η = 0.02 (Small)" and "η = 0.15 (Good)".

#### (c) Not fixed
- Nothing outstanding.

### pages/54Local vs Global Minimum.py

#### (a) Fixes
- **Secret's global minimum unreachable at the default η (High).** The well width (σ²) changed from 0.8 to 1.5, so the Hessian at the global minimum drops from about 30 to about 16 and the stability limit is now η < 0.125.
  - The global coordinates were recomputed as (−2.786066, 2.786066), checked with a Newton refinement.
  - Simulation on a 31×31 grid of starts at η = 0.1: 282 GLOBAL, 405 local, 266 slow plateau, 8 stationary. Before the fix there were 0 GLOBAL.
- **No outcome when the 200-step cap was hit (CONFIRMED).** The cap is now 200 steps *per Run press*, and you can press Run to continue. At the cap the badge says either:
  - "Bouncing: η too large for this valley ↔" (the loss rose, or the direction reversed at least 6 times in the last 12 steps), or
  - "Still creeping (flat region) — press Run to continue".
  - Simulation results: Twins at η 0.3 gives 959/961 runs "oscillating"; the Secret plateau gives "slow". The path is capped at 2000 points.
- **Double animation loop (Low).** The frame id is stored and cancelled (`stopRun`). `placeBall` helper added; `pagehide` stops the loop.
- **3D view clipped (Low).** `fitIso()` scales and centres the isometric view per landscape; about 24% of vertices used to be above the top edge.
- Label "Current Step" became "η (step size multiplier)". The unused `.z` fields were removed.
- Text:
  - "flat ⇒ stop" now mentions local minima, saddles and plateaus.
  - The higher-η advice is hedged (it usually just bounces here).
  - The momentum tip points to page 56's Momentum slider.
  - The Secret tip explains the narrow well.
- **Dangling forward reference (CONFIRMED).** "Next: Convex Functions" now reads "Next: Stochastic Gradient Descent". Page 55 doesn't exist.

#### (b) UI differences to verify
1. Page 54, **The Secret**, click the map near the top-left dark well and Run: the badge says **Global Minimum Found! 🎉** (before, it never could at η = 0.1).
2. The Secret from the default start (2.5, 2.5), Run: the badge says **"Still creeping (flat region)…"**. Press Run a few more times and it settles in the local dip.
3. **The Twins**, η slider at 0.30, Run: the badge says **"Bouncing: η too large…"**.
4. The 3D view shows the whole landscape, with no top cut off, for all three landscapes.
5. The footer says "Next: Stochastic Gradient Descent".

#### (c) Not fixed
- No momentum control was added to this lab. The text points to page 56 instead, to keep scope.

### pages/56Stochastic Gradient Descent.py

#### (a) Fixes
- **"SGD" was the exact gradient plus uniform noise, with batch size only scaling the noise (CONFIRMED).** It is now **real mini-batch SGD**.
  - There is a seeded synthetic dataset of **64 examples**. Each example has its own loss surface:
    `l_i = 0.1(x²+y²) − 0.2(a_i x + b_i y) + A sin(2x−2c_i) + B cos(2y−2d_i)`
    - The offsets a, b are standardised to mean 0 and SD 6.
    - The phases are spread evenly and symmetrically over ±1.05; d is a seeded shuffle of c.
    - A = B = 0.5 / mean(cos 2c).
  - So the dataset average is **exactly** the landscape that is drawn, `0.1(x²+y²)+0.5(sin2x+cos2y)`. I checked this with an exact Python port of the JS PRNG: mean-loss error 4e-16 and mean-gradient error 1e-15.
  - Mini-batches are sampled without replacement, reshuffled each epoch (remainder dropped). Full batch averages all 64 examples, so batch = 64 reproduces full batch exactly.
  - The 64 mini-batch dots light up the actual sampled indices; the elements are created once and only their classes toggle.
- **Overstated escape claims (CONFIRMED).** I re-measured with the exact port, starting at (−4, −4) with η 0.08 and momentum 0.5 for 20 s:
  - Full batch always stays at loss 2.40.
  - Batch 1–2: 100% escape.
  - Batch 4 (the default): about 50% escape.
  - Batch 8 or more: about 0%.

  All the texts now say "can sometimes", explain that it's not guaranteed, and give these numbers.
- **Pills didn't match the sliders at load (Med).** η pill 0.05 → 0.08 and momentum 0.0 → 0.50. Batch default is now 4.
- **Origin marked as the "minimum" (Med).** The origin has gradient (1, 0). Instead, the true global minima are marked with ★ at (−0.714, ±1.426) (loss −0.720, verified), and a legend entry was added.
- **Per-step comparison hid SGD's real advantage (Med).** Added **⚖️ Equal compute** (SGD takes 64/B steps per full-batch step) and "examples used" counters for both optimizers.
- **Perpetual animation loop / refresh-rate-dependent speed (Low).** The loop runs only while playing, at a fixed 60 steps/s from a time accumulator. `pagehide` pauses. There is a NaN guard.
- The no-op "fade" stroke was removed, the shadowed `width` parameter renamed, and `import numpy` (unused) removed. The y axis now points up. The landscape colour scale is clamped.
- Text:
  - The intro no longer claims earlier pages used "every data point".
  - The maths uses per-example sums: (1/N)Σ∇ℓᵢ vs (1/B)Σ_{𝓑ₜ}∇ℓᵢ.
  - `st.error` for "Speed" became `st.info`.
  - Batch sizes now read "32–512 for vision, millions of tokens for LLMs". The footer is hedged.
- Iframe height changed from 700 to 760.

#### (b) UI differences to verify
1. Page 56 at load: the pills read η **0.08**, Batch **4**, Momentum **0.50**. Two yellow ★ mark the global minima; there is no dot at the centre.
2. Press **Play**: 4 of the 64 dots light up in a different random pattern each step. The blue (full-batch) ball sits still at loss **2.400**. The pink ball jitters and escapes the start dip about half the time. Reset and replay to see the variation.
3. Set Batch to **1**: it almost always escapes, often to a ★. Set Batch to **16**: it usually stays stuck. Set Batch to **64**: the pink path lies exactly on the blue one.
4. Tick **⚖️ Equal compute** with Batch 1: SGD makes about 64 steps for each full-batch step, and the "examples used" counters stay equal.
5. Pause: CPU goes idle. Speed is the same on 60 Hz and 120 Hz monitors.

#### (c) Not fixed
- The dataset is synthetic (shifted per-example surfaces) rather than a real ML model's data, so that the averaged landscape stays exactly the original valley. It is still genuine mini-batch SGD.


---

## Pages 57–58


Verification run:
- `ruff check --select F,E9,W605,B,PLE --ignore B905` → clean (both files).
- `python -W error::SyntaxWarning` compile → OK (p57 L782 `\)` warning gone).
- AppTest: both pages standalone → no exceptions. Via `app.py` + `switch_page` → no exceptions, and p58's `st.page_link` renders (page `Information_&_Surprise`).
- Headless Edge: the extracted `html_code` was run with scripted clicks and slider inputs. No JS errors. Results: p57 lottery shows `0.000100`, "≈1 in 10,000", 13.288 bits; the slider at −3 lights "Lightning"; p = 1 shows "100.0%". p58: the counters reset on a slider change. Weather [1,0,0,0] gave 300 Sunny draws with an average of 0 bits. After renormalizing, the sum is 1. After 2000 draws, the running mean is 0.884 vs H = 0.881. Particles stay inside the chamber. Mode switches show 0.50 and 25% ×4 in both the slider and the label. AUTO coin mode now logs results.

---

### pages/57Information & Surprise.py

#### (a) Fixes
| Original issue | Fix |
|---|---|
| L782 `"\)"` invalid escape in non-raw string (SyntaxWarning, future SyntaxError) | Escaped as `\\)`, so JS still receives `/[^,]+(?=\))/`. |
| Graph formula text capped at 10 bits (lottery showed "= 10.00 bits"; true 13.29) | The plot position is still clipped at 10; the text uses the uncapped `rawBits` and adds "(off chart)" when > 10. |
| Linear slider made rare probabilities (0.0001–0.01) unreachable | Slider now holds log10(p), from −4 to 0 in steps of 0.001; the label reads "Event Probability (p) · log scale". `p` is displayed with `toPrecision(3)` when < 0.01. |
| "Chance: 1 in N" wrong for p > 0.5 (0.6 → "1 in 2", 0.75 → "1 in 1") | Shows "≈1 in N" for p ≤ 0.5, otherwise a percentage. |
| Preset match tolerance 0.0002 mislabelled p = 0.0002/0.0003 as Lottery and p = 1 as Sunrise | A preset now matches only on an exact log-space match (\|Δlog10\| < 1e-6). |
| rAF loop never cancelled | Stores the frame id; cancelled on `pagehide`. |
| "log is the **only** function" stated without assumptions; independence not stated | Now says the events are **independent**. Explains Cauchy's functional equation: continuous or monotonic → c·log p, "rarer ⇒ more surprising" makes c < 0, and the base fixes the unit. Shows the worked numbers 1 + 2.585 = 3.585 = log2 12. |
| Cross-entropy "exactly" claim; bits vs nats never mentioned | Now: "for a one-hot label this surprise **is** the cross-entropy". Adds a nats note (−ln 0.01 ≈ 4.61 nats = 6.64 bits) and a nat ↔ bit conversion in the Unit bullet. |
| "log2(p) is negative" (it is 0 at p = 1) | Now "≤ 0 … non-negative". |
| `Information ∝ Surprise` loose | Replaced with "less likely ⇒ more surprise ⇒ more information"; Shannon is now called "father of information theory". |
| 99.9999% (text) vs 0.99999 (preset); unsourced Sahara 0.01% | Text now says "about 99.999%" and "(say, 0.01%)". |
| Lottery preset implied real odds | Renamed "Lottery (demo)"; the description gives real Powerball odds (~1 in 292M ≈ 28.1 bits). |
| Sunrise description said "0 bits" | Now "≈0 bits (0.0000144 bits)". |
| Double sixes and Ace of Spades used rounded p values | Now exact 1/36 and 1/52 (displayed % unchanged). |
| `currentEventDesc` written but never read | Removed. Preset descriptions are now shown in the console log when a preset is clicked. |
| Inconsistent surprise tiers (sparks 0.1/2/6 vs flash 0.1/4/8 vs shake 1/4/8) | Shared constants `TIER_BORING`/`TIER_RARE`/`TIER_ASTRO` (0.1/4/8) are used by sparks, flash and shake. The light shake at ≥ 1 bit is unchanged. |
| `addLog` used `innerHTML` with dynamic text | Uses `createElement` + `textContent`. |
| `components.html(..., scrolling=False)` deprecated | Now `st.iframe(html_code, height=670)`. |
| Unused `import numpy` and `components` import | Removed. |

#### (b) UI differences to verify (browser)
1. Page 57 → drag the probability slider: the track is logarithmic. The left quarter covers 0.0001–0.001, and the middle of the track is p ≈ 0.01. The p readout shows 3 significant figures below 0.01 (e.g. `0.000316`).
2. Drag to the far right (p = 1): the caption reads "Chance: 100.0%", not "1 in 1". At p ≈ 0.75 it reads "Chance: 75.0%".
3. Click **Lottery (demo)**: the canvas formula reads `I(0.000100) = -log₂(0.000100) = 13.29 bits (off chart)` and the gauge shows 13.288. The console shows the Powerball caveat.
4. Click any preset: its description appears in the console, followed by the spark log line.
5. Drag the slider to exactly −3 (p = 0.001): the **Lightning** card lights up. Nearby values show "🍀 Custom Event". p = 1 no longer labels itself "Sunrise".
6. Trigger events between 2 and 4 bits (e.g. Coin Flip → drag to p ≈ 0.1): the sparks are now turquoise, matching the turquoise flash. They used to be purple.
7. The "Why a Logarithm?" section shows independence, the Cauchy caveat and the 3.585-bit example. "Bridge to AI" has the nats note.

#### (c) Not fixed / intentionally left
- The x-axis of the I(p) graph is still linear, and points with p < ~0.001 crowd at the left edge. I kept it because the classic −log2 p curve shape is the teaching point. The readout text is exact now.
- The fixed iframe height of 670 with `overflow:hidden` (possible clipping on very narrow screens) is not changed. I couldn't verify it without a visual check, and a responsive redesign is out of scope.
- The HTML/CSS/JS is not extracted into asset files, and the CSS/`addLog` duplicated with p58 is not shared. That would be a structural refactor, not a targeted fix.
- The `Spark` intensity cap of 1.5 is unreachable but harmless, so I left it.
- No hi-DPI canvas scaling and no ARIA text for the canvas (polish).

---

### pages/58Entropy — Average Uncertainty.py

#### (a) Fixes
| Original issue | Fix |
|---|---|
| L1337 non-raw `"…$H = 1\text{ bit}$…"`: `\t` became a TAB, so the LaTeX was broken | All three `st.info/success/warning` strings are now raw (`r"…"`). |
| Hard-coded `file:///d:/physics-simulation/...` link | Replaced with `st.page_link("pages/57Information & Surprise.py", …)`. If the page runs standalone it falls back to a caption on `StreamlitPageNotFoundError`, following the pattern p59/p60 use. |
| Mode switch built sliders **before** resetting the state, so sliders and labels showed old values while computing with the defaults; the coin label was hard-coded "0.50" | The state is reset before `buildSliders()`, and the coin label template uses `${coinP.toFixed(2)}`. |
| Running-average stats never reset, so after any probability change the mean mixed distributions and didn't converge to the dashed H | Added `resetStats(mode)`, called on coin and weather presets, slider input and mode switch. The preset log says "Convergence chart reset", and the page instructions explain why. |
| Particles spawned at y 220–470, but the chamber is at y 200–320; sun and cloud particles drew over the convergence chart | A single `STORM_BOUNDS` is used for both spawning and drawing. Drawing is clipped to the chamber, and faded particles (life ≤ 0) are removed. |
| Coin AUTO (150 ms) never let the toss animation settle, so nothing was logged; the settle log recomputed p (mismatch if p changed mid-toss) | The result is captured at toss time (`pendingCoinLog`). In AUTO it is logged immediately; otherwise it is logged when the animation settles. Shared `logCoinResult()`. |
| `rand <= cumulative` + default index 0 → could pick a p = 0 state or fall back to Sunny on a floating-point shortfall | Uses strict `<` and falls back to the last state with p > 0. |
| Weather surprise label showed "10.00 bits" for p = 0 and silently capped small p | Shows the true −log2 p, or "∞ (never occurs)" for p = 0. The bar is still capped at 6 bits; the comment was corrected ("linear in bits", not "logarithmic scale"). |
| `log2()` helper returned 0 for p ≤ 0 (trap) | Now plain `Math.log2`; every caller already handles p = 0 (convention documented). |
| Normalization: error spread across states, then clamped (could break sum = 1); dead branch | Values are clamped, then divided by their sum. Verified the sum is 1. |
| "ENTROPY EQUILIBRIUM" balance is unrelated to entropy; stale comment (−2.0/−0.6…) | Renamed "PROBABILITY BALANCE (Sunny ↔ Snowy)" with an accurate comment. Added an entropy meter: `H = x of max log₂4 = 2 bits (y%)`. |
| Information Gain = H(Parent) − H(Children) (missing weights) | Now H(Parent) − Σ (\|S_k\|/\|S\|)·H(S_k), with an explanation. |
| "complete chaos; prediction is impossible"; log2 n maximum never stated | Text now gives H = log2 n and says the best guess is right only 1/n of the time. Added a Bounds bullet: 0 ≤ H ≤ log2 n (1 bit for the coin, 2 bits for the weather lab) and the 0·log0 = 0 convention. |
| Cross-entropy "equivalent to shrinking the model's uncertainty" | Now H(p,q) = H(p) + KL(p‖q): minimizing it drives q toward p. That means certainty only for one-hot labels; with soft labels the optimum is q = p. Added a nats note, plus a nat note in the Unit bullet. |
| Weather chart axis labelled "4.0" though H_max = 2; coin chart clipped early averages above 1 | Coin chart max is 1.5 bits (gridline at 1.0); weather chart max is 3.0 bits with a "2.0" tick. |
| Right "Trial #" label showed `max(10, n)` although the line spans the full width | Now shows the actual last trial (`max(1, n)`). |
| Dead state `weatherChamberActive/Tick`, `weatherResultIdx`; stale comment at L640 | Removed or fixed. |
| `addLog` innerHTML with dynamic text; `logBox.innerHTML=''` | Now `textContent` and `replaceChildren()`. |
| `components.html` deprecated; unused numpy import | `st.iframe(html_code, height=670)`; import removed. |

#### (b) UI differences to verify (browser)
1. Page 58 header (via the app sidebar): a **"💡 Revisit Page 57: Information & Surprise"** link appears under the first paragraph, and clicking it opens Page 57. There is no `file:///` link.
2. "Interactive Insights" → the yellow box renders "$H = 1$ bit" correctly (no broken `ext{ bit}`). The blue box mentions $\log_2 n$ and 1/n.
3. Coin mode: click **Mild Bias**, press **Toss Coin** a few times, then drag the slider. The green running-average line and the "Showing latest N of M trials" count reset to 0, and the log says "Convergence chart reset" on presets.
4. Coin mode: press **AUTO**. Result lines now stream into the console; previously it was silent. Press PAUSE.
5. Set the coin slider to 0.9, switch to **Weather**, then back to **Coin**. The slider thumb is at the middle and the label reads 0.50. Do the same in weather mode (e.g. the Sahara preset): after switching away and back, all four sliders and labels read 25%.
6. Weather mode: click **Generate Weather** until ☀️ or ☁️ appears. The sun discs and clouds stay inside the "STORM SIMULATION CHAMBER" box and no longer overlap the convergence chart.
7. Weather mode: drag ☀️ to 100%. The other surprise labels read "∞ (never occurs)", and AUTO only produces Sunny with 0 bits.
8. The right panel title reads "PROBABILITY BALANCE (Sunny ↔ Snowy)", and below it is `H = … of max log₂4 = 2 bits (…%)`. With Pure Chaos it shows 2.000 (100%).
9. Convergence charts: the coin y-axis shows "1.5 b / 1.0 / 0.0" and the weather y-axis "3.0 b / 2.0 / 0.0". The right label is "Trial #<n>".
10. "Bridge to AI": the Information Gain formula has the weighted sum, and the cross-entropy paragraph mentions KL and soft labels.

#### (c) Not fixed / intentionally left
- `buildSliders()` still uses `innerHTML` templates. They are static markup with only numeric or constant interpolation, so there is no injection path. Only the log text (the dynamic part) was moved to `textContent`.
- The rAF loop still runs continuously while visible; it is cancelled on `pagehide` (already present). Making it idle-aware would be a refactor.
- Displayed whole-number percentages can still add up to 99% or 101% (display rounding only; the internal sum is exactly 1).
- Same structural items as p57: fixed iframe height of 670, JS not extracted into assets, CSS/`addLog` duplicated across pages, no hi-DPI canvas scaling.
- The balance visual is kept (renamed and documented) instead of being redesigned into an entropy visual. An explicit entropy meter was added next to it.


---

## Pages 59–60


Verification run:
- ruff (`F,E9,W605,B,PLE`, ignore B905): clean for both files.
- `python -W error::SyntaxWarning` compile: OK for both files.
- AppTest: no exceptions, both standalone and via `app.py` + `switch_page`. Neither page has Streamlit widgets.
- Headless Edge with the embedded HTML, driving `draw()` frame by frame: no JS errors.
  - p59: per-term contributions now add up to the gauge total.
  - p60 Monte Carlo stays within about 1–2 standard errors of the exact value (e.g. Narrow/forward 3.46 ± 0.23 vs 3.449).
  - Spawn rate is the same at 60 Hz and 120 Hz.
  - Shake is disabled under `prefers-reduced-motion`.
- Numbers re-checked in Python:
  - Narrow Q: forward 3.4486 bits, reverse 0.8561 bits.
  - Separated: 31.1504 bits.
  - Slider extreme: 559.27 bits.
  - log2(3) = 1.585.
  - Base-2 gradient = (Q−P)/ln 2.

---

### pages/59Cross-Entropy — Predicted vs Reality.py

#### (a) Fixes

| # | Original issue | Fix |
|---|---|---|
| 1 | `st.info("...$1.585\text{ bits}$...")` was not a raw string, so `\t` became a TAB and KaTeX showed "1.585ext bits" | Made it a raw string; the text now reads `$\log_2 3 \approx 1.585\text{ bits}$` |
| 2 | The per-term contribution capped at 13.288 only when q ≤ 1e-6, while the gauge floored Q at 1e-4. Repro: Near-zero preset, then Rabbit at 50% showed "14.29 + 0 + 0 = 13.29" | One `Q_FLOOR = 0.0001` and one `surpriseBits()` helper are now used by the gauge, the wires, the particles, the term text and the term contributions |
| 3 | The `log2()` −100 floor could never be reached (dead code) | Removed; entropy uses `Math.log2` directly (it was already guarded by p > 1e-5) |
| 4 | The gradient was given as `∂H/∂z = Q−P` while the page uses log₂, and the reason was misstated ("loss → ∞ keeps gradient strong") | Rewritten: Q−P holds for nats with Q = softmax(z). The log cancels the softmax exp, so the gradient is bounded (\|·\| ≤ 1) but does not vanish. Added the base-2 form (Q−P)/ln 2 |
| 5 | Gauge `maxBits = 10`, but cross-entropy can reach 13.29 bits, so the needle stuck at the end | `maxBits = 14`; ticks now go 0…14 |
| 6 | The 0.01% probability was shown as "0%" on sliders and bars | New `formatPct()` shows two decimals for values between 0% and 1% (e.g. "0.01%") |
| 7 | Alert overlay blinked on `tick % 30`, so the rate depended on screen refresh (4–4.8 Hz at 120/144 Hz); no reduced-motion support | Blink is now time-based (fixed 2 Hz from the rAF timestamp). Under `prefers-reduced-motion`: overlay is steady, and screen shake, needle jitter, wire vibration, lightning and card hover-lift are all off (CSS media query + JS check) |
| 8 | The rAF loop ran forever, including off-screen, with no cleanup | `scheduleDraw()` and an IntersectionObserver pause the loop when the lab is scrolled out of view; a `pagehide` handler cancels the frame |
| 9 | The canvas was fixed at 600px; the clear used device pixels inside a scaled context | Canvas is now `width:100%` (max 600px, centred, aspect kept), DPR capped at 2, and the clear uses 600×500 |
| 10 | Log text was inserted with `innerHTML` | Now uses `span.textContent` |
| 11 | Link to page 58 was `file:///d:/physics-simulation/...`, which only works on the author's machine | `st.page_link` to the real page-58 file, through a `nav_link()` helper that falls back to a caption when the page is run on its own (sibling pages aren't registered then). Added a "Continue to Page 60" link |
| 12 | `components.html` is deprecated in Streamlit 1.67 | `st.iframe(html_code, height=790)` |
| 13 | Unused code: `numpy` import, `components` import, `pColors` in `updateSlidersUI`, `baseFlowSpeed`, `rowY`/`labels`/`logStr` in `drawMathSection` | Removed |
| 14 | Label smoothing "preventing overfitting!"; footer said "distance between reality and expectation" and called KL a "distance metric" | Softened to "often improves calibration and generalization (not a guaranteed cure)"; footer now says "mismatch" / "measure of the gap" |

#### (b) UI differences to verify (browser, open via `streamlit run app.py`)

1. Top of the page, below the intro: a "↩️ Revisit Page 58…" link that opens page 58. Bottom of the page: "➡️ Continue to Page 60…".
2. Under "Interactive Lessons & Warnings", the blue Ignorance box reads "log₂3 ≈ 1.585 bits" with no stray "ext".
3. Lab, Q preset **Near-zero Limit**:
   - The Q(Cat) slider label and the right-hand bar both read **0.01%** (previously 0%).
   - The gauge needle sits near 13.29 on the new 0–14 scale, not stuck at the end.
4. Then drag **Prediction Q(Rabbit)** to about 50%. The bottom row reads `1.00 × 13.29 = 13.29 bits` and `Loss Total: 13.29 + 0.00 + 0.00 = 13.29 bits` (previously 14.29 vs 13.29).
5. Meltdown (Confident Wrong / Near-zero): the red overlay and warning blink about twice per second on any monitor.
6. With OS "reduce motion" on (Windows: Settings → Accessibility → Visual effects → Animation effects off): no shake, no needle jitter, no lightning, and the warning stays steady.
7. Scroll the lab out of view, then back: the animation resumes. CPU should drop while it is off-screen (DevTools Performance).
8. Bridge-to-AI section 1: the gradient now says nats, shows the (Q−P)/ln 2 bits version, and describes the gradient as bounded but non-vanishing.

#### (c) Intentionally not fixed

- `innerHTML` in `buildSliders()`: static templates from constant arrays and numbers only, with no dynamic or user text. Left as is.
- Particles, sparks and energy flow still move per frame, not per second. Purely cosmetic; only the alert blink needed to be time-based.
- Small rounding mismatch in "Loss Total" (each term is `toFixed(2)`): at most ±0.01, which is normal display rounding.
- The iframe height (790) was not changed. The left-panel layout is the same as before.
- Shared CSS/JS duplication with pages 57/58/60 (the `addLog`, `Spark` and card styles): splitting it into a shared module would touch other pages, so it is out of scope.

---

### pages/60KL Divergence — Gap Between Distributions.py

#### (a) Fixes

| # | Original issue | Fix |
|---|---|---|
| 1 | VAE heading said "Forward KL", but D_KL(Q(z\|x)‖N(0,I)) is model‖target, which is **reverse** under the page's own convention (P = target, Q = model) | Heading is now "Reverse KL". Added a note that VI in general minimizes the reverse KL(Q‖P), hence mode-seeking and variance under-estimation |
| 2 | RLHF section called D_KL(Q_θ‖P_base) a "Forward KL" | Now called reverse KL, D_KL(Q_θ‖P_ref) |
| 3 | RLHF objective took the expectation with `x, y ∼ D` (responses from the dataset) | `E_{x∼D}[ E_{y∼Q_θ(·\|x)}[Reward] − β·D_KL(Q_θ(·\|x)‖P_ref(·\|x)) ]`, with text explaining that y is sampled from the policy |
| 4 | Claimed the KL anchor maintains "factual integrity and safety"; the reference was called the "frozen base pre-trained model"; GPT-4/Claude + PPO claim | Now: the anchor helps keep outputs fluent and makes reward hacking harder, but doesn't guarantee facts or safety. Reference is "typically the SFT model". Removed the vendor-specific claim |
| 5 | Tank showed **"Inf 🌋"** for any value above 15 bits, so Separated (31.15 bits, finite) looked infinite while the MC box showed about 31 | Tank shows the real value (`formatBits`, e.g. "▲31.2", "▲559"); the ▲ means it is above the 8-bit fill scale |
| 6 | Narrow Q log message said "Infinitely penalizing Forward KL!" (true value 3.45 bits) | "Forward KL ≈ 3.45 bits vs Reverse ≈ 0.86 bits. (Infinite only if Q were exactly 0 where P > 0.)" Preset card subtitle "Exploded" → "High fwd KL". The asymmetry text also notes that for Gaussians the forward KL stays finite |
| 7 | Droplets already in flight when a preset/slider/mode changed still added their old values to the fresh statistics and flew to the other tank | `resetSamples()` clears the statistics **and** the in-flight droplets and bubbles on every preset, slider or mode change. Changing the drop rate no longer resets the statistics (same distribution) |
| 8 | The Monte Carlo value was a sliding window of the last 100 samples, so it never converged, yet the text promised convergence | Cumulative running mean using Welford's algorithm. The box shows `Samples so far: n`, `Emp: mean ± SE`, `Exact: … bits` and a "± = 1 std. error (shrinks ~1/√n)" note. Intro text updated to match |
| 9 | Meltdown banner always said "TAIL ZERO AVOIDANCE PENALTY", even in reverse mode | Banner text now depends on the mode: forward "Q TOO THIN WHERE P LIVES (ZERO-AVOIDING PENALTY)", reverse "Q PUTS MASS WHERE P IS RARE (ZERO-FORCING PENALTY)" |
| 10 | `const boxW = tkWidth = 94;` created an undeclared global | Removed |
| 11 | `getIntegrand(x, mu1, …)` ignored its parameters and read globals | Now takes generic (A, B) parameters; the caller passes (P, Q) for forward and (Q, P) for reverse |
| 12 | Drop rates "2/6/15 per second" assumed 60 fps (`tick % N`); blink used `tick % 32` | Spawning uses a time accumulator and the real rAF timestamp (dt clamped to 100 ms). Blink is a fixed 2 Hz. Verified the same rate at 60 Hz and 120 Hz |
| 13 | No reduced-motion support | CSS media query turns off shake and hover-lift; JS turns off screen shake, blinking and tank pulsing |
| 14 | Pdf peaks above 1.2 (σ = 0.3 peaks at 1.33) and integrand bars above 3 were clipped silently | Pdf axis cap is now 1.4 with a 1.2 grid line. Clipped integrand bars get a white end marker and an "▪ = off scale (bar clipped)" legend |
| 15 | Invalid escape `"\m"` (and `"\s"`) in a non-raw string: SyntaxWarning now, SyntaxError in a future Python | Raw string; the new `1/\\sqrt{n}` is escaped |
| 16 | `file:///d:/...` link to page 59 | `nav_link` → page 59 at the top, page 61 at the bottom (exact filenames) |
| 17 | `components.html`; Google Fonts `@import` (external request, fails offline); log `innerHTML` | `st.iframe(html_code, height=830)`; system font stack; `textContent` |
| 18 | Unused code: `numpy`, `components`, `plotHeight2`, `maxHistorySize`, tank `label`/`sub` fields | Removed (`drawDetailsPanel` now uses its `klPQ`/`klQP` arguments for the "Exact" line) |
| 19 | Overstatements: "Q will pick just one mode … completely ignoring"; footer "central metric of LLM safety" | "tends to lock onto one mode (well-separated modes) … largely ignoring"; footer toned down |

#### (b) UI differences to verify (browser, via `streamlit run app.py`)

1. Top of the page: a "↩️ Revisit Page 59…" link. Bottom: "➡️ Continue to Page 61: Eigenvectors…". Both navigate.
2. The lab title/body font is now the system UI font, not Inter. No request to fonts.googleapis.com in the DevTools Network tab.
3. Preset **Separated**: both tanks show **▲31.2** (not "Inf 🌋"). The Monte Carlo box shows `Exact: 31.2 bits` and, after about 10 s, `Emp: ~31 ± ~0.5`.
4. Preset **Narrow Q**:
   - The log says "Forward KL ≈ 3.45 bits vs Reverse ≈ 0.86 bits…".
   - The card subtitle reads "High fwd KL".
   - The tanks read 3.45 / 0.86.
5. Set Drop Rate to High-Speed, wait 20 s, and watch "Samples so far" keep rising past 100 while the ± shrinks. Then click **Reverse KL**:
   - The count resets to 0.
   - No old cyan droplets fly to the pink tank.
   - "Sampling x from: Q(x)" is shown.
6. Change Drop Rate (Normal ↔ Fast): the sample count is **not** reset.
7. Drag σ_Q to 0.30 with μ_Q near μ_P:
   - The amber curve peak is no longer flattened at the top.
   - With Separated or extreme sliders, the clipped red bars show white end markers and the legend "▪ = off scale (bar clipped)".
8. Separated in Reverse mode: the banner reads "HIGH REVERSE KL: … ZERO-FORCING PENALTY". In Forward mode it reads "HIGH FORWARD KL: … ZERO-AVOIDING PENALTY". It blinks about twice per second.
9. OS "reduce motion" on: no shake, the banner is steady, and the tank colour doesn't pulse.
10. Bridge-to-AI: VAE heading says "Reverse KL" with an explanatory note. The RLHF formula shows `x∼D` and `y∼Q_θ(·|x)` and says "reverse KL" and "reference model", with no safety guarantee.
11. Text above the lab: μ and σ render as Greek letters, and the 1/√n renders.

#### (c) Intentionally not fixed

- Droplet, bubble and spark motion is still per frame (purely visual; sample timing and statistics are now time-based).
- The canvas `textBaseline` set in `drawLiquidTanks` still carries over to later draws (it already did before). The layout was tuned around it; `drawDetailsPanel` now sets its own baseline explicitly.
- The tank fill scale stays capped at 8 bits (the ▲ prefix marks values off the scale) to keep the visual readable.
- The iframe height (830) is unchanged.
- Duplicated shared CSS/JS (`addLog`, `Spark`, card styles) with pages 57–59 is not refactored; that would touch other pages.


---

## Pages 61–62


Verification run: ruff (F,E9,W605,B,PLE) clean; `python -W error::SyntaxWarning` compile OK; AppTest headless — no exceptions
(neither page has Streamlit widgets, so there are no session_state/widget keys to prefix). The embedded JS was run in headless
Edge with scripted calls to every preset, challenge level, and edge case: 0 JS errors. A Python port of the new
`updateEigenvectors` was checked on 923,521 slider-grid matrices against numpy:
0 failures (31 scalar, 288,322 complex, 631,504 two-eigenvector, 3,664 defective single-eigenvector cases).

---

### pages\61Eigenvectors — Vectors That Don't Rotate.py

#### (a) Fixes
| Original issue | Fix |
|---|---|
| **High**: scalar matrices (Identity = default preset, any a=d, b=c=0) drew only the x-axis eigenvector; v at 34° (Av=v) was reported "not aligned". | `updateEigenvectors` detects A = λI → `scalarLambda`; banner shows "A = λ·I: EVERY nonzero vector is an eigenvector!", the line through v is drawn as an eigen-line, particles fire for any v. |
| Med: the dedupe (`dot > 0.999 → pop()`) dropped a real eigenvector of diagonalizable matrices with close distinct λ (e.g. [[1,3],[0,1.1]]). | Dedupe removed. Alignment now picks the **closest** eigen-line within tolerance instead of the first. |
| Med (CONFIRMED prior): complex eigenvalues shown as "No real eigenvectors… Space is rotating completely" / "No Real Eigenvalues". | Computes complex pair `re ± im·i`; banner: "Complex eigenvalues λ = α ± βi — no REAL eigenvector: every real direction gets turned. (The eigenvectors have complex entries…)". Challenge labels updated likewise. |
| Med: aligned banner said "(Does not rotate!)" also for λ<0 (flip) and λ=0 (Av vanishes). | New `describeLambda()`: λ≈0 → "A·v = 0 … COLLAPSED onto the origin"; λ<0 → "stays on its line but FLIPS to the opposite side (×|λ|)"; else "stays on its line (no rotation!)". Defective case gets its own hint ("Repeated λ but only ONE eigenvector line"). |
| Med: Challenge Mode could be auto-solved with AUTO-SWEEP; lock progress accumulated across passes ("Hold it steady" not enforced). | Sweep button disabled (with tooltip) in Challenge Mode and `toggleSweep` refuses to start there; progress of an unlocked eigenvector resets to 0 when alignment is lost. |
| Med: "784 pixels down to just 2 dimensions without losing its core information". | Reworded: a few dozen components keep most variance; 2 components are only a rough visual map. |
| Med: "This polynomial is called the characteristic equation" with no polynomial shown. | Added λ² − (a+d)λ + (ad−bc) = 0, the trace/determinant quadratic formula, and the 3 discriminant cases (two lines / scalar-vs-defective / complex). |
| Med (CONFIRMED prior): "eigenvalues > 1 → exploding, < 1 → vanishing" for weight matrices. | Rewritten: eigenvalue |λ| rule holds for a repeated matrix (RNN); in general singular values govern stretch; init/normalization keep stretch factors ≈ 1. |
| CONFIRMED prior: invalid escape `"\l"` (old L1562, PageRank paragraph). | `$\\lambda = 1$`; compile with `-W error::SyntaxWarning` passes. |
| Low: particles froze mid-air when interaction stopped. | Short rAF loop (`particleFrame`) keeps fading particles animating; skipped while sweep runs; cancelled on `pagehide`. |
| Low: sweep restarted from a hard-coded 34°. | Sweep starts from the current angle slider value. |
| Low: Av could leave the canvas silently. | Edge marker dot + "Av off-screen ➜" label when the tip is outside the canvas. |
| Low: `$$\mathbf{A v = \lambda v}$$` (λ not bold, inconsistent). | `$$A\mathbf{v} = \lambda \mathbf{v}$$`. |
| Low: intro said directions "only get scaled (stretched or squished)". | Mentions flip / collapse and that rotations have no real eigen-directions. |
| Low: preset button stayed highlighted after manual slider edits. | Slider `oninput` calls `clearPresetHighlight()`. |
| Convention: `components.html(height=750, scrolling=False)` clipped content (measured ≈760 px wide layout, ≈812 px at 950 px width). | `st.iframe(html_code, height=900)`; removed `streamlit.components.v1` import. |
| Convention: Google Fonts `@import`. | Removed; system font stack in CSS and canvas fonts. |

#### (b) UI differences to verify
1. Open page 61 → sandbox loads with **Identity**: banner is green "🌟 A = 1.00·I: EVERY nonzero vector is an eigenvector!…", a dashed green line passes through the yellow v. Drag v anywhere → stays green.
2. Click **Shear** → one dashed line (x-axis) and banner "Repeated λ but only ONE eigenvector line (defective matrix)…".
3. Click **Rotation** → banner "⚠️ Complex eigenvalues λ = 0.00 ± 1.00i — no REAL eigenvector…".
4. Click **Reflection**, set angle slider to 135° (or −45°) → banner "A·v = -1.00v — stays on its line but FLIPS…".
5. Click **Collapse**, set angle ≈ −63° → banner "A·v = 0 (λ = 0): this direction is COLLAPSED onto the origin".
6. Set sliders a=1, b=3, c=0, d=1.1 → **two** close dashed lines (λ=1.10 and λ=1.00) are drawn; the preset highlight disappears when moving a slider.
7. Set a=b=c=d=3, length 3.5 at 45° → pink arrow leaves the canvas; a pink dot + "Av off-screen ➜" appears at the edge.
8. Switch to **Challenge Mode** → AUTO-SWEEP button greyed out (tooltip explains). Align v with an eigenvector, then move away before it locks → the progress bar drops to 0.
9. Explore Mode, rotate the angle slider to e.g. 90°, press AUTO-SWEEP → sweep continues from 90° (no jump to 34°). Stop moving while aligned → green particles fade out instead of freezing.
10. Below the sandbox: "How to Solve" now shows the explicit 2×2 characteristic polynomial, λ formula and the three discriminant cases; AI cards have the softened PCA text and singular-value gradient text. Sandbox is no longer clipped at the bottom (iframe 900 px).

#### (c) Intentionally NOT fixed
- Prior finding "defective matrix may show two directions" — marked **WRONG** in the review; nothing to fix.
- Splitting the 1,690-line file / moving HTML to an asset shared with p62: structural refactor outside "targeted changes".
- Iframe height is fixed (900 px); at very narrow widths (<900 px, stacked layout ≈1,400 px) the iframe scrolls internally rather than growing.
- Eigenvalue text labels of two nearly-collinear eigenvectors may overlap (cosmetic).

---

### pages\62Eigenvalues — How Much Do They Stretch.py

#### (a) Fixes
| Original issue | Fix |
|---|---|
| PARTLY (prior) / Med: "λ > 1 GROWS" badge stayed off for λ = −1.8 ("Flip + Grow" preset). | Badges now: "\|λ\| > 1 GROWS", "λ = 1 SAME", "0 < \|λ\| < 1 SHRINKS", "λ < 0 FLIPS", new "λ = 0 COLLAPSES". λ = −1.8 lights GROWS + FLIPS. `classifyLambda` reports "FLIPS backward and GROWS/SHRINKS", gap-free ordering. Intro adds a sign-vs-size summary sentence. |
| Med: equation box showed "Av = 2.00v" even when v was off the eigen-direction. | Off-axis it shows "Av ≠ λv" + "v is not on an eigen-direction, so Av is not a scaled copy of v"; "Av = λv" only when aligned. |
| Med: Stretch-O-Meter needle used \|λ\|/2.5 while labels 0…2+ were evenly spaced (\|λ\|=1 at 40% vs label at 50%); red gradient at 0 suggested "flip". | Needle = \|λ\|/2 (clamped); labels absolutely positioned at 0/25/50/75/100 %; gradient slate→purple→blue→green (collapse→shrink→same→grow). |
| Med: 2D off-axis badges/needle used the meaningless average (\|λ₁\|+\|λ₂\|)/2. | Off-axis 2D lights the union of badges of λ₁ and λ₂; needle dims (`.idle`) because no single \|λ\| applies. |
| Med: 1D mode at λ = 1 (default preset = identity) told the user to "Drag v onto the horizontal axis". | 1D λ=1 treated as scalar transform: "✓ Every nonzero direction is an eigen-direction!". |
| Med (CONFIRMED prior): "Tiny λ directions are mostly noise — safe to drop". | Reworded: dropping them loses little variance, but low variance ≠ noise; scaling matters. |
| Med (CONFIRMED prior): "eigenvalues > 1 everywhere explode / all λ < 1 vanish / keep λ near 1". | Rewritten: \|λ\| rule only for a repeated matrix (RNN); singular values govern general stacks; init keeps stretch ≈ 1. |
| Low-Med: mini λ bars: origin at x=110 vs track centre 130; λ=2 bar ran past the 260 px canvas. | Origin at `w/2` with a tick, half-width scale, bar never exceeds the track. |
| Low-Med: touch drag had no min-length guard (zero vector counted as "aligned"); mouse guard snapped v onto the x eigen-axis (fake alignment). | Shared `setVFromCanvas()` clamps length to 0.15…3.5 **keeping direction**, ignores exact zero; alignment also requires ‖v‖>0. |
| Low: "ellipse whose width and height are exactly \|λ₁\| and \|λ₂\|". | "semi-axes (half-width and half-height)". |
| Low: "‖Av‖ is exactly twice ‖v‖" (tolerance 0.08 rad). | "≈ twice (exactly 2× when v lies exactly on the axis)"; shrink scenario now says "align v… only 40% as long". |
| Low: pulse + particle rAF ran two draws per frame. | Particle redraw loop skipped while `pulseOn`. |
| Low: parameter `b` shadowed by `forEach(b => …)` in `setMatrix2d`. | Renamed to `btnEl`. |
| Low: "unit circle → ellipse" legend shown in 1D mode (no ellipse). | Legend item hidden in 1D mode. |
| Low: `$\|\lambda\|$` in a markdown table (may render as ‖λ‖). | `$\lvert\lambda\rvert$`. |
| Convention: `components.html(height=820, scrolling=False)` clipped 2D mode (1D content ≈775 px + mini bars ≈125 px). | `st.iframe(html_code, height=920)`; import removed. |
| Convention: Google Fonts `@import`. | Removed; system font stack. |

#### (b) UI differences to verify
1. Open page 62 (1D, λ = 1 preset) → banner "✓ Every nonzero direction is an eigen-direction! λ ≈ 1…", badge "λ = 1 SAME", needle exactly under the "1" label (middle).
2. Click **λ = 2** → v is off-axis: equation box shows "Av ≠ λv" with the grey explanation; GROWS badge on; needle at the "2+" end. Drag v onto the x-axis → "Av = 2.00v", ratio 2.00.
3. Click **λ = −1.8** with v on the x-axis → banner "λ < 0 — direction FLIPS backward and GROWS!", badges GROWS **and** FLIPS lit, needle at 90 %.
4. Click **λ = 0** with v on the x-axis → new "λ = 0 COLLAPSES" badge lights, needle at 0.
5. **2D Matrix View** → legend shows "unit circle → ellipse" (hidden again in 1D). Default λ₁=2: left mini bar starts at the centre tick and stays inside the track. Off-axis: badges show union (e.g. Flip X: GROWS+SHRINKS+FLIPS), needle dimmed.
6. **Uniform Grow** → "Every nonzero direction is an eigen-direction!" for any v.
7. On a touch device / mouse: drag v onto the origin → it stops at a short length but keeps its direction (no jump onto the x-axis, no false "On eigen-direction").
8. Below the lab: table row λ<0 shows |λ| (single bars), "semi-axes" wording, revised PCA and Gradient Stability cards. 2D mode no longer clipped (iframe 920 px).

#### (c) Intentionally NOT fixed
- 2D lab stays diagonal-only (no non-diagonal, defective or complex matrices) — would be a feature addition; page 61 now covers those cases and the characteristic-equation discussion.
- Alignment tolerance (0.08 rad vs p61's 0.05) left as is; copy now says "≈".
- Shared JS helpers with p61 (drawArrow, drag, particles) not extracted — refactor out of scope.


---

## Pages 63–64


Files changed:
- `pages\63PCA Intuition — Finding the Best Angle.py` (modified)
- `pages\64A Single Neuron.py` (modified, now the only page 64)
- `pages\64A Single Neuron2.py` (deleted from disk; not `git rm`)

How it was checked: ruff (`F,E9,W605,B,PLE`, ignoring B905) passes; `python -W error::SyntaxWarning` compile passes; AppTest fuzz with all sliders at their extremes, every selectbox option and every button showed no exceptions (64: 26 runs; 63 has no Streamlit widgets). A targeted AppTest of the cat case study checked every z value in the bias lesson. Headless Edge loaded both iframe HTML documents with an `onerror` hook and drove every mode, preset and activation: no JS errors. Screenshots checked the canvases. A live `streamlit run` checked with Chrome DevTools Protocol that `st.iframe(height="content")` sizes itself: page 63 is 759 px at 1400 px wide and 1327 px at 800 px wide; page 64 is 1686 px. All scratch files were deleted afterwards.

---

### 1. `pages\63PCA Intuition — Finding the Best Angle.py`

#### (a) Fixes
| Original issue | Fix |
|---|---|
| The slider was set to the PC1 angle on load and on every cloud change, so the exercise started solved and "🎯 maximum spread" lit up at once. | `setCloud` now puts the slider at PC1 + 60° (mod 180). |
| Going PCA/Squash → Sweep left `theta` at PC1 while the slider showed another angle. | The Sweep branch of `setMode` calls `onAngleInput()`, which reads theta back from the slider. The unused `theta = pcaInfo.angle` lines were removed. |
| The 1D strip re-scaled itself at every angle, so the spread never looked different. | The strip uses a fixed scale per cloud (`maxR` = largest distance from the mean) and draws a yellow ±1 std bracket with its value. The points are one colour (the old rainbow-by-index had no meaning). |
| Unseeded `Math.random()`; the round-cloud wording overstated how equal the spread is. | Seeded PRNG (mulberry32, seed starts at 1), so the cloud is the same on every load. New **🎲 New random sample of this shape #n** button. A yellow note under the Round Cloud explains that its PC1 is sampling noise. The Python text now gives the measured spread ratios (typical best/worst ≈ 1.3×, up to ≈ 1.7×, from a 20k-run simulation with n=90). |
| Lost variance and reconstruction error were never shown. | New metric card in PCA and Squash modes: "Lost by squashing onto PC1: λ₂ = …, x% of the variance · mean squared reconstruction error = …" (computed from the points as (1/n)Σ(x·v₂)²). The Eigenvalue column now explains that the loss is λ₂ and that MSE = (n−1)/n·λ₂. |
| `components.html(height=900, scrolling=False)` clipped the stacked layout below 920 px. | `st.iframe(html_code, height="content")`, which auto-sizes (checked in a real browser). |
| Google Fonts `@import`, a third-party request the earlier "security fix" commit missed here. | Removed; system `sans-serif` everywhere, canvas fonts included. |
| "BEST!" matched within 2 % of the max variance (about a ±8° band, ~40° on round clouds). | "BEST!" and "🎯" now need the axis within 1.5° of PC1 (lines are undirected, so the comparison is mod 180°). |
| The "vs. worst angle" ratio read about 166× on the diagonal cloud (λ₂ ≈ 0.04). | Replaced by **Share of max spread** (%) = var(θ)/λ₁. |
| "It peaks twice per full rotation", but the sweep only covers 0–179°. | Reworded: the sweep only needs 0–180° because θ and θ+180° are the same line. |
| `onAngleInput(updateSl)` had an unused parameter; `minVar` was unused. | Both removed. |
| "uncorrelated components (orthogonal axes)" | Now says the covariance is diagonal in PC coordinates, and that uncorrelated is weaker than independent. |

#### (b) UI differences to verify
1. Open page 63. The slider shows about 92° (not 32°), the 🎯 tag is off, and "Share of max spread" is well below 100 %. Drag toward about 32°: at the peak, "BEST!" and 🎯 appear and the share reads about 100 %.
2. Drag the slider to e.g. 10°. Click **✨ True PCA Axes**, then **🔄 Sweep Angle**. The blue axis is back at 10°, matching the slider label and the yellow dot on the curve.
3. In Sweep mode, rotate the slider: the dots in the "1D projection" strip spread wide near PC1 and bunch together near PC2, and the yellow "±1 std = …" bracket changes width.
4. Click **Round Cloud**: a yellow note appears. Click **🎲 New random sample** a few times: the counter goes #2, #3, … and the PC1 angle jumps. Reload the page: the diagonal cloud is the same as before (seed #1).
5. Click **✨ True PCA Axes** or **🗜️ Squash to 1D**: the pink card "Lost by squashing onto PC1" shows λ₂, the % lost (≈ 0.7 % on the diagonal blob, ≈ 40–50 % on the round cloud) and the reconstruction MSE.
6. Make the browser narrower than ~920 px: the lab stacks into one column and the iframe grows to fit (no clipped bottom, no inner scrollbar).
7. In DevTools → Network, no request goes to fonts.googleapis.com.

#### (c) Merge
Not applicable.

#### (d) Intentionally not fixed
- The "Spread vs. angle" curve still uses integer degrees, so its peak marker can be up to 0.5° from the exact PC1 angle (cosmetic).
- The legend still says "Your axis" in PCA/Squash modes, where the axis is fixed to PC1 (cosmetic).

---

### 2. `pages\64A Single Neuron.py` (canonical page 64)

#### (a) Fixes to the JS lab
| Original issue | Fix |
|---|---|
| **High:** `const proj = (dot / (wLen*wLen)) * wv;` (number × array) gave NaN, so the "proj" arrow was never drawn. | `drawProjection()` computes `proj = [k·w₁, k·w₂]` with `k = w·x/‖w‖²` (guarded for w = 0). x, w and proj share one auto-fitted scale (the old 0.7 factor on w was removed). Added arrowheads, a faint line along w, a dashed perpendicular from x to proj, and the label "x₁,x₂ slice: w·x = … (x₃ and b not shown)". |
| Negative contribution bars were drawn down from the bottom and clipped. | `drawBars()` draws from a middle zero line; value labels sit above or below each bar. |
| Activation plot: the "axis" line sat at y = 0.25, ReLU/linear ran off the canvas, z was fixed at ±4 so the "your z" dot vanished. | `drawActivationCurve()` sizes the z-axis to ±max(4, ⌈1.15·\|z\|⌉), uses a y-range per activation, draws the axes at the real z = 0 and y = 0, clamps values and labels the z range. |
| Game preset had `Homework done` with weight −1.5 (story backwards). | Weight is now +1.5 and the label says "Share of homework done". |
| "Page 66 shows why stacking layers…" (there is no page 66). | Now points to **Page 67**, which does contain the "collapses into a single affine map" explanation. |
| Contributions mode was identical to Signal Flow except for a label. | Contributions mode now shows a **waterfall** (0 → +w₁x₁ → +w₂x₂ → +w₃x₃ → +b = z) in the small canvas and a "Biggest influence on z" box on the main canvas. Signal Flow keeps the simple per-input bars. |
| Preset defaults weren't on the slider step grid (slider position ≠ displayed value). | Each input has its own step (`inStep`): counts and yes/no inputs are integers ("!!! count" 0–5 step 1; "Unknown sender (0/1)"; "Friend invited (0/1)"; coffee cups step 1; homework hours step 0.25). The defaults were changed to land on the grid. New preset numbers (checked in Python): study z = 0.24 (σ = 0.56, yes), spam z = 1.82 (0.86, spam), game z = 0.91 (0.71, play). |
| Each preset decided "yes" when y > 0.5, which for ReLU/Linear meant z > 0.5. | One rule for every activation: **yes when z ≥ 0** (same as σ ≥ 0.5, tanh ≥ 0, step = 1). It is stated under the Decision card and as pipeline step ⑤ ("z ≥ 0 → …"). |
| No caveat about probabilities. | The Output card and pipeline step ④ name the output type ("probability-like, not calibrated", "unbounded score ≥ 0", …). The Decision card says the output is not a calibrated probability. |
| Pulse glow was dead code; the pulse moved in a straight line on curved edges; the sum pulse started before input 3 arrived. | The pulse follows the quadratic Bézier with a real glow. New timeline: inputs 0–0.7 (staggered), sum→activation 0.7–0.85, activation→output 0.85–1.0. The animation runs slower (step 0.01). |
| Stopping FIRE left pulses frozen on screen. | `toggleFire()` cancels the animation frame and redraws. |
| Math overlay covered the first input node; weight labels were clipped at the left edge; "z=" overlapped "weighted sum". | Overlays moved to the empty lower-right area; weight labels sit centred above each input node; the z label moved down. |
| `ctxM.textAlign` leaked between modes. | Reset in `drawMini()`. |
| Unused `xLen`, `thresh`; sliders built twice at startup; `innerHTML +=` inside the loop. | Removed; the HTML is built once per preset. |
| No tanh. | Added a **Tanh** activation (the activation grid is now 3 columns). |
| `components.html(height=920, scrolling=True)` | `st.iframe(html_code, height="content")`. `import streamlit.components.v1` removed; `import math` added. |

#### (a) Python text fixes
- Step 5 of the intro: "squash … nonlinear" became "(usually nonlinear) function" (Linear is an option in the lab). The Weight row of the math table now says size \|wᵢ\| and sign. A paragraph says only sigmoid is probability-like, and not calibrated.
- Biology table: added dendrites/soma/spike wording, inhibitory synapses, and bias sign (b > 0 can fire with zero input; b < 0 needs evidence).
- "Three things to try" texts describe the new waterfall and projection views.

#### (b) UI differences to verify
1. Page 64, lab: click **🔢 Dot Product**. The small right canvas now shows three arrows (green x, yellow w, light-yellow **proj**) with a dashed perpendicular. Set w₁ = 3, w₂ = 0: proj lies along the horizontal axis with length x₁.
2. Study preset, Signal Flow mode: the red w₁x₁ = −1.26 bar points *down* from a middle line and is fully visible with its value.
3. Click **📊 Contributions**: the small canvas shows a waterfall ending in a blue **z** bar, and the main canvas shows "Biggest influence on z: Tiredness: w₁x₁ = −1.26 …" in the lower-right corner without covering any node.
4. Choose **ReLU**, raise "Homework hrs" to 3 and w₂ to 3: the activation plot rescales (labels "z = −10 … +10") and the yellow "your z" dot stays on screen. With Sigmoid, the plot's horizontal line passes through y = 0 and the vertical line through z = 0.
5. Click **🎮 Should I play outside?**: w₂ on "Homework done" is **+1.50**; raising homework done increases z.
6. Spam preset: "!!! count" and "Unknown sender (0/1)" sliders move in whole steps; the value shown always matches the knob.
7. Press **⚡ FIRE**: pulses follow the curved edges, the Σ→activation pulse starts only after all three input pulses arrive, and pressing **⏹ STOP** clears the pulses.
8. The Decision card shows the "z ≥ 0" rule text; pipeline step ⑤ reads "z ≥ 0 → …". Choose **Tanh**: the output label reads "between −1 and 1".
9. The Bridge section's third card mentions **Page 67**, not Page 66.
10. Scroll to **2) Case Study: Build a Cat Detector 🐱** (see section 2c).

#### (c) Merged from v2 (`64A Single Neuron2.py`)
New Streamlit section **"2) Case Study: Build a Cat Detector 🐱"** (`render_cat_case_study()`). All widget keys are `p64_`-prefixed: `p64_x1..3`, `p64_w1..3`, `p64_b`, `p64_act`, `p64_animal_<i>`, `p64_design_<key>`. Widgets use only `key` plus `session_state` defaults (no `value=`, so no duplicate-default warning), callbacks set the values through `on_click`, and there is no `st.rerun()`.
- **5 animal presets** (Siamese Cat, Golden Retriever, Fluffy Bunny, Majestic Lion, Robo-Dog) with v2's feature values and descriptions. They are now **full presets**: each loads the features and resets the neuron to the starting design w = (4, 5, −8), b = −3, Sigmoid.
- **3 design buttons:** ① Starting design (b = −3), ② Bias-only fix (b = −8.7), ③ Re-weighted fix (w = (0, 10, −8), b = −9.5).
- Sliders for x (0–1, step 0.05), w (±10, step 0.5), b (±15, step 0.1), and an activation selectbox (Sigmoid, Binary Step, ReLU, Tanh).
- **Step-by-step numeric breakdown** of z and a, with the formula, value and decision rule, shown in an `st.code` block (no KaTeX inside raw HTML).
- **Caveats:** output type per activation ("probability-like but NOT calibrated", "unbounded", …) and "toy rule, not a validated real-world cat classifier". When the inputs match a preset, the verdict shows truth vs. prediction (✅/❌).
- **Corrected bias lesson** ("💡 Why bias alone can't fix the Bunny"). It shows the live ranking of w·x under the starting weights (Siamese +9.0 > Bunny +8.5 > Lion +8.2 > Robo-Dog −2.3 > Retriever −6.6). Because bias shifts everyone equally, it can't reorder that ranking. A live table gives z and ✅/❌ for all 5 animals under the 3 designs plus "Your sliders". Values, checked in Python and AppTest:
  - start: Siamese +6.0 ✅, Bunny +5.5 ❌, Lion +5.2 ✅
  - bias-only (b = −8.7): Bunny −0.2 ✅ but Lion −0.5 ❌
  - re-weighted: Siamese +0.5 ✅, Lion +0.5 ✅, Bunny −0.5 ✅, Robo −14.9 ✅, Retriever −15.5 ✅

  It notes that the margin is only ±0.5 because Bunny and cats differ by just 0.1 in whisker length, so better features would help more than better weights.
- **Biology vs. artificial:** the "loosely inspired, not one-to-one" wording, action potential = all-or-nothing (≈ step), graded sigmoid/tanh/ReLU, extra operations like attention. Lives in an expander "Where the analogy breaks" under Biology ↔ Math.

**Dropped from v2:**
- The global CSS block. It forced `.stApp`/sidebar/`.stMarkdown span` colours with `!important`, which broke colour-coding and slider tracks; the page now relies on the app's dark theme.
- The sidebar controls (everything sits in the section now).
- The hand-built SVG neuron diagram (the JS lab already shows the flow; the SVG had invalid `font-weight` values and many unused variables).
- The `st.tabs` analogy and the math cards with literal `$…$` inside HTML.
- `use_container_width` (now `width="stretch"`), the `np.clip` sigmoid (replaced by a numerically stable logistic) and the `numpy` import.
- The generic session keys `ears`, `bias`, `activation`, …

#### (d) Intentionally not fixed
- The JS lab's presets don't reset the selected activation; it stays the student's experiment choice.
- The JS lab is still client-only, so its slider positions reset when the page is left. The case study state persists while on the page, but Streamlit drops widget state on page navigation.
- The re-weighted cat design has a small margin (±0.5) by construction; this is explained on the page rather than hidden.

---

### 3. `pages\64A Single Neuron2.py` — DELETED
Deleted from disk with `Remove-Item`, not `git rm`. Its useful content was merged into `64A Single Neuron.py` (see 2c). The sidebar no longer shows a duplicate "A Single Neuron2" entry.
- The only remaining mention of the name is a code comment in the merged page.
- `pages\__pycache__` still has a git-tracked stale `*.cpython-39.pyc` for it; it was left alone because it is outside this task's scope.
- Two other tracked pyc files (for pages 63 and 64) were removed by accident during compile checks and restored byte-for-byte from HEAD with `git show`; `git status` shows them clean.

**UI to verify:** the sidebar has exactly one "A Single Neuron" entry. Visiting the old URL `/A_Single_Neuron2` gives Streamlit's "page not found" message and falls back to the main page.


---

## Pages 65–67


Validation run:
- `ruff check <both files> --select F,E9,W605,B,PLE --ignore B905` → All checks passed.
- `python -W error::SyntaxWarning` compile → OK for both files.
- `files\fuzz_p65_67.py` (copy of fuzz_pages.py limited to these two pages): p65 23 runs, p67 45 runs, no exceptions.
- `files\test_p65_67.py`: 50 targeted AppTest checks, all PASS. They cover verdict tiers, lock/unlock, probe presets, noise resample, every p67 preset, slider extremes, the custom-weights notice, and switching between pages (4 → 67, 5 → 65 → 67).
- `files\verify_p67_presets.py`: parses `PRESETS` from the page and computes the decision map on a 401×401 grid. It checks that each description matches the map, and that every preset value is in slider bounds and on the 0.5 step grid.
- With logging enabled, AppTest no longer emits "widget … default value but also had its value set via the Session State API" or `use_container_width` deprecation logs.

---

### pages\65Activation Functions Compared.py

#### (a) Fixes (original issue → fix)
1. **Template leak (High):** Challenge zone was a plain string showing `{st.session_state.get('grad_init', 10.0)}` literally. It is now an f-string using the live `grad_init`. Challenge 1 also shows the computed G₀ (e.g. 5.5e-05 for grad 10).
2. **False "leak revived the network" claim (High):** Challenge 2 is rewritten. With ReLU the error is cut to exactly 0 at Layer 3. With Leaky ReLU, G₀ = grad × 0.1³ (0.1 % kept), so the units stay trainable but the verdict still says severe vanishing.
3. **Verdict depended on the starting-gradient slider (Med):** tiers now use the transmitted fraction r = f′(z₃)·f′(z₂)·f′(z₁): BLOCKED (exactly 0), VANISHED (< 0.1 %), SEVERE (< 5 %), WEAKENED (< 50 %), HEALTHY. Each tier has a reason specific to the activation. Sigmoid at z=0 is now "severe" (1.6 % kept) for every grad value, instead of "healthy" for grad ≥ 7.
4. **Dead Leaky-ReLU branch (Med):** the unreachable `G0 < 0.0001 and Leaky ReLU` text is removed. Leaky's minimum of 0.1 % lands in SEVERE by design (threshold 0.999e-3).
5. **Backprop particles moved forward (Med):** `stroke-dashoffset` animation changed from +20 to −20, so particles now travel right→left with the "ERROR FLOW DIRECTION (BACKPROP)" arrow.
6. **Derivative vs. learning rate (Med):** sigmoid card now says "derivative (the gradient multiplier) never exceeds 0.25", not "learning rate capped at 0.25".
7. **Dead-ReLU wording and z = 0 (Med):**
   - Negative z: card says "Inactive at this z…" and explains that a *dead* ReLU means inactive for every input.
   - z = 0: dedicated "At the kink" text for both ReLU and Leaky ReLU. Formula lines state the conventions f′(0)=0 and f′(0)=0.1.
   - The probe value is rounded so float noise (1e-17) cannot defeat the z = 0 case.
   - Tab 3 node label "💀 DEAD" became "💤 INACTIVE (f′ = 0)".
8. **CSS override (Med):** `.stMarkdown span` and `.custom-card span` no longer force `color … !important`. Base text rules lost `!important`, so highlight classes, badges and inline `style="color:…"` keep their colours. The sidebar background is set on `[data-testid="stSidebar"]` only, instead of every descendant `div`/`span`, so slider tracks keep their colours.
9. **KaTeX inside raw HTML (Low):** `$f(z)$`, `$f'(z)$`, `$z$` inside HTML blocks are replaced with `<i>…</i>`. The pure-markdown headers keep their `$…$`.
10. **Inconsistent "frequency" (Low):** all four wave shapes share the period 10/f s (phase = 2πft/10). The triangle uses `(2/π)·arcsin(sin(phase))`. The slider label says "cycles over the 10 s window".
11. **Noise fixed seed (Low):** a "🎲 Resample noise" button appears for Random Noise (seed kept in `p65_noise_seed`). Noise is now `amp·sin + N(0, 0.2·amp)`, so the amplitude slider means the same for every shape.
12. **Lock/unlock state (Low):** the common and per-layer z values live in non-widget stores (`p65_zc_store`, `p65_z_store`), so they survive Streamlit's cleanup of hidden widgets. Unlocking starts all three layers at the common value, and re-locking restores the last common value. Previously both reset to 2.0.
13. **`value=` + `key` warnings, key collisions (Low):** all session keys are prefixed `p65_` (pages 4/5 also use `z3`). Widgets read their initial value only from session state, never via `value=`.
14. **Sigmoid clipping (Low):** `sigmoid` = `0.5·(1+tanh(z/2))`, which is exact and overflow-free, with no clip.
15. **Consistent saturation threshold (Low):** one `SATURATION_THRESHOLD = 0.05` is used by the Tab 1 cards, Tab 3 node warnings and node glow (before: 0.05 / 0.01 / 0.05).
16. **Tiny values printed as 0.0000 (Low):** G values below 1e-3 use scientific notation, transmission is shown as %, and exact 0 prints "0".
17. **Misc (Low):** `use_container_width` → `width="stretch"`. Invalid SVG `font-weight="black"/"semibold"` → `900/600`. Unused `import math` removed. Sigmoid "researchers stopped using" claim softened.

#### (b) UI differences to verify in the browser
- Scroll to **🎓 Quick Challenge Zone**: Challenge 1 shows "incoming error of 10 shrinks to about 5.5e-05" (no `{st.session_state…}` text). Change **Starting Gradient** to 20 and the numbers update.
- Sidebar → **Zero Center (z=0)**: ReLU and Leaky cards show "📍 At the kink (z = 0)…", not "Input is negative". **Deep Negative (z=-3)**: ReLU card shows "💤 Inactive at this z…".
- Sigmoid card at z=1: "…never exceeds 0.25, reached at z = 0" (no "learning rate").
- Highlights such as `y = Wx + b` in the intro and the values in the four probe cards render cyan/pink/green/amber, not grey. Badges (🧬 Sigmoid, etc.) show dark text on coloured pills.
- Tab 3, defaults (Sigmoid, lock on, z=2, grad=10): yellow dashes on the links move **leftwards** with the arrow. f′(2) = 0.105, so 0.105³ ≈ 0.12 % is kept, and the verdict reads **SEVERE VANISHING GRADIENT** with "0.12 %" in the transmission row.
- Tab 3: Sigmoid, Common z = 0 → "SEVERE VANISHING GRADIENT" with "1.56 %" for grad 1, 10 and 20 alike.
- Tab 3: ReLU, Common z = −1 → "⛔ GRADIENT BLOCKED (exactly 0)". Nodes are labelled "💤 INACTIVE (f′ = 0)" and G₀ = 0.
- Tab 3: Leaky ReLU, Common z = −1 → "SEVERE VANISHING GRADIENT", G₀ = 0.0100, transmission 0.10 %.
- Tab 3: Sigmoid, Common z = 4 → "GRADIENT VANISHED", G₀ shown as `5.51e-05`.
- Lock/unlock: set Common Input z = −1.5 → untick **Lock Inputs** → all three layer sliders show −1.5. Move z₃ → tick Lock again → Common shows −1.5 (not 2.0).
- Tab 2: Sine/Square/Triangle at frequency 2 all show exactly 2 cycles. Pick **Random Noise** → a "🎲 Resample noise" button appears in the sidebar and changes the noise when clicked.
- Tab 1 intro sentences show *f(z)*, *f′(z)*, *z* in italics (no `$` signs).
- Sidebar slider tracks are visible/coloured (sidebar background no longer painted over every div).

#### (c) Intentionally NOT fixed
- The shared ~170-line CSS block is still duplicated with p67/p64. The sigmoid/softmax helpers were later moved into `common/mathutils.py`.
- Tab 3's overlap with page 70 (Backpropagation) and the intro's "100-layer affine = single affine" point (meant for the missing page 66) are content/curriculum decisions, left as is.
- Per-layer z values are intentionally replaced by the common value on unlock. Continuity was chosen over remembering both sets; the stores still prevent the old reset to 2.0.
- "Dead ReLU" stays in the Tab 3 heading as the topic name. Only the per-input labels changed.

---

### pages\67Neural Network as Matrix Layers.py

#### (a) Fixes (original issue → fix)
1. **Goldilocks preset never predicted habitable (High).** It is retuned to a ReLU "alarm" network:
   - Weights: W¹ = [[2, 3], [2, −3], [−2, 0]], b¹ = 0, W² = [[−0.5, −0.5, −1], [0.5, 0.5, 1]], b² = [2, −2].
   - The logit difference is 4 − 2·max(2|x₁|, |x₁| + 1.5|x₂|). Habitable region is **exactly the hexagon |x₁| ≤ 1 and |x₁| + 1.5·|x₂| ≤ 2** (0 mismatches on a 401×401 grid): max |x₁| = 1.0, max |x₂| = 1.33, 25 % of the square.
   - P(habitable) is 0.982 at the origin, 0.881 at the default X, and ≤ 0.12 at all edge midpoints and corners.
   - h₁ fires for hot/heavy, h₂ for hot/light, h₃ for cold; every alarm votes barren.
2. **Other preset descriptions were false (Med).** Rewritten to match the measured maps:
   - **Gravity Cautious:** all x₂ ≲ −0.2 habitable; at x₂=+2 only x₁ ≳ 1; hot planets pass at any gravity.
   - **Frozen Oceans:** all x₁ ≲ 0 habitable at any gravity, plus all x₂ ≲ −0.2.
   - **Untrained Brain** (renamed from "Random Brain"; values are fixed): habitable only for x₁ ≳ 0.1 at x₂=−2 up to x₁ ≳ 1.1 at x₂=+2.
3. **Presets outside slider bounds / off the step grid (Med):** Goldilocks b² was ±3.5 (sliders ±3), and the Random Brain values (−1.2, 1.8, …) were off the 0.5 grid. All presets now lie on the 0.5 grid within bounds (asserted in verify script).
4. **Session-key collisions (Med):** every key is prefixed `p67_` (`p67_x1`, `p67_x2`, `p67_w1_11` … `p67_b2_2`, `p67_act`, `p67_preset`). Page 4's `x2 = 3.0` no longer leaks into Gravity (AppTest: page 4 → 67 now gives x₂ = −0.3, before 3.0).
5. **Widget sync and the `value=` + key warnings (Low):** weight/bias sliders and the activation selectbox are keyed and seeded only from session state. Presets use `on_click=load_preset` instead of `if st.button(): …; st.rerun()`. Moving a slider no longer recreates the widget (no identity churn). If Streamlit cleans the widget keys after a page switch, they are re-seeded from the active preset.
6. **Active-preset feedback (Low):** an info box shows "Active preset: … + description", or "Custom weights (started from …)" once any weight differs.
7. **Edge animation ignored negative inputs/activations (Med):** edges are driven by the contribution w·signal:
   - colour = sign (cyan excitatory / red inhibitory / gray ≈ 0)
   - particles and speed = |w·signal|
   - thickness = |w|

   Negative inputs and negative tanh activations now animate. The legend text explains this, and its coloured spans now render in colour (see CSS fix).
8. **`html_vector_2d` ignored its colour (Low):** the argument is now a real colour, default `#22d3ee`. b² is drawn in grey and Z² in pink, matching the output layer.
9. **Tab 3 (Med/Low):**
   - The "circular region" text is replaced by the Goldilocks bounded-pocket explanation. W¹ is described as mapping onto a flat plane inside 3D.
   - Grid is 21×21 (step 0.2, so the ±1 boundaries fall on grid points).
   - Separate legend traces "Predicted habitable" / "Predicted barren" in both plots, with P(habitable) in the hover.
   - Caption: "N of 441 grid points (x %) are predicted habitable".
10. **Recap (Low):** shows W²(W¹X+b¹)+b² = (W²W¹)X + (W²b¹+b²) with the live W_new and b_new numbers.
11. **Duplicated softmax and activation dispatch (Low):** one `softmax(z, axis=0)` (stable, `keepdims`) and one `ACTIVATIONS` dict serve both the single forward pass and the batched grid pass.
12. **CSS override (Med):** same fix as p65. The highlights, inline-coloured legend spans and the verdict paragraph colour now apply.
13. **Typos and misc (Low):** "customized weight weights", "Multipling", "packeting", and the duplicate "Step 1" preset header are fixed. Sigmoid is clip-free. `use_container_width` → `width="stretch"`. SVG `font-weight="black"` → `900`. Unused `import math` and pre-existing F541 placeholder-less f-strings are removed.

#### (b) UI differences to verify in the browser
- Open page 67 fresh: an info box reads "Active preset: 🌌 Goldilocks Zone Brain. Habitable ONLY for …". The verdict is **HABITABLE PLANET DETECTED** (88.1 %), and the activation selectbox shows **ReLU**.
- Tab 3 with Goldilocks: the yellow points form a closed hexagon around the origin (|x₁| ≤ 1, |x₂| ≤ 1.33). The caption says "109 of 441 grid points (25%)". The legend shows "Predicted habitable / Predicted barren", and hover shows P(habitable).
- Drag Temperature to +1.5 → verdict flips to BARREN. Drag Gravity to −2 at Temperature 0 → BARREN.
- Click each preset button: the sidebar sliders jump to the preset values (b² within ±3, all on the 0.5 grid). The info box shows that preset's description, and Tab 3 matches it:
  - Gravity Cautious: whole bottom band habitable.
  - Frozen Oceans: left half plus bottom band habitable.
  - Untrained: right-hand slanted region.
- Move any weight slider → the info box switches to "Custom weights (started from …)".
- Tab 2: set Temperature to −1.5 with Goldilocks. The temp → h₃ edge (w = −2) is **cyan** with moving particles (negative × negative = excitatory). Before, all negative-input edges were frozen. The legend words "cyan… / red… / gray…" render in their colours.
- Tab 1 Step 4/5: b² renders grey and Z² pink (not cyan). Card text says "Multiplying". The preset header reads "Load a Preconfigured Brain Design (each preset loads a full set of weights and biases)".
- Lesson Recap card shows live W_new / b_new numbers, and the gold formula highlight is gold (not grey).
- Visit page 4 (Magnitude), then page 67: Gravity shows −0.3 (previously 3.0, outside its −2…2 range).

#### (c) Intentionally NOT fixed
- **Goldilocks is a hexagon, not a square box.** A 2-3-2 network whose hidden units each draw one straight boundary can only bound a polygon. The max(2|x₁|, |x₁|+1.5|x₂|) construction is exact and uses all three units; a true |x₁|≤1 ∧ |x₂|≤1 box would need 4 hidden units.
- Custom slider edits are lost after leaving the page and coming back (re-seeded from the active preset). Persisting them would need extra non-widget stores for 17 values; judged not worth the complexity.
- The Gravity Cautious / Frozen Oceans / Untrained weights were kept and only their descriptions corrected, as requested ("fix descriptions to match reality").
- The SVG markup keeps its blank lines between elements (pre-existing; it renders correctly). Shared CSS/helper duplication across pages is not extracted (cross-file scope).


---

## Pages 68–75


App-wide conventions applied to all 7 files:
- `use_container_width=True` → `width="stretch"` (st.plotly_chart, st.button). Streamlit 1.67 logs that `use_container_width` "will be removed after 2025-12-31".
- All widgets have page-prefixed keys (`p68_*`, `p69_*`, `p70_*`, `p71_*`, `p73_*`, `p74_*`, `p75_*`), and the session-state key is now `p73_dart_seed`.
- LaTeX strings are raw strings. `python -W error::SyntaxWarning` compiles cleanly, and ruff (`F,E9,W605,B,PLE`) passes.
- Verification:
  - AppTest ran headless on every page, plus the fuzz harness (min/max of every slider, every radio option, button, checkbox). No exceptions or warnings.
  - The changed math was re-checked in Python: exact Lasso solution vs ISTA (difference < 1e-14), 1D closed forms vs a fine grid, the p69 gradient numbers, and exact display arithmetic on p70 across all slider combinations.

---

### 68 MSE Loss — For Regression
**(a) Fixes**
- "MSE … will pull the entire line down" was wrong: the best line *tilts* toward the outlier. Slope goes from 0.87 to 0.30 and intercept from 2.08 to 4.08, so the left end rises. The text now says it tilts and gives the numbers.
- "MAE will ignore the outlier" was too categorical. It now gives the measured MAE slope (≈0.83 vs 0.87) and adds a caveat: MAE is not immune when the outlier sits at an extreme x (high leverage).
- The squares overlap at the default settings (errors larger than the 1.5 x-spacing). A caption under the MSE chart now explains this.
- The comment "Clean linear trend" became "Roughly linear trend"; the outlier comment notes it is a high-leverage point.

**(b) UI to verify**
- Choose MSE → a caption under the squares chart mentions overlapping squares. Choose MAE → the caption disappears.
- Scroll to "Why do we SQUARE…" → point 2 mentions "tilts", slope ≈0.30, and the MAE caveat.

**(c) Not fixed**
- Squares are still drawn to the right of their points (re-laying them out would change the visual design); a caption explains instead. The earlier "squares are not square" finding was wrong, because `scaleanchor` is already set.

### 69 Cross-Entropy Loss — For Classification
**(a) Fixes**
- Removed the unused `import pandas as pd`.
- Added the binary formula −[y ln p + (1−y) ln(1−p)] and the multi-class formula −Σ yₖ ln pₖ, and showed how they reduce to −ln p_true.
- Added a log(0) note: real libraries clip probabilities to ε or use log-softmax.
- Multi-class sliders are now logits (−5…5) passed through a numerically stable **softmax**, instead of "raw confidence" divided by the sum.
- MSE section:
  - "capped at 1.0" now says "≤1 for the true-class term, ≤2 for full one-hot MSE".
  - Added a new **gradient section**: ∂MSE/∂z = −2p(1−p)² vs ∂CE/∂z = p−1. At p=0.01 that is ≈0.02 vs 0.99 (~50× stronger), with a chart of the two gradients.
- Plotly title LaTeX `$y=-\ln(x)$` (no MathJax in Streamlit) became plain text "y = −ln(x)".
- The meaningless shading under the curve became a dotted drop line at the current point.
- The loss readout uses `.5g` / `.4f`, so extreme logits no longer show "−ln(0.000)" or "−ln(1)".
- "Surprise" is clarified as surprisal −ln p.

**(b) UI to verify**
- Section 1 → the formula block shows the Binary and Multi-class formulas, with a caption about ε/log-softmax below it. The chart title reads "y = −ln(x)" with no `$`.
- Section 2 → three "… score (logit)" sliders from −5 to 5. Dog=5, Cat=−5, Bird=−5 with true label Cat → "Loss = -ln(4.54e-05) = 10.0000".
- Section 3 → a new "The real reason: the learning signal (gradient)" block with a 2-line chart; the red CE gradient stays high near p=0.

**(c) Not fixed** — none.

### 70 Backpropagation — Chain Rule Backward
**(a) Fixes**
- Removed the unused `import time`. `numpy` is now used (`np.isclose`).
- The "Perfect!" check used exact float equality (`dLoss_dw1 == 0`). Example: x=1.5, w₁=0.8, w₂=2.5, y=3 gave ŷ=3.0000000000000004 and told users to "decrease w₁". It now uses `np.isclose`, and intermediate values are rounded to 10 decimals to remove float noise.
- An info box states the network is a deliberately **linear toy** (no biases, no activations) and explains how σ′ would join the chain.
- The equations now show **exact** decimals (`fmt`), so "a × b = c" always checks out. The old 2-decimal rounding mismatched in about 12% of slider combinations; verified 0 mismatches over all 162k combinations.
- Chain-rule box wording changed to "How much L changes when ŷ changes", etc.
- Step help/text said "Inputs" / "Input Layer", but ∂L/∂x is never computed. It now says "weights" / "w₁ (first layer)", and the Step 3 heading is "First-Layer Weight Gradient".
- Ruff F541: two `rf""` strings without placeholders became `r""`.

**(b) UI to verify**
- An info box "Our toy network…" appears under the chain-rule explanation.
- Sidebar x=1.5, w₁=0.8, w₂=2.5, y=3, step 3 → green "Perfect!" message.
- x=1.5, w₁=0.1, w₂=0.3, step 3 → equations show −9.955 × 0.15 = −1.49325 and −2.9865 × 1.5 = −4.47975. The diagram still rounds to 2 decimals, and a caption says so.

**(c) Not fixed**
- The "∇" labels on the diagram nodes are kept (they are cosmetic).

### 71 Overfitting & Underfitting
**(a) Fixes**
- The state labels used to be hard-coded by degree (3–5 green). The measured best validation degree is **7** for noise 0.1–1.0, and degree 2 ≈ degree 3. Labels now come from the validation curve:
  - "Near the Validation Sweet Spot" if within 10% (+1e-3) of the best;
  - otherwise "Lower/Higher Complexity (Under/Overfitting Side)" relative to the best degree.
- The complexity chart now uses a **log y-axis** (validation MSE spans 0.07 to 571) with a floor of 1e-6 for zero-noise fits. A dotted "Lowest validation: d" line was added.
- The main plot y-range is clipped to the data ±1. A degree-20 curve reached ±300 and flattened every point. A ⚠️ caption appears when the curve leaves the range, mentioning extrapolation near the edges.
- Added a real **test set** (seed 7) and a "Final Check on a Separate Test Set" section: validation MSE vs test MSE for the validation-chosen degree.
- Removed the misused `st.metric` deltas ("Higher degree", "Above 1.0"). Validation help now notes the noise floor σ².
- The "Degree 3–5" bullet is now dynamic ("lowest validation error is at degree X").
- The degree loop is computed once (it used to be duplicated).

**(b) UI to verify**
- Noise 0.3: degree 2 → blue "Lower Complexity"; degree 7 → green "Near the Validation Sweet Spot"; degree 18 → red, plus the ⚠️ clipped-curve caption.
- The trade-off chart has a log axis and a green dotted "Lowest validation: 7" line.
- At the bottom, two metrics: Validation MSE (degree 7) and Test MSE (degree 7).

**(c) Not fixed**
- Polynomial conditioning: `Polynomial.fit` already rescales, and no RankWarning appears at any degree or noise, so nothing to fix. A comment was added.

### 73 Bias-Variance Tradeoff
**(a) Fixes**
- Added `st.set_page_config(page_title="Bias-Variance Tradeoff", page_icon="🎯", layout="wide")`.
- Renamed the curve variable `bias` → `bias_sq` (the earlier math finding was WRONG; this is only for clarity). Added `curve_bias_sq` / `curve_variance` helpers and a `NOISE` constant. The legend reads "Total Error (Bias² + Variance + Noise)".
- The mini-dartboard used unrelated formulas and showed "Bias Low / Variance Low" at complexity 5, where the curve shows Var 16 > Bias² 7.3. It now uses the **same** curve values: offset = √Bias², per-axis variance = Variance/2, so the mean squared miss is Bias² + Variance. It shows the numbers and whether bias² or variance dominates relative to the sweet spot (≈4.3).
- Dart meaning: each dart is the prediction for one input from a model **trained on a different training set**.
- **Measured decomposition** under the main dartboard: Avg squared miss = Measured Bias² + Measured Variance (an exact identity for the darts thrown). The caption gives the expectation bias² + 2·var.
- The expander no longer says "memorizes the training data perfectly"; variance is now described as sensitivity across training sets. Added the Bias² + Variance + Noise identity.
- Button uses `width="stretch"`, key `p73_throw`; session key `p73_dart_seed`.

**(b) UI to verify**
- The page now opens in wide layout with the tab title "Bias-Variance Tradeoff".
- Dartboard tab → three metrics under the board (avg squared miss = bias² + variance). Click "Throw New Darts!" → the numbers change and the identity still holds.
- Tradeoff tab:
  - complexity 1 → "Underfitting side";
  - 4.3 → green "Near the sweet spot (≈ 4.3)";
  - 10 → "Overfitting side" with widely scattered mini darts.

**(c) Not fixed**
- The tab-1 thresholds (bias 3.5 / variance 2.5) are kept; tab 2 no longer uses High/Medium/Low labels, so they cannot conflict.

### 74 L1 & L2 Regularization
**(a) Fixes**
- The invalid escape `"\l"` (SyntaxWarning, lines 38 and 109) is fixed by using raw strings.
- 1D: exact closed forms w* = max(0, 2−λ/2) for L1 and 2/(1+λ) for L2 replace the grid argmin and the λ≥4 snap. The snap was correct; it is just no longer needed. The grid was 0.01 off for 21/61 L1 and 17/61 L2 slider values. The text now states both formulas.
- 2D:
  - The grid search (≈0.016 error, ±0.05 snapping; at λ=0 the star sat at (2.99, 1.52), not on the X) is replaced by an **exact** solve: ridge via its linear system; Lasso via sign-pattern enumeration, which is the exact global optimum of the convex problem and matches ISTA to 1e-15.
  - "The bowl will almost always hit a corner" was contradicted at the default λ=2, where w = (2.13, 1.33) has no zero. The text now gives the real thresholds: w₁ = 0 for λ ≥ 6.9 (w₂ = (10.5−λ)/4), and both zero for λ ≥ 10.5. It also explains why w₁ (the larger weight) is dropped first (correlation).
  - A dynamic caption says whether the contour touches an edge or a corner, or whether both weights are 0.
- Added the **touching data-loss contour** (dashed yellow ellipse through the optimum), so the tangency is visible. "Blue shape" is now "cyan".
- Comment "hits the w1 axis" became "reaches the w2-axis (w1 = 0)".
- Intro "In the previous lesson … memorizing perfectly … crazy weights" was softened and now references the Overfitting & Underfitting page.
- Summary: "Forces many weights to 0" became "Can set many weights to exactly 0". Added the correlated-feature caveat for feature selection, and noted weight decay = L2 only for plain SGD (AdamW otherwise).

**(b) UI to verify**
- Section 1, L1: λ=1 → "Current Optimal Weight 1.50"; λ=4 → 0.00. L2, λ=1 → 1.00.
- Section 2, L1:
  - λ=2 → star at (2.13, 1.33), yellow dashed ellipse touching the diamond edge, caption "touches a diamond edge";
  - λ=7 → (0.00, 0.88), caption "corner";
  - λ=10.5 → both 0.
- L2, λ=0 → the star sits exactly on the red X (3.00, 1.50).

**(c) Not fixed** — none.

### 75 Learning Curves
**(a) Fixes**
- Removed pandas: the rolling mean became a numpy `trailing_mean`, verified identical to `rolling(3, min_periods=1).mean()`.
- **Gap pattern:** the constant +0.15 validation offset (which gave underfit models a *larger* gap than good models) became `base_gap = 0.02 + 0.012·capacity`. At epoch 100 the gap is now 0.08–0.15 for capacities 1–5 vs 0.66 (capacity 7) and 4.68 (capacity 10).
- **Early-stopping leakage:**
  - The status and marker used `argmin` over all 100 epochs (future data; the marker could be drawn ahead of the current epoch). This is replaced by `online_early_stopping` with a new **patience slider** (1–30, default 10), which only uses epochs up to the current one.
  - The markers "Best epoch B (restored)" and "Stopped (patience P)" are drawn only after stopping has triggered.
  - New statuses: improving / "hasn't improved for k epochs" / early stopping triggered / overfitting (validation rose and the gap widened since the best epoch).
  - An optional checkbox "Reveal hindsight minimum" shows the full-run argmin for comparison only. Example: capacity 5 has its hindsight minimum at epoch 89, while online patience 10 restores epoch 75.
- "The Gap (Generalization Error)" became "Generalization Gap (Val − Train)". The Intuition text explains that the gap is not the generalization error (validation loss estimates that).
- **Dark theme:** the header's dark text and the white cards/plot are gone. The CSS is theme-neutral (`color: inherit`, translucent cards), the plot uses `plotly_dark` with a transparent background, and the green marker is #22c55e.
- `font-family: 'monospace'` (quoted, so not the generic family) became `monospace`.

**(b) UI to verify**
- Dark theme: the title, concept card and metric cards are readable.
- Capacity 7, epoch 60 → "⏳ … hasn't improved for 6 epochs (best so far: epoch 54)". Epoch 100 → red OVERFITTING message, green dashed "Best epoch 62 (restored)" plus a grey "Stopped (patience 10)" line at 72.
- Capacity 5, epoch 100 → green "Early stopping triggered at epoch 85 … restore epoch 75". Tick "Reveal hindsight minimum" → orange line at 89 and a comparison caption.
- Capacity 2 → "Underfitting … close together (small gap)".
- Patience 1 → stopping triggers very early (it is sensitive to noise).

**(c) Not fixed**
- `plot_y_max` still uses the max over the whole run. This keeps the axis stable while scrubbing epochs; it is only a display scale, not a decision.
- The underfit status still keys on the chosen capacity (≤3), which the user knows; it does not use future data.

