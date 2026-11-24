import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="83 · Automatic Differentiation", page_icon="📈", layout="wide")

FD_H = 1e-6  # central finite-difference step


def _sigmoid(z):
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


# ---------------------------------------------------------------- reverse mode: a tiny autograd engine
class Value:
    """A scalar node in the computational graph. Each op records its local derivatives for the backward pass."""

    def __init__(self, data, children=(), op="input", name=""):
        self.data = float(data)
        self.grad = 0.0
        self.name = name
        self.op = op
        self.arg = None  # exponent for pow
        self._local = []  # (child, ∂self/∂child) pairs, computed during the forward pass
        self.contribs = []  # (parent, amount) gradient messages received during backward
        self.saved = "—"  # what the backward pass needs to keep from the forward pass
        self._prev = tuple(children)

    @staticmethod
    def _lift(o):
        return o if isinstance(o, Value) else Value(o, op="const", name=f"{o:g}")

    def __add__(self, other):
        other = Value._lift(other)
        out = Value(self.data + other.data, (self, other), "+")
        out._local = [(self, 1.0), (other, 1.0)]
        return out

    __radd__ = __add__

    def __mul__(self, other):
        other = Value._lift(other)
        out = Value(self.data * other.data, (self, other), "·")
        out._local = [(self, other.data), (other, self.data)]
        out.saved = "both inputs"
        return out

    __rmul__ = __mul__

    def __neg__(self):
        out = Value(-self.data, (self,), "neg")
        out._local = [(self, -1.0)]
        return out

    def __sub__(self, other):
        return self + (-Value._lift(other))

    def __pow__(self, k):
        out = Value(self.data**k, (self,), "pow")
        out.arg = k
        out._local = [(self, k * self.data ** (k - 1))]
        out.saved = "input"
        return out

    def sin(self):
        out = Value(math.sin(self.data), (self,), "sin")
        out._local = [(self, math.cos(self.data))]
        out.saved = "input (for cos)"
        return out

    def exp(self):
        e = math.exp(self.data)
        out = Value(e, (self,), "exp")
        out._local = [(self, e)]
        out.saved = "output"
        return out

    def sigmoid(self):
        s = _sigmoid(self.data)
        out = Value(s, (self,), "σ")
        out._local = [(self, s * (1 - s))]
        out.saved = "output"
        return out


def topo_sort(root):
    topo, seen = [], set()

    def build(v):
        if id(v) not in seen:
            seen.add(id(v))
            for child in v._prev:
                build(child)
            topo.append(v)

    build(root)
    return topo


def backward(root, accumulate=True, steps=None):
    """Reverse-mode sweep. Runs only the first `steps` nodes of the reverse topological order (for the step-through)."""
    topo = topo_sort(root)
    for v in topo:
        v.grad, v.contribs = 0.0, []
    root.grad = 1.0
    order = topo[::-1]
    for v in order[: len(order) if steps is None else steps]:
        for child, local in v._local:
            amount = local * v.grad
            child.contribs.append((v, amount))
            child.grad = child.grad + amount if accumulate else amount  # `=` is the classic reuse bug
    return order


# ---------------------------------------------------------------- forward mode: dual numbers a + b·ε, ε² = 0
class Dual:
    def __init__(self, val, dot=0.0):
        self.val, self.dot = float(val), float(dot)

    @staticmethod
    def _lift(o):
        return o if isinstance(o, Dual) else Dual(o)

    def __add__(self, o):
        o = Dual._lift(o)
        return Dual(self.val + o.val, self.dot + o.dot)

    __radd__ = __add__

    def __mul__(self, o):
        o = Dual._lift(o)
        return Dual(self.val * o.val, self.dot * o.val + self.val * o.dot)

    __rmul__ = __mul__

    def __neg__(self):
        return Dual(-self.val, -self.dot)

    def __sub__(self, o):
        return self + (-Dual._lift(o))

    def __pow__(self, k):
        return Dual(self.val**k, k * self.val ** (k - 1) * self.dot)

    def sin(self):
        return Dual(math.sin(self.val), math.cos(self.val) * self.dot)

    def exp(self):
        e = math.exp(self.val)
        return Dual(e, e * self.dot)

    def sigmoid(self):
        s = _sigmoid(self.val)
        return Dual(s, s * (1 - s) * self.dot)


def sin(v):
    return v.sin() if hasattr(v, "sin") else math.sin(v)


def exp(v):
    return v.exp() if hasattr(v, "exp") else math.exp(v)


def sigmoid(v):
    return v.sigmoid() if hasattr(v, "sigmoid") else _sigmoid(v)


# ---------------------------------------------------------------- expressions (one Python function → floats, Values or Duals)
def expr_f(x, y):
    return (x * y + sin(x)) * exp(-y)


def grad_f(x, y):
    e = math.exp(-y)
    return [(y + math.cos(x)) * e, (x - x * y - math.sin(x)) * e]


def expr_neuron(w, x, b, t):
    return (sigmoid(w * x + b) - t) ** 2


def grad_neuron(w, x, b, t):
    a = _sigmoid(w * x + b)
    common = 2 * (a - t) * a * (1 - a)
    return [common * x, common * w, common, -2 * (a - t)]


def expr_cube(x):
    return x * x * x


EXPRS = {
    "f(x, y) = (x·y + sin x)·exp(−y)": dict(
        slug="fxy", vars=[("x", -3.0, 3.0, 1.0), ("y", -2.0, 2.0, 0.5)], fn=expr_f, grad=grad_f,
        tex=r"\frac{\partial f}{\partial x}=(y+\cos x)e^{-y},\qquad \frac{\partial f}{\partial y}=(x-xy-\sin x)e^{-y}"),
    "Neuron loss L = (σ(w·x + b) − t)²": dict(
        slug="neuron", vars=[("w", -3.0, 3.0, 0.8), ("x", -3.0, 3.0, 1.5), ("b", -3.0, 3.0, -0.5), ("t", 0.0, 1.0, 1.0)],
        fn=expr_neuron, grad=grad_neuron,
        tex=r"a=\sigma(wx+b):\ \frac{\partial L}{\partial w}=2(a-t)\,a(1-a)\,x,\ \frac{\partial L}{\partial x}=2(a-t)\,a(1-a)\,w,"
            r"\ \frac{\partial L}{\partial b}=2(a-t)\,a(1-a),\ \frac{\partial L}{\partial t}=-2(a-t)"),
    "g(x) = x·x·x  (one input used three times)": dict(
        slug="cube", vars=[("x", -2.0, 2.0, 1.5)], fn=expr_cube, grad=lambda x: [3 * x * x], tex=r"g'(x)=3x^2"),
}


def build_graph(spec, vals):
    inputs = [Value(v, name=n) for (n, *_), v in zip(spec["vars"], vals)]
    out = spec["fn"](*inputs)
    topo = topo_sort(out)
    k = 1
    for v in topo:
        if not v.name:
            v.name = f"v{k}"
            k += 1
    out.name = "out"
    return inputs, out, topo


def node_formula(v):
    a = [c.name for c in v._prev]
    return {"+": lambda: f"{a[0]} + {a[1]}", "·": lambda: f"{a[0]} · {a[1]}", "neg": lambda: f"−{a[0]}",
            "sin": lambda: f"sin({a[0]})", "exp": lambda: f"exp({a[0]})", "σ": lambda: f"σ({a[0]})",
            "pow": lambda: f"{a[0]}^{v.arg}"}.get(v.op, lambda: "input" if v.op == "input" else "constant")()


def graph_dot(topo, order, step):
    idx = {id(v): i for i, v in enumerate(topo)}
    done = {id(v) for v in order[:step]}
    current = order[step - 1] if step > 0 else None
    lines = ['digraph G {', 'rankdir=LR; bgcolor="transparent"; nodesep=0.35; ranksep=0.6;',
             'node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=11, fontcolor="white", color="#94a3b8", penwidth=1.5];',
             'edge [color="#64748b", fontname="Helvetica", fontsize=10, fontcolor="#cbd5e1"];']
    for v in topo:
        touched = v is order[0] or id(v) in done or bool(v.contribs)
        grad_txt = f"grad = {v.grad:.4f}" + (" ✓" if id(v) in done else "") if touched else "grad = ?"
        fill = "#1e3a8a" if v.op == "input" else "#334155"
        border = "#ef4444" if v is current else ("#22c55e" if id(v) in done else "#94a3b8")
        width = 3.5 if v is current else 1.5
        title = v.name if v.op in ("input", "const") else f"{v.name} = {node_formula(v)}"
        lines.append(f'n{idx[id(v)]} [label="{title}\\nvalue = {v.data:.4f}\\n{grad_txt}", fillcolor="{fill}", color="{border}", penwidth={width}];')
    for v in topo:
        for child, local in v._local:
            hot = id(v) in done
            attrs = f'label="∂={local:.3f}"' + (', color="#ef4444", penwidth=2.5' if v is current else (', color="#22c55e"' if hot else ""))
            lines.append(f"n{idx[id(child)]} -> n{idx[id(v)]} [{attrs}];")
    lines.append("}")
    return "\n".join(lines)


def enumerate_paths(node, target):
    """All chain-rule paths from `node` down to `target`, as lists of local derivatives."""
    if node is target:
        yield []
        return
    for child, local in node._local:
        for rest in enumerate_paths(child, target):
            yield [local, *rest]


def lab():
    st.header("2 · Lab — a reverse-mode autodiff engine, live")
    c = st.columns([1.6, 1])
    choice = c[0].selectbox("Expression", list(EXPRS), key="p83_expr")
    buggy = c[1].toggle("Buggy engine: overwrite (=) instead of accumulate (+=)", value=False, key="p83_buggy")
    spec = EXPRS[choice]
    sc = st.columns(len(spec["vars"]))
    vals = [sc[i].slider(n, lo, hi, d, 0.05, key=f"p83_{spec['slug']}_{n}") for i, (n, lo, hi, d) in enumerate(spec["vars"])]

    inputs, out, topo = build_graph(spec, vals)
    order = topo_sort(out)[::-1]
    n_steps = len(order)
    step = st.slider("Backward-pass step (nodes processed in reverse topological order)", 0, n_steps, n_steps,
                     key=f"p83_step_{spec['slug']}")
    backward(out, accumulate=not buggy, steps=step)
    if step == 0:
        st.info("Step 0 — **seed**: ∂out/∂out = 1. Nothing has been propagated yet.")
    else:
        cur = order[step - 1]
        sends = ", ".join(f"{local:.4f} × {cur.grad:.4f} → {child.name}" for child, local in cur._local) or "nothing (leaf node)"
        st.info(f"Step {step}/{n_steps} — processing **{cur.name}** ({node_formula(cur)}): its gradient {cur.grad:.4f} is final; "
                f"it sends local × upstream: {sends}.")
    st.graphviz_chart(graph_dot(topo, order, step), width="stretch")
    st.caption("Blue = inputs. Edge labels are local derivatives ∂parent/∂child. Green ✓ = node already processed "
               "(its gradient is complete); red = the node processed at this step; 'grad = ?' = no gradient has arrived yet.")

    rows = []
    for i, v in enumerate(order):
        rows.append({"backward order": i + 1, "node": v.name, "computes": node_formula(v), "forward value": round(v.data, 6),
                     "local derivatives": ", ".join(f"∂/∂{c.name} = {loc:.4f}" for c, loc in v._local) or "—",
                     "saved for backward": v.saved, "grad (so far)": round(v.grad, 6),
                     "messages received": len(v.contribs)})
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")

    # full results (always from a complete sweep, independent of the step slider)
    backward(out, accumulate=not buggy)
    ad = [v.grad for v in inputs]
    multi = [v for v in inputs if len(v.contribs) > 1]
    if multi:
        parts = []
        for v in multi:
            terms = " + ".join(f"{amt:.4f} (from {p.name})" for p, amt in v.contribs)
            parts.append(f"**{v.name}** feeds {len(v.contribs)} operations → ∂out/∂{v.name} = {terms} = **{sum(a for _, a in v.contribs):.4f}**"
                         + (f" — the buggy engine kept only **{v.grad:.4f}**" if buggy else ""))
        st.markdown("**Gradient accumulation (a variable used more than once):**  \n" + "  \n".join(parts))
        if buggy:
            st.error("With `=` each new message **overwrites** the previous one, so only the last path survives — the gradient is wrong. "
                     "This is exactly why PyTorch *accumulates* into `.grad` (and why you must call `optimizer.zero_grad()`).")
    elif buggy:
        st.caption("No input is reused in this expression, so overwrite and accumulate happen to agree here — try the other expressions.")
    return spec, vals, inputs, out, ad, buggy


def compare(spec, vals, inputs, out, ad, buggy):
    st.header("3 · Check it three ways: analytic, finite differences, forward mode")
    names = [n for n, *_ in spec["vars"]]
    analytic = spec["grad"](*vals)
    fd, fwd = [], []
    for i in range(len(vals)):
        plus, minus = list(vals), list(vals)
        plus[i] += FD_H
        minus[i] -= FD_H
        fd.append((spec["fn"](*plus) - spec["fn"](*minus)) / (2 * FD_H))
        duals = [Dual(v, 1.0 if j == i else 0.0) for j, v in enumerate(vals)]  # one forward pass per input
        fwd.append(spec["fn"](*duals).dot)
    df = pd.DataFrame({
        "input": names,
        "reverse-mode AD": ad,
        "forward-mode (dual)": fwd,
        "analytic": analytic,
        "finite difference": fd,
        "|AD − analytic|": np.abs(np.array(ad) - analytic),
        "|FD − analytic|": np.abs(np.array(fd) - analytic),
    })
    st.dataframe(df.style.format({c: "{:.3e}" for c in ("|AD − analytic|", "|FD − analytic|")} | {c: "{:.10f}" for c in df.columns[1:5]}),
                 hide_index=True, width="stretch")
    st.latex(spec["tex"])
    ad_err, fd_err = float(np.max(df["|AD − analytic|"])), float(np.max(df["|FD − analytic|"]))
    if buggy and ad_err > 1e-9:
        st.error(f"The buggy engine is off by up to {ad_err:.3g} — finite differences catch the bug. Gradient checks like this are standard practice.")
    else:
        st.success(f"Autodiff matches the analytic gradient to {ad_err:.1e} (machine precision — AD is exact, not an approximation). "
                   f"Central finite differences (h = {FD_H:g}) are off by {fd_err:.1e}: truncation error ∝ h² plus round-off ∝ ε/h.")

    with st.expander("🔢 How forward mode works: dual numbers  a + b·ε  with ε² = 0", expanded=False):
        st.markdown(r"""
Carry a value and a **tangent** together: $(a+\dot a\,\varepsilon)(b+\dot b\,\varepsilon)=ab+(\dot a b+a\dot b)\,\varepsilon$ because $\varepsilon^2=0$ —
the product rule falls out of the algebra. Likewise $\sin(a+\dot a\varepsilon)=\sin a+\cos a\,\dot a\,\varepsilon$.
Seed the input you care about with tangent 1 (all others 0), run the function **once forward**, and read $\partial\text{out}/\partial x_i$ off the ε-part.
""")
        seed = st.radio("Seed input (tangent = 1)", names, horizontal=True, key=f"p83_seed_{spec['slug']}")
        i = names.index(seed)
        tangents = {}
        for v in topo_sort(out):  # forward-mode on the same graph: tangent = Σ local × tangent(child)
            tangents[id(v)] = (1.0 if v is inputs[i] else 0.0) if not v._local else sum(loc * tangents[id(c)] for c, loc in v._local)
        st.dataframe(pd.DataFrame([{"node": v.name, "computes": node_formula(v), "value": round(v.data, 6),
                                    f"tangent ∂node/∂{seed}": round(tangents[id(v)], 6)} for v in topo_sort(out)]),
                     hide_index=True, width="stretch")
        st.markdown(f"The output's tangent {tangents[id(out)]:.6f} is ∂out/∂{seed}. Getting **all** {len(names)} partials took "
                    f"**{len(names)} forward passes**; reverse mode got them all from **one backward pass**.")


def worked_example(inputs, out):
    st.header("4 · Worked example: chain rule = sum over paths")
    st.markdown("Every path from the output down to an input contributes the **product** of the local derivatives along it; "
                "the gradient is the **sum** over paths. Reverse mode computes this sum without enumerating paths — "
                "it shares the common prefixes, which is why it scales to billions of parameters.")
    for v in inputs:
        paths = list(enumerate_paths(out, v))
        terms = [r"\cdot".join(f"({loc:.4f})" for loc in path) or "1" for path in paths]
        total = sum(math.prod(path) for path in paths)
        st.latex(rf"\frac{{\partial\,\text{{out}}}}{{\partial {v.name}}}=" + " + ".join(terms) + rf"={total:.6f}"
                 + (rf"\quad({len(paths)}\ \text{{paths}})" if len(paths) > 1 else ""))


def ai_connection(n_nodes):
    st.header("5 · AI / ML connection")
    st.markdown(f"""
- **Backpropagation *is* reverse-mode AD** applied to a network's loss. A loss is one scalar with millions to billions of inputs
  (the weights), so one backward pass giving *every* ∂L/∂w is exactly the right tool. PyTorch's **autograd** builds this graph on the fly
  as your Python runs (like the `Value` class above); **JAX** traces the function and transforms it (`jax.grad`, `jax.vjp`, `jax.jvp`).
- **Cost:** reverse mode costs a small constant (≈ 2–4×) times one forward pass, *regardless* of the number of inputs.
  Forward mode needs one pass per input — great for few inputs / many outputs (and for Jacobian-vector products), hopeless for training.
- **Memory of activations:** the backward pass needs values saved during the forward pass (the 'saved for backward' column). Here that is
  {n_nodes} nodes; in a deep net it is every layer's activations for the whole batch — often the main GPU-memory cost of training.
  **Gradient checkpointing** stores only some of them and recomputes the rest during backward (trading compute for memory).
- **Accumulation:** `.grad` in PyTorch is *added to* on every backward — correct for reused variables (shared weights, RNNs unrolled over time,
  residual connections) — which is why training loops call `optimizer.zero_grad()` each step.
""")
    c1, c2 = st.columns(2)
    c1.code("""import torch
x = torch.tensor(1.0, requires_grad=True)
y = torch.tensor(0.5, requires_grad=True)
f = (x * y + torch.sin(x)) * torch.exp(-y)
f.backward()          # reverse mode over the recorded graph
print(x.grad, y.grad) # same numbers as the lab above""", language="python")
    c2.code("""import jax, jax.numpy as jnp
f = lambda x, y: (x * y + jnp.sin(x)) * jnp.exp(-y)
jax.grad(f, argnums=(0, 1))(1.0, 0.5)  # reverse mode
jax.jvp(f, (1.0, 0.5), (1.0, 0.0))     # forward mode: ∂f/∂x""", language="python")
    n = np.logspace(0, 9, 50)
    fig = go.Figure([go.Scatter(x=n, y=n, name="forward mode: n passes", line=dict(color="#fb923c", width=3)),
                     go.Scatter(x=n, y=np.ones_like(n), name="reverse mode: 1 backward pass", line=dict(color="#38bdf8", width=3))])
    fig.add_vline(x=7e8, line=dict(dash="dot", color="#94a3b8"))
    fig.update_layout(xaxis=dict(type="log", title="number of inputs n (parameters)"), yaxis=dict(type="log", title="passes for the full gradient"),
                      height=300, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=-0.3))
    st.plotly_chart(fig, width="stretch")
    st.caption("Passes needed for the gradient of one scalar loss. The dotted line marks a 700 M-parameter model: forward mode would need "
               "7×10⁸ passes per training step, reverse mode one.")


def main():
    st.title("📈 83 · Automatic Differentiation")
    st.header("1 · Intuition")
    st.markdown(r"""
Any formula a computer evaluates is a sequence of **tiny operations** (+, ·, sin, exp, σ, …), each with a derivative we know.
Write them down as a **computational graph** and the chain rule turns differentiation into bookkeeping:

- **Forward pass:** compute every node's value left → right, remembering what each op will need later.
- **Backward pass (reverse mode):** start from $\partial\,\text{out}/\partial\,\text{out}=1$ and walk the graph in **reverse topological order**;
  each node multiplies its gradient by its local derivatives and **adds** the result into its inputs' gradients.

This is not symbolic algebra (no expression swell) and not finite differences (no step-size error): it is the **exact**
derivative, evaluated numerically, for about the cost of one extra pass. It is the engine inside every deep-learning framework.
""")
    c1, c2 = st.columns(2)
    with c1:
        safe_page_link("pages/46Chain Rule — Derivative Through Layers.py", "Refresher: 46 · Chain Rule", icon="📈")
    with c2:
        safe_page_link("pages/70Backpropagation — Chain Rule Backward.py", "Refresher: 70 · Backpropagation", icon="🧠")
    spec, vals, inputs, out, ad, buggy = lab()
    compare(spec, vals, inputs, out, ad, buggy)
    worked_example(inputs, out)
    ai_connection(len(topo_sort(out)))

    st.header("6 · Key takeaways")
    st.success(
        "- A program is a graph of primitive ops; autodiff applies the chain rule to it mechanically and **exactly**.\n"
        "- Reverse mode: one forward pass (save values) + one backward pass in reverse topological order → all ∂out/∂inputs at once.\n"
        "- Forward mode (dual numbers) gives one directional derivative per pass — cheap for few inputs, expensive for many.\n"
        "- A reused variable receives several gradient messages that must be **summed** (accumulated), never overwritten.\n"
        "- Backprop = reverse-mode AD on the loss; its price is memory for the saved activations."
    )
    c1, c2 = st.columns(2)
    with c1:
        safe_page_link("pages/82Jacobian & Hessian.py", "← Previous: 82 · Jacobian & Hessian")
    with c2:
        safe_page_link("pages/84Joint & Marginal Distributions.py", "Next: 84 · Joint & Marginal Distributions →")


main()
