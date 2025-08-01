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
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin: 20px 0;
    border: 2px solid #e9ecef;
}

.plate-grid {
    display: grid;
    grid-template-columns: 40px repeat(12, 45px);
    grid-template-rows: 40px repeat(8, 45px);
    gap: 3px;
    justify-content: center;
    margin: 20px auto;
    max-width: 700px;
}

.row-header, .col-header {
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 14px;
    color: #495057;
    background: #f8f9fa;
    border-radius: 6px;
}

.well-button {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 2px solid;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 11px;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.well-empty {
    background: linear-gradient(145deg, #ffffff, #f1f3f4);
    border-color: #ced4da;
    color: #6c757d;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}

.well-empty:hover {
    background: linear-gradient(145deg, #e9ecef, #dee2e6);
    border-color: #adb5bd;
    transform: scale(1.05);
}

.well-filled {
    background: linear-gradient(145deg, #28a745, #34ce57);
    border-color: #20c997;
    color: white;
    box-shadow: 0 4px 8px rgba(40, 167, 69, 0.3);
}

.well-filled:hover {
    background: linear-gradient(145deg, #34ce57, #28a745);
    transform: scale(1.05);
    box-shadow: 0 6px 12px rgba(40, 167, 69, 0.4);
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
st.title("🧪 Lab Buffer Calculator")
st.markdown("Interactive 96-well plate buffer calculation tool")

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
        value=5, 
        step=1,
        help="Additional reactions to account for pipetting losses and safety margin"
    )
    st.session_state.extra_reactions = extra_reactions

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("96-Well Plate Layout")
    
    # Column selection buttons
    st.markdown('<div class="column-selector">', unsafe_allow_html=True)
    st.markdown("**Select entire columns:**")
    col_buttons = st.columns(12)
    for i, col_btn in enumerate(col_buttons):
        with col_btn:
            column_filled = np.all(st.session_state.plate_state[:, i])
            button_text = f"✓ {i+1}" if column_filled else f"{i+1}"
            button_type = "secondary" if column_filled else "primary"
            
            if st.button(button_text, key=f"col_{i}", use_container_width=True, type=button_type):
                # Toggle entire column
                current_state = np.all(st.session_state.plate_state[:, i])
                st.session_state.plate_state[:, i] = not current_state
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Create interactive plate display
    st.markdown('<div class="plate-container">', unsafe_allow_html=True)
    
    # Create the plate grid using HTML/CSS
    plate_html = '<div class="plate-grid">'
    
    # Empty top-left corner
    plate_html += '<div></div>'
    
    # Column headers
    for col in range(12):
        plate_html += f'<div class="col-header">{col + 1}</div>'
    
    # Rows
    for row in range(8):
        # Row header
        plate_html += f'<div class="row-header">{chr(65 + row)}</div>'
        
        # Wells in this row
        for col in range(12):
            well_id = get_well_id(row, col)
            is_filled = st.session_state.plate_state[row, col]
            well_class = "well-filled" if is_filled else "well-empty"
            symbol = "●" if is_filled else "○"
            
            plate_html += f'''
            <div class="well-button {well_class}" 
                 onclick="toggleWell({row}, {col})" 
                 title="Well {well_id}">
                {symbol}
            </div>
            '''
    
    plate_html += '</div>'
    
    # Add JavaScript for well interaction
    plate_html += '''
    <script>
    function toggleWell(row, col) {
        // This would need to communicate back to Streamlit
        // For now, we'll use the button approach below
    }
    </script>
    '''
    
    st.markdown(plate_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Fallback: Create clickable buttons in a more organized way
    st.markdown("**Click wells to toggle:**")
    
    # Create a more organized grid of buttons
    for row in range(8):
        cols = st.columns([0.8] + [1] * 12)  # Row label + 12 wells
        
        with cols[0]:
            st.markdown(f"<div style='text-align: center; font-weight: bold; padding: 8px;'>{chr(65 + row)}</div>", unsafe_allow_html=True)
        
        for col in range(12):
            with cols[col + 1]:
                well_id = get_well_id(row, col)
                is_filled = st.session_state.plate_state[row, col]
                
                # Use emoji-based representation
                if is_filled:
                    button_label = "🟢"
                    button_help = f"Well {well_id} - Click to empty"
                else:
                    button_label = "⚪"
                    button_help = f"Well {well_id} - Click to fill"
                
                if st.button(
                    button_label, 
                    key=f"well_{row}_{col}",
                    help=button_help,
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
