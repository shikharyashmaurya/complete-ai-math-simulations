import streamlit as st
import random

st.set_page_config(page_title="Bayes' Theorem", layout="wide")

def local_css():
    st.markdown("""
    <style>
    .population-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 20px;
        justify-content: center;
        background: #0f172a;
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #334155;
        box-shadow: inset 0 4px 20px rgba(0,0,0,0.5);
        max-width: 1000px;
        margin-left: auto;
        margin-right: auto;
    }
    .person {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    .sick {
        background: linear-gradient(135deg, #f87171, #ef4444, #dc2626);
        box-shadow: 0 2px 5px rgba(239, 68, 68, 0.4);
    }
    .healthy {
        background: linear-gradient(135deg, #60a5fa, #3b82f6, #2563eb);
        box-shadow: 0 2px 5px rgba(59, 130, 246, 0.4);
    }
    .test-pos {
        box-shadow: 0 0 0 3px #fbbf24, 0 0 12px 4px rgba(251, 191, 36, 0.8) !important;
        transform: scale(1.3);
        z-index: 10;
        border: 1px solid #fff;
    }
    .test-neg {
        opacity: 0.4;
        transform: scale(0.8);
    }
    .dimmed {
        opacity: 0.05 !important;
        filter: grayscale(100%);
        transform: scale(0.4);
        box-shadow: none !important;
        border: none !important;
    }
    .highlight {
        transform: scale(1.5);
        z-index: 20;
    }
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
        The doctor explains the test's <b>sensitivity</b>: how often it detects people who have the disease.<br>
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
        help="What percentage of the total population actually has the disease?"
    )
   
    sensitivity_pct = st.sidebar.slider(
        "✅ True Positive Rate (Sensitivity)",
        min_value=50.0, max_value=100.0, value=90.0, step=1.0,
        help="If someone HAS the disease, what is the chance the test is POSITIVE?"
    )
   
    fpr_pct = st.sidebar.slider(
        "❌ False Positive Rate",
        min_value=0.5, max_value=25.0, value=9.0, step=0.5,
        help="If someone is HEALTHY, what is the chance the test is incorrectly POSITIVE?"
    )
   
    population_size = 10000

    # Round expected counts to whole people for the population visualization.
    total_sick = round((prevalence_pct / 100) * population_size)
    total_healthy = population_size - total_sick
   
    true_positives = round((sensitivity_pct / 100) * total_sick)
    false_negatives = total_sick - true_positives
   
    false_positives = round((fpr_pct / 100) * total_healthy)
    true_negatives = total_healthy - false_positives
   
    total_positives = true_positives + false_positives
   
    if total_positives > 0:
        posterior_prob = (true_positives / total_positives) * 100
    else:
        posterior_prob = 0.0

    # Generate population array deterministically based on parameters so it doesn't flicker wildly
    population = []
    # Sick people
    for i in range(true_positives):
        population.append({"status": "sick", "test": "pos"})
    for i in range(false_negatives):
        population.append({"status": "sick", "test": "neg"})
    # Healthy people
    for i in range(false_positives):
        population.append({"status": "healthy", "test": "pos"})
    for i in range(true_negatives):
        population.append({"status": "healthy", "test": "neg"})
       
    # Shuffle predictably
    random.Random(42).shuffle(population)

    st.markdown("---")
    step = st.radio(
        "**Timeline:**",
        [
            "1️⃣ The Population (Prior)",
            "2️⃣ Administering the Test (Evidence)",
            "3️⃣ The Results (Posterior)"
        ],
        horizontal=True
    )
    st.markdown("---")

    # Render Visual Grid
    html_parts = ['<div class="population-grid">']
    for person in population:
        status = person["status"]
        test = person["test"]
       
        state_class = f"{status}"
       
        if step.startswith("2️⃣"):
            if test == "pos":
                state_class += " test-pos"
            else:
                state_class += " test-neg"
        elif step.startswith("3️⃣"):
            if test == "pos":
                state_class += " test-pos highlight"
            else:
                state_class += " test-neg dimmed"
               
        html_parts.append(f'<div class="person {state_class}"></div>')
    html_parts.append('</div>')

    st.markdown("".join(html_parts), unsafe_allow_html=True)

    # Render Explanations and Metrics
    if step.startswith("1️⃣"):
        st.markdown("### Phase 1: The Population")
        st.markdown(f"We have a population of **{population_size}** people. Most are healthy (<span style='color:#3b82f6; font-weight:bold;'>blue</span>), but a small fraction are actually sick (<span style='color:#ef4444; font-weight:bold;'>red</span>).", unsafe_allow_html=True)
        st.markdown("This initial belief is our **Prior**. Before any tests are done, the chance of a random person being sick is just the prevalence rate.")
       
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"<div class='metric-box'><div class='metric-val'>{population_size}</div><div class='metric-label'>Total Population</div></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='metric-box border-blue'><div class='metric-val'>{total_healthy}</div><div class='metric-label'>Healthy People</div></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='metric-box border-red'><div class='metric-val'>{total_sick}</div><div class='metric-label'>Sick People (Prior: {prevalence_pct:.1f}%)</div></div>", unsafe_allow_html=True)

    elif step.startswith("2️⃣"):
        st.markdown("### Phase 2: Administering the Test")
        st.markdown("Everyone takes the medical test. People with a <span style='color:#fbbf24; font-weight:bold;'>glowing yellow aura</span> tested **POSITIVE**.", unsafe_allow_html=True)
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
        col3.markdown(f"<div class='metric-box' style='border-top-color: {result_color}; background: rgba(16, 185, 129, 0.1);'><div class='metric-val' style='color:{result_color};'>{posterior_prob:.1f}%</div><div class='metric-label'>Chance you are sick<br>P(Sick | Positive)</div></div>", unsafe_allow_html=True)
       
        if posterior_prob < 50:
            st.success(f"**The Paradox:** Even though the test detects {sensitivity_pct}% of people who are sick, you only have a {posterior_prob:.1f}% chance of being sick! Why? Because false positives outnumber true positives.")
        else:
            st.warning(f"You have a {posterior_prob:.1f}% chance of being sick. The high prevalence makes the positive result much more likely to be true.")

    st.divider()
    st.header("The Math Behind the Magic")
    st.markdown("""
    This visual intuition is formalized by **Bayes' Theorem**. It tells us how to update our beliefs when we get new evidence.
   
    $$
    P(A | B) = \\frac{P(B | A) \\times P(A)}{P(B)}
    $$
   
    In the context of our medical test:
    - **$P(\\text{Sick})$** = Prior probability (Prevalence)
    - **$P(\\text{Positive} | \\text{Sick})$** = True Positive Rate (Sensitivity)
    - **$P(\\text{Positive})$** = Total probability of testing positive (True Positives + False Positives)
   
    Substituting our specific scenario:
   
    $$
    P(\\text{Sick} | \\text{Positive}) = \\frac{P(\\text{Positive} | \\text{Sick}) \\times P(\\text{Sick})}{P(\\text{Positive})}
    $$
    """)
   
    if total_positives > 0:
        st.latex(rf"P(\text{{Sick}} | \text{{Positive}}) = \frac{{{true_positives}}}{{{total_positives}}} \approx {posterior_prob:.1f}\%")
   
    st.info("💡 **Takeaway:** When evaluating a test for a rare condition, the **Base Rate** (Prevalence) is incredibly important. Ignoring it is a common cognitive bias known as the *Base Rate Fallacy*.")

if __name__ == "__main__":
    main()
