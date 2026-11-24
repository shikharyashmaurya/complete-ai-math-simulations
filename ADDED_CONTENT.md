# What was added — change log & UI verification guide

Branch: `feat/add-next-content` (based on `fix/review-improvements`). This branch implements the **"What to add next"** list.

## Summary

- **29 new lessons**: the 6 numbering gaps (24, 39, 43, 55, 66, 72) and 23 new topic pages (76–98) covering linear algebra, calculus, probability,
  information theory, optimization and deep learning. Total: 98 lessons.
- **A quiz under every lesson** (98 quiz files in `quizzes/`), with pass/fail feedback, explanations, and per-section progress on Home and in the sidebar.
- **Sidebar sections now include the new pages**: 76–78 in Vectors & Matrices, 79–83 in Calculus, 84–88 in Probability & Statistics,
  89 in Information Theory, 90–92 in Optimization, 93–98 in Neural Networks & ML.
- **Embedded HTML/JS labs moved to `assets/labs/*.html`** (36 files, 30 pages), loaded with `common.assets.load_lab`. The HTML passed to the browser is
  byte-for-byte identical to before, so these labs should look and behave exactly the same.
- **Curriculum cross-links**: 19 existing pages now link into the new lessons (e.g. 23 → 24, 54 → 55, 75 → 93).
- **Tests**: 824 tests pass (`pytest -n auto`), including strict "every page has a valid quiz", "every `load_lab` asset exists" and "every page link target exists".

## How to verify

```powershell
pip install -r requirements-dev.txt
streamlit run app.py
ruff check .
pytest -n auto
```

Quick UI tour:
1. **Home**: each section shows quiz progress, and the sidebar shows an overall progress count.
2. Open **24 · Complement, Union & Intersection** in the Probability section. Scroll down: a "🧠 Check your understanding" quiz sits under the lesson.
   Answer, press **Check answers** → ✅/❌ with explanations and a score; **Try again** resets it.
3. Open the new lessons in the table below. Each has an intuition section, interactive labs, a live worked example, an AI connection and Previous/Next links.
4. Open any embedded-lab page, for example **52 · Gradient Descent**. It should behave exactly as before.

## New lessons

| # | Lesson file |
|---|---|
| 24 | `pages/24Complement, Union & Intersection.py` |
| 39 | `pages/39Quantiles, IQR & Outliers.py` |
| 43 | `pages/43Residuals & Least Squares.py` |
| 55 | `pages/55Convex Functions.py` |
| 66 | `pages/66Stacking Linear Layers Collapses.py` |
| 72 | `pages/72Train, Validation & Test Splits.py` |
| 76 | `pages/76Span, Basis & Rank.py` |
| 77 | `pages/77Projections — Shadows onto Subspaces.py` |
| 78 | `pages/78SVD — Rotate, Stretch, Rotate.py` |
| 79 | `pages/79Limits & Continuity.py` |
| 80 | `pages/80Product & Quotient Rules.py` |
| 81 | `pages/81Taylor Series — Local Approximation.py` |
| 82 | `pages/82Jacobian & Hessian.py` |
| 83 | `pages/83Automatic Differentiation.py` |
| 84 | `pages/84Joint & Marginal Distributions.py` |
| 85 | `pages/85Poisson & Exponential Distributions.py` |
| 86 | `pages/86Beta Distribution — Beliefs about Probabilities.py` |
| 87 | `pages/87Maximum Likelihood Estimation.py` |
| 88 | `pages/88Confidence Intervals & Hypothesis Tests.py` |
| 89 | `pages/89Mutual Information.py` |
| 90 | `pages/90Momentum.py` |
| 91 | `pages/91RMSProp & Adam.py` |
| 92 | `pages/92Learning-Rate Schedules.py` |
| 93 | `pages/93Weight Initialization.py` |
| 94 | `pages/94Dropout.py` |
| 95 | `pages/95Batch Normalization.py` |
| 96 | `pages/96Convolution.py` |
| 97 | `pages/97Embeddings.py` |
| 98 | `pages/98Attention.py` |

## All files changed

<details><summary><b>Added</b> (166)</summary>

- `assets/labs/p19_conveyor_belt.html`
- `assets/labs/p20_linear_function_lab.html`
- `assets/labs/p20_neuron_cartoon.html`
- `assets/labs/p22_relu_visualizer.html`
- `assets/labs/p22_stitch_lab.html`
- `assets/labs/p22_xor_piecewise_lab.html`
- `assets/labs/p23_2d_space.html`
- `assets/labs/p23_sample_space.html`
- `assets/labs/p23_venn.html`
- `assets/labs/p25_conditional_probability.html`
- `assets/labs/p26_two_spinners.html`
- `assets/labs/p38_mean_median_mode.html`
- `assets/labs/p40_covariance.html`
- `assets/labs/p41_correlation_lab.html`
- `assets/labs/p41_nonlinear_gotcha.html`
- `assets/labs/p42_regression_lab.html`
- `assets/labs/p44_derivative.html`
- `assets/labs/p45_derivative_rules.html`
- `assets/labs/p46_chain_rule.html`
- `assets/labs/p47_partial_derivatives.html`
- `assets/labs/p48_gradient.html`
- `assets/labs/p49_integral_area.html`
- `assets/labs/p50_loss_function.html`
- `assets/labs/p51_loss_landscape.html`
- `assets/labs/p52_gradient_descent.html`
- `assets/labs/p53_learning_rate.html`
- `assets/labs/p54_local_global_minimum.html`
- `assets/labs/p56_sgd.html`
- `assets/labs/p57_surprise.html`
- `assets/labs/p58_entropy.html`
- `assets/labs/p59_cross_entropy.html`
- `assets/labs/p60_kl_divergence.html`
- `assets/labs/p61_eigenvectors.html`
- `assets/labs/p62_eigenvalues.html`
- `assets/labs/p63_pca.html`
- `assets/labs/p64_neuron.html`
- `common/assets.py`
- `common/quiz.py`
- `pages/24Complement, Union & Intersection.py`
- `pages/39Quantiles, IQR & Outliers.py`
- `pages/43Residuals & Least Squares.py`
- `pages/55Convex Functions.py`
- `pages/66Stacking Linear Layers Collapses.py`
- `pages/72Train, Validation & Test Splits.py`
- `pages/76Span, Basis & Rank.py`
- `pages/77Projections — Shadows onto Subspaces.py`
- `pages/78SVD — Rotate, Stretch, Rotate.py`
- `pages/79Limits & Continuity.py`
- `pages/80Product & Quotient Rules.py`
- `pages/81Taylor Series — Local Approximation.py`
- `pages/82Jacobian & Hessian.py`
- `pages/83Automatic Differentiation.py`
- `pages/84Joint & Marginal Distributions.py`
- `pages/85Poisson & Exponential Distributions.py`
- `pages/86Beta Distribution — Beliefs about Probabilities.py`
- `pages/87Maximum Likelihood Estimation.py`
- `pages/88Confidence Intervals & Hypothesis Tests.py`
- `pages/89Mutual Information.py`
- `pages/90Momentum.py`
- `pages/91RMSProp & Adam.py`
- `pages/92Learning-Rate Schedules.py`
- `pages/93Weight Initialization.py`
- `pages/94Dropout.py`
- `pages/95Batch Normalization.py`
- `pages/96Convolution.py`
- `pages/97Embeddings.py`
- `pages/98Attention.py`
- `quizzes/p01.json`
- `quizzes/p02.json`
- `quizzes/p03.json`
- `quizzes/p04.json`
- `quizzes/p05.json`
- `quizzes/p06.json`
- `quizzes/p07.json`
- `quizzes/p08.json`
- `quizzes/p09.json`
- `quizzes/p10.json`
- `quizzes/p11.json`
- `quizzes/p12.json`
- `quizzes/p13.json`
- `quizzes/p14.json`
- `quizzes/p15.json`
- `quizzes/p16.json`
- `quizzes/p17.json`
- `quizzes/p18.json`
- `quizzes/p19.json`
- `quizzes/p20.json`
- `quizzes/p21.json`
- `quizzes/p22.json`
- `quizzes/p23.json`
- `quizzes/p24.json`
- `quizzes/p25.json`
- `quizzes/p26.json`
- `quizzes/p27.json`
- `quizzes/p28.json`
- `quizzes/p29.json`
- `quizzes/p30.json`
- `quizzes/p31.json`
- `quizzes/p32.json`
- `quizzes/p33.json`
- `quizzes/p34.json`
- `quizzes/p35.json`
- `quizzes/p36.json`
- `quizzes/p37.json`
- `quizzes/p38.json`
- `quizzes/p39.json`
- `quizzes/p40.json`
- `quizzes/p41.json`
- `quizzes/p42.json`
- `quizzes/p43.json`
- `quizzes/p44.json`
- `quizzes/p45.json`
- `quizzes/p46.json`
- `quizzes/p47.json`
- `quizzes/p48.json`
- `quizzes/p49.json`
- `quizzes/p50.json`
- `quizzes/p51.json`
- `quizzes/p52.json`
- `quizzes/p53.json`
- `quizzes/p54.json`
- `quizzes/p55.json`
- `quizzes/p56.json`
- `quizzes/p57.json`
- `quizzes/p58.json`
- `quizzes/p59.json`
- `quizzes/p60.json`
- `quizzes/p61.json`
- `quizzes/p62.json`
- `quizzes/p63.json`
- `quizzes/p64.json`
- `quizzes/p65.json`
- `quizzes/p66.json`
- `quizzes/p67.json`
- `quizzes/p68.json`
- `quizzes/p69.json`
- `quizzes/p70.json`
- `quizzes/p71.json`
- `quizzes/p72.json`
- `quizzes/p73.json`
- `quizzes/p74.json`
- `quizzes/p75.json`
- `quizzes/p76.json`
- `quizzes/p77.json`
- `quizzes/p78.json`
- `quizzes/p79.json`
- `quizzes/p80.json`
- `quizzes/p81.json`
- `quizzes/p82.json`
- `quizzes/p83.json`
- `quizzes/p84.json`
- `quizzes/p85.json`
- `quizzes/p86.json`
- `quizzes/p87.json`
- `quizzes/p88.json`
- `quizzes/p89.json`
- `quizzes/p90.json`
- `quizzes/p91.json`
- `quizzes/p92.json`
- `quizzes/p93.json`
- `quizzes/p94.json`
- `quizzes/p95.json`
- `quizzes/p96.json`
- `quizzes/p97.json`
- `quizzes/p98.json`
- `tests/test_quizzes.py`

</details>

<details><summary><b>Modified</b> (39)</summary>

- `README.md`
- `app.py`
- `pages/18Matrix Inverse — Undoing a Transform.py`
- `pages/19Functions as Machines.py`
- `pages/20Linear Functions.py`
- `pages/22Piecewise Functions.py`
- `pages/23Sample Space & Basic Probability.py`
- `pages/25Conditional Probability.py`
- `pages/26Independence.py`
- `pages/38Mean, Median, Mode.py`
- `pages/40Covariance.py`
- `pages/41Pearson Correlation.py`
- `pages/42Scatter Plot & Line of Best Fit.py`
- `pages/44What is a Derivative.py`
- `pages/45Derivative Rules (Power & Constant).py`
- `pages/46Chain Rule — Derivative Through Layers.py`
- `pages/47Partial Derivatives.py`
- `pages/48The Gradient — Steepest Climb.py`
- `pages/49Integral as Area.py`
- `pages/50What is a Loss Function.py`
- `pages/51Loss Landscape — Hills and Valleys.py`
- `pages/52Gradient Descent.py`
- `pages/53Learning Rate.py`
- `pages/54Local vs Global Minimum.py`
- `pages/56Stochastic Gradient Descent.py`
- `pages/57Information & Surprise.py`
- `pages/58Entropy — Average Uncertainty.py`
- `pages/59Cross-Entropy — Predicted vs Reality.py`
- `pages/60KL Divergence — Gap Between Distributions.py`
- `pages/61Eigenvectors — Vectors That Don't Rotate.py`
- `pages/62Eigenvalues — How Much Do They Stretch.py`
- `pages/63PCA Intuition — Finding the Best Angle.py`
- `pages/64A Single Neuron.py`
- `pages/65Activation Functions Compared.py`
- `pages/67Neural Network as Matrix Layers.py`
- `pages/71Overfitting Underfitting.py`
- `pages/73Bias-Variance Tradeoff.py`
- `pages/75Learning Curves.py`
- `tests/test_static.py`

</details>

## Detailed notes and UI checks per work item


---

## New pages 24 & 39


### `pages\24Complement, Union & Intersection.py` (new)
- Complement rule + "at least one" trick: birthday problem with live n slider (1–100), exact 1 − ∏(365−k)/365 vs a seeded
  4,000-room simulation (±95% error bar), naive n/365 curve for contrast, product shown in LaTeX.
- Addition rule lab: sliders P(A), P(B), P(A∩B); valid overlap range [max(0, P(A)+P(B)−1), min(P(A), P(B))] shown;
  invalid combinations raise an `st.error` explaining which bound is violated and the nearest valid value is used.
  Area-to-scale Venn (bisection on lens area) + "probability ruler" bars; seeded 2,000-outcome simulation shows the
  identity holds exactly for counts. Buttons "Make mutually exclusive" / "Make independent".
- Mutually exclusive vs independent panel (live verdict, P(A|B) vs P(A)); De Morgan's laws with live numbers.
- Exact event builder (52-card deck or 36 dice pairs): pick A, B and an operation (∪, ∩, Aᶜ, A∖B, neither); grid
  heatmap of regions + gold frames on the result; counts and `Fraction` probabilities; addition rule in exact fractions;
  exact independence check.
- AI: family-wise error rate 1−(1−α)^m vs union bound mα vs Bonferroni, seeded simulation; pass@k, finite-class union
  bound in learning theory, guardrail failure example. Worked example, takeaways, prev (23) / next (25) links.

**UI to verify** (sidebar → "Complement, Union & Intersection")
- Section 1: drag "People in the room" to 23 → exact 0.5073; to 57 → 0.9901; click 🎲 Resample → simulated value/diamond moves, exact doesn't.
- Section 2: set P(A)=0.8, P(B)=0.7, P(A∩B)=0.2 → red "Impossible … at least 0.50" error, diagrams use 0.50.
  Set P(A∩B)=0.9 → "exceeds min(P(A),P(B))" error. Click "Make … independent" → P(A∩B) slider jumps to 0.56, green "Independent".
  Click "Make … mutually exclusive" with P(A)+P(B) ≤ 1 → slider goes to 0, warning "Mutually exclusive → dependent".
- Venn circles shrink/grow with P(A), P(B); overlap shrinks to zero / nests fully at the bounds.
- Section 4: Heart & King → caption "independent: 1/52 = 1/4 × 1/13"; Heart & Spade → "mutually exclusive — and therefore dependent";
  switch to Two dice, Sum = 7 & First die even → "independent: 1/12 = 1/6 × 1/2". Change "Combine into" → gold frames move.
- Section 6: m slider/α select update the curves; at m=20, α=0.05 → 0.6415.

**Known limitations**: P(A∩B) is clamped (not slider-range-restricted) so invalid values can be selected and are explained;
"Make independent" rounds P(A)·P(B) to the 0.01 slider grid (an "almost independent" note appears when that happens).
Venn rectangle Ω is not to scale (only circles and overlap are). Event lists are fixed presets (no free-form events).

### `pages\39Quantiles, IQR & Outliers.py` (new)
- Quantile/percentile definition, five-number summary metrics, IQR, quartile skewness; 5 seeded presets (normal,
  log-normal, left-skewed, Student-t df=2, uniform), n slider, Tukey k slider, numpy interpolation-method selector,
  🎲 Resample. Expander table compares Q1/median/Q3/IQR across 9 numpy methods (linear = default, PERCENTILE.INC; weibull = .EXC).
- Box plot built step by step (select-slider: sort → median → box → fences → whiskers & outliers); histogram tab with
  quartiles and mean; outlier counts Tukey vs |z|>3 with normal reference rates (0.70% vs 0.27%).
- Robustness lab: 9 fixed latencies + slider-driven 10th value (0–1000) and z-threshold slider; Tukey band vs mean ± t·SD
  band, sweep plot (log y) of mean/SD/median/IQR; masking warning (Samuelson: |z| ≤ √(n−1) = 3 for n=10), breakdown points.
- ECDF lab with quantile-lookup slider p: linear vs inverted-ECDF quantiles, F̂ check, p50/p95/p99.
- Worked example (positions h = 1+(n−1)p, interpolation, fences, z of your point) computed live; AI section: StandardScaler
  vs RobustScaler table on the live data, percentile clipping slider, bullets (IQR filtering, AutoClip, INT8 percentile
  calibration, QuantileTransformer, pinball loss). Prev (38) / next (40) links + link back to page 35.

**UI to verify** (sidebar → "Quantiles, IQR & Outliers")
- Section 1: move "Build the box plot" through 1→5; each step adds median, box, fences, whiskers + red open-circle outliers.
  Switch dataset to "Right-skewed" → many upper outliers, mean > median in histogram tab. Set n=10 and open the
  interpolation expander → methods disagree visibly. Change k to 3.0 → fewer outliers.
- Section 2: drag "Tenth latency" from 60 → 1000: mean/SD metrics explode, median 50.50 / IQR 7.25 stay; Tukey says outlier
  above 65.375; "|z| > 3.0" never flags (z → 3 from below). Lower z-threshold to 2.5 → flagged.
- Section 3: slide p → gold lookup line moves on ECDF; p=0 → min, p=1 → max.
- Section 5: drag the tenth latency up → StandardScaler spread of 9 normal points shrinks, RobustScaler stays 2.207.

**Known limitations**: box plot is drawn with shapes (not `go.Box`) so it follows the selected interpolation method exactly;
z-scores use population SD (÷n, as StandardScaler). Robustness lab uses a fixed 9-point base dataset.

### `quizzes\p24.json`, `quizzes\p39.json` (new)
4 questions each (overlap bounds, disjoint vs independent, FWER complement, De Morgan; Tukey vs z masking, robustness,
linear percentile computation, RobustScaler). All answers verified with python.

### Verification
- ruff: clean on both pages. JSON: both quiz files load.
- `tests\test_pages_smoke.py` + `tests\test_pages_fuzz.py -k "24Complement or 39Quantiles"`: 6 passed.
- `tests\test_static.py`: all checks for pages 24/39 pass. A temporary failure in page 83 (unprefixed keys) during parallel work was fixed before the final run.


---

## New pages 43 & 55


Validation: ruff clean; `tests\test_static.py` 205 passed; smoke + fuzz `-k "43Residuals or 55Convex"` 6 passed;
`tests\test_quizzes.py -k "43 or 55"` passed. All formulas checked numerically in throwaway scripts (OLS vs lstsq, hat-matrix
diagonal = leverage, Σh = 2, SST = SSR + SSE, R² = r², Cook's D vs delete-one refits, f'' vs finite differences, chord scan
verdicts, descent lemma / O(1/k) bound / (1 − μ/L)ᵏ rate over the whole slider grid, unit-swap network loss).

### `pages\43Residuals & Least Squares.py` (398 lines)
- Seeded data lab (scenario select, n 1–100, noise σ, 🎲 Resample) → closed-form OLS with tabs: fit + residual segments;
  residuals-vs-fitted plot with quadratic trend and ±2·SD bins (curve share / spread-ratio metrics); leverage & Cook's distance
  with "fit without the most influential point"; R² decomposition bars (SST vs SSR + SSE, R² = r²); normal equations (XᵀX β = Xᵀy)
  vs cov/var formula plus a ✅ table of properties (Σe = 0, Σxe = 0, line through (x̄, ȳ), mean ŷ = ȳ).
- Edge cases: n = 1 and "all x identical" (Sxx = 0, det XᵀX = n·Sxx = 0) show warnings instead of a fit; Cook's needs n > 2 and SSE > 0; h = 1 → ∞.
- Worked example table + e₁/SSE/MSE/RMSE in LaTeX; 3D projection view (n = 3, sliders y1–y3) with column-space plane, ŷ, e ⟂ plane; link to page 77.
- AI section: linear regression = single linear neuron, residual analysis for debugging, residual connections clarified as a different idea. Prev 42 / Next 44 links.

**UI to verify**: sidebar "Residuals & Least Squares" → scenario "Curvature" → tab "Residual plot": U-shaped dashed trend;
"Heteroscedasticity" → purple ±2·SD band widens (spread ratio ≫ 1); "High-leverage outlier" → tab "Leverage & influence": point #29 at x = 25 large/yellow,
dashed refit line much steeper, Cook's D ≫ 4/n; "Edge case — all x identical" → warning, no tabs; Points n = 1 → warning.
Tab "Normal equations & checks": all ✅. Projection section: move y1–y3 → e·1 and e·x stay ~1e-16.

Known limitations: diagnostic metrics are heuristics (the outlier scenario also shows a high "curve share"); page 42's footer still says "Page 42 & 43" (not my file).

### `pages\55Convex Functions.py` (475 lines)
- Lab 1 (function select incl. x², |x|, eˣ, x⁴, softplus, sin, x³, double well): chord test with sliders a, b, λ, red markers where the graph rises above the chord,
  live inequality in LaTeX and a 61×61×11 grid scan verdict; Jensen tab (seeded samples, Resample, gap metric); f'' tab (negative region shaded, analytic vs finite-difference table).
- Lab 2: Hessian H = R diag(λ₁, λ₂) Rᵀ surface; bowl / trough / flat / saddle / ridge / dome classification from eigvalsh, det/trace.
- "Local = global" proof + GD from 9 starts on a convex vs a page-54-style double well (one vs two end points).
- ML losses (0–1, hinge, logistic, squared vs margin) + convexity table; concrete non-convexity proof for a 2-unit tanh net via unit swap (midpoint loss 0.266 > 0).
- Lab 3: GD on ½(Lx² + μy²) with sliders L, μ, η, iterations and buttons η = 1/L, η = 2/(L+μ); regime message (monotone / zig-zag / bounce at 2/L / diverge),
  contour path, log-loss curve with the O(1/k) bound (η ≤ 1/L), descent-lemma factor, ρ, κ; worked first 3 iterations; tie-back to page 53's η < 2/λ. Prev 54 / Next 56 links.

**UI to verify**: sidebar "Convex Functions" → select "sin x" → red chord-violation markers + red "Not convex" box; "x⁴" → green scan message, f'' tab shows 0 at x = 0.
Jensen tab: 🎲 Resample changes points, gap ≥ 0 for convex functions, can go negative for sin/double well. Lab 2: λ₂ = −1 → "Saddle ❌"; λ₂ = 0 → "Trough".
Lab 3: L = 4, η = 0.5 → "🏓 bounce"; η = 0.6 → "💥 divergence"; η = 0.3 → zig-zag converging; click "η = 2/(L+μ)" → slider jumps to 0.40.

Known limitations: η buttons round to the slider step (0.01), so "η = 1/L" is approximate for some L; chord-scan verdict is numerical on [−3, 3] only.

### Quizzes
`quizzes\p43.json`, `quizzes\p55.json` — 4 questions each, matching page notation (created the `quizzes\` folder entry files only).


---

## New pages 66 & 72


### pages\66Stacking Linear Layers Collapses.py (new, ~420 lines)
- Intro with the identity W²(W¹x+b¹)+b² = (W²W¹)x + (W²b¹+b²) and why depth needs non-linearity.
- Lab 1: k-layer (1–10) stack 2→w→…→w→2 with seeded random weights; shows W_eff, b_eff, rank per layer and of W_eff,
  max |deep − collapsed| (≈1e-15, checked against 1e-12 × output scale); input grid / deep net / collapsed map plots;
  activation radio (None / ReLU / tanh) makes the grid fold and the collapse break; width 1 shows the rank-1 bottleneck.
- Lab 2: XOR clusters — best linear model (= any-depth linear net, logistic regression via numpy Adam) vs one hidden ReLU
  layer (hand-built 2-unit net or trained numpy net with 2–16 units) with decision-region heatmaps and accuracies.
- Worked example: integer 2→3→2 net, x sliders, Path A (layer by layer) vs Path B (collapsed), ranks.
- AI connection: Transformer MLP needs GELU, W_Qᵀ W_K low-rank bilinear form, linear attention re-association,
  LoRA W + BA (param counter + rank(BA) check). Takeaways + prev(65)/next(67) links.
- UI to verify: sidebar "Stacking Linear Layers Collapses" → Lab 1: move "Number of layers k" → middle and right grids stay
  identical and green success box; pick "ReLU" → middle grid bends/folds, red box with difference; set Hidden width to 1 →
  output grid becomes a line, rank(W_eff)=1. Lab 2: linear panel ≈50 %, ReLU panel 100 %; switch to "Trained" and move
  hidden units to 2 → may get stuck at 75 % with a warning. Worked example: move x₁/x₂ → both paths equal. 🎲 Resample changes all.
- Limitations: trained ReLU net with very few units may get stuck (explained in-page); the "collapsed" map with activations
  on is the activation-free composition (shown to illustrate the mismatch).

### pages\72Train, Validation & Test Splits.py (new, ~500 lines)
- Lab 1: n, noise and train/val/test fraction sliders; sum > 1 or too-small splits → st.error + fallback to 60/20/20;
  sum < 1 → unused (grey) points; scatter coloured by split.
- Lab 2: polynomial degree sweep, choose by validation, report test once; winner's-curse Monte Carlo (200 fresh
  datasets) comparing the selected model's validation MSE vs error on 2 000 fresh points (histograms + medians).
- Lab 3: k-fold CV (numpy) on train+val pool: fold-assignment heatmap, mean ± sd band per degree, per-fold table,
  refit-on-pool test MSE. Lab 4: leakage — duplicate rows (1-NN, random vs group split) and preprocessing
  (scaling + feature selection fit on all data vs scaling only vs inside folds, random labels → true 50 %).
- Lab 5: stratification table (random vs stratified per split) + hypergeometric histogram of positives in validation and
  P(zero positives). Time-series caution: random vs chronological split with a nearest-in-time model + forward-chaining folds.
- Worked example (live split counts and CV mean/sd formulas), AI connection (benchmark contamination, hyper-parameter
  tuning, early stopping → link to page 75), takeaways + prev(71)/next(73) links.
- UI to verify: sidebar "Train, Validation & Test Splits" → set Train fraction 0.9 → red "sum to 1.30 > 1" error and the
  defaults are used; lower Test fraction → grey unused points. Lab 2: change "Largest polynomial degree" → chosen degree &
  metrics update; histogram shows fresh error to the right of validation error. Lab 3: change k → heatmap rows and
  mean ± sd update. Lab 4: dup slider 0 → both accuracies ≈60 %, 0.9 → random split ≈86 %; switch to "Preprocessing" →
  leaky ≈85 % vs honest ≈50 %. Lab 5: positive rate 0.01 → high % of zero-positive validation sets. Time series: random
  MSE ≪ chronological MSE; folds slider changes the expanding-window grid.
- Limitations: Monte Carlo / leakage simulations take ~1 s on first run per setting (cached afterwards); stratified sizes
  can differ by ±1 from the random split because of per-class rounding.

### quizzes\p66.json, quizzes\p72.json (new)
- 4 questions each matching the page notation (collapse formula, bottleneck rank, XOR, LoRA / winner's curse,
  CV mean ± sd, selection leakage, stratification).

Checks: ruff clean; tests\test_static.py passes for these pages (one unrelated failure in page 83 owned by another todo);
smoke + fuzz `-k "66Stacking"` 3 passed, `-k "72Train"` 3 passed; JSON valid.


---

## New pages 76–78 (linear algebra)


Verified: ruff clean; tests/test_static.py (own pages) + smoke + fuzz `-k "76Span or 77Projections or 78SVD"` → 9 passed.
Throwaway numeric checks: null-space/rank–nullity for all presets, P²=P / Pᵀ=P / QQᵀ=P on 200 random (incl. dependent/zero) A,
SVD stage path ends exactly at I, Vᵀ, ΣVᵀ, UΣVᵀ=A on 500 random matrices, Eckart–Young (Frobenius & spectral) for every image,
condition numbers match np.linalg.cond.

### pages\76Span, Basis & Rank.py
- Linear-combination lab: v₁, v₂, c₁, c₂ sliders, tip-to-tail arrows, integer-combination skew grid, ▶ animation tracing 400 seeded random combinations (🎲 Resample).
- det vs numerical rank: float example (v₂ = 3v₁ gives det ≈ −5.6e−17 but rank 1), tolerance select-slider vs NumPy default tol.
- Basis & coordinates: solve Bc = w; dependent basis → "on the line (min-norm pinv solution)" or "no solution (closest point)".
- 3-D span of 1–3 vectors (line / plane / all ℝ³), rank & null space of editable 2×3/3×3 matrix (SVD null basis, rank+nullity=3, rows ⟂ null space).
- AI: embedding numerical rank, LoRA parameter count (r slider), multicollinearity.
**UI to verify:** sidebar "Span, Basis & Rank" → Preset "Parallel (dependent)": purple cloud collapses onto a line, rank 1; press "▶ Trace the reachable set". Preset "Nearly parallel" → lab 2 tolerance 0.1 shows rank 1 vs default 2. Lab 3: w slider with parallel preset shows "no recipe"/closest point. Lab 4: shape 2×3 → nullity ≥ 1; preset "Zero matrix" → nullity 3 warning.
**Limitations:** 3-D vector sliders step 0.5; matrix entries integers −9…9.

### pages\77Projections — Shadows onto Subspaces.py
- 2-D projection onto a line with right-angle marker, a·e ≈ 0, P = aaᵀ/aᵀa; zero vector handled.
- 3-D projection onto plane P = A(AᵀA)⁻¹Aᵀ, pinv fallback for dependent/zero columns; numeric checks P²=P, Pᵀ=P, Aᵀe=0, eigenvalues {0,1}.
- Gram–Schmidt step-by-step (skips dependent columns), QQᵀ = P.
- Least squares as projection (seeded data, Σr = 0, Σxr = 0, degenerate identical-x case → pinv; n = 3 shows y, ŷ, r in ℝ³). Links page 43.
- AI: regression, attention (scores are dot products; output is a weighted average, *not* a projection), toy hard-debiasing table with caveat.
**UI to verify:** "Projections" → lab 2 preset "Dependent columns" → warning + column space becomes a line; lab 4 set n = 3 → 3-D plot appears; tick "Degenerate" → warning and flat fit line.
**Limitations:** debiasing uses toy 3-D vectors.

### pages\78SVD — Rotate, Stretch, Rotate.py
- Editable 2×2 (presets: shear, symmetric PSD/indefinite, rotation, near-singular, singular); Plotly animation circle → Vᵀ → Σ → U = ellipse (reflections shown as flips), plus UΣVᵀ LaTeX and orthogonality/reconstruction checks.
- Singular values vs eigenvalues table (complex λ supported), σ₁σ₂ = |det| = |λ₁λ₂|, symmetric/PSD messages.
- Rank-k approximation of 3 deterministic 64×64 synthetic images (+ optional seeded noise), Eckart–Young errors, σ log-bar + cumulative energy plot, storage count.
- PCA = SVD of centred data (σ²/(n−1) vs eig(cov)), condition number lab (ε select-slider, error amplification bound), AI tabs incl. small rank-2 recommender demo.
**UI to verify:** "SVD — Rotate, Stretch, Rotate" → press "▶ Play circle → ellipse"; preset "Shear" → σ 1.618/0.618 vs λ 1,1; image k = 64 → "Full rank … exact"; noise 0.3 + k ≈ 10 looks cleaner; ε = 0 → singular error.
**Limitations:** animation interpolates reflections as a squash-through-zero flip; images are synthetic (no external data).

### quizzes\p76.json, p77.json, p78.json
4 questions each, matching page notation/numbers.

Note: a temporary `tests\test_static.py` failure in page 83 (unprefixed keys) during parallel work was fixed before the final run.


---

## New pages 79–81 (calculus)


### `pages\79Limits & Continuity.py` (472 lines) + `quizzes\p79.json` (4 questions)
- **Limit table lab**: 8 presets (sin x/x at 0, (x²−1)/(x−1) at 1, step, sign, 1/x, 1/x², sin(1/x), continuous x² at 2), log-scale h slider (10⁻⁸…1), table of f(a−h), f(a+h) per decade, plot with holes/one-sided limits/f(a) markers, optional zoom to [a−3h, a+3h]; verdict for left/right limit and whether the two-sided limit exists.
- **ε–δ lab**: 3x+1 (δ* = ε/3) or x² at any a (δ* = √(a²+ε) − |a|, derived + verified with 20 000 samples); "your δ" multiplier shows success/failure with a witness x.
- **Continuity**: 3-condition checklist evaluated for the chosen preset; table of discontinuity types.
- **Kinks**: |x|, ReLU, x², softplus — left/right/central difference quotients, exact one-sided derivatives, half-tangents; subgradient interval; warning that central differences hide kinks.
- **AI tabs**: ReLU subgradient convention (PyTorch/JAX use 0) and L1 sparsity; finite-difference error-vs-h U-curve (sin at 1; best forward h ≈ 3e−9, central ≈ 3e−6) + link to page 44; softmax(z/T) with temperature slider and tie checkbox (T→0 → argmax / even split over ties).
- Nav: previous 49, next 80.

**UI to verify**
- Sidebar → "Limits & Continuity". Preset "Removable hole: sin(x)/x" → move "log₁₀ h" to −8: both table columns → 1.000000000, green "exists and equals 1".
- Preset "Jump: sign(x)" → red "left limit −1 ≠ right limit 1"; section 3 shows ✅ f(a) defined, ❌ limit exists.
- Preset "Oscillating: sin(1/x)" + toggle "Zoom" → noisy band; metrics say "does not exist (oscillates)".
- Section 2: Function "Quadratic", ε = 0.5, a = 1 → δ* = 0.22474; set multiplier 1.05 → red "δ too big" with witness x.
- Section 4: ReLU at x₀ = 0 → right quotient 1, left 0, central 0.5, red "Not differentiable" + subgradient [0, 1]; move x₀ to 0.5 and h to 1e−3 → green.
- Section 6 tab "Softmax": drag log₁₀ T to −2 → bar for class 0 ≈ 1; tick "Make a tie" → class 0 and 3 at 0.5.

**Known limitations**: one-sided limits/verdicts are stored per preset (exact math), the table is numerical evidence; at h ≈ 1e−8 with zoom, (x²−1)/(x−1) shows floating-point round-off (captioned).

### `pages\80Product & Quotient Rules.py` (314 lines) + `quizzes\p80.json` (4 questions)
- **Growing rectangle**: f = 1+x (width), g = 1+x²/2 (height), Δx slider; colored base, two strips (gΔf, fΔg) and corner ΔfΔg; table for Δx = 1…0.001 showing corner/Δx → 0 and ΔA/Δx → f′g + fg′.
- **Rule explorer**: product/quotient of any pair from {x², x³−2x, x²+1, sin, cos, eˣ, ln x}; symbolic-like LaTeX of the rule, exact value vs central difference (h = 1e−5) with |error| (~1e−10), "wrong guess" f′g′ or f′/g′; plot of h and h′ with gaps at domain/poles; errors for ln domain (x ≤ 0), g(x) = 0; warning near poles or when the FD stencil leaves the domain.
- **Worked example** with the explorer's numbers substituted step by step + numeric check.
- **σ′ = σ(1−σ)** derived via quotient rule, live x slider (quotient form, σ(1−σ), FD all agree); tanh′ = 1 − tanh².
- **AI tabs**: softmax Jacobian diag(s) − ssᵀ via quotient rule, checked by FD; x/‖x‖ Jacobian (I − uuᵀ)/‖x‖ with sliders, Jx = 0, x = 0 error. Nav: 79 / 46 / 81.

**UI to verify**
- Sidebar → "Product & Quotient Rules". Move "Δx (nudge)" toward 0.01 → red corner shrinks; table last column → 0.
- Explorer default (x² · sin x at x = 1): rule 2.22324…, central diff equal, error ~1e−10, wrong guess 1.0806.
- Operation "Quotient f/g", g = "sin x", x = 0 → red "division by zero"; f = "ln x", x = −1 → red domain error; worked example says to move x.
- Section 4: x = 0 → σ′ = 0.25; x = 8 → ≈ 0.000335.
- Section 5 tab "Normalization": set x₁ = x₂ = 0 → red undefined message; 3,4 → J = [[0.128, −0.096], [−0.096, 0.072]].

**Known limitations**: curves are clipped at |value| > 25 for display; explorer uses a fixed function library (no free-form input).

### `pages\81Taylor Series — Local Approximation.py` (401 lines) + `quizzes\p81.json` (4 questions)
- **Explorer**: eˣ, sin, cos, ln(1+x), 1/(1−x), sigmoid; center a (per-function range keeps a inside the domain) and order n 0–10; f vs P_n (+ two previous orders faint), convergence interval shaded, |f − P_n| on log scale. Coefficients: closed forms; sigmoid via reciprocal power series of 1 + e^{−a}e^{−t} (verified vs exact rational derivative-polynomial recurrence, rel. err ≤ 1e−13 up to order 30).
- **Radius of convergence**: evaluate-at-x slider, |P_n(x) − f(x)| vs n up to 30 (log) → converges inside R, diverges outside (R = 1+a, 1−a, √(a²+π²), ∞). **Lagrange bound** for exp/sin/cos checked (tolerance for float round-off; brute-force checked over a grid of a, x, n).
- **Worked example**: coefficient table c_k, terms, P_n(x), error.
- **GD vs Newton**: 4 losses (quadratic, log-cosh, quartic, non-convex), x₀ and η sliders; tangent and quadratic models, one GD and one Newton step, 8-step table for each (nan on divergence), f″ = 0 error, f″ < 0 warning, η < 2/f″ stability note; η table showing linear-prediction relative error ≈ f″η/2.
- **AI tabs**: GELU tanh approximation with adjustable cubic coefficient (max error 4.73e−4 at 0.044715; ~70× worse at c = 0) vs pure Taylor; second-order optimization (Newton, L-BFGS, K-FAC/Shampoo, Adam caveat) and learning-rate validity. Nav: 80 / 82.

**UI to verify**
- Sidebar → "Taylor Series — Local Approximation". f = ln(1 + x), a = 0, raise n → fit improves only on (−1, 1); "Evaluate at x" = 1.5 → red "diverge", error curve rises with n.
- f = σ(x): R = π shown in the LaTeX line; f = eˣ, x = 3 → Lagrange bound line with green "Bound holds".
- Section 4: Loss "Quadratic", x₀ = −1 → Newton lands at 1.0000 in one step; GD with η = 0.1 at −0.2. Loss "log-cosh" x₀ = −1 → Newton column diverges to nan. Loss "Quartic", x₀ = 0 → red "Newton step undefined". Loss "Non-convex", x₀ = 0 → warning f″ < 0.
- Section 5: move cubic coefficient slider to 0 → max error metric ≈ 3.4e−2.

**Known limitations**: Lagrange bound shown only for exp/sin/cos (others explained in text); plot y-ranges are fixed per function so high-order P_n can leave the view.

### Verification
- `ruff check` on the 3 pages: clean. `pytest tests\test_static.py`: pass. Smoke + fuzz (`-k "79Limits or 80Product or 81Taylor"`, excluding app reachability before platform mapping): pass, also with `-W error::RuntimeWarning`.
- Extra scripted AppTest sweep over all presets/function pairs/edge values (domain errors, poles, zero vector, extreme sliders): no exceptions.
- All formulas/numbers verified with throwaway python (sigmoid coefficients, δ*, GELU error, Lagrange bound, FD optimal h, Jacobians, quiz answers).


---

## New pages 82–83 (calculus)


### pages\82Jacobian & Hessian.py
- **Lab A (Jacobian):** four R²→R² presets: linear map, polar→Cartesian, the nonlinear warp (x²−y², 2xy), and 2-logit softmax. A grid square around p (half-width h) is shown next to its true image (blue) and the Jacobian's linear approximation (orange dashed), plus the J-columns as arrows.
- Metrics: det J, the signed image-area ratio from the shoelace formula (it approaches det J as h → 0), the max linearisation error (scales with h²), and max |J_analytic − J_numeric| from central differences (~1e-11).
- **Lab B (Hessian):** four functions: bowl, saddle, Rosenbrock and x⁴+y⁴. It includes an eigenvalue-based classification (min/max/saddle/inconclusive/not critical) and a contour map with the Hessian eigenvectors and the direction v. Other panels:
  - a vᵀHv-vs-θ curvature plot (Rayleigh quotient between λ₁ and λ₂)
  - a 1-D slice of the true function vs the quadratic Taylor model, plus a 3-D comparison in an expander
  - Newton vs gradient-descent paths, with a pseudo-inverse fallback when H is singular and a divergence guard
  - a saddle warning explaining why Newton is attracted to saddles
  - a numeric Hessian check
- Worked example with live numbers: J, J_num, det, the closed-form eigenvalue formula, vᵀHv, and the Newton and GD steps.
- AI section:
  - VJPs in backprop
  - a 3-logit softmax Jacobian diag(p)−ppᵀ checked against finite differences; J·1 = 0, and the VJP with a cross-entropy upstream gradient equals p − y
  - condition number and the η < 2/λmax bound using Lab B's Hessian (links page 53)
  - sharp vs flat minima plot
- Links to page 17 (determinant) and page 53. Prev/Next links to 81 and 83.

**UI to verify**
1. Sidebar "82 · Jacobian & Hessian" → Lab A, default linear map: the blue and orange grids overlap exactly, and det J = area ratio = 1.32.
2. Select "Polar → Cartesian" and move x₀ (r) to 0: det J = 0 and the warning appears. Make h smaller: the area ratio approaches det J and the linearisation error shrinks about 4× each time h halves.
3. Select "Softmax over 2 logits": the image collapses onto the line p₁+p₂=1 and det J = 0.
4. Lab B, select "Saddle": the Newton path (orange diamonds) jumps to (0,0) in one step and the warning is shown. GD slides away along y.
5. Select "Rosenbrock" and turn on "Snap the point to the critical point": classification is local minimum and κ ≈ 2508. In the AI section, the stable-η bound reads ≈ 0.001997.
6. Select "Quartic" and snap: the result is "inconclusive" and the condition number shows ∞ (singular).
7. Move the θ slider: the yellow dot moves along the vᵀHv curve, staying between the λ lines, and the slice plot updates.
8. AI section: move the logits and the true class. A green box confirms that J matches J_num and that the VJP equals p − y.

**Known limitations:** the linear-map matrix A and the eigenvector-arrow length are fixed. Contour colours use log₁₀(1+f) for Rosenbrock only. GD runs at most 40 steps and Newton at most 8.

### pages\83Automatic Differentiation.py
- A minimal reverse-mode engine in pure Python: a `Value` class with +, ·, neg/sub, pow, sin, exp and sigmoid. Each op records its local derivatives, followed by a topological sort and `backward()` with an optional step limit.
- Three expressions:
  - f(x,y) = (x·y + sin x)·exp(−y)
  - the neuron loss L = (σ(wx+b) − t)²
  - g(x) = x·x·x, where x is used three times
- A graph is drawn with `st.graphviz_chart` (DOT string) showing the value and gradient of every node and the local derivatives on the edges. A step slider walks the reverse topological order; the current node is red and finished nodes are green ✓. A node table shows the local derivatives, what each node saves for backward, and how many messages it received.
- A gradient-accumulation panel lists the per-path messages for reused inputs. The toggle "Buggy engine: overwrite (=)" produces visibly wrong gradients, and finite differences catch the error.
- Comparison table: reverse-mode AD vs dual-number forward mode vs analytic vs central finite differences. AD error is about 1e-17 or exactly 0; FD error is about 1e-11 to 1e-10.
- A forward-mode expander shows a per-node tangent table for a chosen seed input. The worked example shows the "sum over paths of products of local derivatives".
- AI section: PyTorch autograd and JAX code snippets, a cost plot (forward mode needs n passes, reverse mode needs 1), activation memory and checkpointing, and zero_grad/accumulation.

**UI to verify**
1. Sidebar "83 · Automatic Differentiation": the graph shows 8 nodes, all with gradients and green ✓.
2. Drag the "Backward-pass step" slider to 0: only the output has grad = 1 and the rest show "grad = ?". Step forward: the red node moves right-to-left and its edges turn red.
3. Default x=1, y=0.5: the accumulation panel shows ∂f/∂x = 0.3277 + 0.3033 = 0.6310. The comparison table shows 0.630975 in all four method columns.
4. Turn on the buggy toggle: the AD column is wrong (x: 0.303265) and red error boxes appear. Choose "g(x) = x·x·x": buggy 2.25 vs correct 6.75.
5. Choose the neuron loss: there are 4 sliders and 4 rows that all agree. The buggy toggle makes no difference, and a caption explains why.
6. Open the "dual numbers" expander and switch the seed radio: the tangent column changes, and the output tangent equals that input's partial derivative.

**Known limitations:** scalar-only engine with a fixed set of ops. The graph layout comes from Graphviz (left-to-right), and edge labels can overlap for x·x (two parallel edges).

### quizzes\p82.json, quizzes\p83.json
- Four questions each, matching the page notation. p82 covers det J as area scaling, an inconclusive Hessian test, Newton attracted to a saddle, and why the softmax Jacobian is singular. p83 covers accumulation for a reused variable, why reverse mode is used for training, dual-number arithmetic, and activation memory.

### Checks run
- ruff passed on both pages; test_static.py passed; smoke and fuzz `-k "82Jacobian or 83Automatic"` passed (6 tests). An extra combinational fuzz (every preset × slider extremes, every expression × slider extremes × seed × buggy) found no exceptions. Numbers were checked by script (listed above).


---

## New pages 84–86 (probability)


### pages\84Joint & Marginal Distributions.py (+ quizzes\p84.json)
- Discrete joint table weather × activity (3×3 editable `number_input` counts, ≥0, decimals allowed) → joint heatmap, marginals (table margins + bar charts), conditionals (rows/columns re-normalized; zero-probability conditioning flagged as undefined).
- Independence check: P(x)P(y) heatmap, signed gap heatmap, max |gap| metric; "🔗 Make independent" sets the table to the outer product of marginals (rescaled if a cell would exceed the 1000 input max); "↩️ Reset example table".
- Worked example: pick a cell → P(x,y), P(x), P(y), P(y|x), P(x)P(y) live in LaTeX.
- Continuous lab: bivariate Gaussian (μx, μy, σx, σy, ρ or σxy entered directly), Σ shown with det & eigenvalues; non-PSD Σ → st.error and stop; |ρ|=1 handled as singular (eigen-sampling, no density). Contour + seeded samples + marginal histograms with N(μ,σ²) overlays; conditional slice at y₀ = μy + z·σy: formula mean vs numerical slice mean vs nearby-sample mean, conditional variance σx²(1−ρ²). Links to 26, 40, 41, 85.
- UI to verify: sidebar "84 · Joint & Marginal Distributions" → change "Sunny/Walk" count → heatmaps update; press "Make independent" → green "independent" success, conditional rows all equal; tab "Conditionals" radio switches rows/columns. Lab 2: move ρ → contours tilt, red slice line; "Slice position" slider → formula and numerical means match (delta ~1e-10); radio "Covariance σxy directly", set σxy=5 → red PSD error; ρ=1 → singular warning; "🎲 Resample" changes the cloud.
- Limitations: the table is fixed 3×3 with fixed category names.

### pages\85Poisson & Exponential Distributions.py (+ quizzes\p85.json)
- Poisson PMF + CDF (λ 0.1–60), mean/variance computed from the PMF (= λ), mode text, e^(−λ); optional continuity-corrected N(λ,λ) overlay with TV distance (small vs large λ).
- Binomial(n, λ/n) → Poisson: overlay, exact TV distance, TV-vs-n log-log curve with Le Cam bound λ²/n (verified to hold on the whole slider grid).
- Seeded Poisson process (rate, window T, 🎲 Resample): timeline, counts-per-minute vs Poisson PMF, gaps vs λe^(−λt), exponential CDF/survival + empirical survival, mean/median markers.
- Memorylessness: formula vs simulation (200k seeded draws; "too few survivors" handled) and a same-mean Uniform(0, 2/λ) counter-example plot. Worked example: server capacity c → P(K>c) via scipy `poisson.sf`, P(K=0), P(K=1), P(T>0.5).
- UI to verify: "85 · Poisson & Exponential Distributions" → λ slider to 0.3 (skewed, TV large) and 50 (bell, TV small); Lab 2 n slider 10→1000 → red dot slides down below the dashed bound; Lab 3 "🎲 Resample" changes timeline; Lab 4 s slider → orange dashed exponential curve stays on the blue one, uniform curves diverge; rate=10 & s=5 → "too few survivors".
- Limitations: counts-per-minute variance is noisy for short windows (30 samples by default).

### pages\86Beta Distribution — Beliefs about Probabilities.py (+ quizzes\p86.json)
- Beta(α,β) explorer (0.1–20): PDF with mean/mode lines, mean/variance/mode metrics for every shape (interior, edge, U-shape, flat) cross-checked against `scipy.stats.beta.stats`; plot clipped at edge spikes; 4-shape gallery.
- Bayesian coin: prior α₀, β₀ (pseudo-counts), credible level; data from seeded flips (true p slider, Flip 1/10/100, reset, new seed; capped 10,000) or typed counts. Prior, normalized likelihood, posterior Beta(α₀+h, β₀+t), shaded equal-tailed credible interval via `beta.ppf`, MLE (undefined at n=0), history plot of posterior mean & band vs flips.
- Worked example: conjugacy derivation, posterior mean = weighted average of prior mean and MLE (weights shown), credible interval, Laplace smoothing (h+1)/(n+2); link to 27 Bayes.
- Thompson sampling: 3 arms (true-rate sliders), Step 1 / Run 50 / Reset / new seed (deterministic replay, cap 3000 rounds), posteriors per arm, cumulative regret, P(arm is best) by seeded Monte Carlo, last-round draws.
- UI to verify: "86 · Beta Distribution — Beliefs about Probabilities" → α=β=0.5 → U-shape + info box; α=β=1 → flat, mode "every p". Lab 2: click "Flip 100" a few times → posterior narrows around red true-p line, band plot narrows; radio "Type counts" (7 H / 3 T, prior 2,2) → posterior mean 0.6429. Lab 3: "Run 50 rounds" several times → arm 3 (0.60) gets most pulls, P(arm 3 is best) → ~1, regret flattens.
- Limitations: Thompson history is replayed from the seed each rerun (fast up to the 3000-round cap); changing a true-rate slider replays the whole history with the new rates.

### Verification
- ruff clean; tests\test_static.py passes for these pages (the only failure is 83Automatic Differentiation, owned by another todo); smoke + fuzz `-k "84Joint or 85Poisson or 86Beta"`: 9 passed. Quiz JSON valid (4 questions each).
- Throwaway numeric checks: Poisson mean/var = λ, Le Cam bound never violated (λ 0.5–10, n 10–1000), Beta moments vs scipy, Gaussian conditional mean/variance vs numerical slice integration; AppTest interaction checks (make independent → success, σxy=5 → error, ρ=1 → warning, flips, Thompson steps, counts mode).


---

## New pages 87–89 (probability & information)


All numbers cross-checked with scipy/sklearn (BCE = −ℓ/n; Gaussian NLL formula = scipy `norm.logpdf` sum;
t-crit, chi² = z², power formula vs 200k-run simulation within 0.001; BSC I = 1 − H_b(ε), 3-ary channel,
KL(p(x,y)‖p(x)p(y)) = H(X)+H(Y)−H(X,Y)). Checks: ruff clean, test_static 203 passed,
smoke + fuzz for the 3 pages: 9 passed.

### pages\87Maximum Likelihood Estimation.py (Probability & Statistics)
- Likelihood vs probability; seeded Bernoulli coin lab (n, true p) with relative likelihood L(p)/L(p̂) and log-likelihood (nats), star at h/n.
- Worked derivation p̂ = h/n; table showing −ℓ(p)/n = averaged binary cross-entropy (nats, and bits).
- Gaussian lab: μ̂, σ̂²(1/n) vs s²(1/(n−1)); 2-D log-likelihood contour over (μ, σ); 4000-dataset bias simulation vs (n−1)/n·σ²; Gaussian NLL = const + n/(2σ²)·MSE (scipy vs formula).
- Gradient ascent in logit space (x̄ − σ(θ)) converging to h/n; boundary case h ∈ {0, n} warns θ → ±∞.
- Small-n overfitting table (n = 3) MLE vs MAP with Beta(a, a) prior (link to page 86); AI: training = MLE, priors/weight decay/label smoothing = MAP-like.

**UI to verify:** sidebar "87 · Maximum Likelihood Estimation" → move "True (hidden) bias p" to 0 and "Number of flips n" to 3: star moves to p = 0, two warnings appear, Lab 3 final p creeps towards 0; "Try a model p" → pink dot moves on ℓ curve, both table rows stay equal; "Sample size n" (Lab 2) = 2 → avg σ̂²_MLE ≈ half of σ²; "Candidate prediction μ" → both NLL metrics change together; "Prior strength a" = 1 → MAP column equals MLE.

**Limitations:** the contour grid is centered on the MLE, so the true (μ, σ) marker can be off-screen for tiny n.

### pages\88Confidence Intervals & Hypothesis Tests.py (Probability & Statistics)
- Sampling distribution of x̄ (3000 seeded experiments, Normal or skewed population) vs N(μ, σ²/n).
- 100 t-intervals x̄ ± t·s/√n (scipy.stats.t) colored by coverage, counts + coverage over 3000; misinterpretation warning; worked CI; t vs z width; one-sample t-test (scipy ttest_1samp) with CI duality.
- A/B two-proportion pooled z-test: p-value tail area shaded on N(0,1), ±z critical lines, chi² cross-check, Type I/II verdict, error table.
- Power curves vs n for 0.5×/1×/2× effect (formula) + simulated points (2000 runs each), n for 80% power.
- 20 null tests (−log10 p bars) with α and Bonferroni lines, false-positive counts, FWER theory vs simulation; AI: "+0.5% accuracy" calculator, benchmark noise, paired-test note.

**UI to verify:** sidebar "88 · Confidence Intervals & Hypothesis Tests" → "Confidence level" 0.80 → ~80 green intervals; "Population" skewed + n = 2 → coverage drops below nominal; "Null value μ₀" 40 → p < 0.05 and "inside CI? no"; A/B "True lift" 0 → power row shows α, a rejection is labelled Type I; "Users per arm" 50000 → shaded tail shrinks; "Run 20 new null tests" → bars change, ~1 yellow per run; "Test-set size" 100000 → +0.5% becomes significant.

**Limitations:** A/B uses the normal approximation (pooled z); AI calculator uses an unpaired test (caption explains paired McNemar is better).

### pages\89Mutual Information.py (Information Theory, after 57–60)
- I(X;Y) = H(X)+H(Y)−H(X,Y) = KL(p(x,y)‖p(x)p(y)) in bits; 2×2/3×3 joint with presets: Independent (I = 0), Deterministic copy (I = H(X)), Noisy channel (ε slider, closed form + capacity curve), Custom (st.data_editor; NaN/negative/inf → 0 with warnings; all-zero → uniform with error; normalized).
- Heatmaps of p(x,y) vs p(x)p(y), table with marginals, six entropy metrics, information-diagram bars, H(Y|X) computed row-by-row as a check, information-gain sentence.
- MI vs correlation lab: y = x² (r ≈ 0, high binned MI), linear, independent; bins/n/noise sliders; shuffled baseline + (b−1)²/(2n ln 2) bias; optional sklearn mutual_info_regression (nats → bits).
- AI: feature selection, InfoNCE bound, decision-tree information gain (links 58, 60, 84, 88).

**UI to verify:** sidebar "89 · Mutual Information" → preset "Noisy channel", ε = 0.1 → I = 0.5310 bits and star on the curve; ε = 0.5 → 0; size 3×3 + "Deterministic copy" → I = H(X) = 1.4855; "Custom" → edit a cell to −1 or clear it → warning, values renormalize; Lab 2 "Histogram bins per axis" 40 with "independent" → shuffled/bias metrics grow; tick the sklearn checkbox → extra metric.

**Limitations:** the data editor is not exercised by the fuzz test; the binned estimator is crude by design (bias is explained on-page).

### quizzes\p87.json, p88.json, p89.json
4 questions each, matching page notation (bits on 89, nats on 87).


---

## New pages 90–92 (optimization)


Files created: `pages\90Momentum.py`, `pages\91RMSProp & Adam.py`, `pages\92Learning-Rate Schedules.py`,
`quizzes\p90.json`, `quizzes\p91.json`, `quizzes\p92.json`. No other files touched.
All optimizers are implemented in numpy on the Python side (deterministic, seeded via `pNN_seed` + 🎲 buttons).

### pages\90Momentum.py
- Lab 1 "narrow valley race": f = ½(a x² + b y²), a = 1, b = κ (slider 1–200); step set as η·λ_max; plain GD vs
  heavy-ball vs Nesterov trajectories on a Plotly contour + loss curves (log). Steps-to-tolerance table (f/f₀ ≤ 1e-6)
  with theory rate ρ (eigen-analysis of each method) and rows for textbook-optimal GD / heavy-ball (κ vs √κ).
- Worked example: first two heavy-ball steps with the live numbers.
- Tabs: exponentially weighted average (window 1/(1−β), weight 1−βⁿ, zig-zag damping A(1−β)/(1+β) theory vs seeded
  measurement); too much momentum (ringing, sign changes, critical damping β = (1−√(ηλ))²); bumpy 1-D landscape with
  a shallow dip, seeded noisy gradients, escape rate over 40 seeds per β; stability region heatmap (ρ from roots)
  with the boundary ηλ = 2(1+β), verified by renormalised simulation (100% agreement, max |Δρ| ≈ 0.002), plus
  Nesterov's smaller range ηλ < 2(1+β)/(1+2β) (derived via Jury test, simulation-checked).
- AI connection: SGD + momentum 0.9 for CNNs/ResNet, PyTorch convention, effective lr η/(1−β).

**UI to verify**: Sidebar → Optimization → "Momentum". Lab 1 default (κ=50, η·λ_max=1.3, β=0.9): red GD zig-zags
and is slowest; table shows HB ≈ 109 and Nesterov ≈ 53 steps vs GD ≈ 223. Move η·λ_max to 1.6 → only Nesterov
diverges (red error box). Move β to 0 → HB equals GD. Tab "Escaping a shallow dip": β=0 table row 0%, β≥0.8 ≈100%;
click 🎲 Resample noise → numbers change slightly. Tab "Stability region": blue markers move with Lab 1 sliders;
metric shows 100.00% agreement.

**Limitations**: "predicted steps" uses only the asymptotic rate (rough for repeated roots / fast-direction-dominated
starts — stated in caption). Plot box is fixed; diverging paths are clipped to it.

### pages\91RMSProp & Adam.py
- Intuition cards: AdaGrad → RMSProp (ρ) → Adam (β₁, β₂, ε, bias-corrected m̂, v̂).
- Lab 1: landscapes (a) ill-conditioned bowl with κ slider and rotation 0–45°, (b) Rosenbrock, (c) badly scaled
  features (gradient scales differ 10⁴×); SGD/Momentum/AdaGrad/RMSProp/Adam trajectories + loss curves + summary table;
  per-landscape default learning rates (keys `p91_lr_*_{landscape}`); hyper-parameters in an expander.
- "Inside Adam": first steps table (g, m, v, m̂, v̂, step, step/η, step/η without bias correction) for x or y, latex of
  step 1 (= η·g/(|g|+ε) ≈ η·sign g) and the uncorrected factor (1−β₁)/√(1−β₂) = 3.16 for defaults; plot of |step|/η.
- Tab "Myth": Adam ≠ sign descent — steady-state m̂/√v̂ ≈ μ/√(μ²+σ²) (signal-to-noise), seeded simulation vs formula.
- Tab "AdamW vs Adam + L2": two unused weights with loud (σ=10) vs quiet (σ=0.1) gradient noise; Adam+L2 barely decays
  the loud one and crushes the quiet one; AdamW shrinks both like (1−ηλ)ᵗ (20 seeded runs averaged).
- AI connection: PyTorch AdamW defaults, β₂ = 0.95 in LLM pretraining, ε, why AdamW, optimizer-state memory (56 GB for 7B fp32).

**UI to verify**: Sidebar → "RMSProp & Adam". Default bowl: Adam/Momentum reach f < 1e-6, SGD does not. Set rotation
to 45° → Adam's final f gets much worse (≈0.39) while SGD is unaffected. Choose "Badly scaled features" → SGD/Momentum
barely move in y; RMSProp/Adam go straight to (1,1). "Inside Adam" table: step/η = −1.000 at t=1 and −3.162 in the
"no bias correction" column. Open hyper-parameters, set β₂ = 0.9 → text switches to "too small". Tab "AdamW vs Adam + L2":
table ≈ Adam+L2 0.84 / 0.07, AdamW 0.20 / 0.23, pure decay 0.135.

**Limitations**: one shared η for the three adaptive methods (AdaGrad usually wants a larger η — stated in the page).
All runs are full-batch (deterministic) except the noise demos.

### pages\92Learning-Rate Schedules.py
- Lab 1: constant, step decay, exponential, cosine, warmup + cosine, 1-cycle (PyTorch OneCycleLR defaults), inverse-√t
  (Transformer) with sliders (η_max, T, W, η_min ratio, step every/γ, 1-cycle rise fraction, log toggle); 2/L line.
- Worked example: η(t) checkpoint table for all schedules + live latex of warmup+cosine at t = T/2.
- Lab 2: seeded logistic regression (400 points, Newton-solved optimum), mini-batch SGD with identical batches for every
  schedule; excess-loss curves (log) and final-loss table; curvature tie-in L = λ_max(XᵀX)/(4N) and λ_max(H*).
- Tabs: noise floor (formula ησ²/(2(2−ηλ)) vs 400 seeded chains; constant η, η/2, cosine); warmup instability demo on
  f = ½w² + ¼w⁴ (|w| grows iff η(a+w²) > 2; constant η diverges iff η > 2/(a+w₀²), warmup survives); learning-rate finder.
- AI connection: warmup + cosine in GPT-3/LLaMA, WSD, Transformer inverse-√t, step decay/1-cycle for CNNs, LR finder.

**UI to verify**: Sidebar → "Learning-Rate Schedules". Default: table in Lab 2 puts Constant last (≈4e-2) and decayed
schedules ≈3e-3. Set batch size 400 → all curves smooth, decayed ones reach ~1e-5. Set η_max = 8 → yellow warning about
2/L. Tab "Why decay": measured 0.1246 vs formula 0.1250 at η=0.4. Tab "Why warmup": constant η_max = 0.5 "diverged 💥",
warmup run converges; set η_max to 0.15 → both converge. Click 🎲 Resample data & batches → curves/LR-finder change.

**Limitations**: Lab 2's model is convex, so warmup gives little benefit there (stated; the warmup tab uses a toy with
high initial curvature instead). LR-finder suggestion is noisy by design (caption says so).

### Checks run
`ruff check` (3 pages) clean; quiz JSON loads; `tests\test_static.py` passes; smoke + fuzz with
`-k "90Momentum or 91RMSProp or 92Learning"`: 9 passed (render, reachable from app, widget fuzz). Full `test_static.py`: 205 passed.


---

## New pages 93–95 (deep learning)


### pages\93Weight Initialization.py (+ quizzes\p93.json)
- Deep bias-free MLP lab: depth 2–50, width 16–256, ReLU/tanh, 5 schemes (N(0,1), N(0,0.01²), Xavier, He, orthogonal with gain √2 for ReLU / 1 for tanh). All schemes share the same seeded Gaussian draws.
- Three log plots per layer: std of activations (forward), ‖∂L/∂h_ℓ‖ (backward signal), ‖∂L/∂W_ℓ‖ (loss = fixed random read-out; backward pass verified against finite differences). Metrics with vanishing/stable/exploding verdicts, tanh saturation %.
- Activation histograms (h or z) for layers 1, L/3, 2L/3, L.
- Derivation Var(z)=n·Var(w)·E[x²] (½ for ReLU) with a live 40 000-sample check; table of predicted vs measured Var(z_L) for all schemes.
- Symmetry lab: 3→4(tanh)→1 net trained 150 GD steps from zeros / constant c / random; gradient + final W₁ heatmaps, "distinct hidden units" metric.
- AI: PyTorch default kaiming_uniform_(a=√5) ⇒ Var = 1/(3 n_in); GPT-2 1/√N residual scaling, DeepNet.

**UI to verify** (sidebar "93 · Weight Initialization"):
- Lab 1: select "He / Kaiming" + ReLU → green bold curve flat around 1; switch to "Xavier / Glorot" → decays ~×0.7/layer; "N(0, 1)" → explodes (10⁴⁰+); tanh + N(0,1) → forward flat near 1 but backward ratio huge, saturation % high. Toggle overlay off → single curve. Click 🎲 Resample → curves change slightly.
- Expander histograms: radio pre/post activation, x-ranges differ per scheme.
- Section 2: move fan-in/σ_w/σ_x; "Empirical Var(z)" within a few % of formula; ReLU inputs → ½ factor appears in LaTeX.
- Section 4: "All zeros"/"constant" → 1/4 distinct units + warning; "Small random" → 4/4.

Limitations: overlay at width 256/depth 50 is several 256×256 QRs (orthogonal) — can take a few seconds on a slow/loaded machine (cached afterwards). For narrow ReLU nets prediction vs measurement agree only to order of magnitude (finite-width drift, stated in caption).

### pages\94Dropout.py (+ quizzes\p94.json)
- 8×12 activation grid: keep-probability slider, train/eval radio, inverted vs classic scaling checkbox, mask & output heatmaps, kept-unit count.
- Expectation check over up to 5000 seeded masks: mean of m·h/(1−p) ≈ h (scatter vs y = h and y = (1−p)h), Var = h²p/(1−p) verified for one unit.
- Ensemble: 2⁹⁶ sub-networks; exact enumeration of all 1024 masks on a 10-input toy shows ensemble mean = eval output for a linear model, only approximate with ReLU.
- Overfitting: 14-point sin(3x) regression, 1→48→48→1 ReLU MLP, 1200 full-batch Adam steps (~0.3 s per run, cached) with/without dropout; train/val curves + fitted functions.
- MC dropout: T stochastic passes of the dropout net → mean ± 2 std band, std inside vs outside data range. Worked example with binomial count of kept units. AI: residual/attention dropout, DropConnect, DropPath, why LLMs use little dropout.

**UI to verify** (sidebar "94 · Dropout"):
- Lab 1: move "Keep probability" → mask darkens, output brighter (scaled); uncheck inverted → warning; "Evaluation" → all-white mask, output = h. 🎲 Resample mask changes mask.
- Expectation slider "number of random masks": green dots approach y = h.
- Lab 3 (default seed): red val curve rises to ≈1.0 while green (p=0.30) stays ≈0.19; 🎲 Resample data changes it (dropout not always better — caption says so).
- Lab 4: band wider in grey shaded extrapolation zones; T slider changes smoothness.

Limitations: with 14 points the dropout benefit varies by seed (honestly stated). MC-dropout uncertainty is approximate.

### pages\95Batch Normalization.py (+ quizzes\p95.json)
- One-feature batch lab: shift/scale/B/ε/γ/β, histograms of x, x̂, y, metrics (mean x̂ = 0, var x̂ = σ²_B/(σ²_B+ε)); "undo" checkbox sets γ=√(σ²_B+ε), β=μ_B ⇒ y = x exactly. Worked example table + LaTeX.
- Batch-size noise: 400 seeded batches per B ∈ {2..256}: std of μ_B vs σ/√B, σ_B 5–95% band, same example normalised in different batches.
- Running averages (PyTorch convention, unbiased variance, init 0/1) with momentum slider and optional drift.
- BN vs LayerNorm vs RMSNorm heatmaps (6×8) with column/row stats after normalisation.
- Deep net (He × gain, ReLU) std per layer with/without BN; scale-invariance check; careful ICS vs smoother-landscape discussion (Santurkar et al. 2018). AI: LayerNorm/RMSNorm (defined), BN in CNNs, small-batch issues (SyncBN, GroupNorm).

**UI to verify** (sidebar "95 · Batch Normalization"):
- Lab 1: move shift/scale → x histogram moves, x̂ stays centred at 0; set scale 0.1 and ε = 1 → var of x̂ well below 1; tick "undo" → success message, y = x.
- Section 3: measured curve sits on dashed σ/√B; batch size 2 → x̂ histogram of the example only at ±1.
- Section 4: momentum 0.01 → running mean lags; 1.0 → equals batch mean (noisy).
- Section 5: switch radio → after-heatmap and stats tables change (columns vs rows normalised; RMSNorm rows RMS = 1, means ≠ 0).
- Section 6: gain 1.5 → red curve explodes, green flat at 1; gain 0.5 → red vanishes.

Limitations: deep-net no-BN vs √2·gain^L agrees only up to finite-width fluctuations at large depth.

### Verification
- ruff clean; `pytest tests\test_static.py` (203 passed), `tests\test_quizzes.py` (passed), smoke + fuzz `-k "93Weight or 94Dropout or 95Batch"` all passed.
- Numerics checked with throwaway scripts: backward passes vs finite differences (p93 MLP, p94 MLP), orthogonality WᵀW = g²I (err 2e-15), BN/LN/RMSNorm statistics, Var formula live check, √2·gain^L prediction.


---

## New pages 96–98 (deep learning)


Checks run: ruff (clean), `tests\test_static.py` (all pages pass; a temporary page-83 key-prefix failure was fixed before the final run),
`pytest tests\test_pages_smoke.py tests\test_pages_fuzz.py -k "96Convolution or 97Embeddings or 98Attention"` → 9 passed. Quiz JSON validated.

### pages\96Convolution.py
- 1D lab: signal presets (noisy step with 🎲 resample, sine, spike + ramp) × 6 kernel presets (box/Gaussian smoothing, difference, central difference, spike detector); padding + stride sliders; position slider steps the window (highlighted) and the output point, with the sum written out in LaTeX.
- Output-length formula ⌊(n+2p−k)/s⌋+1 vs the counted windows (✓), plus check vs `np.correlate` and `np.convolve(x, flip(k))`.
- 2D lab: 16×16 synthetic shapes image or sklearn digit "3" (8×8 upscaled); preset kernels (identity, box/Gaussian blur, sharpen, Sobel x/y, Laplacian edge) load into an editable 3×3 grid of number inputs; row/col sliders select the output pixel; feature-map strip of 5 kernels with ReLU toggle; check vs `scipy.signal.correlate2d` / `convolve2d(flip)`.
- Parameter sharing (conv vs dense counts) and receptive field (closed form vs brute-force index tracing, stride 1 vs 2 plot).
- Worked example: input patch, kernel, patch⊙kernel tables, 9-term sum, flipped-convolution value and whether it differs.

UI to verify:
- Sidebar "96 · Convolution" → tab "1D sliding window": move "Output position i" — orange window and diamond move; set Padding 3 / Stride 3 → metrics show 6 = 6 for the 5-tap box kernel, position slider max shrinks.
- Tab "2D image filters": choose preset "Sharpen" → the 9 number inputs change to 0,−1,0/−1,5,−1/0,−1,0; edit one → "Kernel edited" caption; move row/col sliders → orange box on input and cyan box on feature map move; Worked example table/latex update.
- Tab "Sharing & receptive field": kernel 3, stride 2, 12 layers → RF 8191 (formula = brute force ✓); stride 1 → 25.

Known limitations: 2D lab is fixed to 3×3 kernels, stride 1, 'same' padding.

### pages\97Embeddings.py
- Hand-crafted 21-word vocabulary with 4 interpretable dims (royalty, gender, plural, animal); global noise slider + 🎲 resample (seeded).
- Lookup lab: heatmap of E with highlighted row, one-hot × E vs E[i] equality check.
- Neighbours lab: 2D (choose axes) / 3D scatter, top-k cosine neighbours table.
- Vector arithmetic a − b + c with arrows, top-5 (toggle to exclude inputs), caveats (noise, exclusion, bias).
- PCA of an 8-d version (4 noise dims + random orthogonal rotation): projection, explained variance, SVD vs covariance-eigenvalue check.
- Positional encoding: heatmap, PE[ref]·PE[q] curve, verified that the Gram matrix = Σ cos(ωᵢ(p−q)) for all pairs.
- Worked example: analogy vectors, dot product and cosine for the top answer.

UI to verify:
- Sidebar "97 · Embeddings" → tab "Vector arithmetic": default king − man + woman → top answer queen (cos 1.000). Raise noise to 0.3 → answer may change (e.g. queens); click 🎲 Resample noise → changes again.
- Tab "Lookup table": pick a token → orange row moves, both columns equal, ✓ shown.
- Tab "Positional encoding": change d_model / Positions; reference slider clamps when Positions shrinks; peak value = d/2.

Known limitations: toy vectors are hand-made; cat/dog differ only slightly (4 dims cannot separate everything).

### pages\98Attention.py
- Shared controls: 4 sentences (5–6 tokens; "the" repeated), d_model 4–16, 🎲 resample weights (seeded embeddings, Wq/Wk/Wv/Wo), PE toggle, causal mask, √d_k toggle, temperature.
- Attention map heatmap + checks (row sums, A ≥ 0, masked cells exactly 0, A·V = explicit sums), residual Y = X + AV·W_O norms.
- √d_k lab: measured Var(q·k) vs d_k and after scaling (log–log), mean max softmax weight scaled vs unscaled, bar chart for one query at chosen d_k.
- Two heads (d_head = d_model/2): side-by-side heatmaps, difference metrics, concat·W_O shape.
- Cost & KV cache: n² score memory, attention FLOPs, KV cache size for a Llama-2-7B-like shape.
- Worked example: query selector → table raw → scaled/T (masked) → softmax, LaTeX for the top key, weighted sum of V rows with ✓.

UI to verify:
- Sidebar "98 · Attention": toggle "Causal mask" → upper triangle 0, "Masked (future) weights 15 cells, max = 0.0" for 6 tokens; token 0 row = [1,0,…].
- Temperature 0.1 → rows near one-hot; 3.0 → near uniform. Toggle PE off (causal off) → rows for "0:the" and "4:the" identical.
- Tab "Why √d_k": slide e to 9 → orange bars one-hot, cyan bars spread; measured variance ≈ 512 vs ≈ 1.
- Worked example: choose query token; change sentence to a 5-token one → selection clamps.

Known limitations: heads use random (seeded) weights, so patterns differ but are not semantically meaningful; cost tab uses a fixed model shape.

### quizzes\p96.json, p97.json, p98.json
- 4 questions each (output length, cross-correlation, parameter count, receptive field / lookup, cosine, analogy caveat, PE / √d_k variance, causal mask, n² cost, attention ≠ explanation).


---

## Quiz engine, progress tracking & navigation sections


### app.py
- `SECTIONS` now holds explicit page-number sets per section: Vectors & Matrices 1–18 + 76–78; Functions 19–22;
  Probability & Statistics 23–43 + 84–88 (43 "Residuals & Least Squares" previously fell in no range → now after 42);
  Calculus 44–49 + 79–83; Optimization 50–56 + 90–92; Information Theory 57–60 + 89; Eigenvectors & PCA 61–63;
  Neural Networks & ML 64–75 + 93–98. Unknown numbers → "More Lessons". Titles/url_paths unchanged (`/pNN-slug`).
- Keeps `PAGE_NUMBERS` (url_path → number) and `SECTION_NUMBERS`; after `pg.run()` renders the page's quiz under an `st.divider()` (not on Home).
- Home curriculum map: each section expander starts with an `st.progress` "Progress: x / y quizzes passed" (only pages with a valid quiz count). Sidebar (below nav): overall "🧠 Overall: x / y quizzes passed". Caption explains 75 % pass mark and per-session progress.

### common/quiz.py (new)
- `QUIZ_DIR` (repo-root `quizzes/`), overridable via env var `AI_MATH_QUIZ_DIR` (tests).
- `validate_quiz(data, n)` → list of problems; `read_quiz(n)` → (quiz, error); `load_quiz(n)` → dict | None. Missing file → nothing; malformed → caption "⚠️ Quiz unavailable — malformed quiz file (...)".
- `render_quiz(n)`: bordered box "🧠 Check your understanding", `st.form("quiz_pNN_form")`, radios `quiz_pNN_qI` (index=None, markdown options via format_func), "Check answers" → per-question ✅/❌ + explanation + correct answer, score, "🔄 Try again" reset. Best fraction in `st.session_state["quiz_scores"][n]`; pass ≥ 75 %.

### tests/test_quizzes.py (new)
- Schema test per quiz file (incl. page field = filename, page file exists); `xfail(strict=False)` test that every page has a quiz (make strict at integration); unit tests for `validate_quiz` rejections; AppTest: fixture quiz renders, grades (2/3 → warning, not passed; reset; 3/3 → passed), Home progress shows "1 / 1"; missing/malformed quiz doesn't crash.

### README.md
- Section table with new pages, explicit-sections note, "Quizzes" section (how it works, how to add `quizzes/pNN.json`, schema rules), test list + project structure updated.

### UI to verify
1. Sidebar: "Vectors & Matrices" lists 01–18 then 76–78; Calculus lists 44–49 then 79–83; Probability shows 24, 39, 43, 84–88; Optimization 55, 90–92; Information Theory 89; Neural Networks 66, 72, 93–98.
2. Open any lesson with a quiz (e.g. "01 · From Number to Arrow to List"), scroll to the bottom: divider, then bordered "🧠 Check your understanding" with no option preselected. Check LaTeX in questions/options renders as math.
3. Answer some wrong, click "Check answers": each question shows green ✅ or red ❌ (with correct answer and explanation), a score line; < 75 % → yellow warning. Click "🔄 Try again": selections and feedback cleared.
4. Answer all correctly → "🎉 Score: n / n … passed!". Sidebar bottom "🧠 Overall" progress bar increases.
5. Home: each section expander shows "Progress: x / y quizzes passed"; Vectors & Matrices reflects the quiz just passed. Reload browser → progress resets (per session).
6. Home itself has no quiz box.

### Known limitations
- Progress is per browser session (session_state), not persisted.
- LaTeX inside radio options relies on Streamlit's label markdown; not visually verified here (no browser automation available).
- Editing answers after checking shows stale feedback until "Check answers" is pressed again (form batches input).


---

## Quizzes for pages 1–22


Created 22 files in `quizzes\` (UTF-8 JSON, schema `{"page": N, "questions": [{q, options, answer, explain}]}`),
4 questions each, 4 options each, one correct answer. Every question was written after reading the page source
and uses the page's own notation, presets and default slider values; all numeric answers were computed with Python.
Answer positions are deterministically shuffled (distribution over indices 0/1/2/3 = 26/20/22/20).
No page or other repo file was touched.

| File | Topic |
|---|---|
| `quizzes\p01.json` | Scalar vs 1D vector, zero vector, flattening 28×28 → 784 and 32×32×3 → 3072 |
| `quizzes\p02.json` | Component-wise A+B / A−B with defaults (3,4),(4,−2); tip-to-tail; A−B = tip of B → tip of A |
| `quizzes\p03.json` | Scalar k: flip/shrink/stretch cases, kv = (kx, ky), length scales by \|k\| |
| `quizzes\p04.json` | Magnitude via Pythagoras: (3,4)→5, (−6,8)→10, (3,4,12)→13, any dimension |
| `quizzes\p05.json` | Normalization (3,4)→(0.6,0.8), stretching short vectors, zero vector, 3D default (2,3,6)/7 |
| `quizzes\p06.json` | Geometric dot product: defaults → 24.57 vs shadow 4.91, presets, sign from angle, neuron score 1.39 |
| `quizzes\p07.json` | Algebraic dot product: (2,1)·(1,2)=4, (3,−2)·(4,5)=2, cos θ = 0.8, perpendicular vectors |
| `quizzes\p08.json` | Cosine similarity vs dot product (length-free), 60° example, 180° → −1, zero-vector undefined |
| `quizzes\p09.json` | Data as vectors: 5-D movie ratings, PCA to 3-D, separate PCA per dataset, clusters = similarity |
| `quizzes\p10.json` | m×n shape, A[i,j] on the inventory matrix, Full-HD RGB count 6,220,800, row vector 1×n |
| `quizzes\p11.json` | Cell-wise addition, same-shape rule, (kA)[i,j] = k·A[i,j], k = −1 flips signs |
| `quizzes\p12.json` | Matrix×vector shapes, row-dot-x computation, Σ rule, mismatched x length |
| `quizzes\p13.json` | (m,n)(n,p)→(m,p), shape gate, C[1,2] row·column, n terms per cell |
| `quizzes\p14.json` | Columns = images of î, ĵ; preset Stretch X/Squash Y on (2,1); H R S order; singular collapse |
| `quizzes\p15.json` | Transpose shape swap, (Aᵀ)ᵢⱼ = Aⱼᵢ, (Aᵀ)ᵀ = A, row i → column i |
| `quizzes\p16.json` | Identity structure, (Iv)ₖ = vₖ, AI = IA = A, geometric "do nothing" |
| `quizzes\p17.json` | det = ad − bc, Mirror-world preset (−0.52), det(kM) = k² det M, Near-singular preset |
| `quizzes\p18.json` | 2×2 inverse formula, det = 0 ⇒ no inverse, Gentle-zoom inverse, fragile (tiny det) undo |
| `quizzes\p19.json` | g∘f order, preset "Double, then add one" at x = 1.25, DIY affine composition 1.6x + 2.5, definition of a function |
| `quizzes\p20.json` | w = sensitivity, Number-Lab defaults (w=1.5, b=−1, x=2 → 2), bias shift, linear vs affine |
| `quizzes\p21.json` | XOR impossibility proof, best line = 1 error, θ=0°/b=−0.5 → 2 errors, half-planes |
| `quizzes\p22.json` | ReLU/Leaky ReLU at −2.5, Stitch-Lab continuity b₂ = (m₁−m₂)a + b₁ = −1, signed jump, XOR auto-solve at (1,1) |

### Verification done
- Throwaway validator (not in repo): all 22 files parse, top-level keys `page`/`questions`,
  `page` int matches filename, 3–4 questions, 3–4 unique options, `answer` in range, non-empty fields,
  balanced `$` delimiters, no stray backslashes → ALL OK.
- Spec JSON check (`json.load` on all 22 files) OK.
- `python -m pytest tests\test_quizzes.py -q -k "p01 or … or p22"` → 22 passed (uses `common.quiz.validate_quiz`).

### UI to verify
- Open **page 1 (From Number to Arrow to List)** → scroll to the bottom → Quiz shows 4 questions; pick "784" for Q2 → after submitting, it is marked correct.
- Open **page 6 (Dot Product — Geometric View)** → scroll to the bottom → Quiz shows 4 questions; Q1's option "≈ 24.57" matches the "Dot product" metric shown with the default sliders.
- Open **page 11 / 12 / 13 / 16 / 17 / 18** → check that the 2×2 matrices in the questions/options render as LaTeX bmatrix/pmatrix (two rows), not raw `\\begin{...}` text.
- Open **page 17 (Determinant — Area Scaling)** → choose preset "Mirror world (flip)" → det metric reads −0.52, matching quiz Q2.
- Open **page 20 (Linear Functions)** → Number Lab table row x = 2.0 shows y = 2.0, matching quiz Q2.
- Open **page 22 (Piecewise Functions)** → Stitch Lab defaults show jump at a = 0.00 (b₂ = −1.00), matching quiz Q2.

### Known limitations
- Questions reference page defaults/presets; if a page author later changes those defaults, the affected
  questions (p06 Q1, p14 Q2, p17 Q2/Q4, p18 Q3, p19 Q2/Q3, p20 Q2, p22 Q2/Q4) need updating.
- LaTeX in radio options relies on Streamlit's markdown math support in `st.radio` labels.


---

## Quizzes for pages 23–49


New files (4 questions each, 4 options, answers balanced across positions 0–3; numbers verified with numpy/scipy):

- `quizzes\p23.json` — sample space counting, two-dice sum trap (1/6 vs 1/11), union via inclusion–exclusion, complement.
- `quizzes\p25.json` — P(A|B) from the page's Club A counts (12/20), P(A|B) vs P(B|A) denominators, Club B independence, formula.
- `quizzes\p26.json` — independence definition, spinner Dependent Mode P(T-Shirt)=0.58, product test 0.348≠0.54, AI dependence example.
- `quizzes\p27.json` — Bayes with page defaults (2%/90%/9% → ≈17%), natural frequencies 180 vs 882, total probability, base-rate fallacy.
- `quizzes\p28.json` — discrete vs continuous, P(exact value)=0, binomial P(5 of 10 heads)≈0.246, histogram→density bridge.
- `quizzes\p29.json` — balance-beam EV (weights 20/50/10 → 4.5), casino default EV −$5, EV meaning, MSE regression predicts mean.
- `quizzes\p30.json` — population variance/SD example, squared units, n−1 correction, 68.3% rule.
- `quizzes\p31.json` — Bernoulli mean/variance, variance peak at p=0.5, PMF p^x(1−p)^(1−x), dropout as Bernoulli(r).
- `quizzes\p32.json` — binomial PMF computations, meaning of C(n,k), bell shape as n grows (CLT hint).
- `quizzes\p33.json` — U(a,b) height 1/(b−a), interval probability, discrete die mean/variance, log-uniform LR search.
- `quizzes\p34.json` — normalizer role, density > 1 when σ small, 68/95/99.7 rule, diffusion noise.
- `quizzes\p35.json` — Z=(85−70)/10=1.5, percentile ≈93% (only if Normal), standardizing keeps skew, feature scaling for GD.
- `quizzes\p36.json` — 2-dice triangle, SD of mean σ/√n, CLT statement caveats, CLT in SGD.
- `quizzes\p37.json` — softmax of default logits (Cat≈0.79), why exponentiate, max-subtraction invariance, temperature.
- `quizzes\p38.json` — mean/median/mode of the lab's initial data, outlier drag 19→30, even-count median, robust measure.
- `quizzes\p40.json` — sample vs population covariance, quadrant signs, unit change ×100, zero covariance ≠ independence.
- `quizzes\p41.json` — r = Cov/(σxσy), °C vs °F r=1 (not slope), U-shape r≈0, constant variable → undefined.
- `quizzes\p42.json` — least squares objective, fit through 3 points (y=1.5x+1/3), squared penalty 1 vs 25, slope=weight/intercept=bias.
- `quizzes\p44.json` — secant slope on f=0.2x²−2 (0.6), why not h=0, tangent slope 0.4, zero derivative ≠ extremum.
- `quizzes\p45.json` — power rule, lab cubic slope at x=2 (1.2), quadratic derivative drops the constant, MSE slope 2(pred−y).
- `quizzes\p46.json` — multiply rates (3×2), d/dx sin(x²), lab Power preset at x=3 (=3), backprop as chain rule.
- `quizzes\p47.json` — ∂f/∂x and ∂f/∂y of x²+3xy+y², lab Saddle partials at (2,1), meaning of the slice.
- `quizzes\p48.json` — ∇(x²+y²) at (3,4) and |∇f|=10, ascent vs descent, saddle zero-gradient, gradient as vector.
- `quizzes\p49.json` — ∫₋₂² x² = 16/3, left Riemann sum n=2, signed area of sin over [0,2π], probability as area.

Not written here: p24, p39 and p43 (written together with those new pages).

### UI to verify
- Open each page in the sidebar (e.g. "Bayes' Theorem", "Softmax", "Chain Rule — Derivative Through Layers"); scroll below the page content to the quiz renderer: 4 questions should appear, LaTeX renders (fractions, ∂, ∇, \binom), no raw `\\` or `$` visible.
- Page 29 quiz Q2 uses escaped dollars (`\$10`) for money — check they show as "$10" and not as broken math.
- Pick the correct option in each question → success + explanation; pick a wrong one → explanation shows.

### Validation
- All 24 files parse; keys/answer range/unique options/3–4 questions checked by a throwaway validator (also no control chars, balanced `$`).
- `python -m pytest tests\test_quizzes.py -q` → 78 passed, 1 xfailed.

### Known limitations
- Numbers in questions use the pages' default widget values; if a page's defaults change later the quiz text (not the math) may drift.


---

## Quizzes for pages 50–75


23 new files in `quizzes\`, 4 questions each (92 total), 4 options, correct answers spread evenly over positions 0–3.
Every numeric answer was checked with Python. Notation follows each page (bits on 57–60, nats on 69, ½·MSE on 70, and so on).

| File | Topic of the questions |
|---|---|
| quizzes\p50.json | MSE vs MAE computation, outlier sensitivity, MAE kink, loss as a single score |
| quizzes\p51.json | global minimum meaning, vertical offset invariance, steep walls, gradient as local info |
| quizzes\p52.json | GD update with η=0.15, −∇f direction, gradient ⟂ contours, lumpy-terrain local dips |
| quizzes\p53.json | x←(1−2η)x step, BOUNCY regime η=0.75, η<2/λ limit for 4x², NaN ⇒ LR too high |
| quizzes\p54.json | local-minimum definition, greedy stop at zero gradient, convex OLS, "The Secret" init |
| quizzes\p56.json | mini-batch update, unbiased-but-noisy gradient, equal-compute 64/B, batch-size escape behaviour |
| quizzes\p57.json | I(1/8)=3 bits, coin+die additivity, nats→bits, confident-wrong surprise |
| quizzes\p58.json | entropy of [.5,.25,.25], binary entropy p=0.75, max entropy log₂4, information gain |
| quizzes\p59.json | one-hot CE in bits, Gibbs/KL gap, softmax gradient Q−P, label-smoothing optimum |
| quizzes\p60.json | Gaussian closed-form KL (bits), asymmetry, reverse-KL mode seeking, discrete KL |
| quizzes\p61.json | Av=λv check, eigenvalues via trace/det, rotation has no real eigenvectors, why det(A−λI)=0 |
| quizzes\p62.json | λ=−1.8 flip+grow, shrink without flip, ellipse semi-axes, 0.9¹⁰ vanishing |
| quizzes\p63.json | % explained λ₁/(λ₁+λ₂), lost variance λ₂, variance along u with n−1, round-cloud noise |
| quizzes\p64.json | Robo-Dog z=−5.3, why bias can't separate Bunny/Lion, output meaning, layer = 10×784 matrix |
| quizzes\p65.json | 0.25³ sigmoid chain, tanh′(1), ReLU/Leaky at z=−3, dead-ReLU definition |
| quizzes\p67.json | parameter count 17, ReLU forward pass, collapse to W²W¹ without activation, Goldilocks pocket |
| quizzes\p68.json | MSE/MAE of errors, sub-unit errors, rogue-outlier slopes, smooth bowl |
| quizzes\p69.json | −ln 0.5, softmax logits [2,1,0] loss, MSE vs CE gradient at p=0.01, true-class-only penalty |
| quizzes\p70.json | ∂L/∂w₁ in the toy chain, update direction, chain rule, the extra σ′ factor |
| quizzes\p71.json | overfitting gap, training error non-increasing, σ² noise floor, why a separate test set |
| quizzes\p73.json | dartboard diagnosis, Bias²+2·var=7, irreducible noise, complexity tradeoff |
| quizzes\p74.json | 1D L1/L2 optima at λ=2, exact zero vs shrink, diamond corners ⇒ sparsity, feature selection |
| quizzes\p75.json | overfitting curves, underfitting signature, early stopping with patience 3, hindsight minimum |

### UI to verify
- Open any of these pages from the sidebar (e.g. "Learning Rate", "KL Divergence — Gap Between Distributions", "Learning Curves"). Scroll below the lesson. The quiz should show 4 questions, and LaTeX should render in the questions, the radio options and the feedback.
- Answer a question wrongly and check that the ❌ feedback shows the correct option and its explanation. Answer correctly and check that ✅ shows the explanation.
- On p53, p59, p60, p63 and p64, check that inline LaTeX such as `$\begin{bmatrix}…\end{bmatrix}$` (p61/p62/p67) and `$\frac{…}{…}$` renders inside radio labels.

### Known limitations
- No quizzes for 55, 66 and 72. Other todos own those.
- Pages 50–64 had their HTML labs moved to `assets\labs\` by the parallel assets refactor while these quizzes were being written. I re-checked the lesson text these quizzes rely on, and it is unchanged.


---

## Lab HTML moved to assets (pages 19–42)


Shared helper: `common\assets.py` (`load_lab(name, **values)`) — **created by assets-a** (did not exist at start).
All pages below gained the spec path shim + `from common.assets import load_lab  # noqa: E402`; each
`html_code = """..."""` literal became `html_code = load_lab("<asset>")`. Asset bytes = the exact former string
value (leading newline/indentation kept so output is byte-identical); Python-escape pitfalls are gone
(e.g. p22 `doesn\\'t` is now plain `doesn\'t` in the .html).

| Page | Asset(s) created | Placeholders |
|---|---|---|
| 19 Functions as Machines | `p19_conveyor_belt.html` | `$x_val $mid_val $out_val` (passed pre-formatted `:.2f`), `$f_name $g_name` (html-escaped as before); f-string `{{ }}` → `{ }` |
| 20 Linear Functions | `p20_linear_function_lab.html`, `p20_neuron_cartoon.html` | none (static) |
| 22 Piecewise Functions | `p22_stitch_lab.html`, `p22_relu_visualizer.html`, `p22_xor_piecewise_lab.html` | none |
| 23 Sample Space & Basic Probability | `p23_sample_space.html`, `p23_venn.html`, `p23_2d_space.html` | none |
| 25 Conditional Probability | `p25_conditional_probability.html` | none; page still does `.replace("__CONFIG_JSON__", json.dumps(config))` |
| 26 Independence | `p26_two_spinners.html` | none |
| 38 Mean, Median, Mode | `p38_mean_median_mode.html` | none |
| 40 Covariance | `p40_covariance.html` | none |
| 41 Pearson Correlation | `p41_correlation_lab.html`, `p41_nonlinear_gotcha.html` | none |
| 42 Scatter Plot & Line of Best Fit | `p42_regression_lab.html` | none |

### Equality evidence
Capture script (session `files\assets_a_capture.py`) runs each page with AppTest, monkeypatching `streamlit.iframe`
to record `(src, kwargs)` of every call; before/after JSON compared with `==` on src and kwargs — **all 23 calls identical**:
default state for all 10 pages, plus 2 extra states for p19 (preset radio + all 6 sliders changed; 3 distinct outputs)
and p25 (both scenarios; outputs differ between scenarios). SHA-256 prefixes (after == before):
p19 default 5c2a5b93a54c19d2/9d03d4acb770bac4, state1 f9c4a0be6b16e44d/61bfbc8e293e7d68, state2 1345cd05d43155a7/33e7c07a5966b3aa;
p20 691515448167fb82, d02f77028fdc2fc5; p22 9268865c24a78334, 8b0862f5d9bfea47, 271367f9b5a8b79c;
p23 6df06984a35183e3, b7d403e12b78d076, 5b9da6cc103ed15c; p25 48eacf959cf10c6d (club A), 4644f882984fc5ee (club B);
p26 16a26aa460538289; p38 9b7420617f760850; p40 efa50731d7d7a476; p41 df5926a719e5a768, b86492685c9c2f7b; p42 579fd00dc620d005.
Heights unchanged. ruff (common, pages) clean; test_static 149 passed; smoke+fuzz for the 10 pages: 30 passed.

### UI to verify
Labs look and behave exactly as before: open each page above in the sidebar and interact with its lab(s)
(p19: change preset / x slider → orb shows x, f(x), g(f(x)); p25: switch scenario radio → Venn counts change;
p20/22/23/26/38/40/41/42: sliders/buttons inside the iframes animate as before).

### Known limitations
Asset files keep the original leading newline + 4-space indentation to guarantee byte-identical output.


---

## Lab HTML moved to assets (pages 44–54)


`common\assets.py` already existed when this todo started (created by a sibling agent with the exact spec content) — used unchanged.

### Approach (all 11 pages)
- Every page's lab HTML was a **static** (non-f-string) triple-quoted constant passed straight to `st.iframe(html, height=...)`.
- An AST-driven script wrote the *evaluated* Python string value to `assets\labs\pNN_<name>.html` (UTF-8, no BOM, LF; leading newline/indentation kept so bytes are identical) and replaced the assignment + call with `st.iframe(load_lab("pNN_<name>"), height=<same>)`.
- Added the spec's sys.path shim + `from common.assets import load_lab  # noqa: E402` (before `st.set_page_config`, which stays the first Streamlit call). Page files keep their CRLF line endings. No other lines changed.
- **No placeholders** anywhere (static HTML ⇒ no `$`-escaping needed; `${...}` JS template literals untouched).

### Per page (asset · height · equality evidence)
Evidence: subprocess with `st.iframe = lambda src, **k: captured.append((src, k))` + `runpy.run_path(page)` at default widget state, before and after; src compared byte-for-byte and kwargs compared (scripts + JSON captures in `files\assets_b\`). Since no page is an f-string, the iframe src does not depend on widget state.

| Page | Asset | kwargs | src UTF-8 bytes | sha256[:16] before = after | Lines before → after |
|---|---|---|---|---|---|
| 44What is a Derivative | p44_derivative.html | height=860 | 14912 | 80aa0b9e627eacdd | 386 → 99 |
| 45Derivative Rules (Power & Constant) | p45_derivative_rules.html | height=800 | 17005 | 0eb69eef316ebbeb | 461 → 106 |
| 46Chain Rule — Derivative Through Layers | p46_chain_rule.html | height=800 | 17107 | a255a72ddd17f676 | 432 → 97 |
| 47Partial Derivatives | p47_partial_derivatives.html | height=800 | 15586 | 22cc2e503b6d7cb9 | 475 → 89 |
| 48The Gradient — Steepest Climb | p48_gradient.html | height=800 | 17903 | fbc05489b3784adc | 476 → 89 |
| 49Integral as Area | p49_integral_area.html | height=800 | 12890 | 43b787f9313ba17d | 394 → 77 |
| 50What is a Loss Function | p50_loss_function.html | height=660 | 14146 | 72d32e8d1968449d | 458 → 79 |
| 51Loss Landscape — Hills and Valleys | p51_loss_landscape.html | height=700 | 16704 | 24beb855251d0d68 | 537 → 109 |
| 52Gradient Descent | p52_gradient_descent.html | height=640 | 17304 | bbc33b1de88a228a | 534 → 113 |
| 53Learning Rate | p53_learning_rate.html | height=700 | 14108 | 2c241330bf89cbee | 503 → 112 |
| 54Local vs Global Minimum | p54_local_global_minimum.html | height=850 | 16783 | b740dc469733916a | 505 → 74 |

compare.py result: `ALL EQUAL` (11/11, 1 iframe call each, identical kwargs).

### Verification
- `ruff check common pages --no-cache` → All checks passed
- `pytest tests\test_static.py -q` → 159 passed
- `pytest tests\test_pages_smoke.py tests\test_pages_fuzz.py -q -k "<44–54 stems>"` → 33 passed

### UI to verify
- Open each of pages 44–54 in the sidebar: the embedded lab appears at the same height and looks/behaves exactly as before (e.g. 44: drag the h slider → secant turns into tangent with the "Limit h → 0" label; 52: run gradient descent animation; 53: switch learning-rate presets; 54: start balls from different points).
- Run a page standalone (`streamlit run "pages\44What is a Derivative.py"`) → lab still loads (path shim).

### Known limitations
- Asset files keep the original leading newline + 4-space indentation inside the HTML to guarantee byte-identical output; cosmetic re-indentation was deliberately not done.


---

## Lab HTML moved to assets (pages 56–64)


`common/assets.py` already existed when this step started (created by the parallel assets refactor). It was used unchanged.
For each page, the `html_code = """..."""` literal was replaced with `html_code = load_lab("<name>")`. The `st.iframe(...)` call and its kwargs did not change.
Pages that had no path shim (56, 57, 61, 62, 63) got the spec's `sys.path` shim plus `from common.assets import load_lab  # noqa: E402`.
The other pages got only the import line. Line endings in pages stayed CRLF. Assets are UTF-8 with LF line endings.
None of the strings were f-strings, so **no placeholders** are used: `load_lab` is called without values and any `$`/`${...}` in the JS stays literal.
Each asset file contains the runtime string value: the source literal was evaluated with `ast.literal_eval` and checked equal to the captured value before writing.

| Page | Asset | Placeholders | iframe kwargs | Page lines before → after |
|---|---|---|---|---|
| 56 Stochastic Gradient Descent | assets/labs/p56_sgd.html | none | height=760 | 581 → 78 |
| 57 Information & Surprise | assets/labs/p57_surprise.html | none | height=670 | 944 → 101 |
| 58 Entropy — Average Uncertainty | assets/labs/p58_entropy.html | none | height=670 | 1454 → 105 |
| 59 Cross-Entropy — Predicted vs Reality | assets/labs/p59_cross_entropy.html | none | height=790 | 1245 → 103 |
| 60 KL Divergence — Gap Between Distributions | assets/labs/p60_kl_divergence.html | none | height=830 | 1428 → 123 |
| 61 Eigenvectors — Vectors That Don't Rotate | assets/labs/p61_eigenvectors.html | none | height=900 | 1691 → 156 |
| 62 Eigenvalues — How Much Do They Stretch | assets/labs/p62_eigenvalues.html | none | height=920 | 741 → 138 |
| 63 PCA Intuition — Finding the Best Angle | assets/labs/p63_pca.html | none | height="content" | 803 → 147 |
| 64 A Single Neuron | assets/labs/p64_neuron.html | none | height="content" | 1163 → 369 |

### Equality evidence
Scripts are in `files/assets_c/`. `capture.py` patches `st.iframe` to record `(src, kwargs)` and runs the page with `runpy` in bare mode. For page 64 it also uses AppTest for 3 states:
- default
- state2: bias −7.3, activation Tanh
- state3: 🐰 Fluffy Bunny preset clicked, x₂=0.15, w₂=−9.5

`compare.py` checks that the before and after captures match byte for byte (UTF-8) and that the kwargs are identical:
```
56     default          IDENTICAL len=19007 sha256=208427822ec76a89 kwargs={'height': 760}
57     default          IDENTICAL len=24538 sha256=5695d7cfde6e9794 kwargs={'height': 670}
58     default          IDENTICAL len=43295 sha256=668e391d59887629 kwargs={'height': 670}
59     default          IDENTICAL len=34390 sha256=5875ab059dc72056 kwargs={'height': 790}
60     default          IDENTICAL len=39655 sha256=bcc1d1a55745632e kwargs={'height': 830}
61     default          IDENTICAL len=48911 sha256=3fd19c8f2219cec9 kwargs={'height': 900}
62     default          IDENTICAL len=28231 sha256=075e2f80b94023c6 kwargs={'height': 920}
63     default          IDENTICAL len=26184 sha256=7bbdca854f90ff87 kwargs={'height': 'content'}
64     default          IDENTICAL len=31287 sha256=e873256233bbacbb kwargs={'height': 'content'}
64_at  apptest_default  IDENTICAL len=31287 sha256=e873256233bbacbb kwargs={'height': 'content'}
64_at  state2           IDENTICAL len=31287 sha256=e873256233bbacbb kwargs={'height': 'content'}
64_at  state3           IDENTICAL len=31287 sha256=e873256233bbacbb kwargs={'height': 'content'}
```
Checks run:
- ruff on `common pages`: passed
- `tests\test_static.py`: 165 passed
- smoke + fuzz tests filtered to pages 56–64: 27 passed

### UI to verify
In the sidebar, open each page from 56 to 64. Each embedded lab should look and behave exactly as before, at the same iframe height:
- 56: SGD batch dots animate
- 57: surprise lab
- 58: coin/weather modes
- 59: preset/manual modes and the shake effect
- 60: forward/reverse KL toggle
- 61: eigenvector sandbox
- 62: 1D/2D toggle and badges
- 63: PCA mode buttons and the peak tag
- 64: neuron lab; the cat case study widgets below it still work

### Known limitations
None. The page titles in `set_page_config` were left as they were, without the "NN ·" prefix, because this task allows no behavior changes.


---

## Cross-links, tests & integration


### 1. Cross-links in existing pages

All links use `common.nav.safe_page_link("pages/<exact file>.py", label, icon)`; pages that lacked the
import got `from common.nav import safe_page_link` (71, 73, 75 also got the standard repo-root path shim).
Lab HTML in `assets/labs/` was checked: no curriculum "next/previous" text there (only "Page 51/52/53"
cross-references inside the gradient-descent labs, which are still correct) — no HTML edits.
Every edited page was opened via `app.py` under AppTest: all new links render as real `st.page_link`s
(no fallback captions), no exceptions.

| Page | Change | UI to verify |
| --- | --- | --- |
| 18 Matrix Inverse | Recap gains "Next up: Span, Basis & Rank"; link **Next: 76 · Span, Basis & Rank** | Bottom of page 18 → click link → page 76 opens |
| 23 Sample Space | "Next up (Page 25): Conditional Probability" → "Next up (Page 24): Complement, Union & Intersection"; link **Next: 24 · …** | Bottom of 23 → Recap box text says Page 24; link opens 24 |
| 25 Conditional Probability | Added row **Previous: 24 · Complement, Union & Intersection** / **Next: 26 · Independence** | Bottom of 25 → both links work |
| 38 Mean, Median, Mode | "Next up" sentence + link **Next: 39 · Quantiles, IQR & Outliers** | Below the lab iframe → link opens 39 |
| 40 Covariance | Row **Previous: 39 · Quantiles, IQR & Outliers** / **Next: 41 · Pearson Correlation** | Below the caption → links work |
| 42 Scatter Plot | Footer "Page 42 & 43 … Up next: Calculus" → "Page 42 … Up next: Page 43 opens the hood …"; link **Next: 43 · Residuals & Least Squares** | Footer text no longer says "42 & 43"; link opens 43 |
| 44 What is a Derivative | Row **Previous: 43 · Residuals & Least Squares** / **Next: 45 · Derivative Rules (Power & Constant)** | Bottom of 44 → links work |
| 49 Integral as Area | Footer "Next: Section 8 — Optimization" → "Calculus continues with Limits & Continuity (Page 79) …"; link **Next: 79 · Limits & Continuity** | Footer + link opens 79 (79 links back to 49) |
| 52 Gradient Descent | Factual fix: "optimizers like Adam (Page 53)" → "(Page 91)" (53 is Learning Rate) | "Real-world" paragraph mentions Page 91 |
| 54 Local vs Global Minimum | Footer "Next: Stochastic Gradient Descent" → "Next: Convex Functions (Page 55) …"; link **Next: 55 · Convex Functions** | Footer + link opens 55 |
| 56 SGD | Footer "Next: … world of Information!" → "optimization story continues with Momentum (Page 90)"; row **Previous: 55 · Convex Functions** / **Next: 90 · Momentum** | Footer; links open 55 / 90 (90 links back to 56; 92 → 57 continues to Information Theory) |
| 60 KL Divergence | Footer now points to Mutual Information (Page 89); link "Continue to Page 61 …" replaced by **Next: 89 · Mutual Information** | Footer + link opens 89 (89 → 61) |
| 61 Eigenvectors | Added **Previous: 89 · Mutual Information**, **Related: 78 · SVD — Rotate, Stretch, Rotate**, **Next: 62 · Eigenvalues — How Much Do They Stretch** | Bottom of 61 → three links |
| 63 PCA | Added **Related: 78 · SVD — how PCA is computed in practice** and **Next: 64 · A Single Neuron** | Bottom of 63 → two links |
| 64 A Single Neuron | "Page 67 shows why stacking layers without nonlinear activations collapses" → "Page 66 shows why stacking linear layers … collapses …, and Page 67 builds whole networks from matrix layers"; link **Next: 65 · Activation Functions Compared** | "➡️ Next: Activations" column text; link at bottom |
| 65 Activation Functions | Link **Next: 66 · Stacking Linear Layers Collapses** under the footer | Very bottom of 65 → link opens 66 |
| 67 NN as Matrix Layers | Recap card: "(Page 66 explores this collapse interactively)"; link **Previous: 66 · Stacking Linear Layers Collapses** | "Lesson Recap: Non-Linearity" card; link under it |
| 71 Overfitting | "Next up" sentence + link **Next: 72 · Train, Validation & Test Splits** | Below "Final Check on a Separate Test Set" |
| 73 Bias-Variance | Row **Previous: 72 · Train, Validation & Test Splits** / **Next: 74 · L1 & L2 Regularization** | Bottom of 73 |
| 75 Learning Curves | "Next up" sentence + link **Next: 93 · Weight Initialization** | Bottom of 75 → link opens 93 (93 links back to 75) |

Resulting learning path through the additions: 18→76→77→78→61; 23→24→25; 38→39→40; 42→43→44;
49→79→…→83→84→…→88→89→61; 54→55→56→90→91→92→57; 60→89; 65→66→67; 71→72→73; 75→93→…→98.
(Note: 78 → 61 and 92 → 57 / 83 → 84 are the new pages' own choices and were kept.)

### 2. Tests

- `tests/test_quizzes.py::test_every_page_has_a_quiz` — `xfail` removed; now strict (98/98 pages have a quiz).
- `tests/test_static.py::test_load_lab_targets_exist[<page>]` (new, AST-based): every `load_lab(...)` call
  has a string-literal name and `assets/labs/<name>.html` exists.
- `tests/test_static.py::test_page_link_targets_exist[<page>]` (new, AST-based): every
  `page_link`/`safe_page_link` first argument is a literal `pages/<file>.py` that exists — needed because
  `safe_page_link` silently degrades to a caption on a typo, so smoke tests would never catch it.
  (Placed in `test_static.py` with the other static source checks rather than in `test_quizzes.py`.)

### 3. README.md

- Added a short "Lessons added after 1–75" list grouped by section (page numbers + titles), and a note on the
  Previous/Next path (18→76, 49→79, 56→90, 60→89, 75→93).
- Test section: static tests now mention lab/page-link target checks; quiz test mentions every page has a quiz.
- Project structure: `assets/labs/` entry; conventions: `load_lab` usage (`$placeholder`/`$$`) and `safe_page_link`.

### 4. Verification

- `python -m ruff check . --no-cache` → All checks passed!
- `python -m pytest -q -n auto` (full suite incl. slow fuzz) → **824 passed in 362.61s (0:06:02)**;
  after the 93–95 seed fix, `-k "93Weight or 94Dropout or 95Batch"` (static+smoke+fuzz) → 21 passed;
  final full re-run result: **824 passed in 355.26s (0:05:55)** (ruff: All checks passed!).
- `streamlit run app.py --server.headless true --server.port 8622`: `/` 200, `/p24-complement-union-intersection` 200,
  `/p55-convex-functions` 200, `/p98-attention` 200, `/_stcore/health` 200; server stopped.
  (Streamlit serves the SPA for any path, so the AppTest navigation check above is the real routing proof.)

Default-state AppTest run time (sequential, single process, includes per-page cold start), slowest 10 overall:

| s | page |
| --- | --- |
| 3.37 | 9 Data as Vectors |
| 2.97 | 10 What is a Matrix |
| 2.44 | 18 Matrix Inverse |
| 2.08 | 3 Scalar Multiplication |
| 1.88 | 7 Dot Product — Algebraic View |
| 1.49 | 1 From Number to Arrow to List |
| 1.31 | 17 Determinant |
| 1.28 | 21 Why Non-linearity |
| 1.25 | 4 Magnitude |
| 1.00 | 24 Complement, Union & Intersection |

Slowest new pages: 24 (1.00 s), 72 (0.99), 90 (0.93), 94 (0.92), 55 (0.79), 92 (0.70), 91 (0.69), 85 (0.69),
96 (0.64), 87 (0.61); all other new pages ≤ 0.56 s. No page exceeds 3 s except 9 (3.4 s, original page,
matplotlib-heavy). Slowest fuzz tests: 17 (93 s), 10 (90 s), 18 (88 s), 55 (73 s), 97 (70 s), 77 (65 s).

### 5. Spot-check of new pages (24, 39, 43, 55, 66, 72, 76–98)

Checked for: wrong cross-link filenames (now enforced by the new static test — all pass), TODO/FIXME/placeholder
text (none), debug `print` (only inside a displayed `st.code` snippet in 83 — intended), legacy `np.random.*`
(none), unseeded randomness, KaTeX inside HTML (no new page uses `unsafe_allow_html`/iframes/labs), slow default runs (none).

Fixed (trivial):
- 93 Weight Initialization, 94 Dropout (2 buttons), 95 Batch Normalization: "🎲 Resample" drew the new seed from an
  unseeded `np.random.default_rng()`; now derived from the current seed
  (`default_rng(st.session_state[key]).integers(...)`) like pages 76–78 — reproducible resample sequences.
- 52: wrong page reference for Adam (53 → 91).

Remaining / not changed (judgement calls, not bugs):
- Sidebar order vs. link path differs in places (e.g. sidebar lists 43 then 84 in Probability, while 43's Next is 44;
  78 → 61 skips the Functions section). Links follow the learning path; the sidebar groups by topic.
- Original pages 38, 40 have no `main()` and minimal structure; only links were added.
- Page 70 has no Previous/Next links and a non-standard `page_title` (pre-existing, untouched).

