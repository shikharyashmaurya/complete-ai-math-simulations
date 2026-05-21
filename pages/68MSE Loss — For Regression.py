import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Set up the page config
st.set_page_config(page_title="MSE Loss — For Regression", layout="wide", initial_sidebar_state="collapsed")

# --- Custom Premium CSS Styling ---
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF0055, #00F0FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #A0A0B0;
        margin-bottom: 2rem;
    }
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(30, 30, 45, 0.8), rgba(15, 15, 20, 0.8));
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.4);
        text-align: center;
    }
    .highlight {
        color: #FF0055;
        font-weight: bold;
    }
    .highlight-blue {
        color: #00F0FF;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<div class="main-title">Page 68: MSE Loss — The Cost of Mistakes</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">How do we measure how "wrong" a model is? By literally drawing squares! 🟦</div>', unsafe_allow_html=True)

st.markdown("""
When a machine learning model makes a prediction, it usually misses the true value by a little bit. 
The gap between the <span class="highlight-blue">True Data</span> and the <span class="highlight">Prediction Line</span> is our **Error**.
To train a model, we need a single number that summarizes all its mistakes. This is the **Loss**.
""", unsafe_allow_html=True)

st.markdown("---")

# Main Interactive Section
col1, col2 = st.columns([1, 2.5])

with col1:
    st.markdown("### 🎛️ Be the Optimizer!")
    st.write("Adjust the line's parameters to minimize the total loss.")
    
    # Sliders for the line equation y = wx + b
    w = st.slider("Slope (w)", 0.0, 2.0, 0.5, 0.1)
    b = st.slider("Intercept (b)", 0.0, 10.0, 2.0, 0.5)
    
    st.markdown("### 📏 Choose the Metric")
    metric = st.radio("How should we measure mistakes?", 
                      ["Mean Squared Error (MSE)", "Mean Absolute Error (MAE)"])
    
    st.markdown("### 🌪️ Data Mode")
    has_outlier = st.checkbox("Add a Rogue Outlier Point")
    
    # Generate Data
    x_data = np.array([1, 2.5, 4, 5.5, 7, 8.5, 10])
    if has_outlier:
        y_true = np.array([3, 4.5, 5.5, 6.5, 8, 9.5, 3]) # Outlier at the end
    else:
        y_true = np.array([3, 4.5, 5.5, 6.5, 8, 9.5, 11]) # Clean linear trend
        
    # Calculate predictions and errors
    y_pred = w * x_data + b
    errors = y_true - y_pred
    
    # Display dynamic metric
    st.markdown("<br>", unsafe_allow_html=True)
    if metric == "Mean Squared Error (MSE)":
        loss = np.mean(errors**2)
        st.metric("Total MSE Loss", f"{loss:.2f}", help="Average AREA of all the purple squares.")
    else:
        loss = np.mean(np.abs(errors))
        st.metric("Total MAE Loss", f"{loss:.2f}", help="Average LENGTH of all the green lines.")
        

with col2:
    def create_squares_plot(x, y, w, b, metric):
        fig = go.Figure()
        
        y_pred = w * x + b
        
        # Draw the visual representation of errors
        for i in range(len(x)):
            xi = x[i]
            yi = y[i]
            y_hat = y_pred[i]
            error = yi - y_hat
            
            if metric == "Mean Squared Error (MSE)":
                # Vertices of the square
                sq_x = [xi, xi, xi + np.abs(error), xi + np.abs(error), xi]
                sq_y = [yi, y_hat, y_hat, yi, yi]
                
                fig.add_trace(go.Scatter(
                    x=sq_x, y=sq_y,
                    mode='lines',
                    fill='toself',
                    fillcolor='rgba(157, 0, 255, 0.25)',
                    line=dict(color='rgba(157, 0, 255, 0.8)', width=1.5),
                    showlegend=False,
                    hoverinfo='skip'
                ))
                # Add text label for the area of the square
                if np.abs(error) > 0.5:
                    fig.add_annotation(
                        x=xi + np.abs(error)/2, y=(yi + y_hat)/2,
                        text=f"{error**2:.1f}", showarrow=False,
                        font=dict(color="rgba(255,255,255,0.8)", size=10)
                    )
            else:
                # For MAE, we just draw a vertical line representing distance
                fig.add_trace(go.Scatter(
                    x=[xi, xi], y=[yi, y_hat],
                    mode='lines',
                    line=dict(color='#00FF66', width=3, dash='dot'),
                    showlegend=False,
                    hoverinfo='skip'
                ))
                # Add text label for the length of the line
                if np.abs(error) > 0.5:
                    fig.add_annotation(
                        x=xi + 0.3, y=(yi + y_hat)/2,
                        text=f"{np.abs(error):.1f}", showarrow=False,
                        font=dict(color="#00FF66", size=10)
                    )

        # Draw the prediction line
        line_x = np.array([0, 15])
        line_y = w * line_x + b
        
        fig.add_trace(go.Scatter(
            x=line_x, y=line_y,
            mode='lines', name='Prediction (y = wx + b)',
            line=dict(color='#FF0055', width=3)
        ))
        
        # Draw the true data points on top
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='markers', name='True Data',
            marker=dict(color='#00F0FF', size=12, line=dict(color='white', width=1))
        ))
        
        fig.update_layout(
            xaxis=dict(range=[0, 15], title="X", showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False),
            yaxis=dict(
                range=[0, 15], title="Y",
                scaleanchor="x", scaleratio=1,
                showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False
            ),
            template="plotly_dark",
            margin=dict(l=10, r=10, t=10, b=10),
            height=500,
            plot_bgcolor='rgba(10, 10, 15, 1)',
            paper_bgcolor='rgba(10, 10, 15, 1)',
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(0,0,0,0.5)")
        )
        return fig

    st.plotly_chart(create_squares_plot(x_data, y_true, w, b, metric), use_container_width=True)

# Explanation Section
st.markdown("---")
st.markdown("### 🤔 Why do we SQUARE the error instead of just taking the absolute value?")

col_text, col_plot = st.columns([1.5, 1])

with col_text:
    st.markdown("""
    In Machine Learning, **Mean Squared Error (MSE)** is the most popular loss function for regression. 
    But why not just measure the straight line distance (**Mean Absolute Error - MAE**)?
    
    1. **The Outlier Penalty 🧨**: 
       Look at the graph on the right. If your model makes a small mistake, both MSE and MAE give a similar penalty. 
       But if the model makes a huge mistake, **MSE penalizes it exponentially!** 
       MSE acts like an alarm system that screams loudly if there is even one massive error.
       
    2. **Try the Outlier Checkbox 👆**: 
       Turn on the rogue outlier point above. If you use **MAE**, the best fit line will ignore the outlier to keep the majority happy. 
       If you use **MSE**, the outlier's giant square will pull the entire line down just to shrink that one massive square!
       
    3. **Calculus Loves Smooth Bowls 🥣**:
       To train a neural network, we calculate derivatives. The Absolute Error creates a sharp "V" shape at the bottom (non-differentiable at zero). Squaring it creates a beautiful, smooth parabola (a bowl) that makes Gradient Descent very happy!
    """)
    
with col_plot:
    def create_penalty_plot():
        errors = np.linspace(-5, 5, 100)
        mse_penalty = errors**2
        mae_penalty = np.abs(errors)
        
        fig = go.Figure()
        
        # Plot MSE curve
        fig.add_trace(go.Scatter(
            x=errors, y=mse_penalty, mode='lines', name='Squared Error (x²)', 
            line=dict(color='#9D00FF', width=3),
            fill='tozeroy', fillcolor='rgba(157, 0, 255, 0.1)'
        ))
        
        # Plot MAE curve
        fig.add_trace(go.Scatter(
            x=errors, y=mae_penalty, mode='lines', name='Absolute Error (|x|)', 
            line=dict(color='#00FF66', width=3),
            fill='tozeroy', fillcolor='rgba(0, 255, 102, 0.1)'
        ))
        
        fig.update_layout(
            xaxis_title="Error Size (Mistake)",
            yaxis_title="Penalty (Loss)",
            template="plotly_dark",
            height=350,
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor='rgba(10, 10, 15, 1)',
            paper_bgcolor='rgba(10, 10, 15, 1)',
            legend=dict(yanchor="top", y=0.95, xanchor="center", x=0.5, orientation="h")
        )
        return fig
        
    st.plotly_chart(create_penalty_plot(), use_container_width=True)