import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(page_title="Dot Product - Geometric View", layout="wide")


def vector_from_polar(magnitude: float, angle_deg: float) -> np.ndarray:
    angle_rad = math.radians(angle_deg)
    return np.array(
        [magnitude * math.cos(angle_rad), magnitude * math.sin(angle_rad)],
        dtype=float,
    )


def build_vector_figure(a: np.ndarray, b: np.ndarray) -> go.Figure:
    dot_value = float(np.dot(a, b))
    b_norm = float(np.linalg.norm(b))
    projection_length = 0.0 if b_norm == 0 else dot_value / b_norm
    projection_vector = np.zeros(2) if b_norm == 0 else (dot_value / (b_norm**2)) * b
    rejection_vector = a - projection_vector

    max_extent = max(np.linalg.norm(a), np.linalg.norm(b), np.linalg.norm(projection_vector), 1.0)
    axis_limit = max(4.0, math.ceil(max_extent * 1.6))

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=[0, a[0]],
            y=[0, a[1]],
            mode="lines+markers",
            name="Vector A",
            line=dict(color="#4F46E5", width=6),
            marker=dict(size=10),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[0, b[0]],
            y=[0, b[1]],
            mode="lines+markers",
            name="Vector B",
            line=dict(color="#F97316", width=6),
            marker=dict(size=10),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[projection_vector[0], a[0]],
            y=[projection_vector[1], a[1]],
            mode="lines",
            name="Missed sideways part",
            line=dict(color="#94A3B8", width=3, dash="dot"),
            hovertemplate="This part is perpendicular to B<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[0, projection_vector[0]],
            y=[0, projection_vector[1]],
            mode="lines+markers",
            name="Shadow of A on B",
            line=dict(color="#10B981", width=7),
            marker=dict(size=10),
        )
    )

    fig.add_annotation(
        x=a[0],
        y=a[1],
        text="A",
        showarrow=False,
        font=dict(size=18, color="#4F46E5"),
        xshift=12,
        yshift=12,
    )
    fig.add_annotation(
        x=b[0],
        y=b[1],
        text="B",
        showarrow=False,
        font=dict(size=18, color="#F97316"),
        xshift=12,
        yshift=12,
    )
    fig.add_annotation(
        x=projection_vector[0],
        y=projection_vector[1],
        text="shadow",
        showarrow=False,
        font=dict(size=15, color="#059669"),
        xshift=8,
        yshift=-16,
    )

    if b_norm > 0:
        unit_b = b / b_norm
        fig.add_annotation(
            x=projection_vector[0] * 0.55,
            y=projection_vector[1] * 0.55,
            text=f"signed shadow length = {projection_length:.2f}",
            showarrow=False,
            bgcolor="rgba(16,185,129,0.12)",
            bordercolor="#10B981",
            font=dict(size=14),
        )
        foot = projection_vector
        rejection_length = float(np.linalg.norm(rejection_vector))
        if rejection_length > 1e-9:
            # Right-angle marker: a small square at the foot of the perpendicular, with one side
            # along B (pointing back toward the origin) and one side along the "missed sideways part".
            size = 0.045 * axis_limit
            along_b = -unit_b if projection_length > 1e-9 else unit_b
            sideways = rejection_vector / rejection_length
            p1 = foot + size * along_b
            p2 = p1 + size * sideways
            p3 = foot + size * sideways
            fig.add_shape(
                type="path",
                path=f"M {p1[0]} {p1[1]} L {p2[0]} {p2[1]} L {p3[0]} {p3[1]}",
                line=dict(color="#64748B", width=2),
            )

    fig.update_layout(
        title="The dot product measures how much of A points along B",
        xaxis=dict(
            range=[-axis_limit, axis_limit],
            zeroline=True,
            showgrid=True,
            scaleanchor="y",
        ),
        yaxis=dict(range=[-axis_limit, axis_limit], zeroline=True, showgrid=True),
        height=620,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        margin=dict(l=10, r=10, t=70, b=10),
    )
    return fig


SIDEWAYS_TOL = 0.01  # |cos(theta)| below this counts as "sideways" (avoids 1e-15 rounding noise at 90 degrees)


def build_agreement_meter(cos_theta: float) -> go.Figure:
    if cos_theta > SIDEWAYS_TOL:
        color, label = "#10B981", "same direction energy"
    elif cos_theta < -SIDEWAYS_TOL:
        color, label = "#EF4444", "opposite direction clash"
    else:
        color, label = "#F59E0B", "perfect sideways"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=cos_theta,
            number={"suffix": "", "font": {"size": 38}},
            title={"text": f"Agreement meter: cos(θ)<br><span style='font-size:0.7em'>{label}</span>"},
            gauge={
                "axis": {"range": [-1, 1]},
                "bar": {"color": color},
                "steps": [
                    {"range": [-1, -SIDEWAYS_TOL], "color": "rgba(239,68,68,0.18)"},
                    {"range": [-SIDEWAYS_TOL, SIDEWAYS_TOL], "color": "rgba(245,158,11,0.18)"},
                    {"range": [SIDEWAYS_TOL, 1], "color": "rgba(16,185,129,0.18)"},
                ],
            },
        )
    )
    fig.update_layout(height=280, margin=dict(l=20, r=20, t=60, b=10))
    return fig


PRESETS = {
    "Best friends": (6.0, 20, 5.0, 20),
    "Sideways strangers": (6.0, 90, 5.0, 0),
    "Pulling opposite ways": (6.0, 180, 5.0, 0),
}
SLIDER_DEFAULTS = {"p06_mag_a": 6.0, "p06_angle_a": 35, "p06_mag_b": 5.0, "p06_angle_b": 0}
for _key, _value in SLIDER_DEFAULTS.items():
    st.session_state.setdefault(_key, _value)


def apply_preset(values) -> None:
    # Presets write into the slider keys so the sliders always show the vectors actually drawn
    for key, value in zip(SLIDER_DEFAULTS, values):
        st.session_state[key] = value


st.title("Dot Product - Geometric View")
st.caption("Two arrows meet. One casts a shadow on the other. That shadow decides the dot product.")

with st.sidebar:
    st.header("Control the arrows")
    st.write("Pretend a flashlight shines perpendicular to vector `B`. The shadow of `A` falling on `B` tells the story.")
    mag_a = st.slider("Length of A", 0.5, 10.0, step=0.1, key="p06_mag_a")
    angle_a = st.slider("Angle of A (degrees)", -180, 180, key="p06_angle_a")
    mag_b = st.slider("Length of B", 0.5, 10.0, step=0.1, key="p06_mag_b")
    angle_b = st.slider("Angle of B (degrees)", -180, 180, key="p06_angle_b")

    st.markdown("### Quick presets")
    st.caption("Jump to a classic case (the sliders above move with it):")
    for preset_name, preset_values in PRESETS.items():
        st.button(preset_name, key=f"p06_preset_{preset_name}", on_click=apply_preset, args=(preset_values,),
                  width="stretch")
    st.button("Reset to start", key="p06_preset_reset", on_click=apply_preset,
              args=(tuple(SLIDER_DEFAULTS.values()),), width="stretch")

a = vector_from_polar(mag_a, angle_a)
b = vector_from_polar(mag_b, angle_b)

dot_value = float(np.dot(a, b))
norm_a = float(np.linalg.norm(a))
norm_b = float(np.linalg.norm(b))
cos_theta = 0.0 if norm_a == 0 or norm_b == 0 else dot_value / (norm_a * norm_b)
cos_theta = float(np.clip(cos_theta, -1.0, 1.0))
theta_deg = float(np.degrees(np.arccos(cos_theta)))
shadow_length = 0.0 if norm_b == 0 else dot_value / norm_b

col1, col2 = st.columns([1.7, 1])

with col1:
    st.plotly_chart(build_vector_figure(a, b), width="stretch")

with col2:
    st.plotly_chart(build_agreement_meter(cos_theta), width="stretch")

    st.metric("Dot product", f"{dot_value:.2f}")
    st.metric("Angle between A and B", f"{theta_deg:.1f}°")
    st.metric("Signed shadow length of A on B", f"{shadow_length:.2f}",
              help="The scalar projection A·B / |B|. It is negative when the shadow points against B.")

    if cos_theta > SIDEWAYS_TOL:
        st.success("Positive dot product: A and B are mostly pointing together.")
    elif cos_theta < -SIDEWAYS_TOL:
        st.error("Negative dot product: A and B push in opposite directions.")
    else:
        st.warning("Near zero dot product: A is almost perfectly sideways to B.")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Shadow story", "Formula bridge", "Tiny AI connection"])

with tab1:
    st.subheader("Geometric intuition")
    st.write(
        """
        Imagine sliding vector `A` onto the direction of `B`.
        The part that lands on `B` is the **projection** or **shadow**.
        """
    )

    c1, c2, c3 = st.columns(3)
    c1.markdown("**If the shadow points with B**  \nDot product is **positive**.")
    c2.markdown("**If the shadow disappears**  \nDot product is **zero**.")
    c3.markdown("**If the shadow points against B**  \nDot product is **negative**.")

    st.info(
        "The dot product is not just about length. It is about length multiplied by agreement in direction."
    )

with tab2:
    st.subheader("From picture to formula")
    st.latex(r"\mathbf{A}\cdot\mathbf{B}=|\mathbf{A}|\,|\mathbf{B}|\,\cos(\theta)")
    st.write(
        "This formula says: big arrows make the score bigger, but the angle decides whether they cooperate, ignore each other, or fight."
    )

    st.code(
        "\n".join(
            [
                f"|A| = {norm_a:.2f}",
                f"|B| = {norm_b:.2f}",
                f"theta = {theta_deg:.2f} degrees",
                f"cos(theta) = {cos_theta:.3f}",
                f"dot = |A| x |B| x cos(theta) = {dot_value:.2f}",
            ]
        ),
        language="text",
    )

with tab3:
    st.subheader("Why this matters in AI")
    st.write(
        """
        Later, when data becomes vectors, the dot product acts like an **agreement detector**.
        A neuron uses it to ask:

        "How much does this input line up with what I am looking for?"
        """
    )

    example_features = ["brightness", "curve-ness", "vertical edge", "loop shape"]
    example_weights = [0.9, 0.1, -0.7, 0.8]
    example_input = [0.8, 0.2, 0.1, 0.9]
    ai_dot = sum(w * x for w, x in zip(example_weights, example_input))

    st.write("A pretend neuron pattern:")
    st.code(
        "\n".join(
            [
                f"{name:>14}: weight={w:>4}, input={x:>4}, contribution={w * x:>5.2f}"
                for name, w, x in zip(example_features, example_weights, example_input)
            ]
            + [f"\nfinal dot product score = {ai_dot:.2f}"]
        ),
        language="text",
    )

st.markdown("---")
st.subheader("One-line takeaway")
st.markdown(
    """
    **Dot product = "How much does one arrow go in the direction of another?"**

    If you can understand the shadow, you can understand the geometry.
    """
)