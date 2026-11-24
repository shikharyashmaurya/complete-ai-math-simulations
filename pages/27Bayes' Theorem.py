import math
import random

import streamlit as st

st.set_page_config(page_title="Bayes' Theorem", layout="wide")

def local_css():
    st.markdown("""
    <style>
    /* One <i> per person. Classes: s/h = sick/healthy, p/n = tested positive/negative.
       The timeline step is a class on the grid, so each dot needs only two letters of markup. */
    .bt-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 2px;
        margin-bottom: 20px;
        justify-content: center;
        background: #0f172a;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #334155;
        box-shadow: inset 0 4px 20px rgba(0,0,0,0.5);
        max-width: 1000px;
        margin-left: auto;
        margin-right: auto;
    }
    .bt-grid i {
        display: block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #3b82f6;
    }
    .bt-grid i.sp, .bt-grid i.sn { background: #ef4444; }
    .bt-grid.step-2 i.hp, .bt-grid.step-2 i.sp,
    .bt-grid.step-3 i.hp, .bt-grid.step-3 i.sp {
        box-shadow: 0 0 0 1.5px #fbbf24, 0 0 5px 1px rgba(251, 191, 36, 0.8);
        position: relative;
        z-index: 1;
    }
    .bt-grid.step-2 i.hn, .bt-grid.step-2 i.sn { opacity: 0.45; }
    .bt-grid.step-3 i.hn, .bt-grid.step-3 i.sn { opacity: 0.06; filter: grayscale(100%); }
    .bt-grid.step-3 i.hp, .bt-grid.step-3 i.sp { transform: scale(1.35); }
    .bt-legend { text-align: center; color: #94a3b8; font-size: 0.9rem; margin-top: -10px; margin-bottom: 16px; }
    .metric-box {
        background: #1e293b;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border-top: 4px solid #334155;
        height: 100%;
    }
    .border-blue { border-top-color: #3b82f6; }
    .border-red { border-top-color: #ef4444; }
    .border-yellow { border-top-color: #fbbf24; }
    .border-green { border-top-color: #10b981; }
   
    .metric-val {
        font-size: 36px;
        font-weight: 800;
        color: #f8fafc;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 15px;
        color: #94a3b8;
        margin-top: 8px;
        font-weight: 500;
    }
    .narrative-box {
        background: #1e293b;
        color: #f8fafc;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #10b981;
        margin-bottom: 20px;
        font-size: 1.1rem;
    }
    .narrative-box h3 {
        color: #ffffff !important;
        margin-top: 0;
    }
    </style>
    """, unsafe_allow_html=True)


def render_intro():
    st.title("Page 27: Bayes' Theorem")
    st.markdown(
        """
        <div class="narrative-box">
        <h3>The Medical Test Paradox 🏥</h3>
        You go to the doctor for a routine checkup and take a test for a rare disease. <br><br>
        The doctor explains the test's <b>sensitivity</b> (how often it detects people who have the disease)
        and its <b>false positive rate</b> (how often it wrongly flags healthy people).<br>
        A few days later, the doctor calls: <b>You tested POSITIVE.</b><br><br>
        Panic sets in. But wait... what are the <i>actual</i> chances you have the disease?
        The answer is completely unintuitive until you visualize it. Welcome to <b>Bayes' Theorem</b>.
        </div>
        """, unsafe_allow_html=True
    )

def main():
    local_css()
    render_intro()

    st.sidebar.header("⚙️ Disease & Test Parameters")
   
    prevalence_pct = st.sidebar.slider(
        "🦠 Disease Prevalence (Prior)",
        min_value=0.1, max_value=25.0, value=2.0, step=0.1,
        help="What percentage of the total population actually has the disease?",
        key="p27_prevalence",
    )
   
    sensitivity_pct = st.sidebar.slider(
        "✅ True Positive Rate (Sensitivity)",
        min_value=50.0, max_value=100.0, value=90.0, step=1.0,
        help="If someone HAS the disease, what is the chance the test is POSITIVE?",
        key="p27_sensitivity",
    )
   
    fpr_pct = st.sidebar.slider(
        "❌ False Positive Rate",
        min_value=0.5, max_value=25.0, value=9.0, step=0.5,
        help="If someone is HEALTHY, what is the chance the test is incorrectly POSITIVE? (Specificity = 100% − this.)",
        key="p27_fpr",
    )
   
    population_size = 10000

    prior = prevalence_pct / 100
    sensitivity = sensitivity_pct / 100
    fpr = fpr_pct / 100

    # Exact Bayes. The slider minimums guarantee P(Positive) >= 0.5% * 75% > 0.
    p_positive = sensitivity * prior + fpr * (1 - prior)
    posterior_prob = sensitivity * prior / p_positive * 100

    # Whole-person counts are only used for the picture and the "natural frequency" view.
    def round_half_up(x):
        return math.floor(x + 0.5 + 1e-9)

    total_sick = round_half_up(prior * population_size)
    total_healthy = population_size - total_sick
   
    true_positives = round_half_up(sensitivity * total_sick)
    false_negatives = total_sick - true_positives
   
    false_positives = round_half_up(fpr * total_healthy)
    true_negatives = total_healthy - false_positives
   
    total_positives = true_positives + false_positives
    count_posterior = true_positives / total_positives * 100

    # Shuffle with a fixed seed so switching timeline steps doesn't reshuffle the crowd.
    population = ["sp"] * true_positives + ["sn"] * false_negatives + ["hp"] * false_positives + ["hn"] * true_negatives
    random.Random(42).shuffle(population)

    st.markdown("---")
    step = st.radio(
        "**Timeline:**",
        [
            "1️⃣ The Population (Prior)",
            "2️⃣ Administering the Test (Evidence)",
            "3️⃣ The Results (Posterior)"
        ],
        horizontal=True,
        key="p27_step",
    )
    st.markdown("---")

    step_class = "step-" + step[0]
    st.html(
        f'<div class="bt-grid {step_class}">'
        + "".join(f'<i class="{code}"></i>' for code in population)
        + "</div>"
    )
    st.markdown(
        "<div class='bt-legend'>Each dot is one of 10,000 people · "
        "<span style='color:#3b82f6'>●</span> healthy · <span style='color:#ef4444'>●</span> sick · "
        "<span style='color:#fbbf24'>◯</span> ring = tested positive</div>",
        unsafe_allow_html=True,
    )

    # Render Explanations and Metrics
    if step.startswith("1️⃣"):
        st.markdown("### Phase 1: The Population")
        st.markdown(f"We have a population of **{population_size:,}** people. Most are healthy (<span style='color:#3b82f6; font-weight:bold;'>blue</span>), but a small fraction are actually sick (<span style='color:#ef4444; font-weight:bold;'>red</span>).", unsafe_allow_html=True)
        st.markdown("This initial belief is our **Prior**. Before any tests are done, the chance of a random person being sick is just the prevalence rate.")
       
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"<div class='metric-box'><div class='metric-val'>{population_size}</div><div class='metric-label'>Total Population</div></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='metric-box border-blue'><div class='metric-val'>{total_healthy}</div><div class='metric-label'>Healthy People</div></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='metric-box border-red'><div class='metric-val'>{total_sick}</div><div class='metric-label'>Sick People (Prior: {prevalence_pct:.1f}%)</div></div>", unsafe_allow_html=True)

    elif step.startswith("2️⃣"):
        st.markdown("### Phase 2: Administering the Test")
        st.markdown("Everyone takes the medical test. People with a <span style='color:#fbbf24; font-weight:bold;'>glowing yellow ring</span> tested **POSITIVE**.", unsafe_allow_html=True)
        st.markdown("Notice something strange? Because the healthy population is *so much larger* than the sick population, even a small **False Positive Rate** creates a massive amount of false alarms!")
       
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"<div class='metric-box border-red'><div class='metric-val'>{true_positives}</div><div class='metric-label'>True Positives<br>(Sick & Tested +)</div></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='metric-box border-blue'><div class='metric-val'>{false_positives}</div><div class='metric-label'>False Positives<br>(Healthy but Tested +)</div></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='metric-box border-yellow'><div class='metric-val'>{total_positives}</div><div class='metric-label'>Total Positive Tests</div></div>", unsafe_allow_html=True)

    elif step.startswith("3️⃣"):
        st.markdown("### Phase 3: The Result (Posterior)")
        st.markdown("You tested positive. This means you are one of the glowing yellow dots. We can ignore everyone who tested negative (they fade away).")
        st.markdown("The crucial question: **Out of all the people who tested positive, how many are actually sick?**")
       
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"<div class='metric-box border-yellow'><div class='metric-val'>{total_positives}</div><div class='metric-label'>New Sample Space<br>(All Positives)</div></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='metric-box border-red'><div class='metric-val'>{true_positives}</div><div class='metric-label'>Actually Sick<br>(True Positives)</div></div>", unsafe_allow_html=True)
       
        result_color = "#10b981" if posterior_prob < 50 else "#ef4444"
        result_bg = "rgba(16, 185, 129, 0.1)" if posterior_prob < 50 else "rgba(239, 68, 68, 0.1)"
        col3.markdown(f"<div class='metric-box' style='border-top-color: {result_color}; background: {result_bg};'><div class='metric-val' style='color:{result_color};'>{posterior_prob:.1f}%</div><div class='metric-label'>Chance you are sick<br>P(Sick | Positive)</div></div>", unsafe_allow_html=True)
        if abs(count_posterior - posterior_prob) >= 0.05:
            st.caption(
                f"Counting whole people gives {true_positives} / {total_positives} ≈ {count_posterior:.1f}%; "
                f"the exact Bayes value is {posterior_prob:.1f}% (the gap is just rounding people to integers)."
            )
       
        if posterior_prob < 50:
            st.success(f"**The Paradox:** Even though the test detects {sensitivity_pct:.0f}% of people who are sick, you only have a {posterior_prob:.1f}% chance of being sick! Why? Because false positives outnumber true positives.")
        else:
            expected_tp = sensitivity * prior * population_size
            expected_fp = fpr * (1 - prior) * population_size
            st.warning(
                f"You have a {posterior_prob:.1f}% chance of being sick. Out of {population_size:,} people we expect about "
                f"{expected_tp:,.0f} true positives but only about {expected_fp:,.0f} false positives: the sick group "
                f"({prevalence_pct:.1f}% of people, {sensitivity_pct:.0f}% detected) produces at least as many positives as the "
                f"healthy majority does at a {fpr_pct:.1f}% false positive rate. It is the *balance* of prevalence and false "
                "positive rate — not prevalence alone — that makes a positive result trustworthy."
            )

    st.divider()
    st.header("The Math Behind the Magic")
    st.markdown(r"""
    This visual intuition is formalized by **Bayes' Theorem**. It tells us how to update our beliefs when we get new evidence.
   
    $$
    P(A \mid B) = \frac{P(B \mid A) \times P(A)}{P(B)}
    $$
   
    In the context of our medical test:
    - **$P(\text{Sick})$** = Prior probability (Prevalence)
    - **$P(\text{Positive} \mid \text{Sick})$** = True Positive Rate (Sensitivity)
    - **$P(\text{Positive} \mid \text{Healthy})$** = False Positive Rate (= 1 − Specificity)
    - **$P(\text{Positive})$** = Total probability of testing positive, from the *law of total probability*:
   
    $$
    P(\text{Positive}) = P(\text{Positive} \mid \text{Sick})\,P(\text{Sick}) + P(\text{Positive} \mid \text{Healthy})\,P(\text{Healthy})
    $$
   
    Substituting our specific scenario:
   
    $$
    P(\text{Sick} \mid \text{Positive}) = \frac{P(\text{Positive} \mid \text{Sick}) \times P(\text{Sick})}{P(\text{Positive} \mid \text{Sick})\,P(\text{Sick}) + P(\text{Positive} \mid \text{Healthy})\,P(\text{Healthy})}
    $$
    """)
   
    st.latex(
        rf"P(\text{{Sick}} \mid \text{{Positive}}) = \frac{{{sensitivity:.2f} \times {prior:.3f}}}"
        rf"{{{sensitivity:.2f} \times {prior:.3f} + {fpr:.3f} \times {1 - prior:.3f}}} \approx {posterior_prob:.1f}\%"
    )
    st.caption(
        f"Same answer with natural frequencies: of {population_size:,} people, about {true_positives} true positives and "
        f"{false_positives} false positives → {true_positives} / {total_positives} ≈ {count_posterior:.1f}%."
    )
   
    st.info("💡 **Takeaway:** When evaluating a test for a rare condition, the **Base Rate** (Prevalence) is incredibly important. Ignoring it is a common cognitive bias known as the *Base Rate Fallacy*.")

if __name__ == "__main__":
    main()
