import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go

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
            "tagline": "Nonlinear first acts — the second machine still sees a plain number.",
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

def render_conveyor_belt(x_val, mid_val, out_val, f_name, g_name):
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        body {{
            margin: 0;
            padding: 0;
            background-color: transparent;
            font-family: 'Inter', sans-serif;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }}
        .factory-container {{
            position: relative;
            width: 100%;
            max-width: 900px;
            height: 300px;
        }}
        .track {{
            position: absolute;
            top: 50%;
            left: 5%;
            right: 5%;
            height: 6px;
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-50%);
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(255,255,255,0.05);
        }}
        .track-glow {{
            position: absolute;
            top: 50%;
            left: 5%;
            width: 0%;
            height: 6px;
            background: linear-gradient(90deg, #38bdf8, #c084fc, #f472b6);
            transform: translateY(-50%);
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(255,255,255,0.4);
            animation: trackFill 4s ease-in-out forwards;
        }}
        
        @keyframes trackFill {{
            0% {{ width: 0%; }}
            15% {{ width: 30%; }}
            45% {{ width: 30%; }}
            60% {{ width: 70%; }}
            90% {{ width: 90%; }}
            100% {{ width: 90%; }}
        }}

        .machine {{
            position: absolute;
            top: 50%;
            transform: translate(-50%, -50%);
            width: 150px;
            height: 130px;
            background: #111827;
            border: 3px solid;
            border-radius: 15px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 10;
            transition: all 0.2s;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}
        
        .machine.f {{
            left: 35%;
            border-color: #fb923c;
        }}
        
        .machine.g {{
            left: 75%;
            border-color: #4ade80;
        }}
        
        .machine-processing.f {{
            animation: processF 1.2s ease-in-out 0.6s;
        }}
        
        .machine-processing.g {{
            animation: processG 1.2s ease-in-out 2.4s;
        }}
        
        @keyframes processF {{
            0%, 100% {{ transform: translate(-50%, -50%) scale(1); box-shadow: 0 0 0 rgba(251, 146, 60, 0); }}
            50% {{ transform: translate(-50%, -50%) scale(1.1); box-shadow: 0 0 40px rgba(251, 146, 60, 1); border-color: #fff; }}
        }}
        
        @keyframes processG {{
            0%, 100% {{ transform: translate(-50%, -50%) scale(1); box-shadow: 0 0 0 rgba(74, 222, 128, 0); }}
            50% {{ transform: translate(-50%, -50%) scale(1.1); box-shadow: 0 0 40px rgba(74, 222, 128, 1); border-color: #fff; }}
        }}

        .machine-title {{
            font-size: 20px;
            font-weight: 900;
            margin-bottom: 8px;
        }}
        
        .f .machine-title {{ color: #fb923c; }}
        .g .machine-title {{ color: #4ade80; }}
        
        .machine-desc {{
            font-size: 15px;
            color: #94a3b8;
            text-align: center;
            padding: 0 10px;
            font-style: italic;
        }}

        .orb {{
            position: absolute;
            top: 50%;
            left: 5%;
            transform: translate(-50%, -50%);
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: #38bdf8;
            color: #0b1020;
            font-weight: 900;
            font-size: 14px;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 20;
            box-shadow: 0 0 20px #38bdf8;
            animation: moveOrb 4s ease-in-out forwards;
        }}
        
        @keyframes moveOrb {{
            0% {{ left: 5%; background: #38bdf8; box-shadow: 0 0 20px #38bdf8; transform: translate(-50%, -50%) scale(1); }}
            15% {{ left: 35%; background: #38bdf8; box-shadow: 0 0 20px #38bdf8; transform: translate(-50%, -50%) scale(1); opacity: 1;}}
            25% {{ left: 35%; opacity: 0; transform: translate(-50%, -50%) scale(0); }}
            35% {{ left: 35%; opacity: 0; transform: translate(-50%, -50%) scale(0); }}
            45% {{ left: 35%; background: #c084fc; box-shadow: 0 0 20px #c084fc; opacity: 1; transform: translate(-50%, -50%) scale(1); }}
            60% {{ left: 75%; background: #c084fc; box-shadow: 0 0 20px #c084fc; transform: translate(-50%, -50%) scale(1); opacity: 1; }}
            70% {{ left: 75%; opacity: 0; transform: translate(-50%, -50%) scale(0); }}
            80% {{ left: 75%; opacity: 0; transform: translate(-50%, -50%) scale(0); }}
            90% {{ left: 75%; background: #f472b6; box-shadow: 0 0 20px #f472b6; opacity: 1; transform: translate(-50%, -50%) scale(1); }}
            100% {{ left: 95%; background: #f472b6; box-shadow: 0 0 20px #f472b6; opacity: 1; transform: translate(-50%, -50%) scale(1); }}
        }}

        .station-label {{
            position: absolute;
            bottom: 20px;
            transform: translateX(-50%);
            font-weight: bold;
            color: #e2e8f0;
            font-size: 16px;
            text-align: center;
        }}
        .station-label span {{
            display: block;
            font-size: 18px;
            color: #ffffff;
            margin-top: 6px;
            background: rgba(255,255,255,0.1);
            padding: 4px 8px;
            border-radius: 8px;
        }}
        
        .station-label.start {{ left: 5%; color: #38bdf8; }}
        .station-label.mid {{ left: 55%; color: #c084fc; opacity: 0; animation: fadeInMid 4s forwards; }}
        .station-label.end {{ left: 95%; color: #f472b6; opacity: 0; animation: fadeInEnd 4s forwards; }}
        
        @keyframes fadeInMid {{
            0%, 40% {{ opacity: 0; transform: translateX(-50%) translateY(10px); }}
            45%, 100% {{ opacity: 1; transform: translateX(-50%) translateY(0); }}
        }}
        
        @keyframes fadeInEnd {{
            0%, 85% {{ opacity: 0; transform: translateX(-50%) translateY(10px); }}
            90%, 100% {{ opacity: 1; transform: translateX(-50%) translateY(0); }}
        }}

    </style>
    </head>
    <body>
        <div class="factory-container">
            <div class="track"></div>
            <div class="track-glow"></div>
            
            <div class="station-label start">
                INPUT x
                <span>{x_val:.2f}</span>
            </div>
            
            <div class="station-label mid" style="left: 55%;">
                MIDDLE f(x)
                <span>{mid_val:.2f}</span>
            </div>
            
            <div class="station-label end">
                OUTPUT g(f(x))
                <span>{out_val:.2f}</span>
            </div>

            <div class="machine f machine-processing">
                <div class="machine-title">Machine f</div>
                <div class="machine-desc">{f_name}</div>
            </div>
            
            <div class="machine g machine-processing">
                <div class="machine-title">Machine g</div>
                <div class="machine-desc">{g_name}</div>
            </div>
            
            <div class="orb" id="orb">{x_val:.2f}</div>
        </div>
        
        <script>
            const orb = document.getElementById('orb');
            const midVal = '{mid_val:.2f}';
            const outVal = '{out_val:.2f}';
            
            setTimeout(() => {{
                orb.innerText = midVal;
            }}, 1200); 
            
            setTimeout(() => {{
                orb.innerText = outVal;
            }}, 3000); 
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=350)

def draw_interactive_compose_curve(f_call, g_call, xmin, xmax):
    xs = np.linspace(xmin, xmax, 400)
    ys_f = np.array([f_call(float(x)) for x in xs])
    ys_g_f = np.array([g_call(y) for y in ys_f])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=xs, y=ys_g_f,
        mode='lines',
        name='g(f(x))',
        line=dict(color='#fde68a', width=4),
        hovertemplate='Input x: %{x:.2f}<br>Output g(f(x)): %{y:.2f}<extra></extra>'
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
        height=350
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
        )
        row = catalog[choice]
        st.caption(row["tagline"])
        
        x = st.slider("Drop a number onto the belt (x)", -4.0, 4.0, 1.25, 0.05, key="d19_x_play")
        
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
        fig_curve = draw_interactive_compose_curve(row["f"], row["g"], -4.0, 4.0)
        st.plotly_chart(fig_curve, use_container_width=True)

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
            a_f = st.slider("a (slope of f)", -3.0, 3.0, 0.8, 0.05, key="d19_af")
        with cB:
            b_f = st.slider("b (shift of f)", -4.0, 4.0, 1.5, 0.05, key="d19_bf")
        with cC:
            c_g = st.slider("c (slope of g)", -3.0, 3.0, 2.0, 0.05, key="d19_cg")
        with cD:
            d_g = st.slider("d (shift of g)", -4.0, 4.0, -0.5, 0.05, key="d19_dg")

        f_call = lambda x: a_f * float(x) + b_f
        g_call = lambda z: c_g * float(z) + d_g

        x2 = st.slider("Test input x", -5.0, 5.0, 0.75, 0.05, key="d19_x_diy")
        mid2 = f_call(x2)
        out2 = g_call(mid2)
        
        f_name_diy = f"{a_f:.2f}x + {b_f:.2f}"
        g_name_diy = f"{c_g:.2f}z + {d_g:.2f}"
        
        render_conveyor_belt(x2, mid2, out2, f_name_diy, g_name_diy)

        coef_x = c_g * a_f
        const_part = c_g * b_f + d_g

        st.success(
            f"**Composed slope**: {coef_x:.4f} &nbsp;&nbsp;|&nbsp;&nbsp; "
            f"**Composed intercept**: {const_part:.4f} \n\n"
            f"**Mega-Machine**: g(f(x)) = {coef_x:.4f}·x + ({const_part:.4f})"
        )

        fig_curve2 = draw_interactive_compose_curve(f_call, g_call, -5.0, 5.0)
        st.plotly_chart(fig_curve2, use_container_width=True)

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
