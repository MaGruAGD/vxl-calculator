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
.well-grid {
    display: grid;
    grid-template-columns: repeat(13, 1fr);
    gap: 2px;
    max-width: 600px;
    margin: 20px auto;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 10px;
    border: 2px solid #dee2e6;
}

.well-cell, .header-cell {
    width: 35px;
    height: 35px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.header-cell {
    background: transparent;
    border-radius: 3px;
    cursor: pointer;
    color: #495057;
}

.header-cell:hover {
    background: #e9ecef;
}

.well-empty {
    background: linear-gradient(145deg, #f8f9fa, #e9ecef);
    border: 2px solid #ced4da;
    color: #6c757d;
}

.well-filled {
    background: linear-gradient(145deg, #28a745, #20c997);
    border: 2px solid #20c997;
    color: white;
    box-shadow: 0 2px 4px rgba(40, 167, 69, 0.3);
}

.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #007bff;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    text-align: center;
}

.metric-value {
    font-size: 2rem;
    font-weight: bold;
    color: #007bff;
}

.metric-label {
    color: #6c757d;
    font-size: 0.9rem;
}

.buffer-item {
    background: white;
    padding: 12px;
    margin: 8px 0;
    border-radius: 6px;
    border-left: 4px solid #28a745;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.instructions {
    background: #e3f2fd;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #2196f3;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'plate_state' not in st.session_state:
    st.session_state.plate_state = np.zeros((8, 12), dtype=bool)

if 'selected_wells' not in st.session_state:
    st.session_state.selected_wells = set()

# Helper functions
def get_well_id(row, col):
    return f"{chr(65 + row)}{col + 1}"

def parse_well_range(well_range):
    """Parse well ranges like A1-A5 or single wells like B3"""
    wells = []
    if '-' in well_range:
        start, end = well_range.split('-')
        start_row = ord(start[0]) - 65
        start_col = int(start[1:]) - 1
        end_row = ord(end[0]) - 65
        end_col = int(end[1:]) - 1
        
        for row in range(min(start_row, end_row), max(start_row, end_row) + 1):
            for col in range(min(start_col, end_col), max(start_col, end_col) + 1):
                if 0 <= row < 8 and 0 <= col < 12:
                    wells.append((row, col))
    else:
        if len(well_range) >= 2:
            row = ord(well_range[0]) - 65
            col = int(well_range[1:]) - 1
            if 0 <= row < 8 and 0 <= col < 12:
                wells.append((row, col))
    return wells

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
    - **Individual Wells**: Use the well selector below to click individual wells
    - **Column Selection**: Use column buttons to select entire columns
    - **Range Selection**: Enter ranges like "A1-A5" or lists like "A1,B2,C3"
    - **Quick Fill**: Use the sidebar buttons for common patterns
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
    
    # Pattern filling
    st.subheader("Fill Patterns")
    pattern = st.selectbox("Select Pattern", [
        "Custom", "Checkerboard", "First 48 wells", "Last 48 wells",
        "Rows A-D", "Rows E-H", "Columns 1-6", "Columns 7-12"
    ])
    
    if st.button("Apply Pattern 🎨", use_container_width=True):
        if pattern == "Checkerboard":
            for i in range(8):
                for j in range(12):
                    st.session_state.plate_state[i, j] = (i + j) % 2 == 0
        elif pattern == "First 48 wells":
            st.session_state.plate_state = np.zeros((8, 12), dtype=bool)
            st.session_state.plate_state[:4, :] = True
        elif pattern == "Last 48 wells":
            st.session_state.plate_state = np.zeros((8, 12), dtype=bool)
            st.session_state.plate_state[4:, :] = True
        elif pattern == "Rows A-D":
            st.session_state.plate_state = np.zeros((8, 12), dtype=bool)
            st.session_state.plate_state[:4, :] = True
        elif pattern == "Rows E-H":
            st.session_state.plate_state = np.zeros((8, 12), dtype=bool)
            st.session_state.plate_state[4:, :] = True
        elif pattern == "Columns 1-6":
            st.session_state.plate_state = np.zeros((8, 12), dtype=bool)
            st.session_state.plate_state[:, :6] = True
        elif pattern == "Columns 7-12":
            st.session_state.plate_state = np.zeros((8, 12), dtype=bool)
            st.session_state.plate_state[:, 6:] = True
        st.rerun()
    
    # Manual well entry
    st.subheader("Manual Entry")
    well_input = st.text_input(
        "Enter wells/ranges:", 
        placeholder="A1,B2,C3-C5",
        help="Examples: A1,B2 or A1-A5 or A1,B2-B5,C3"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add Wells ➕", use_container_width=True) and well_input:
            wells_to_add = []
            for item in well_input.split(','):
                wells_to_add.extend(parse_well_range(item.strip().upper()))
            
            for row, col in wells_to_add:
                st.session_state.plate_state[row, col] = True
            st.rerun()
    
    with col2:
        if st.button("Remove Wells ➖", use_container_width=True) and well_input:
            wells_to_remove = []
            for item in well_input.split(','):
                wells_to_remove.extend(parse_well_range(item.strip().upper()))
            
            for row, col in wells_to_remove:
                st.session_state.plate_state[row, col] = False
            st.rerun()
    
    # Extra reactions
    st.subheader("Additional Settings")
    extra_reactions = st.number_input("Extra reactions:", min_value=0, value=5, step=1)
    st.session_state.extra_reactions = extra_reactions
    
    # Safety margin
    safety_margin = st.selectbox(
        "Safety margin:",
        options=[1.0, 1.1, 1.2, 1.5],
        index=2,
        format_func=lambda x: f"{int((x-1)*100)}% extra" if x > 1 else "No extra"
    )

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("96-Well Plate Layout")
    
    # Column selection buttons
    st.markdown("**Select entire columns:**")
    col_buttons = st.columns(12)
    for i, col_btn in enumerate(col_buttons):
        with col_btn:
            if st.button(f"{i+1}", key=f"col_{i}", use_container_width=True):
                # Toggle entire column
                current_state = np.all(st.session_state.plate_state[:, i])
                st.session_state.plate_state[:, i] = not current_state
                st.rerun()
    
    # Create interactive plate display
    st.markdown("**Click wells to toggle:**")
    
    # Create a grid of buttons for wells
    for row in range(8):
        cols = st.columns([0.5] + [1] * 12)  # Row label + 12 wells
        
        with cols[0]:
            st.markdown(f"**{chr(65 + row)}**")
        
        for col in range(12):
            with cols[col + 1]:
                well_id = get_well_id(row, col)
                is_filled = st.session_state.plate_state[row, col]
                
                # Use different button styles based on state
                button_style = "🟢" if is_filled else "⚪"
                
                if st.button(
                    button_style, 
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
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{int(filled_wells)}</div>
            <div class="metric-label">Filled Wells</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
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
            base_volume = per_reaction * total_reactions
            final_volume = int(base_volume * safety_margin)
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
                base_volume = per_reaction * total_reactions
                final_volume = int(base_volume * safety_margin)
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
Safety Margin: {int((safety_margin-1)*100)}%

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
st.markdown("💡 **Tips:** Use column buttons for quick selection, or enter ranges like 'A1-A5' for multiple wells at once!")
