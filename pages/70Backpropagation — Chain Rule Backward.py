import streamlit as st
import numpy as np
import time

def get_node_style(bg_color, is_highlighted):
    base_style = f"background: {bg_color}; color: white; padding: 20px; border-radius: 50%; width: 80px; height: 80px; display: flex; align-items: center; justify-content: center; font-size: 24px; margin: 0 auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: all 0.3s;"
    if is_highlighted:
        return base_style + " box-shadow: 0 0 20px 5px rgba(255, 75, 75, 0.8); border: 3px solid #ff4b4b; transform: scale(1.15);"
    return base_style

def get_arrow_style(is_highlighted):
    base_style = "text-align: center; font-weight: bold; padding: 0 15px; transition: all 0.3s;"
    if is_highlighted:
        return base_style + " color: #ff4b4b; transform: scale(1.15);"
    return base_style + " color: #7f8c8d;"

st.set_page_config(page_title="Backpropagation - Chain Rule", layout="wide", initial_sidebar_state="expanded")

st.title("🔄 Backpropagation: The Chain Rule Backward")
st.markdown("### How the network finds out who is to blame for the error!")
st.markdown("When a neural network makes a mistake, it needs to figure out which weights caused the error so it can fix them. It does this by passing the error backward through the network using the **Chain Rule** from calculus. This process is called **Backpropagation**.")

st.markdown("---")
st.subheader("🔗 What is the Chain Rule?")
st.markdown("Before we play the movie, let's understand the **Chain Rule**. Imagine a sequence of connected gears. If gear A turns gear B, and gear B turns gear C, how does gear A affect gear C? You just multiply their individual effects!")

# Visual chain rule explanation
st.markdown(r"""
<div style='background-color: #2c3e50; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
    <h4 style='color: #ffffff; margin-bottom: 20px;'>The Chain of Influence</h4>
    <div style='display: flex; justify-content: space-around; align-items: center; font-size: 16px; flex-wrap: wrap; gap: 10px;'>
        <div style='background: #e74c3c; color: white; padding: 15px; border-radius: 10px; flex: 1; min-width: 150px;'>How much <b>ŷ</b> changes <b>L</b><br><span style='font-size: 24px; font-family: serif; font-style: italic;'>∂L / ∂ŷ</span></div>
        <div style='color: white;'><b style='font-size: 30px;'>×</b></div>
        <div style='background: #e67e22; color: white; padding: 15px; border-radius: 10px; flex: 1; min-width: 150px;'>How much <b>h</b> changes <b>ŷ</b><br><span style='font-size: 24px; font-family: serif; font-style: italic;'>∂ŷ / ∂h</span></div>
        <div style='color: white;'><b style='font-size: 30px;'>×</b></div>
        <div style='background: #9b59b6; color: white; padding: 15px; border-radius: 10px; flex: 1; min-width: 150px;'>How much <b>w₁</b> changes <b>h</b><br><span style='font-size: 24px; font-family: serif; font-style: italic;'>∂h / ∂w₁</span></div>
        <div style='color: white;'><b style='font-size: 30px;'>=</b></div>
        <div style='background: #34495e; color: white; padding: 15px; border-radius: 10px; border: 3px solid #ff4b4b; flex: 1; min-width: 150px;'>Total effect of <b>w₁</b> on <b>L</b><br><span style='font-size: 24px; font-family: serif; font-style: italic;'>∂L / ∂w₁</span></div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("This means we don't have to calculate a huge, complicated derivative all at once. We can just chop it into small, easy pieces (local derivatives) and **multiply them together** as we move backwards!")

# Sidebar for inputs
st.sidebar.header("🎛️ Network Controls")
st.sidebar.markdown("Change the inputs and see how the error and gradients change.")
x = st.sidebar.slider("Input (x)", 1.0, 5.0, 2.0, 0.5)
w1 = st.sidebar.slider("Weight 1 (w₁)", 0.1, 3.0, 1.5, 0.1)
w2 = st.sidebar.slider("Weight 2 (w₂)", 0.1, 3.0, 2.0, 0.1)
y_true = st.sidebar.slider("Target Output (y_true)", 1.0, 20.0, 10.0, 1.0)

# Forward Pass calculations
h = w1 * x
y_pred = w2 * h
# Using 1/2 MSE for cleaner derivative: L = 0.5 * (y_pred - y_true)^2
loss = 0.5 * (y_pred - y_true)**2

# Backward Pass calculations
dLoss_dy_pred = y_pred - y_true
dy_pred_dw2 = h
dLoss_dw2 = dLoss_dy_pred * dy_pred_dw2

dy_pred_dh = w2
dLoss_dh = dLoss_dy_pred * dy_pred_dh

dh_dw1 = x
dLoss_dw1 = dLoss_dh * dh_dw1

st.markdown("---")

# Step selector
st.subheader("🎬 Play the Backpropagation Movie")
st.markdown("Scrub through the slider below to watch the gradient flow backward from the Loss to the Inputs.")
step = st.slider("Select Backprop Step:", 0, 3, 0, format="Step %d", help="0: Forward Pass, 1: Error at Output, 2: Blame Hidden Layer, 3: Blame Input Layer")

step_descriptions = [
    "**Step 0: Forward Pass.** Data flows left-to-right. We calculate the hidden state $h$, the prediction $\\hat{y}$, and finally the Loss (error).",
    "**Step 1: Output Gradient.** The journey begins! We calculate the raw error signal: $\\frac{\\partial L}{\\partial \\hat{y}}$. How far off is our prediction?",
    "**Step 2: Blame Hidden & Weight 2.** The error flows backward. Using the Chain Rule, we multiply the upstream error by the local derivatives to find out how much $w_2$ and $h$ contributed to the mistake.",
    "**Step 3: Blame Weight 1.** The error continues to flow to the first layer. Chain Rule again! We find the gradient for $w_1$ by multiplying the error at $h$ by the local derivative of $w_1$."
]
st.info(step_descriptions[step])

# Formatting gradient strings for display
dLoss_dy_pred_str = f"∇ = {dLoss_dy_pred:.2f}" if step >= 1 else ""
dLoss_dw2_str = f"∇w₂ = {dLoss_dw2:.2f}" if step >= 2 else ""
dLoss_dh_str = f"∇h = {dLoss_dh:.2f}" if step >= 2 else ""
dLoss_dw1_str = f"∇w₁ = {dLoss_dw1:.2f}" if step >= 3 else ""

# HTML Visualization
html_code = f"""
<div style="display: flex; align-items: center; justify-content: center; font-family: sans-serif; margin: 50px 0; overflow-x: auto; padding: 20px;">
   
   <!-- Node x -->
   <div style="text-align: center; width: 140px;">
      <div style="{get_node_style('#3498db', False)}">x</div>
      <div style="margin-top: 15px; font-weight: bold;">Input</div>
      <div style="font-size: 18px;">{x:.2f}</div>
   </div>
   
   <!-- Arrow w1 -->
   <div style="{get_arrow_style(step >= 3)}">
      <div style="font-size: 18px;">w₁ = {w1:.2f}</div>
      <div style="font-size: 50px; line-height: 1;">➔</div>
      <div style="color: #ff4b4b; font-size: 18px; min-height: 27px; font-weight: bold;">{dLoss_dw1_str}</div>
   </div>

   <!-- Node h -->
   <div style="text-align: center; width: 140px;">
      <div style="{get_node_style('#9b59b6', step >= 2)}">h</div>
      <div style="margin-top: 15px; font-weight: bold;">Hidden</div>
      <div style="font-size: 18px;">{h:.2f}</div>
      <div style="color: #ff4b4b; font-size: 18px; min-height: 27px; font-weight: bold;">{dLoss_dh_str}</div>
   </div>
   
   <!-- Arrow w2 -->
   <div style="{get_arrow_style(step >= 2)}">
      <div style="font-size: 18px;">w₂ = {w2:.2f}</div>
      <div style="font-size: 50px; line-height: 1;">➔</div>
      <div style="color: #ff4b4b; font-size: 18px; min-height: 27px; font-weight: bold;">{dLoss_dw2_str}</div>
   </div>

   <!-- Node y_pred -->
   <div style="text-align: center; width: 140px;">
      <div style="{get_node_style('#e67e22', step >= 1)}">ŷ</div>
      <div style="margin-top: 15px; font-weight: bold;">Prediction</div>
      <div style="font-size: 18px;">{y_pred:.2f}</div>
      <div style="color: #ff4b4b; font-size: 18px; min-height: 27px; font-weight: bold;">{dLoss_dy_pred_str}</div>
   </div>
   
   <!-- Arrow Loss -->
   <div style="{get_arrow_style(step >= 1)}">
      <div style="font-size: 18px;">Error</div>
      <div style="font-size: 50px; line-height: 1;">➔</div>
      <div style="color: transparent; font-size: 18px; min-height: 27px;">.</div>
   </div>

   <!-- Node Loss -->
   <div style="text-align: center; width: 140px;">
      <div style="{get_node_style('#e74c3c', step >= 1)}">L</div>
      <div style="margin-top: 15px; font-weight: bold;">Loss</div>
      <div style="font-size: 18px;">{loss:.2f}</div>
   </div>
</div>
"""
st.markdown(html_code, unsafe_allow_html=True)

st.markdown("---")

# The Math Unfolded Section
if step >= 1:
    st.markdown("### 📝 The Math Unfolded")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Step 1: Output Gradient**")
        st.markdown("Derivative of Loss (using $\\frac{1}{2} MSE$):")
        st.latex(rf"\frac{{\partial L}}{{\partial \hat{{y}}}} = \hat{{y}} - y_{{true}}")
        st.latex(rf"= {y_pred:.2f} - {y_true:.2f} = \mathbf{{{dLoss_dy_pred:.2f}}}")
        
    if step >= 2:
        with col2:
            st.markdown("**Step 2: Hidden Gradients**")
            st.markdown("Local derivatives:")
            st.latex(rf"\frac{{\partial \hat{{y}}}}{{\partial w_2}} = h = {h:.2f}")
            st.latex(rf"\frac{{\partial \hat{{y}}}}{{\partial h}} = w_2 = {w2:.2f}")
            st.markdown("Chain Rule (Upstream $\\times$ Local):")
            st.latex(rf"\frac{{\partial L}}{{\partial w_2}} = {dLoss_dy_pred:.2f} \times {h:.2f} = \mathbf{{{dLoss_dw2:.2f}}}")
            st.latex(rf"\frac{{\partial L}}{{\partial h}} = {dLoss_dy_pred:.2f} \times {w2:.2f} = \mathbf{{{dLoss_dh:.2f}}}")
            
    if step >= 3:
        with col3:
            st.markdown("**Step 3: Input Gradients**")
            st.markdown("Local derivative:")
            st.latex(rf"\frac{{\partial h}}{{\partial w_1}} = x = {x:.2f}")
            st.markdown("Chain Rule (Upstream $\\times$ Local):")
            st.latex(rf"\frac{{\partial L}}{{\partial w_1}} = \frac{{\partial L}}{{\partial h}} \times \frac{{\partial h}}{{\partial w_1}}")
            st.latex(rf"= {dLoss_dh:.2f} \times {x:.2f} = \mathbf{{{dLoss_dw1:.2f}}}")

if step == 3:
    st.markdown("---")
    st.markdown("### 🎯 What does this mean for Learning?")
    direction_w1 = "decrease" if dLoss_dw1 > 0 else "increase" if dLoss_dw1 < 0 else "not change"
    direction_w2 = "decrease" if dLoss_dw2 > 0 else "increase" if dLoss_dw2 < 0 else "not change"
    
    if dLoss_dw1 == 0 and dLoss_dw2 == 0:
        st.success("**Perfect!** The gradients are exactly zero. The model's prediction perfectly matches the target, so the loss is 0. No weight updates are needed.")
    else:
        st.success(f"""
        **Conclusion for Optimization:**
        - The gradient of $w_1$ is **{dLoss_dw1:.2f}**. To reduce the loss, we should **{direction_w1}** $w_1$.
        - The gradient of $w_2$ is **{dLoss_dw2:.2f}**. To reduce the loss, we should **{direction_w2}** $w_2$.
        
        By moving the weights in the **opposite** direction of their gradients, Gradient Descent helps the network "learn" and reduce its mistakes!
        """)