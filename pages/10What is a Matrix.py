import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle
import seaborn as sns

st.set_page_config(page_title="What is a Matrix?", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main-title {
        font-size: 3em;
        font-weight: bold;
        color: #2E86DE;
        text-align: center;
        margin-bottom: 0.5em;
    }
    .section-title {
        font-size: 2em;
        font-weight: bold;
        color: #A23B72;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }
    .concept-box {
        background-color: #D8E6FF;
        color: #111827;
        padding: 1.5em;
        border-radius: 10px;
        border-left: 4px solid #2E86DE;
        box-shadow: 0 2px 10px rgba(46, 134, 222, 0.08);
        margin-bottom: 1em;
    }
    .highlight {
        background-color: #FFD66D;
        color: #111827;
        padding: 0.2em 0.4em;
        border-radius: 3px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 What is a Matrix?</div>', unsafe_allow_html=True)
st.markdown("From grids of numbers to the language of transformations", unsafe_allow_html=True)

# ============ SECTION 1: Intuitive Introduction ============
st.markdown('<div class="section-title">🎯 Part 1: Think of a Matrix as a Spreadsheet</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="concept-box">
    <strong>A matrix is just a rectangular grid of numbers.</strong>
    
    Think of it like:
    - 📋 A spreadsheet
    - 🏪 A store inventory
    - 📷 Pixel colors in an image
    - 🌡️ Temperature readings across cities
    
    <span class="highlight">It's organized data!</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Create a simple visual spreadsheet
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.5, 4.5)
    ax.axis('off')
    
    # Draw grid
    data = [[3, 7, 2], [5, 1, 8], [4, 6, 9]]
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            # Draw cell
            rect = FancyBboxPatch((j-0.4, 2-i-0.4), 0.8, 0.8, 
                                   boxstyle="round,pad=0.05", 
                                   edgecolor='#2E86DE', facecolor='#E8F0FF', linewidth=2)
            ax.add_patch(rect)
            # Add number
            ax.text(j, 2-i, str(val), ha='center', va='center', fontsize=20, fontweight='bold', color='#2E86DE')
    
    ax.text(-0.7, 1, "Store A\nStore B\nStore C", fontsize=10, ha='right', va='center', fontweight='bold')
    ax.text(0, -0.7, "Red  Blue  Green", fontsize=10, ha='center', va='top', fontweight='bold')
    ax.text(0, 2.8, "Inventory Matrix", fontsize=14, ha='center', fontweight='bold', color='#A23B72')
    
    st.pyplot(fig, use_container_width=True)

# ============ SECTION 2: Dimensions & Notation ============
st.markdown('<div class="section-title">📐 Part 2: Rows, Columns & Dimensions</div>', unsafe_allow_html=True)

st.markdown("""
<div class="concept-box">
A matrix's <span class="highlight">m × n</span> notation tells you:
- <strong>m</strong> = number of ROWS (horizontal layers)
- <strong>n</strong> = number of COLUMNS (vertical stacks)

Think: **Rows across, Columns down** (like reading a book: left to right, top to bottom)
</div>
""", unsafe_allow_html=True)

# Interactive dimension explorer
col1, col2, col3 = st.columns(3)

with col1:
    rows = st.slider("Number of Rows (m)", 1, 6, 3, key="rows")
with col2:
    cols = st.slider("Number of Columns (n)", 1, 6, 3, key="cols")
with col3:
    color_choice = st.selectbox("Color Theme", ["Blue", "Purple", "Green", "Orange"])

color_map = {
    "Blue": "#2E86DE",
    "Purple": "#A23B72",
    "Green": "#00A86B",
    "Orange": "#FF6B35"
}
chosen_color = color_map[color_choice]

# Generate random matrix
matrix = np.random.randint(-10, 11, size=(rows, cols))

# Visualize the matrix with labels
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(-2, cols + 1)
ax.set_ylim(-2, rows + 1)
ax.axis('off')

# Draw matrix
for i in range(rows):
    for j in range(cols):
        # Cell background
        rect = FancyBboxPatch((j-0.45, rows-1-i-0.45), 0.9, 0.9,
                               boxstyle="round,pad=0.05",
                               edgecolor=chosen_color, facecolor=f'{chosen_color}20', 
                               linewidth=2.5)
        ax.add_patch(rect)
        # Number
        ax.text(j, rows-1-i, str(matrix[i, j]), ha='center', va='center', 
               fontsize=16, fontweight='bold', color=chosen_color)

# Labels for rows
for i in range(rows):
    ax.text(-1.2, rows-1-i, f"Row {i+1}", ha='right', va='center', fontsize=11, fontweight='bold')

# Labels for columns
for j in range(cols):
    ax.text(j, rows+0.4, f"Col {j+1}", ha='center', va='bottom', fontsize=11, fontweight='bold')

# Title
ax.text(cols/2-0.5, rows+1.2, f"A {rows}×{cols} Matrix", ha='center', fontsize=16, 
       fontweight='bold', color=chosen_color)

st.pyplot(fig, use_container_width=True)

# Show the mathematical notation
st.markdown(f"**Matrix Notation:** A ∈ ℝ^({rows}×{cols})")

# ============ SECTION 3: Element Naming ============
st.markdown('<div class="section-title">🏷️ Part 3: How to Read Individual Elements</div>', unsafe_allow_html=True)

st.markdown("""
<div class="concept-box">
Each element in a matrix has an <span class="highlight">address</span>: <strong>A[i,j]</strong>
- <strong>i</strong> = row index (which row, counting from top)
- <strong>j</strong> = column index (which column, counting from left)

Example: A[2,3] means the element in Row 2, Column 3
</div>
""", unsafe_allow_html=True)

# Interactive element selector
col1, col2 = st.columns(2)

with col1:
    sel_row = st.slider("Select Row (i)", 1, rows, 1, key="sel_row")
with col2:
    sel_col = st.slider("Select Column (j)", 1, cols, 1, key="sel_col")

# Highlight the selected element
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(-2, cols + 1)
ax.set_ylim(-2, rows + 1)
ax.axis('off')

selected_val = matrix[sel_row-1, sel_col-1]

# Draw matrix with highlight
for i in range(rows):
    for j in range(cols):
        is_selected = (i == sel_row-1 and j == sel_col-1)
        
        # Cell background
        if is_selected:
            facecolor = chosen_color
            edgecolor = 'gold'
            linewidth = 4
            text_color = 'white'
        else:
            facecolor = f'{chosen_color}20'
            edgecolor = chosen_color
            linewidth = 2
            text_color = chosen_color
        
        rect = FancyBboxPatch((j-0.45, rows-1-i-0.45), 0.9, 0.9,
                               boxstyle="round,pad=0.05",
                               edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth)
        ax.add_patch(rect)
        
        # Number
        fontsize = 20 if is_selected else 16
        ax.text(j, rows-1-i, str(matrix[i, j]), ha='center', va='center',
               fontsize=fontsize, fontweight='bold', color=text_color)

# Labels
for i in range(rows):
    ax.text(-1.2, rows-1-i, f"Row {i+1}", ha='right', va='center', fontsize=11, fontweight='bold')

for j in range(cols):
    ax.text(j, rows+0.4, f"Col {j+1}", ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.text(cols/2-0.5, rows+1.2, f"A[{sel_row},{sel_col}] = {selected_val}", ha='center', 
       fontsize=16, fontweight='bold', color=chosen_color)

st.pyplot(fig, use_container_width=True)

# ============ SECTION 4: Real-World Examples ============
st.markdown('<div class="section-title">🌍 Part 4: Matrices in the Real World</div>', unsafe_allow_html=True)

tabs = st.tabs(["📷 Images", "🎮 Game Board", "📊 Data Table", "🌡️ Weather"])

with tabs[0]:
    st.markdown("**An image is a matrix of pixel colors!**")
    st.markdown("Each pixel has RGB values (or just grayscale). Here's a tiny 4×4 image:")
    
    # Create a small image matrix
    img_matrix = np.random.randint(0, 256, size=(4, 4))
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # Show as numbers
    ax1.set_xlim(-0.5, 4.5)
    ax1.set_ylim(-0.5, 4.5)
    ax1.set_title("Pixel Values (0-255)", fontsize=12, fontweight='bold')
    ax1.axis('off')
    
    for i in range(4):
        for j in range(4):
            rect = Rectangle((j-0.4, 3-i-0.4), 0.8, 0.8, edgecolor='black', facecolor='lightgray')
            ax1.add_patch(rect)
            ax1.text(j, 3-i, str(img_matrix[i, j]), ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Show as image
    ax2.imshow(img_matrix, cmap='gray', vmin=0, vmax=255)
    ax2.set_title("Rendered as Image", fontsize=12, fontweight='bold')
    ax2.axis('off')
    
    st.pyplot(fig, use_container_width=True)

with tabs[1]:
    st.markdown("**A chess board is a 8×8 matrix!**")
    
    board = np.array([
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
    ])
    
    fig, ax = plt.subplots(figsize=(8, 8))
    im = ax.imshow(board, cmap='RdGy', vmin=0, vmax=1)
    
    ax.set_xticks(range(8))
    ax.set_yticks(range(8))
    ax.set_xticklabels(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    ax.set_yticklabels(['8', '7', '6', '5', '4', '3', '2', '1'])
    ax.set_title("Chess Board as 8×8 Matrix", fontsize=14, fontweight='bold')
    
    st.pyplot(fig, use_container_width=True)

with tabs[2]:
    st.markdown("**Student grades as a matrix:**")
    
    students = np.array([
        [85, 92, 78, 88],
        [90, 87, 91, 94],
        [78, 81, 75, 80],
        [95, 93, 97, 96],
        [88, 85, 89, 87]
    ])
    
    fig, ax = plt.subplots(figsize=(8, 4))
    im = ax.imshow(students, cmap='RdYlGn', vmin=70, vmax=100)
    
    ax.set_xticks(range(4))
    ax.set_yticks(range(5))
    ax.set_xticklabels(['Math', 'Science', 'English', 'History'])
    ax.set_yticklabels(['Alice', 'Bob', 'Carol', 'David', 'Eve'])
    ax.set_title("5×4 Matrix: Students × Subjects", fontsize=14, fontweight='bold')
    
    # Add value labels
    for i in range(5):
        for j in range(4):
            text = ax.text(j, i, f'{students[i, j]}', ha="center", va="center",
                          color="black", fontsize=10, fontweight='bold')
    
    plt.colorbar(im, ax=ax, label='Grade')
    st.pyplot(fig, use_container_width=True)

with tabs[3]:
    st.markdown("**Temperature readings: 5 cities × 7 days**")
    
    temps = np.array([
        [20, 22, 24, 23, 25, 26, 24],
        [15, 14, 13, 15, 14, 16, 17],
        [30, 31, 32, 31, 30, 29, 28],
        [18, 19, 20, 21, 22, 21, 20],
        [25, 26, 27, 28, 27, 26, 25]
    ])
    
    fig, ax = plt.subplots(figsize=(10, 4))
    im = ax.imshow(temps, cmap='coolwarm', vmin=10, vmax=35)
    
    ax.set_xticks(range(7))
    ax.set_yticks(range(5))
    ax.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    ax.set_yticklabels(['NYC', 'Alaska', 'Delhi', 'London', 'Sydney'])
    ax.set_title("5×7 Temperature Matrix (°C)", fontsize=14, fontweight='bold')
    
    # Add value labels
    for i in range(5):
        for j in range(7):
            text = ax.text(j, i, f'{temps[i, j]}°', ha="center", va="center",
                          color="black", fontsize=9, fontweight='bold')
    
    plt.colorbar(im, ax=ax, label='Temperature (°C)')
    st.pyplot(fig, use_container_width=True)

# ============ SECTION 5: Special Matrices ============
st.markdown('<div class="section-title">⭐ Part 5: Special Matrix Types</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 🟩 Square Matrix (m = n)
    Same number of rows and columns.
    Perfect for rotations and transformations!
    
    Example: 3×3
    """)
    
    square = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(-0.5, 3.5)
    ax.axis('off')
    
    for i in range(3):
        for j in range(3):
            rect = FancyBboxPatch((j-0.4, 2-i-0.4), 0.8, 0.8,
                                   boxstyle="round,pad=0.05",
                                   edgecolor='#2E86DE', facecolor='#E8F0FF', linewidth=2)
            ax.add_patch(rect)
            ax.text(j, 2-i, str(square[i, j]), ha='center', va='center', fontsize=14, fontweight='bold')
    
    ax.text(1, 3.3, "3×3 Square Matrix", ha='center', fontsize=12, fontweight='bold')
    st.pyplot(fig, use_container_width=True)

with col2:
    st.markdown("""
    #### 🟩 Row Vector (1 × n)
    Just one row!
    
    Example: 1×4
    """)
    
    row_vec = np.array([[5, -2, 8, 3]])
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.5, 1.5)
    ax.axis('off')
    
    for j in range(4):
        rect = FancyBboxPatch((j-0.4, -0.4), 0.8, 0.8,
                               boxstyle="round,pad=0.05",
                               edgecolor='#A23B72', facecolor='#F0E8F5', linewidth=2)
        ax.add_patch(rect)
        ax.text(j, 0, str(row_vec[0, j]), ha='center', va='center', fontsize=14, fontweight='bold')
    
    ax.text(1.5, 1.3, "1×4 Row Vector", ha='center', fontsize=12, fontweight='bold')
    st.pyplot(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 🟩 Column Vector (m × 1)
    Just one column!
    
    Example: 4×1
    """)
    
    col_vec = np.array([[5], [-2], [8], [3]])
    fig, ax = plt.subplots(figsize=(2, 6))
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 4.5)
    ax.axis('off')
    
    for i in range(4):
        rect = FancyBboxPatch((-0.4, 3-i-0.4), 0.8, 0.8,
                               boxstyle="round,pad=0.05",
                               edgecolor='#00A86B', facecolor='#E8F5F0', linewidth=2)
        ax.add_patch(rect)
        ax.text(0, 3-i, str(col_vec[i, 0]), ha='center', va='center', fontsize=14, fontweight='bold')
    
    ax.text(0, 4.3, "4×1 Column Vector", ha='center', fontsize=12, fontweight='bold')
    st.pyplot(fig, use_container_width=True)

with col2:
    st.markdown("""
    #### 🟩 Zero Matrix
    All elements are zero.
    
    Example: 3×3
    """)
    
    zero_matrix = np.zeros((3, 3), dtype=int)
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(-0.5, 3.5)
    ax.axis('off')
    
    for i in range(3):
        for j in range(3):
            rect = FancyBboxPatch((j-0.4, 2-i-0.4), 0.8, 0.8,
                                   boxstyle="round,pad=0.05",
                                   edgecolor='#FF6B35', facecolor='#FFE8DB', linewidth=2)
            ax.add_patch(rect)
            ax.text(j, 2-i, "0", ha='center', va='center', fontsize=14, fontweight='bold', color='#2E86DE')
    
    ax.text(1, 3.3, "3×3 Zero Matrix", ha='center', fontsize=12, fontweight='bold')
    st.pyplot(fig, use_container_width=True)

# ============ SECTION 6: Key Takeaway ============
st.markdown('<div class="section-title">🎓 Key Takeaways</div>', unsafe_allow_html=True)

st.markdown("""
<div class="concept-box">
✅ <strong>A matrix is an m × n rectangular grid of numbers</strong>
- <strong>m</strong> rows (horizontal)
- <strong>n</strong> columns (vertical)

✅ <strong>Access any element using A[i, j]</strong>
- i = row number
- j = column number

✅ <strong>Matrices appear everywhere!</strong>
- Images as pixel grids
- Data in spreadsheets
- Transformations in graphics
- Neural network weights

✅ <strong>Special types matter:</strong>
- Square matrices (m = n)
- Row/Column vectors
- Zero matrices

Next: Learn how matrices ADD, SUBTRACT, and most importantly—MULTIPLY! 🚀
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("💭 **Fun Fact:** A single image (1920×1080 pixels) is a matrix of 2,073,600 numbers! Your computer stores and processes millions of matrices every second.")
