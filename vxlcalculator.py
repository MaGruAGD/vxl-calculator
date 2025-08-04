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

# Custom CSS for focused, single-screen layout
st.markdown("""
<style>
/* Hide Streamlit elements to save space */
.stDeployButton {display: none;}
header[data-testid="stHeader"] {display: none;}
.stAppViewContainer > .main > div {padding-top: 1rem;}
footer {display: none;}

.metric-card {
    background: linear-gradient(145deg, #ffffff, #f8f9fa);
    padding: 1rem;
    border-radius: 10px;
    border-left: 5px solid #007bff;
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    text-align: center;
    margin-bottom: 0.8rem;
}

.metric-value {
    font-size: 2rem;
    font-weight: bold;
    color: #007bff;
    margin-bottom: 0.3rem;
}

.metric-label {
    color: #6c757d;
    font-size: 0.9rem;
    font-weight: 600;
}

.buffer-card {
    background: linear-gradient(145deg, #ffffff, #f8f9fa);
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 10px;
    border-left: 5px solid #28a745;
    box-shadow: 0 4px 8px rgba(0,0,0,0.12);
    transition: transform 0.2s ease;
}

.buffer-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.18);
}

.buffer-name {
    font-weight: bold;
    font-size: 1rem;
    color: #333;
    margin-bottom: 0.3rem;
}

.buffer-volume {
    font-size: 1.1rem;
    color: #28a745;
    font-weight: 600;
}

/* Improved well button styling */
.stButton > button {
    height: 32px !important;
    width: 32px !important;
    min-height: 32px !important;
    min-width: 32px !important;
    padding: 0 !important;
    font-size: 16px !important;
    line-height: 1 !important;
    margin: 1px !important;
    font-weight: bold !important;
    border-radius: 6px !important;
    transition: all 0.15s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* Selected well style - much more visible */
.well-selected {
    background: linear-gradient(145deg, #007bff, #0056b3) !important;
    color: white !important;
    font-weight: bold !important;
    border: 2px solid #0056b3 !important;
    box-shadow: 0 0 12px rgba(0, 123, 255, 0.8) !important;
    transform: scale(1.05) !important;
}

/* Unselected well style */
.well-unselected {
    background: linear-gradient(145deg, #f8f9fa, #e9ecef) !important;
    color: #6c757d !important;
    border: 1px solid #dee2e6 !important;
}

.well-unselected:hover {
    background: linear-gradient(145deg, #e9ecef, #dee2e6) !important;
    border: 1px solid #adb5bd !important;
    transform: scale(1.02) !important;
}

/* Improved checkbox styling and centering */
.stCheckbox {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    margin: 0 !important;
    padding: 0 !important;
    height: 32px !important;
    width: 32px !important;
}

.stCheckbox > label {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 32px !important;
    height: 32px !important;
    margin: 0 !important;
    padding: 0 !important;
    cursor: pointer !important;
}

.stCheckbox > label > div {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
    height: 100% !important;
}

.stCheckbox input[type="checkbox"] {
    width: 18px !important;
    height: 18px !important;
    margin: 0 !important;
    transform: scale(1.2) !important;
}

/* Remove excessive margins */
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

/* Compact columns */
[data-testid="column"] {
    padding: 0 0.1rem;
}

/* Compact text elements */
h1 {
    font-size: 2rem !important;
    margin-bottom: 0.5rem !important;
    text-align: center;
}

h2 {
    font-size: 1.4rem !important;
    margin-bottom: 0.5rem !important;
}

h3 {
    font-size: 1.1rem !important;
    margin-bottom: 0.3rem !important;
}

/* Main layout sections */
.plate-section {
    background: linear-gradient(145deg, #f8f9fa, #ffffff);
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 1.5rem;
    border: 1px solid #e9ecef;
}

.results-section {
    background: linear-gradient(145deg, #f8f9fa, #ffffff);
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    border: 1px solid #e9ecef;
}

.total-volume-card {
    background: linear-gradient(145deg, #007bff, #0056b3);
    color: white;
    padding: 1.2rem;
    border-radius: 12px;
    box-shadow: 0 6px 16px rgba(0, 123, 255, 0.3);
    text-align: center;
    margin-top: 1rem;
}

.total-volume-value {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 0.3rem;
}

/* Plate grid container for better alignment */
.plate-grid {
    display: table;
    margin: 0 auto;
    border-spacing: 2px;
}

.plate-row {
    display: table-row;
}

.plate-cell {
    display: table-cell;
    text-align: center;
    vertical-align: middle;
    padding: 1px;
}

.row-label, .col-label {
    font-weight: bold;
    font-size: 14px;
    color: #333;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 32px;
    width: 32px;
    margin: 1px;
}

.drag-instructions {
    background: linear-gradient(145deg, #fff3cd, #ffeaa7);
    border: 1px solid #ffc107;
    border-radius: 8px;
    padding: 0.8rem;
    margin-bottom: 1rem;
    text-align: center;
    font-size: 0.9rem;
    color: #856404;
}
</style>

<script>
// JavaScript for drag selection functionality
let isDragging = false;
let dragStartState = null;

function enableDragSelection() {
    document.addEventListener('mousedown', function(e) {
        if (e.target.tagName === 'BUTTON' && e.target.textContent.match(/[●○]/)) {
            isDragging = true;
            dragStartState = e.target.textContent === '●' ? false : true;
            e.preventDefault();
        }
    });

    document.addEventListener('mouseover', function(e) {
        if (isDragging && e.target.tagName === 'BUTTON' && e.target.textContent.match(/[●○]/)) {
            const currentState = e.target.textContent === '●';
            if (currentState !== dragStartState) {
                e.target.click();
            }
        }
    });

    document.addEventListener('mouseup', function() {
        isDragging = false;
        dragStartState = null;
    });

    document.addEventListener('mouseleave', function() {
        isDragging = false;
        dragStartState = null;
    });
}

// Initialize drag selection when page loads
document.addEventListener('DOMContentLoaded', enableDragSelection);
// Re-initialize after Streamlit reruns
setTimeout(enableDragSelection, 100);
</script>
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

# Main app header
st.title("🧪 VXL Buffer Calculator")

# Sidebar with minimal controls
with st.sidebar:
    st.header("🎛️ Quick Controls")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Fill All", use_container_width=True):
            st.session_state.plate_state = np.ones((8, 12), dtype=bool)
            st.rerun()
    with col2:
        if st.button("Clear All", use_container_width=True):
            st.session_state.plate_state = np.zeros((8, 12), dtype=bool)
            st.rerun()
    
    st.markdown("---")
    extra_reactions = st.number_input(
        "Extra reactions (safety margin):", 
        min_value=0, 
        value=4, 
        step=1,
        help="Additional reactions for pipetting losses"
    )
    st.session_state.extra_reactions = extra_reactions

# Main layout: Two columns - Plate selector and Buffer calculations
main_col1, main_col2 = st.columns([1.8, 1.2])

with main_col1:
    st.markdown('<div class="plate-section">', unsafe_allow_html=True)
    st.subheader("🔬 96-Well Plate Selection")
    
    # Instructions for drag selection
    st.markdown("""
    <div class="drag-instructions">
        💡 <strong>Tips:</strong> Click wells to select • Hold and drag to select multiple • Use checkboxes for entire rows/columns
    </div>
    """, unsafe_allow_html=True)
    
    # Create a more structured grid layout
    # Column headers with properly centered checkboxes
    header_cols = st.columns([0.5, 0.5] + [0.6] * 12)
    with header_cols[0]:
        st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)
    with header_cols[1]:
        st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

    for i in range(12):
        with header_cols[i + 2]:
            col_filled = np.all(st.session_state.plate_state[:, i])
            if st.checkbox("", value=col_filled, key=f"col_check_{i}"):
                if not col_filled:
                    st.session_state.plate_state[:, i] = True
                    st.rerun()
            else:
                if col_filled:
                    st.session_state.plate_state[:, i] = False
                    st.rerun()

    # Column numbers row
    number_cols = st.columns([0.5, 0.5] + [0.6] * 12)
    with number_cols[0]:
        st.markdown("")
    with number_cols[1]:
        st.markdown("")
    for i in range(12):
        with number_cols[i + 2]:
            st.markdown(f"<div class='col-label'>{i+1}</div>", unsafe_allow_html=True)

    # 96-well plate grid with improved styling
    for row in range(8):
        cols = st.columns([0.5, 0.5] + [0.6] * 12)
        
        with cols[0]:
            row_filled = np.all(st.session_state.plate_state[row, :])
            if st.checkbox("", value=row_filled, key=f"row_check_{row}"):
                if not row_filled:
                    st.session_state.plate_state[row, :] = True
                    st.rerun()
            else:
                if row_filled:
                    st.session_state.plate_state[row, :] = False
                    st.rerun()
        
        with cols[1]:
            st.markdown(f"<div class='row-label'>{chr(65 + row)}</div>", unsafe_allow_html=True)
        
        for col in range(12):
            with cols[col + 2]:
                is_filled = st.session_state.plate_state[row, col]
                button_text = "●" if is_filled else "○"
                
                # Apply custom CSS classes based on state
                if is_filled:
                    st.markdown(f"""
                    <style>
                    div[data-testid="column"]:nth-child({col + 3}) .stButton > button {{
                        background: linear-gradient(145deg, #007bff, #0056b3) !important;
                        color: white !important;
                        border: 2px solid #0056b3 !important;
                        box-shadow: 0 0 12px rgba(0, 123, 255, 0.8) !important;
                        transform: scale(1.05) !important;
                    }}
                    </style>
                    """, unsafe_allow_html=True)
                
                if st.button(
                    button_text, 
                    key=f"well_{row}_{col}",
                    use_container_width=True,
                ):
                    st.session_state.plate_state[row, col] = not st.session_state.plate_state[row, col]
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

with main_col2:
    st.markdown('<div class="results-section">', unsafe_allow_html=True)
    
    # Calculate current state
    filled_wells, total_reactions = update_calculations()
    
    # Key metrics at the top
    st.subheader("📊 Reaction Summary")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{int(filled_wells)}</div>
            <div class="metric-label">Wells Selected</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_reactions}</div>
            <div class="metric-label">Total Reactions</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Buffer calculations - main feature
    st.subheader("🧪 Buffer Requirements")
    
    if total_reactions > 0:
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
            
            st.markdown(f"""
            <div class="buffer-card">
                <div class="buffer-name">{buffer_name}</div>
                <div class="buffer-volume">{final_volume:,} µl ({final_volume/1000:.2f} ml)</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Total volume - prominent display
        st.markdown(f"""
        <div class="total-volume-card">
            <div class="total-volume-value">{total_volume:,} µl</div>
            <div>({total_volume/1000:.2f} ml total volume)</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Export functionality
        st.markdown("---")
        if st.button("📥 Export Buffer Calculations", use_container_width=True, type="primary"):
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
            summary_info = f"""VXL Buffer Calculator Results
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
Wells Selected: {int(filled_wells)}
Extra Reactions: {extra_reactions}
Total Reactions: {total_reactions}
Total Volume: {total_volume:,} µl ({total_volume/1000:.2f} ml)

"""
            csv_data = summary_info + df.to_csv(index=False)
            
            st.download_button(
                label="💾 Download CSV Report",
                data=csv_data,
                file_name=f"VXL_buffer_calc_{int(filled_wells)}wells_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.info("👈 Select wells on the plate to calculate buffer requirements")
    
    st.markdown('</div>', unsafe_allow_html=True)

# JavaScript to enable drag selection functionality
st.markdown("""
<script>
let isDragging = false;
let dragStartState = null;

function setupDragSelection() {
    const buttons = document.querySelectorAll('button');
    
    buttons.forEach(button => {
        if (button.textContent.match(/[●○]/)) {
            button.addEventListener('mousedown', function(e) {
                isDragging = true;
                dragStartState = this.textContent === '●' ? false : true;
                e.preventDefault();
            });
            
            button.addEventListener('mouseenter', function() {
                if (isDragging) {
                    const currentState = this.textContent === '●';
                    if (currentState !== dragStartState) {
                        this.click();
                    }
                }
            });
        }
    });
    
    document.addEventListener('mouseup', function() {
        isDragging = false;
        dragStartState = null;
    });
}

// Setup drag selection after a short delay to ensure buttons are rendered
setTimeout(setupDragSelection, 500);

// Re-setup after each Streamlit rerun
const observer = new MutationObserver(function(mutations) {
    setTimeout(setupDragSelection, 100);
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});
</script>
""", unsafe_allow_html=True)
