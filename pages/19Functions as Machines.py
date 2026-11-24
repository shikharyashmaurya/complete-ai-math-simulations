import html

import numpy as np
import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402

st.set_page_config(page_title="Functions as Machines", layout="wide")

def preset_catalog():
    return [
        {
            "title": "Double, then add one",
            "tagline": "Two simple moves, one new rule.",
            "f_tex": r"f(x) = 2x",
            "g_tex": r"g(z) = z + 1",
            "compose_tex": r"(g \circ f)(x) = 2x + 1",
            "f": lambda x: 2.0 * x,
            "g": lambda z: z + 1.0,
            "f_name": "Multiply by 2",
            "g_name": "Add 1"
        },
        {
            "title": "Square, then gentle shrink",
            "tagline": "The first machine bends the input (x²) — the second machine still just sees a plain number.",
            "f_tex": r"f(x) = x^2",
            "g_tex": r"g(z) = 0.12\,z",
            "compose_tex": r"(g \circ f)(x) = 0.12\,x^2",
            "f": lambda x: float(x) ** 2,
            "g": lambda z: 0.12 * z,
            "f_name": "Square it",
            "g_name": "Multiply by 0.12"
        },
        {
            "title": "Sinusoidal Wave",
            "tagline": "A wavy function into an absolute value trap.",
            "f_tex": r"f(x) = 3\sin(x)",
            "g_tex": r"g(z) = |z|",
            "compose_tex": r"(g \circ f)(x) = |3\sin(x)|",
            "f": lambda x: 3.0 * np.sin(x),
            "g": lambda z: abs(float(z)),
            "f_name": "3 * sin(x)",
            "g_name": "Absolute value"
        },
        {
            "title": "Flip sign, then absolute value",
            "tagline": "Watch negatives get caught by the second gate.",
            "f_tex": r"f(x) = -x",
            "g_tex": r"g(z) = |z|",
            "compose_tex": r"(g \circ f)(x) = |-x| = |x|",
            "f": lambda x: -float(x),
            "g": lambda z: abs(float(z)),
            "f_name": "Flip sign (-)",
            "g_name": "Absolute value"
        },
    ]

def fmt_affine(slope, intercept, var):
    """'0.80x - 1.50' instead of '0.80x + -1.50'."""
    sign = "-" if intercept < 0 else "+"
    return f"{slope:.2f}{var} {sign} {abs(intercept):.2f}"


def render_conveyor_belt(x_val, mid_val, out_val, f_name, g_name):
    f_name = html.escape(f_name)
    g_name = html.escape(g_name)
    html_code = load_lab("p19_conveyor_belt", x_val=f"{x_val:.2f}", mid_val=f"{mid_val:.2f}", out_val=f"{out_val:.2f}", f_name=f_name, g_name=g_name)
    st.iframe(html_code, height=350)

def draw_interactive_compose_curve(f_call, g_call, xmin, xmax):
    xs = np.linspace(xmin, xmax, 400)
    ys_f = np.array([f_call(float(x)) for x in xs])
    ys_g_f = np.array([g_call(y) for y in ys_f])
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=xs, y=ys_f,
        mode='lines',
        name='f(x) (middle value)',
        line=dict(color='#fb923c', width=2, dash='dash'),
        hovertemplate='f(x): %{y:.2f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=xs, y=ys_g_f,
        mode='lines',
        name='g(f(x))',
        line=dict(color='#fde68a', width=4),
        hovertemplate='g(f(x)): %{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        plot_bgcolor='#0f172a',
        paper_bgcolor='#0b1020',
        font=dict(color='#e2e8f0'),
        title='Graph of the Composed Machine: h(x) = g(f(x))',
        xaxis=dict(title='Input x', gridcolor='#334155', zerolinecolor='#64748b', zerolinewidth=2),
        yaxis=dict(title='Output h(x)', gridcolor='#334155', zerolinecolor='#64748b', zerolinewidth=2),
        hovermode='x unified',
        margin=dict(l=20, r=20, t=50, b=20),
        height=350,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    return fig

def render_intro():
    st.title("🏭 Page 19: Functions as Machines")
    st.markdown(
        """
        A **function** is the least dramatic superhero: it takes **one input**, follows **one rule**, and hands you **exactly one output**.
        
        In AI, you will stack thousands of these "machines." Before any of that feels fair, make peace with the cartoon version:
        
        > **Input → Black Box → Output.**  
        > **Compose** two boxes by letting the **output of the first** become the **input of the second**.
        
        That glued story is written **g ∘ f** (say "g after f"): first apply **f**, then apply **g**.
        """
    )

def main():
    render_intro()

    st.sidebar.header("Machine Shop")
    st.sidebar.markdown(
        """
        **Try this**
        - Change **x** and watch the factory process it live.
        - Switch recipes — notice how **g ∘ f** creates an entirely new shape.
        - Open **DIY affine** to build your own straight-line machines.
        """
    )

    tab_play, tab_diy = st.tabs(["Assembly Line (Presets)", "DIY: Two Affine Machines"])

    with tab_play:
        st.subheader("1) The Conveyor Belt")
        
        catalog = preset_catalog()
        choice = st.radio(
            "Pick a factory setting",
            list(range(len(catalog))),
            format_func=lambda i: catalog[i]["title"],
            horizontal=True,
            key="p19_preset",
        )
        row = catalog[choice]
        st.caption(row["tagline"])
        
        x = st.slider("Drop a number onto the belt (x)", -4.0, 4.0, 1.25, 0.05, key="p19_x_play")
        
        mid = row["f"](x)
        out = row["g"](mid)
        
        render_conveyor_belt(x, mid, out, row["f_name"], row["g_name"])
        
        st.markdown("### The Blueprint (Math)")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("**First Machine (f)**")
            st.latex(row["f_tex"])
        with col2:
            st.success("**Second Machine (g)**")
            st.latex(row["g_tex"])
        with col3:
            st.warning("**The Full Assembly (g ∘ f)**")
            st.latex(row["compose_tex"])

        st.markdown("### Shape of the Final Machine")
        st.caption("Dashed orange = the middle value f(x); solid yellow = the final output g(f(x)).")
        fig_curve = draw_interactive_compose_curve(row["f"], row["g"], -4.0, 4.0)
        st.plotly_chart(fig_curve, width="stretch")

    with tab_diy:
        st.subheader("2) Build Your Own Affine Machines")
        st.markdown(
            """
            Build **f(x) = a x + b** and **g(z) = c z + d**.  
            The composition is still affine — that is a *nice* special case:

            > **g(f(x)) = c·(a·x + b) + d = (c·a) x + (c·b + d)**  
            One straight-line machine hiding two boxes.
            """
        )
        
        cA, cB, cC, cD = st.columns(4)
        with cA:
            a_f = st.slider("a (slope of f)", -3.0, 3.0, 0.8, 0.05, key="p19_af")
        with cB:
            b_f = st.slider("b (shift of f)", -4.0, 4.0, 1.5, 0.05, key="p19_bf")
        with cC:
            c_g = st.slider("c (slope of g)", -3.0, 3.0, 2.0, 0.05, key="p19_cg")
        with cD:
            d_g = st.slider("d (shift of g)", -4.0, 4.0, -0.5, 0.05, key="p19_dg")

        f_call = lambda x: a_f * float(x) + b_f
        g_call = lambda z: c_g * float(z) + d_g

        x2 = st.slider("Test input x", -5.0, 5.0, 0.75, 0.05, key="p19_x_diy")
        mid2 = f_call(x2)
        out2 = g_call(mid2)
        
        f_name_diy = fmt_affine(a_f, b_f, "x")
        g_name_diy = fmt_affine(c_g, d_g, "z")
        
        render_conveyor_belt(x2, mid2, out2, f_name_diy, g_name_diy)

        coef_x = c_g * a_f
        const_part = c_g * b_f + d_g

        st.success(
            f"**Composed slope**: {coef_x:.4f} &nbsp;&nbsp;|&nbsp;&nbsp; "
            f"**Composed intercept**: {const_part:.4f} \n\n"
            f"**Mega-Machine**: g(f(x)) = {fmt_affine(coef_x, const_part, '·x')}"
        )

        fig_curve2 = draw_interactive_compose_curve(f_call, g_call, -5.0, 5.0)
        st.plotly_chart(fig_curve2, width="stretch")

    st.divider()
    st.markdown(
        """
        ### Recap
        - Treat a function as a **reliable vending machine**: same snack every time you press the same button.
        - **Composition** is **wiring machines in series** — the algebra is whatever falls out when you substitute.
        - **Order is part of the definition** of **g ∘ f**: always **f first**, then **g** (unless someone explicitly writes the opposite).

        Next stops in your curriculum: **linear machines** `y = wx + b`, then **non-linearity** — where the black boxes start bending space for real.
        """
    )

if __name__ == "__main__":
    main()
