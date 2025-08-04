import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="VXL Buffer Calculator", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
<style>
/* Hide Streamlit branding */
.stDeployButton {display: none;}
header[data-testid="stHeader"] {display: none;}
footer {display: none;}
.stAppViewContainer > .main > div {padding-top: 1rem;}

/* Professional color scheme */
:root {
    --primary-color: #2c5aa0;
    --secondary-color: #34495e;
    --success-color: #27ae60;
    --background-light: #f8f9fa;
    --border-color: #e9ecef;
    --text-dark: #2c3e50;
    --shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* Main container styling */
.main-header {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: var(--shadow);
}

.main-header h1 {
    font-size: 2.5rem !important;
    margin-bottom: 0.5rem !important;
    font-weight: 300 !important;
}

.main-header p {
    opacity: 0.9;
    font-size: 1.1rem;
    margin: 0;
}

/* Section styling */
.section-card {
    background: white;
    border-radius: 15px;
    padding: 1.5rem;
    box-shadow: var(--shadow);
    border: 1px solid var(--border-color);
    margin-bottom: 1.5rem;
}

/* Well grid styling */
.well-grid {
    display: grid;
    grid-template-columns: 30px 30px repeat(12, 35px);
    grid-template-rows: 30px 30px repeat(8, 35px);
    gap: 2px;
    justify-content: center;
    margin: 1rem 0;
    user-select: none;
    max-width: 650px;
    margin-left: auto;
    margin-right: auto;
}

.grid-label {
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    color: var(--text-dark);
    font-size: 12px;
}

/* Button styling */
.stButton > button {
    width: 35px !important;
    height: 35px !important;
    min-width: 35px !important;
    min-height: 35px !important;
    padding: 0 !important;
    margin: 0 !important;
    border-radius: 6px !important;
    font-size: 16px !important;
    font-weight: bold !important;
    transition: all 0.2s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border: 2px solid transparent !important;
}

/* Well states */
.well-empty {
    background: linear-gradient(145deg, #ffffff, #f8f9fa) !important;
    color: #6c757d !important;
    border: 2px solid #dee2e6 !important;
}

.well-empty:hover {
    background: linear-gradient(145deg, #f8f9fa, #e9ecef) !important;
    border-color: var(--primary-color) !important;
    transform: scale(1.05) !important;
}

.well-selected {
    background: linear-gradient(135deg, var(--primary-color), #1e3a5f) !important;
    color: white !important;
    border: 2px solid #1e3a5f !important;
    box-shadow: 0 0 15px rgba(44, 90, 160, 0.5) !important;
    transform: scale(1.1) !important;
}

.well-selected:hover {
    background: linear-gradient(135deg, #1e3a5f, var(--primary-color)) !important;
    transform: scale(1.15) !important;
}

/* Checkbox styling */
.stCheckbox {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    height: 35px !important;
    width: 30px !important;
    margin: 0 !important;
    padding: 0 !important;
}

.stCheckbox > label {
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
    height: 100% !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

.stCheckbox input[type="checkbox"] {
    width: 16px !important;
    height: 16px !important;
    accent-color: var(--primary-color) !important;
    margin: 0 !important;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(145deg, #ffffff, var(--background-light));
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    border-left: 4px solid var(--primary-color);
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    transition: transform 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
}

.metric-value {
    font-size: 2.2rem;
    font-weight: bold;
    color: var(--primary-color);
    margin-bottom: 0.3rem;
}

.metric-label {
    color: #6c757d;
    font-size: 0.9rem;
    font-weight: 600;
}

/* Buffer cards */
.buffer-card {
    background: white;
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 0.8rem;
    border-left: 4px solid var(--success-color);
    transition: all 0.3s ease;
}

.buffer-card:hover {
    transform: translateX(3px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    border-left-color: var(--primary-color);
}

.buffer-name {
    font-weight: 600;
    color: var(--text-dark);
    margin-bottom: 0.3rem;
}

.buffer-volume {
    font-weight: bold;
    color: var(--success-color);
    font-size: 1.1rem;
}

/* Total volume card */
.total-volume-card {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    margin: 1rem 0;
    box-shadow: 0 8px 25px rgba(44, 90, 160, 0.3);
}

.total-value {
    font-size: 1.8rem;
    font-weight: bold;
    margin-bottom: 0.3rem;
}

/* Control buttons */
.control-btn {
    margin: 0.2rem !important;
}

/* Instructions */
.instructions {
    background: linear-gradient(135deg, #fff3cd, #ffeaa7);
    border: 1px solid #ffc107;
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
    text-align: center;
    color: #856404;
}

/* Responsive design */
@media (max-width: 768px) {
    .well-grid {
        grid-template-columns: 25px 25px repeat(12, 30px);
        grid-template-rows: 25px 25px repeat(8, 30px);
        gap: 1px;
    }
    
    .stButton > button {
        width: 30px !important;
        height: 30px !important;
        min-width: 30px !important;
        min-height: 30px !important;
        font-size: 14px !important;
    }
    
    .main-header h1 {
        font-size: 2rem !important;
    }
}

/* Sidebar styling */
.stSidebar {
    background: var(--background-light);
}

.stSidebar .stButton > button {
    width: 100% !important;
    height: auto !important;
    min-height: 2.5rem !important;
    font-size: 14px !important;
    border-radius: 8px !important;
}

/* Number input styling */
.stNumberInput > div > div > input {
    border-radius: 8px !important;
    border: 1px solid var(--border-color) !important;
    padding: 0.5rem !important;
}

/* Selection pattern buttons */
.pattern-btn {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    margin: 0.2rem;
    background: var(--background-light);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.8rem;
    transition: all 0.2s ease;
}

.pattern-btn:hover {
    background: var(--primary-color);
    color: white;
    transform: translateY(-1px);
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'plate_state' not in st.session_state:
    st.session_state.plate_state = np.zeros((8, 12), dtype=bool)
if 'extra_reactions' not in st.session_state:
    st.session_state.extra_reactions = 5

# Helper functions
def get_well_id(row, col):
    return f"{chr(65 + row)}{col + 1}"

def update_calculations():
    filled_wells = np.sum(st.session_state.plate_state)
    total_reactions = int(filled_wells + st.session_state.extra_reactions)
    return filled_wells, total_reactions

def apply_pattern(pattern_name):
    """Apply common well selection patterns"""
    if pattern_name == "edge":
        # Select edge wells
        st.session_state.plate_state = np.zeros((8, 12), dtype=bool)
        st.session_state.plate_state[0, :] = True  # Top row
        st.session_state.plate_state[7, :] = True  # Bottom row
        st.session_state.plate_state[:, 0] = True  # Left column
        st.session_state.plate_state[:, 11] = True  # Right column
    elif pattern_name == "checkerboard":
        # Checkerboard pattern
        st.session_state.plate_state = np.zeros((8, 12), dtype=bool)
        for i in range(8):
            for j in range(12):
                if (i + j) % 2 == 0:
                    st.session_state.plate_state[i, j] = True
    elif pattern_name == "columns_135":
        # Select columns 1, 3, 5, etc.
        st.session_state.plate_state = np.zeros((8, 12), dtype=bool)
        for col in range(0, 12, 2):
            st.session_state.plate_state[:, col] = True

# Main header
st.markdown("""
<div class="main-header">
    <h1>🧪 VXL Buffer Calculator</h1>
    <p>Professional laboratory buffer calculation tool</p>
</div>
""", unsafe_allow_html=True)

# Sidebar controls
with st.sidebar:
    st.markdown("### 🎛️ Quick Controls")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔵 Fill All", key="fill_all", help="Select all wells"):
            st.session_state.plate_state = np.ones((8, 12), dtype=bool)
            st.rerun()
    
    with col2:
        if st.button("⚪ Clear All", key="clear_all", help="Deselect all wells"):
            st.session_state.plate_state = np.zeros((8, 12), dtype=bool)
            st.rerun()
    
    st.markdown("---")
    
    # Pattern selection
    st.markdown("### 🎯 Quick Patterns")
    
    pattern_cols = st.columns(2)
    with pattern_cols[0]:
        if st.button("🔲 Edge", key="edge_pattern", help="Select edge wells"):
            apply_pattern("edge")
            st.rerun()
        if st.button("🔳 Checker", key="checker_pattern", help="Checkerboard pattern"):
            apply_pattern("checkerboard")
            st.rerun()
    
    with pattern_cols[1]:
        if st.button("📊 Cols 1,3,5", key="odd_cols", help="Select odd columns"):
            apply_pattern("columns_135")
            st.rerun()
        if st.button("🎲 Random", key="random_pattern", help="Random selection"):
            st.session_state.plate_state = np.random.choice([True, False], size=(8, 12), p=[0.3, 0.7])
            st.rerun()
    
    st.markdown("---")
    
    # Extra reactions input
    st.session_state.extra_reactions = st.number_input(
        "Extra reactions (safety margin):",
        min_value=0,
        max_value=50,
        value=st.session_state.extra_reactions,
        step=1,
        help="Additional reactions to account for pipetting losses and dead volume"
    )

# Main content area
col_plate, col_results = st.columns([1.8, 1.2])

with col_plate:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    
    st.markdown("### 🔬 96-Well Plate Selection")
    
    # Instructions
    st.markdown("""
    <div class="instructions">
        <strong>💡 How to use:</strong> Click individual wells • Use row/column checkboxes for bulk selection • Try quick patterns in sidebar
    </div>
    """, unsafe_allow_html=True)
    
    # Create well grid using native Streamlit columns
    # Column headers
    header_cols = st.columns([0.4, 0.4] + [0.45] * 12)
    with header_cols[0]:
        st.markdown("")
    with header_cols[1]:  
        st.markdown("")
    
    for i in range(12):
        with header_cols[i + 2]:
            col_filled = np.all(st.session_state.plate_state[:, i])
            new_state = st.checkbox("", value=col_filled, key=f"col_check_{i}", label_visibility="collapsed")
            if new_state != col_filled:
                st.session_state.plate_state[:, i] = new_state
                st.rerun()

    # Column numbers
    num_cols = st.columns([0.4, 0.4] + [0.45] * 12)
    with num_cols[0]:
        st.markdown("")
    with num_cols[1]:
        st.markdown("")
    for i in range(12):
        with num_cols[i + 2]:
            st.markdown(f"<div class='grid-label'>{i+1}</div>", unsafe_allow_html=True)

    # Well rows
    for row in range(8):
        row_cols = st.columns([0.4, 0.4] + [0.45] * 12)
        
        # Row checkbox
        with row_cols[0]:
            row_filled = np.all(st.session_state.plate_state[row, :])
            new_state = st.checkbox("", value=row_filled, key=f"row_check_{row}", label_visibility="collapsed")
            if new_state != row_filled:
                st.session_state.plate_state[row, :] = new_state
                st.rerun()
        
        # Row label
        with row_cols[1]:
            st.markdown(f"<div class='grid-label'>{chr(65 + row)}</div>", unsafe_allow_html=True)
        
        # Wells
        for col in range(12):
            with row_cols[col + 2]:
                is_filled = st.session_state.plate_state[row, col]
                button_text = "●" if is_filled else "○"
                
                # Apply CSS class based on state
                css_class = "well-selected" if is_filled else "well-empty"
                
                if st.button(
                    button_text,
                    key=f"well_{row}_{col}",
                    help=f"Well {get_well_id(row, col)}"
                ):
                    st.session_state.plate_state[row, col] = not st.session_state.plate_state[row, col]
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_results:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    
    # Calculate current state
    filled_wells, total_reactions = update_calculations()
    
    # Metrics
    st.markdown("### 📊 Reaction Summary")
    
    met_col1, met_col2 = st.columns(2)
    with met_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{int(filled_wells)}</div>
            <div class="metric-label">Wells Selected</div>
        </div>
        """, unsafe_allow_html=True)
    
    with met_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_reactions}</div>
            <div class="metric-label">Total Reactions</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Buffer calculations
    st.markdown("### 🧪 Buffer Requirements")
    
    if total_reactions > 0:
        buffers = {
            "Buffer VXL": 100,
            "Buffer ACB": 400,
            "MagAttract Suspension G": 25,
            "Carrier RNA": 1
        }
        
        total_volume = 0
        for buffer_name, per_reaction in buffers.items():
            final_volume = per_reaction * total_reactions
            total_volume += final_volume
            
            st.markdown(f"""
            <div class="buffer-card">
                <div class="buffer-name">{buffer_name}</div>
                <div class="buffer-volume">{final_volume:,} µl ({final_volume/1000:.2f} ml)</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Total volume
        st.markdown(f"""
        <div class="total-volume-card">
            <div class="total-value">{total_volume:,} µl</div>
            <div>({total_volume/1000:.2f} ml total volume)</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Export functionality
        if st.button("📥 Export Buffer Calculations", type="primary", use_container_width=True):
            # Prepare export data
            export_data = []
            for buffer_name, per_reaction in buffers.items():
                final_volume = per_reaction * total_reactions
                export_data.append({
                    'Reagent': buffer_name,
                    'Per Reaction (µl)': per_reaction,
                    'Total Volume (µl)': final_volume,
                    'Total Volume (ml)': round(final_volume/1000, 3)
                })
            
            df = pd.DataFrame(export_data)
            
            # Create summary
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            summary = f"""VXL Buffer Calculator Results
Generated: {timestamp}
Wells Selected: {int(filled_wells)}
Extra Reactions: {st.session_state.extra_reactions}
Total Reactions: {total_reactions}
Total Volume: {total_volume:,} µl ({total_volume/1000:.2f} ml)

"""
            
            csv_data = summary + df.to_csv(index=False)
            
            st.download_button(
                label="💾 Download CSV Report",
                data=csv_data,
                file_name=f"VXL_buffer_calc_{int(filled_wells)}wells_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    else:
        st.info("👈 Select wells on the plate to calculate buffer requirements")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer with well selection summary
if filled_wells > 0:
    selected_wells = []
    for row in range(8):
        for col in range(12):
            if st.session_state.plate_state[row, col]:
                selected_wells.append(get_well_id(row, col))
    
    st.markdown("---")
    st.markdown(f"**Selected wells ({len(selected_wells)}):** {', '.join(selected_wells[:20])}")
    if len(selected_wells) > 20:
        st.markdown(f"... and {len(selected_wells) - 20} more wells")
