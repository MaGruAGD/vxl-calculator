import streamlit as st
import pandas as pd
import numpy as np
import json

# Set page config
st.set_page_config(
    page_title="Lab Buffer Calculator", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for compact, single-screen layout
st.markdown("""
<style>
/* Hide Streamlit elements to save space */
.stDeployButton {display: none;}
header[data-testid="stHeader"] {display: none;}
.stAppViewContainer > .main > div {padding-top: 1rem;}
footer {display: none;}

.plate-container {
    background: white;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    margin: 10px 0;
    border: 1px solid #e9ecef;
}

.metric-card {
    background: linear-gradient(145deg, #ffffff, #f8f9fa);
    padding: 0.8rem;
    border-radius: 8px;
    border-left: 4px solid #007bff;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    text-align: center;
    margin-bottom: 0.5rem;
}

.metric-value {
    font-size: 1.5rem;
    font-weight: bold;
    color: #007bff;
    margin-bottom: 0.2rem;
}

.metric-label {
    color: #6c757d;
    font-size: 0.8rem;
    font-weight: 500;
}

.buffer-item {
    background: linear-gradient(145deg, #ffffff, #f8f9fa);
    padding: 6px 10px;
    margin: 3px 0;
    border-radius: 6px;
    border-left: 3px solid #28a745;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    font-size: 0.85rem;
}

/* Compact plate styling */
.stButton > button {
    height: 26px !important;
    min-height: 26px !important;
    padding: 0 !important;
    font-size: 12px !important;
    line-height: 1 !important;
    margin: 0 !important;
}

.well-selected {
    background-color: #007bff !important;
    color: white !important;
    font-weight: bold !important;
    border: 2px solid #0056b3 !important;
    box-shadow: 0 0 4px rgba(0, 123, 255, 0.5) !important;
}

.well-unselected {
    background-color: #f8f9fa !important;
    color: #6c757d !important;
    border: 1px solid #dee2e6 !important;
}

.well-unselected:hover {
    background-color: #e9ecef !important;
    border: 1px solid #adb5bd !important;
}

/* Center checkboxes properly */
.stCheckbox {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    margin: 0 !important;
    padding: 0 !important;
    height: 26px !important;
}

.stCheckbox > label {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    height: 26px !important;
}

.stCheckbox > label > div {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

/* Compact sidebar */
.css-1d391kg {
    padding-top: 1rem;
}

/* Remove excessive margins */
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

/* Compact columns */
[data-testid="column"] {
    padding: 0 0.15rem;
}

/* Compact text elements */
h1 {
    font-size: 1.8rem !important;
    margin-bottom: 0.5rem !important;
}

h2 {
    font-size: 1.2rem !important;
    margin-bottom: 0.3rem !important;
}

h3 {
    font-size: 1rem !important;
    margin-bottom: 0.3rem !important;
}

p {
    margin-bottom: 0.5rem !important;
}

/* Make results section more compact */
.results-section {
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'plate_state' not in st.session_state:
    st.session_state.plate_state = np.zeros((8, 12), dtype=bool)

# Helper functions
def get_well_id(row, col):
    return f"{chr(65 + row)}{col + 1}"

def update_calculations():
    """Update all calculations based on current plate state"""
    filled_wells = np.sum(st.session_state.plate_state)
    extra_reactions = st.session_state.get('extra_reactions', 5)
    total_reactions = int(filled_wells + extra_reactions)
    
    return filled_wells, total_reactions

# Main app - compact header
st.title("🧪 VXL Calculator")

# Compact instructions in sidebar
with st.sidebar:
    st.header("🎛️ Controls")
    
    # Compact instructions
    st.markdown("**Quick Actions:**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Fill All", use_container_width=True):
            st.session_state.plate_state = np.ones((8, 12), dtype=bool)
            st.rerun()
    with col2:
        if st.button("Clear All", use_container_width=True):
            st.session_state.plate_state = np.zeros((8, 12), dtype=bool)
            st.rerun()
    
    # Extra reactions
    extra_reactions = st.number_input(
        "Extra reactions:", 
        min_value=0, 
        value=4, 
        step=1
    )
    st.session_state.extra_reactions = extra_reactions
    
    # Compact instructions
    st.markdown("**Usage:**")
    st.markdown("• Click wells to select  \n• Use ☑️ for rows/columns  \n• Click/drag for multiple")

# Main content - single column for plate, then results below
st.subheader("96-Well Plate Layout")

# Column headers with properly centered checkboxes
header_cols = st.columns([0.6, 0.6] + [0.7] * 12)
with header_cols[0]:
    st.markdown("<div style='height: 26px;'></div>", unsafe_allow_html=True)
with header_cols[1]:
    st.markdown("<div style='height: 26px;'></div>", unsafe_allow_html=True)

for i in range(12):
    with header_cols[i + 2]:
        col_filled = np.all(st.session_state.plate_state[:, i])
        st.markdown(f"<div style='display: flex; justify-content: center; align-items: center; height: 26px;'>", unsafe_allow_html=True)
        if st.checkbox("", value=col_filled, key=f"col_check_{i}"):
            if not col_filled:
                st.session_state.plate_state[:, i] = True
                st.rerun()
        else:
            if col_filled:
                st.session_state.plate_state[:, i] = False
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# Column numbers row
number_cols = st.columns([0.6, 0.6] + [0.7] * 12)
with number_cols[0]:
    st.markdown("")
with number_cols[1]:
    st.markdown("")
for i in range(12):
    with number_cols[i + 2]:
        st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 11px; color: #333; margin: 2px 0;'>{i+1}</div>", unsafe_allow_html=True)

# 96-well plate grid
for row in range(8):
    cols = st.columns([0.6, 0.6] + [0.7] * 12)
    
    with cols[0]:
        row_filled = np.all(st.session_state.plate_state[row, :])
        st.markdown(f"<div style='display: flex; justify-content: center; align-items: center; height: 26px;'>", unsafe_allow_html=True)
        if st.checkbox("", value=row_filled, key=f"row_check_{row}"):
            if not row_filled:
                st.session_state.plate_state[row, :] = True
                st.rerun()
        else:
            if row_filled:
                st.session_state.plate_state[row, :] = False
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown(f"<div style='display: flex; justify-content: center; align-items: center; height: 26px; font-weight: bold; font-size: 12px; color: #333;'>{chr(65 + row)}</div>", unsafe_allow_html=True)
    
    for col in range(12):
        with cols[col + 2]:
            is_filled = st.session_state.plate_state[row, col]
            button_text = "●" if is_filled else "○"
            
            if st.button(
                button_text, 
                key=f"well_{row}_{col}",
                use_container_width=True,
            ):
                st.session_state.plate_state[row, col] = not st.session_state.plate_state[row, col]
                st.rerun()

# Results section below the plate
st.markdown("<div class='results-section'>", unsafe_allow_html=True)

# Calculate current state
filled_wells, total_reactions = update_calculations()

# Results in columns below the plate
result_col1, result_col2, result_col3 = st.columns([1, 1.5, 1.2])

with result_col1:
    st.subheader("📊 Metrics")
    
    # Compact metrics
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{int(filled_wells)}</div>
        <div class="metric-label">Filled Wells</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_reactions}</div>
        <div class="metric-label">Total Reactions</div>
    </div>
    """, unsafe_allow_html=True)

with result_col2:
    if total_reactions > 0:
        st.subheader("🧪 Buffer Calculations")
        
        # Buffer composition per reaction
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
            
            # Compact buffer display
            st.markdown(f"""
            <div class="buffer-item">
                <strong>{buffer_name.replace('MagAttract Suspension G', 'MagAttract G')}:</strong>
                {final_volume:,} µl ({final_volume/1000:.1f} ml)
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="buffer-item" style="border-left-color: #007bff;">
            <strong>Total Volume:</strong> {total_volume:,} µl ({total_volume/1000:.1f} ml)
        </div>
        """, unsafe_allow_html=True)
        
        # Compact export
        if st.button("📥 Export Results", use_container_width=True):
            export_data = []
            for buffer_name, per_reaction in buffers.items():
                final_volume = per_reaction * total_reactions
                export_data.append({
                    'Reagent': buffer_name,
                    'Per Reaction (µl)': per_reaction,
                    'Total Volume (µl)': final_volume,
                    'Total Volume (ml)': round(final_volume/1000, 2)
                })
            
            df = pd.DataFrame(export_data)
            summary_info = f"""Lab Buffer Calculator Results
Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}
Filled Wells: {int(filled_wells)}
Extra Reactions: {extra_reactions}
Total Reactions: {total_reactions}

"""
            csv_data = summary_info + df.to_csv(index=False)
            
            st.download_button(
                label="💾 Download CSV",
                data=csv_data,
                file_name=f"buffer_calc_{int(filled_wells)}wells_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.subheader("🧪 Buffer Calculations")
        st.info("👆 Select wells to see calculations")

with result_col3:
    st.subheader("📋 Well Summary")
    
    if np.any(st.session_state.plate_state):
        filled_positions = []
        for row in range(8):
            for col in range(12):
                if st.session_state.plate_state[row, col]:
                    filled_positions.append(get_well_id(row, col))
        
        st.markdown(f"**Selected Wells ({len(filled_positions)}):**")
        
        # Group by rows for compact display
        summary_text = []
        for row in range(8):
            row_wells = [str(col + 1) for col in range(12) if st.session_state.plate_state[row, col]]
            if row_wells:
                summary_text.append(f"**{chr(65 + row)}:** {', '.join(row_wells)}")
        
        if summary_text:
            for line in summary_text:
                st.markdown(line)
        else:
            st.markdown("*No wells selected*")
    else:
        st.markdown("*No wells selected*")

st.markdown("</div>", unsafe_allow_html=True)

# Compact footer
st.markdown("---")
st.markdown("💡 **Tip:** Click wells or use checkboxes to select entire rows/columns")
