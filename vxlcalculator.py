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

# Custom CSS for better styling
st.markdown("""
<style>
.plate-container {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin: 20px 0;
    border: 1px solid #e9ecef;
}

.metric-card {
    background: linear-gradient(145deg, #ffffff, #f8f9fa);
    padding: 1.5rem;
    border-radius: 12px;
    border-left: 5px solid #007bff;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    text-align: center;
    margin-bottom: 1rem;
}

.metric-value {
    font-size: 2.5rem;
    font-weight: bold;
    color: #007bff;
    margin-bottom: 0.5rem;
}

.metric-label {
    color: #6c757d;
    font-size: 1rem;
    font-weight: 500;
}

.buffer-item {
    background: linear-gradient(145deg, #ffffff, #f8f9fa);
    padding: 15px;
    margin: 10px 0;
    border-radius: 10px;
    border-left: 5px solid #28a745;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    transition: transform 0.2s ease;
}

.buffer-item:hover {
    transform: translateY(-2px);
}

.instructions {
    background: linear-gradient(145deg, #e3f2fd, #bbdefb);
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #2196f3;
    margin-bottom: 20px;
}

.column-selector {
    background: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 20px;
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

# Main app
st.title("🧪 VXL Calculator")
st.markdown("Interactive 96-well plate VXL calculation tool")

# Instructions
with st.expander("📋 Instructions", expanded=False):
    st.markdown("""
    - **Individual Wells**: Click on any well to toggle its selection
    - **Column Selection**: Use the column buttons to select entire columns
    - **Quick Fill/Clear**: Use the sidebar buttons to fill or clear the entire plate
    """)

# Sidebar controls
with st.sidebar:
    st.header("🎛️ Plate Controls")
    
    # Quick operations
    st.subheader("Quick Operations")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Fill All 🔄", use_container_width=True):
            st.session_state.plate_state = np.ones((8, 12), dtype=bool)
            st.rerun()
    with col2:
        if st.button("Clear All ❌", use_container_width=True):
            st.session_state.plate_state = np.zeros((8, 12), dtype=bool)
            st.rerun()
    
    # Extra reactions (safety margin)
    st.subheader("Additional Settings")
    extra_reactions = st.number_input(
        "Extra reactions (safety margin):", 
        min_value=0, 
        value=4, 
        step=1,
        help="Additional reactions to account for pipetting losses and safety margin"
    )
    st.session_state.extra_reactions = extra_reactions

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("96-Well Plate Layout")
    

    
    # Create interactive plate display
    st.markdown("**Select rows/columns or click individual wells:**")
    
    # Column headers with checkboxes
    header_cols = st.columns([0.5, 0.5] + [1] * 12)
    with header_cols[0]:
        st.markdown("")  # Empty space 
    with header_cols[1]:
        st.markdown("")  # Empty space for row checkboxes
    for i in range(12):
        with header_cols[i + 2]:
            col_filled = np.all(st.session_state.plate_state[:, i])
            if st.checkbox("", value=col_filled, key=f"col_check_{i}", help=f"Select entire column {i+1}"):
                if not col_filled:  # If checkbox is now checked and column wasn't filled
                    st.session_state.plate_state[:, i] = True
                    st.rerun()
            else:
                if col_filled:  # If checkbox is now unchecked and column was filled
                    st.session_state.plate_state[:, i] = False
                    st.rerun()
            st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 12px; color: #666;'>{i+1}</div>", unsafe_allow_html=True)
    
    # Create the 96-well plate grid
    for row in range(8):
        cols = st.columns([0.5, 0.5] + [1] * 12)  # Row checkbox + Row label + 12 wells
        
        with cols[0]:
            row_filled = np.all(st.session_state.plate_state[row, :])
            if st.checkbox("", value=row_filled, key=f"row_check_{row}", help=f"Select entire row {chr(65 + row)}"):
                if not row_filled:  # If checkbox is now checked and row wasn't filled
                    st.session_state.plate_state[row, :] = True
                    st.rerun()
            else:
                if row_filled:  # If checkbox is now unchecked and row was filled
                    st.session_state.plate_state[row, :] = False
                    st.rerun()
        
        with cols[1]:
            st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 14px; color: #666; padding: 5px;'>{chr(65 + row)}</div>", unsafe_allow_html=True)
        
        for col in range(12):
            with cols[col + 2]:
                well_id = get_well_id(row, col)
                is_filled = st.session_state.plate_state[row, col]
                
                if st.button(
                    "●" if is_filled else "○", 
                    key=f"well_{row}_{col}",
                    help=f"Well {well_id}",
                    use_container_width=True
                ):
                    st.session_state.plate_state[row, col] = not st.session_state.plate_state[row, col]
                    st.rerun()

with col2:
    st.subheader("📊 Results")
    
    # Calculate current state
    filled_wells, total_reactions = update_calculations()
    
    # Display metrics
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
    
    if total_reactions > 0:
        st.subheader("🧪 Buffer Calculations")
        
        # Buffer composition per reaction
        buffers = {
            "Buffer VXL": 100,
            "Buffer ACB": 400, 
            "MagAttract Suspension G": 25,
            "Carrier RNA": 1
        }
        
        st.markdown("**Volumes needed:**")
        total_volume = 0
        
        for buffer_name, per_reaction in buffers.items():
            final_volume = per_reaction * total_reactions
            total_volume += final_volume
            
            st.markdown(f"""
            <div class="buffer-item">
                <strong>{buffer_name}:</strong><br>
                {final_volume:,} µl ({final_volume/1000:.2f} ml)
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="buffer-item" style="border-left-color: #007bff;">
            <strong>Total Volume:</strong><br>
            {total_volume:,} µl ({total_volume/1000:.2f} ml)
        </div>
        """, unsafe_allow_html=True)
        
        # Export functionality
        if st.button("📥 Export Results", use_container_width=True):
            # Create export data
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
            
            # Add summary info
            summary_info = f"""
Lab Buffer Calculator Results
Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}
Filled Wells: {int(filled_wells)}
Extra Reactions: {extra_reactions}
Total Reactions: {total_reactions}

"""
            
            csv_data = summary_info + df.to_csv(index=False)
            
            st.download_button(
                label="💾 Download CSV",
                data=csv_data,
                file_name=f"buffer_calculation_{int(filled_wells)}_wells_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.info("👆 Select wells on the plate to see buffer calculations")

# Display current plate summary
with st.expander("📋 Current Plate Summary", expanded=False):
    if np.any(st.session_state.plate_state):
        filled_positions = []
        for row in range(8):
            for col in range(12):
                if st.session_state.plate_state[row, col]:
                    filled_positions.append(get_well_id(row, col))
        
        st.write(f"**Filled wells ({len(filled_positions)}):**")
        st.write(", ".join(filled_positions))
        
        # Show by rows
        for row in range(8):
            row_wells = [get_well_id(row, col) for col in range(12) if st.session_state.plate_state[row, col]]
            if row_wells:
                st.write(f"Row {chr(65 + row)}: {', '.join(row_wells)}")
    else:
        st.write("No wells selected")

# Footer
st.markdown("---")
st.markdown("💡 **Tips:** Use column buttons for quick selection of entire columns, or click individual wells to toggle them!")
