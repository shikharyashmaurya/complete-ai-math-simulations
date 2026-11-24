import sys
import warnings
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="72 · Train, Validation & Test Splits", page_icon="✂️", layout="wide")

COLORS = {"train": "#38bdf8", "val": "#f59e0b", "test": "#f472b6", "unused": "#64748b"}
DEFAULT_FRACS = (0.6, 0.2, 0.2)
MIN_COUNTS = (3, 2, 2)


# ---------------------------------------------------------------- data + model helpers
def true_f(x):
    return np.sin(3 * x) + 0.5 * x


def make_data(n, noise, rng):
    x = rng.uniform(-1, 1, n)
    return x, true_f(x) + rng.normal(0, noise, n)


def split_counts(n, fracs):
    """Cut points round(cumsum(fracs)·n), so the three counts never exceed n."""
    cuts = np.minimum(np.round(np.cumsum(fracs) * n).astype(int), n)
    return int(cuts[0]), int(cuts[1] - cuts[0]), int(cuts[2] - cuts[1])


def poly_fit(x, y, d):
    with warnings.catch_warnings():  # RankWarning for near-degenerate x is harmless here
        warnings.simplefilter("ignore")
        return np.polynomial.Polynomial.fit(x, y, d)


def mse(p, x, y):
    return float(np.mean((p(x) - y) ** 2))


def degree_sweep(xtr, ytr, xva, yva, max_deg):
    fits = [poly_fit(xtr, ytr, d) for d in range(max_deg + 1)]
    return fits, np.array([mse(p, xtr, ytr) for p in fits]), np.array([mse(p, xva, yva) for p in fits])


@st.cache_data(show_spinner=False)
def optimism_mc(n_tr, n_va, noise, max_deg, seed, reps=200):
    """Repeat 'select the degree on validation' on fresh datasets; compare the winner's val MSE to its true error."""
    rng = np.random.default_rng(seed + 123)
    xf, yf = make_data(2000, noise, rng)
    val_sel, fresh, degs = [], [], []
    for _ in range(reps):
        xtr, ytr = make_data(n_tr, noise, rng)
        xva, yva = make_data(n_va, noise, rng)
        fits, _, va = degree_sweep(xtr, ytr, xva, yva, max_deg)
        best = int(np.argmin(va))
        val_sel.append(va[best])
        fresh.append(mse(fits[best], xf, yf))
        degs.append(best)
    return np.array(val_sel), np.array(fresh), np.array(degs)


def kfold_scores(x, y, k, max_deg, rng):
    perm = rng.permutation(len(x))
    folds = np.array_split(perm, k)
    scores = np.zeros((k, max_deg + 1))
    for i, f in enumerate(folds):
        tr = np.concatenate([g for j, g in enumerate(folds) if j != i])
        for d in range(max_deg + 1):
            scores[i, d] = mse(poly_fit(x[tr], y[tr], d), x[f], y[f])
    return folds, scores


def one_nn(Xtr, ytr, Xte):
    d2 = ((Xte[:, None, :] - Xtr[None, :, :]) ** 2).sum(axis=2)
    return ytr[np.argmin(d2, axis=1)]


@st.cache_data(show_spinner=False)
def duplicate_leak(dup_frac, seed, n_unique=200, flip=0.25, reps=30, test_frac=0.3):
    rng = np.random.default_rng(seed + 321)
    naive, grouped, copies = [], [], []
    for _ in range(reps):
        X = rng.uniform(-1, 1, (n_unique, 2))
        y = (X.sum(axis=1) > 0).astype(int)
        flips = rng.random(n_unique) < flip
        y[flips] = 1 - y[flips]
        ids = np.concatenate([np.arange(n_unique), rng.choice(n_unique, int(round(dup_frac * n_unique)), replace=False)])
        perm = rng.permutation(len(ids))
        n_te = int(round(test_frac * len(ids)))
        te, tr = ids[perm[:n_te]], ids[perm[n_te:]]
        naive.append(np.mean(one_nn(X[tr], y[tr], X[te]) == y[te]))
        copies.append(np.mean(np.isin(te, tr)))
        test_ids = rng.permutation(n_unique)[: int(round(test_frac * n_unique))]
        mask = np.isin(ids, test_ids)
        grouped.append(np.mean(one_nn(X[ids[~mask]], y[ids[~mask]], X[ids[mask]]) == y[ids[mask]]))
    return float(np.mean(naive)), float(np.mean(grouped)), float(np.mean(copies))


def standardize(X_fit, X_apply):
    mu, sd = X_fit.mean(axis=0), X_fit.std(axis=0)
    return (X_apply - mu) / np.where(sd < 1e-12, 1.0, sd)


def top_features(Xs, y, m):
    gap = np.abs(Xs[y == 1].mean(axis=0) - Xs[y == 0].mean(axis=0))
    return np.argsort(gap)[::-1][:m]


def centroid_acc(Xtr, ytr, Xte, yte):
    c0, c1 = Xtr[ytr == 0].mean(axis=0), Xtr[ytr == 1].mean(axis=0)
    pred = (((Xte - c1) ** 2).sum(axis=1) < ((Xte - c0) ** 2).sum(axis=1)).astype(int)
    return float(np.mean(pred == yte))


@st.cache_data(show_spinner=False)
def selection_leak(p, m, seed, n=60, k=5, reps=10):
    """5-fold CV accuracy on pure-noise features with RANDOM labels (true accuracy = 50 %)."""
    rng = np.random.default_rng(seed + 654)
    out = {"leaky": [], "scale_only": [], "honest": []}
    for _ in range(reps):
        X = rng.normal(size=(n, p))
        y = rng.permutation(np.arange(n) % 2)
        Xs_all = standardize(X, X)
        sel_all = top_features(Xs_all, y, m)
        folds = np.array_split(rng.permutation(n), k)
        for i, te in enumerate(folds):
            tr = np.concatenate([g for j, g in enumerate(folds) if j != i])
            out["leaky"].append(centroid_acc(Xs_all[tr][:, sel_all], y[tr], Xs_all[te][:, sel_all], y[te]))
            sel_tr = top_features(Xs_all[tr], y[tr], m)
            out["scale_only"].append(centroid_acc(Xs_all[tr][:, sel_tr], y[tr], Xs_all[te][:, sel_tr], y[te]))
            Xs_tr, Xs_te = standardize(X[tr], X[tr]), standardize(X[tr], X[te])
            sel_h = top_features(Xs_tr, y[tr], m)
            out["honest"].append(centroid_acc(Xs_tr[:, sel_h], y[tr], Xs_te[:, sel_h], y[te]))
    return {key: float(np.mean(v)) for key, v in out.items()}


def assignment_heatmap(z, labels, title, xaxis_title):
    """Rows = rounds/folds, columns = data points; 0 train, 1 validation, 2 unused/future."""
    scale = [[0, COLORS["train"]], [0.33, COLORS["train"]], [0.33, COLORS["val"]], [0.67, COLORS["val"]],
             [0.67, COLORS["unused"]], [1, COLORS["unused"]]]
    fig = go.Figure(go.Heatmap(z=z, y=labels, zmin=0, zmax=2, colorscale=scale, showscale=False, xgap=1, ygap=3,
                               hovertemplate="%{y}, point %{x}: %{customdata}<extra></extra>",
                               customdata=np.array(["train", "validation", "not used"])[z.astype(int)]))
    fig.update_layout(title=title, template="plotly_dark", height=90 + 34 * len(labels), margin=dict(l=10, r=10, t=45, b=10),
                      xaxis_title=xaxis_title, yaxis=dict(autorange="reversed"))
    return fig


# ---------------------------------------------------------------- sections
def render_intro():
    st.title("✂️ Train, Validation & Test Splits")
    st.markdown(
        "If a teacher hands out the exam questions as homework, a perfect exam score proves only that students "
        "**remember answers**. A model is the same: scoring it on data it learned from — or on data you used to "
        "**choose** it — says little about new data. So one dataset is cut into three jobs:"
    )
    c1, c2, c3 = st.columns(3)
    c1.success("**Train** — the model fits its weights here.")
    c2.warning("**Validation** — you compare models / hyper-parameters here and pick a winner.")
    c3.error("**Test** — opened **once**, at the end, to report an honest number.")


def render_split_lab(seed):
    st.header("🧪 Lab 1 — Cut one dataset into three")
    c0, c1, c2, c3, c4 = st.columns(5)
    n = c0.slider("Total points n", 20, 400, 120, 10, key="p72_n")
    noise = c1.slider("Noise σ", 0.05, 1.0, 0.3, 0.05, key="p72_noise")
    f_tr = c2.slider("Train fraction", 0.0, 1.0, DEFAULT_FRACS[0], 0.05, key="p72_ftr")
    f_va = c3.slider("Validation fraction", 0.0, 1.0, DEFAULT_FRACS[1], 0.05, key="p72_fva")
    f_te = c4.slider("Test fraction", 0.0, 1.0, DEFAULT_FRACS[2], 0.05, key="p72_fte")
    fracs = (f_tr, f_va, f_te)
    total = sum(fracs)
    counts = split_counts(n, fracs)
    if total > 1 + 1e-9:
        st.error(f"The fractions sum to {total:.2f} > 1 — a point cannot be in two splits. "
                 f"Using the default {DEFAULT_FRACS[0]:.0%} / {DEFAULT_FRACS[1]:.0%} / {DEFAULT_FRACS[2]:.0%} below.")
        fracs = DEFAULT_FRACS
    elif any(c < m for c, m in zip(counts, MIN_COUNTS)):
        st.error(f"Counts {counts} are too small: the labs need ≥ {MIN_COUNTS[0]} train, ≥ {MIN_COUNTS[1]} validation and "
                 f"≥ {MIN_COUNTS[2]} test points. Using the default 60 / 20 / 20 split below.")
        fracs = DEFAULT_FRACS
    elif total < 1 - 1e-9:
        st.info(f"Fractions sum to {total:.2f}: {1 - total:.0%} of the data is simply left unused (grey).")
    counts = split_counts(n, fracs)

    rng = np.random.default_rng(seed)
    x, y = make_data(n, noise, rng)
    perm = rng.permutation(n)
    c_tr, c_va, c_te = counts
    idx = {"train": perm[:c_tr], "val": perm[c_tr:c_tr + c_va], "test": perm[c_tr + c_va:c_tr + c_va + c_te],
           "unused": perm[c_tr + c_va + c_te:]}

    fig = go.Figure()
    xs = np.linspace(-1, 1, 300)
    fig.add_trace(go.Scatter(x=xs, y=true_f(xs), mode="lines", name="hidden truth", line=dict(color="white", dash="dash")))
    for name, ids in idx.items():
        if len(ids):
            fig.add_trace(go.Scatter(x=x[ids], y=y[ids], mode="markers", name=f"{name} ({len(ids)})",
                                     marker=dict(color=COLORS[name], size=8, line=dict(color="black", width=0.5))))
    fig.update_layout(template="plotly_dark", height=360, margin=dict(l=10, r=10, t=30, b=10), xaxis_title="x", yaxis_title="y",
                      legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig, width="stretch")
    st.caption("A shuffled permutation is cut into consecutive blocks, so every point lands in exactly one split.")
    return x, y, idx, fracs, noise


def render_selection_lab(x, y, idx, noise, seed):
    st.header("🧪 Lab 2 — Pick a model on validation, report test once")
    max_deg_req = st.slider("Largest polynomial degree to try", 1, 15, 12, key="p72_maxdeg")
    xtr, ytr, xva, yva = x[idx["train"]], y[idx["train"]], x[idx["val"]], y[idx["val"]]
    xte, yte = x[idx["test"]], y[idx["test"]]
    max_deg = min(max_deg_req, len(xtr) - 1)
    if max_deg < max_deg_req:
        st.caption(f"Capped at degree {max_deg}: a degree-d polynomial needs at least d + 1 training points.")
    fits, tr_err, va_err = degree_sweep(xtr, ytr, xva, yva, max_deg)
    best = int(np.argmin(va_err))
    test_err = mse(fits[best], xte, yte)

    a, b = st.columns(2)
    with a:
        degs = np.arange(max_deg + 1)
        fig = go.Figure([go.Scatter(x=degs, y=np.maximum(tr_err, 1e-6), name="train MSE", mode="lines+markers", line=dict(color=COLORS["train"])),
                         go.Scatter(x=degs, y=np.maximum(va_err, 1e-6), name="validation MSE", mode="lines+markers", line=dict(color=COLORS["val"]))])
        fig.add_vline(x=best, line_dash="dot", line_color="#22c55e", annotation_text=f"chosen d = {best}")
        fig.update_layout(template="plotly_dark", height=340, yaxis_type="log", xaxis_title="degree", yaxis_title="MSE (log)",
                          margin=dict(l=10, r=10, t=30, b=10), legend=dict(orientation="h", y=1.12))
        st.plotly_chart(fig, width="stretch")
    with b:
        xs = np.linspace(-1, 1, 300)
        fig = go.Figure([go.Scatter(x=xtr, y=ytr, mode="markers", name="train", marker=dict(color=COLORS["train"])),
                         go.Scatter(x=xva, y=yva, mode="markers", name="validation", marker=dict(color=COLORS["val"])),
                         go.Scatter(x=xs, y=fits[best](xs), mode="lines", name=f"chosen fit (d = {best})", line=dict(color="#22c55e", width=3))])
        lo, hi = float(min(y.min(), true_f(xs).min())) - 0.8, float(max(y.max(), true_f(xs).max())) + 0.8
        fig.update_layout(template="plotly_dark", height=340, yaxis_range=[lo, hi], margin=dict(l=10, r=10, t=30, b=10),
                          legend=dict(orientation="h", y=1.12))
        st.plotly_chart(fig, width="stretch")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Chosen degree", best)
    m2.metric("Train MSE", f"{tr_err[best]:.4f}")
    m3.metric("Validation MSE (used to choose)", f"{va_err[best]:.4f}")
    m4.metric("Test MSE (looked at once)", f"{test_err:.4f}", help=f"Irreducible noise alone gives σ² = {noise ** 2:.4f}.")

    st.subheader("Why not just report the validation score? — the winner's curse")
    val_sel, fresh, _ = optimism_mc(len(xtr), len(xva), noise, max_deg, seed)
    gap = fresh - val_sel
    x_hi = float(np.quantile(np.r_[val_sel, fresh], 0.95)) * 1.05
    n_clipped = int(np.sum(fresh > x_hi) + np.sum(val_sel > x_hi))
    bins = dict(start=0, end=x_hi, size=x_hi / 40)
    fig = go.Figure([go.Histogram(x=val_sel, name="val MSE of the selected model", marker_color=COLORS["val"], opacity=0.7, xbins=bins),
                     go.Histogram(x=fresh, name="its MSE on fresh data", marker_color=COLORS["test"], opacity=0.7, xbins=bins)])
    fig.update_layout(barmode="overlay", template="plotly_dark", height=300, xaxis_title="MSE", margin=dict(l=10, r=10, t=30, b=10),
                      legend=dict(orientation="h", y=1.15), xaxis_range=[0, x_hi])
    st.plotly_chart(fig, width="stretch")
    if n_clipped:
        st.caption(f"{n_clipped} values above {x_hi:.3f} lie off the right edge (wild high-degree fits extrapolating).")
    st.markdown(
        f"Over **{len(val_sel)} fresh datasets** of the same sizes ({len(xtr)} train / {len(xva)} val), the selected model's "
        f"validation MSE has median **{np.median(val_sel):.4f}**, but its error on 2 000 fresh points has median "
        f"**{np.median(fresh):.4f}** (fresh error was higher in {np.mean(gap > 0):.0%} of runs). Picking the minimum of "
        f"{max_deg + 1} noisy scores favours models that got **lucky** on this validation set — so the test set must stay untouched."
    )


def render_cv_lab(x, y, idx, seed):
    st.header("🧪 Lab 3 — k-fold cross-validation")
    st.markdown("Instead of one validation set, rotate: split train + validation into k folds, train on k − 1, score on the held-out fold, repeat.")
    pool = np.concatenate([idx["train"], idx["val"]])
    xp, yp = x[pool], y[pool]
    c1, c2 = st.columns(2)
    k_req = c1.slider("Number of folds k", 2, 10, 5, key="p72_k")
    deg_req = c2.slider("Largest degree for CV", 1, 15, 10, key="p72_cv_maxdeg")
    k = min(k_req, len(pool))
    min_train = len(pool) - int(np.ceil(len(pool) / k))
    max_deg = max(0, min(deg_req, min_train - 1))
    folds, scores = kfold_scores(xp, yp, k, max_deg, np.random.default_rng(seed + 77))
    mean, sd = scores.mean(axis=0), scores.std(axis=0, ddof=1)
    best = int(np.argmin(mean))

    z = np.zeros((k, len(pool)))
    for i, f in enumerate(folds):
        z[i, f] = 1
    st.plotly_chart(assignment_heatmap(z, [f"round {i + 1}" for i in range(k)],
                                       "Fold assignment (blue = train, amber = validation fold)", "data point (pool index)"), width="stretch")
    a, b = st.columns([3, 2])
    with a:
        degs = np.arange(max_deg + 1)
        lower = np.maximum(mean - sd, mean / 10)
        fig = go.Figure([
            go.Scatter(x=np.concatenate([degs, degs[::-1]]), y=np.concatenate([mean + sd, lower[::-1]]), fill="toself",
                       fillcolor="rgba(245,158,11,0.2)", line=dict(width=0), name="mean ± sd", hoverinfo="skip"),
            go.Scatter(x=degs, y=mean, mode="lines+markers", name="CV mean MSE", line=dict(color=COLORS["val"]))])
        fig.add_vline(x=best, line_dash="dot", line_color="#22c55e", annotation_text=f"CV choice d = {best}")
        fig.update_layout(template="plotly_dark", height=330, yaxis_type="log", xaxis_title="degree", yaxis_title="MSE (log)",
                          margin=dict(l=10, r=10, t=30, b=10), legend=dict(orientation="h", y=1.12))
        st.plotly_chart(fig, width="stretch")
    with b:
        st.dataframe([{"fold": i + 1, "points held out": len(f), f"MSE (d = {best})": round(float(scores[i, best]), 4)}
                      for i, f in enumerate(folds)], hide_index=True, width="stretch")
        final = poly_fit(xp, yp, best)
        st.metric(f"CV score, d = {best}", f"{mean[best]:.4f} ± {sd[best]:.4f}")
        st.metric("Refit on all train + val → test MSE", f"{mse(final, x[idx['test']], y[idx['test']]):.4f}")
    if k < k_req:
        st.caption(f"k capped at {k}: there are only {len(pool)} points in the pool (k = n is leave-one-out).")
    return scores[:, best], best


def render_leakage_lab(seed):
    st.header("🧪 Lab 4 — Data leakage: when the test set peeks")
    kind = st.radio("Leak type", ["Duplicate rows across splits", "Preprocessing fit on all data"], horizontal=True, key="p72_leak")
    if kind.startswith("Duplicate"):
        dup = st.slider("Fraction of rows that appear twice", 0.0, 0.9, 0.5, 0.1, key="p72_dup")
        naive, grouped, copies = duplicate_leak(dup, seed)
        c1, c2, c3 = st.columns(3)
        c1.metric("1-NN test accuracy, rows split at random", f"{naive:.1%}")
        c2.metric("1-NN test accuracy, duplicates kept together", f"{grouped:.1%}")
        c3.metric("Test rows with an exact copy in train", f"{copies:.1%}")
        st.markdown(
            "Labels follow $x_1+x_2>0$ but **25 % are flipped**, so no model can honestly beat ≈ 75 %. A 1-nearest-neighbour model "
            "simply looks up an identical training row — memorising even the flipped labels — so every duplicated test row is a free hit. "
            "Fix: de-duplicate, or split by **group** (user, patient, document) so copies never straddle the boundary."
        )
    else:
        c1, c2 = st.columns(2)
        p = c1.select_slider("Number of pure-noise features", options=[50, 200, 500, 1000, 2000], value=1000, key="p72_p")
        m = c2.slider("Features kept by selection", 1, 50, 10, key="p72_m")
        res = selection_leak(p, m, seed)
        c1, c2, c3 = st.columns(3)
        c1.metric("Scaling + selection fit on ALL data", f"{res['leaky']:.1%}")
        c2.metric("Only scaling fit on all data", f"{res['scale_only']:.1%}")
        c3.metric("Everything fit inside each training fold", f"{res['honest']:.1%}")
        st.markdown(
            f"60 samples, {p} random features and **random labels**: the true accuracy is 50 %. Choosing the {m} features most "
            "correlated with the labels **before** splitting lets the validation folds vote on the features, so CV reports a "
            "fantasy score. Leaking only the scaler's mean/sd is mild here — but the rule is the same: every step that *learns* "
            "from data (scaler, imputer, feature selector, tokenizer vocab…) is fit on the training fold only."
        )


def render_strat_lab(fracs, seed):
    st.header("🧪 Lab 5 — Stratify imbalanced classes")
    c1, c2 = st.columns(2)
    n = c1.slider("Dataset size", 50, 2000, 200, 50, key="p72_strat_n")
    pos = c2.slider("Positive-class rate", 0.01, 0.5, 0.05, 0.01, key="p72_pos")
    n_pos = int(round(pos * n))
    n_neg = n - n_pos
    counts = split_counts(n, fracs)
    pos_counts = split_counts(n_pos, fracs)
    neg_counts = split_counts(n_neg, fracs)
    rng = np.random.default_rng(seed + 999)
    labels = np.r_[np.ones(n_pos, int), np.zeros(n_neg, int)][rng.permutation(n)]
    cuts = np.cumsum((0,) + counts)
    rows = []
    for i, name in enumerate(["train", "val", "test"]):
        part = labels[cuts[i]:cuts[i + 1]]
        strat_n = pos_counts[i] + neg_counts[i]
        rows.append({"split": name, "random: size": len(part), "random: positives": int(part.sum()),
                     "random: rate": f"{part.mean():.1%}" if len(part) else "–",
                     "stratified: size": strat_n, "stratified: positives": pos_counts[i],
                     "stratified: rate": f"{pos_counts[i] / strat_n:.1%}" if strat_n else "–"})
    st.dataframe(rows, hide_index=True, width="stretch")
    sims = rng.hypergeometric(n_pos, n_neg, counts[1], size=5000) if n_pos and n_neg else np.full(5000, n_pos and counts[1])
    fig = go.Figure(go.Histogram(x=sims, marker_color=COLORS["val"], name="random split"))
    fig.add_vline(x=pos_counts[1], line_color="#22c55e", line_width=3, annotation_text="stratified (always)")
    fig.update_layout(template="plotly_dark", height=280, xaxis_title="positives in the validation split (5 000 random splits)",
                      margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig, width="stretch")
    st.markdown(
        f"Overall rate {n_pos / n:.1%} ({n_pos} positives). With a plain random split the validation set receives **zero** "
        f"positives in {np.mean(sims == 0):.1%} of shuffles — then recall is undefined and the score is noise. Stratifying "
        "applies the same fractions **within each class**, so every split mirrors the overall ratio."
    )


def render_timeseries(seed):
    st.header("⏳ Caution — time series must be split by time")
    rng = np.random.default_rng(seed + 31)
    n = 200
    t = np.arange(n)
    series = np.cumsum(rng.normal(0, 1, n)) + 0.05 * t
    te_rand = np.sort(rng.permutation(n)[: n // 5])
    tr_rand = np.setdiff1d(t, te_rand)
    tr_chr, te_chr = t[: n - n // 5], t[n - n // 5:]

    def nearest_in_time(tr, te):
        return series[tr[np.argmin(np.abs(te[:, None] - tr[None, :]), axis=1)]]

    err_rand = float(np.mean((nearest_in_time(tr_rand, te_rand) - series[te_rand]) ** 2))
    err_chr = float(np.mean((nearest_in_time(tr_chr, te_chr) - series[te_chr]) ** 2))
    fig = go.Figure([go.Scatter(x=t, y=series, mode="lines", line=dict(color="#94a3b8"), name="series"),
                     go.Scatter(x=te_rand, y=series[te_rand], mode="markers", marker=dict(color=COLORS["test"]), name="random test points"),
                     go.Scatter(x=te_chr, y=series[te_chr], mode="lines", line=dict(color=COLORS["val"], width=4), name="future test block")])
    fig.update_layout(template="plotly_dark", height=280, xaxis_title="time step", margin=dict(l=10, r=10, t=30, b=10),
                      legend=dict(orientation="h", y=1.15))
    st.plotly_chart(fig, width="stretch")
    c1, c2 = st.columns(2)
    c1.metric("‘Copy the nearest training time’ — random split MSE", f"{err_rand:.2f}")
    c2.metric("Same model — train on past, test on future", f"{err_chr:.2f}")
    st.markdown("A random split lets the model **interpolate** between yesterday and tomorrow; deployment only ever sees the past. "
                "Use forward-chaining folds instead (each round trains on everything before its validation block):")
    k = st.slider("Forward-chaining folds", 2, 8, 4, key="p72_ts_k")
    block = n // (k + 1)
    z = np.full((k, n), 2.0)
    for i in range(k):
        z[i, : block * (i + 1)] = 0
        z[i, block * (i + 1): block * (i + 2)] = 1
    st.plotly_chart(assignment_heatmap(z, [f"round {i + 1}" for i in range(k)],
                                       "Expanding-window split (blue train, amber validation, grey not yet seen)", "time step"), width="stretch")


def render_worked_example(fracs, n, fold_scores, best):
    st.header("🔢 Worked example — the numbers behind this page")
    c = split_counts(n, fracs)
    f1, f12, f123 = fracs[0], fracs[0] + fracs[1], sum(fracs)
    st.markdown("**Split sizes** come from rounding cumulative cut points of the shuffled list:")
    st.latex(rf"n_\text{{train}}=\operatorname{{round}}({f1:.2f}\cdot{n})={c[0]},\quad "
             rf"n_\text{{val}}=\operatorname{{round}}({f12:.2f}\cdot{n})-{c[0]}={c[1]},\quad "
             rf"n_\text{{test}}=\operatorname{{round}}({f123:.2f}\cdot{n})-{c[0] + c[1]}={c[2]}")
    k = len(fold_scores)
    s = ", ".join(f"{v:.4f}" for v in fold_scores)
    mean = float(np.mean(fold_scores))
    sd = float(np.std(fold_scores, ddof=1))
    st.markdown(f"**Cross-validation score** of the chosen degree d = {best} from its {k} fold MSEs ({s}):")
    st.latex(rf"\bar s=\frac1{{{k}}}\sum_{{i=1}}^{{{k}}} s_i={mean:.4f},\qquad "
             rf"\mathrm{{sd}}=\sqrt{{\frac1{{{k}-1}}\sum_i (s_i-\bar s)^2}}={sd:.4f}")
    st.caption("The sd shows how much the score depends on *which* points were held out — "
               "differences between models smaller than this are often noise.")


def render_ai_connection():
    st.header("🤖 AI / ML connection")
    st.markdown(
        "- **Benchmark contamination.** If test questions of an LLM benchmark leaked into web-scale pre-training data, the score "
        "measures memory, not skill — the duplicate-row leak at internet scale. Labs counter it with n-gram overlap checks, "
        "held-out/private test sets and freshly written benchmarks.\n"
        "- **Hyper-parameter tuning** (learning rate, weight decay, depth, dropout) is model selection on the **validation** set; "
        "after hundreds of trials the best validation score is optimistic, exactly like Lab 2's winner's curse. Public "
        "leaderboards that are queried too often get overfit the same way.\n"
        "- **Early stopping** watches validation loss every epoch and keeps the best checkpoint — it is also a choice made with "
        "validation data (see *Learning Curves*).\n"
        "- **Production splits** are by user, by document or by time, so evaluation mimics the data the model will actually meet."
    )
    safe_page_link("pages/75Learning Curves.py", "Early stopping on validation loss → Learning Curves", icon="📈")


def render_takeaways():
    st.header("✅ Key takeaways")
    st.markdown(
        "1. Train fits weights, validation chooses between models, test is opened once for the final report.\n"
        "2. The validation score of the *selected* model is optimistically biased — report test (or nested CV) instead.\n"
        "3. k-fold CV reuses every point for validation once and reports mean ± sd across folds.\n"
        "4. Leakage (duplicates, preprocessing fit on all data, future information) silently inflates scores.\n"
        "5. Stratify rare classes; split time series by time; split grouped data by group."
    )
    c1, c2 = st.columns(2)
    with c1:
        safe_page_link("pages/71Overfitting Underfitting.py", "← Previous: Overfitting & Underfitting")
    with c2:
        safe_page_link("pages/73Bias-Variance Tradeoff.py", "Next: Bias-Variance Tradeoff →")


def main():
    st.session_state.setdefault("p72_seed", 72)
    render_intro()
    top = st.columns([4, 1])
    with top[1]:
        if st.button("🎲 Resample data & splits", key="p72_resample"):
            st.session_state["p72_seed"] += 1
    seed = int(st.session_state["p72_seed"])
    top[0].caption(f"Random seed: {seed} — every dataset, shuffle and simulation below is reproducible from it.")
    x, y, idx, fracs, noise = render_split_lab(seed)
    st.divider()
    render_selection_lab(x, y, idx, noise, seed)
    st.divider()
    fold_scores, best = render_cv_lab(x, y, idx, seed)
    st.divider()
    render_leakage_lab(seed)
    st.divider()
    render_strat_lab(fracs, seed)
    st.divider()
    render_timeseries(seed)
    st.divider()
    render_worked_example(fracs, len(x), fold_scores, best)
    st.divider()
    render_ai_connection()
    st.divider()
    render_takeaways()


main()
