<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lab Buffer Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .header {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        
        .main-content {
            display: flex;
            gap: 30px;
        }
        
        .plate-section {
            flex: 2;
        }
        
        .results-section {
            flex: 1;
            background: #f9f9f9;
            padding: 20px;
            border-radius: 8px;
        }
        
        .plate-container {
            background: #fff;
            border: 3px solid #ddd;
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .plate-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .col-labels {
            display: flex;
            margin-left: 30px;
            margin-bottom: 5px;
        }
        
        .col-label {
            width: 35px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 12px;
            color: #666;
            cursor: pointer;
            margin: 1px;
            border-radius: 3px;
            transition: background-color 0.2s;
        }
        
        .col-label:hover {
            background-color: #e3f2fd;
        }
        
        .plate-row {
            display: flex;
            align-items: center;
            margin-bottom: 2px;
        }
        
        .row-label {
            width: 25px;
            height: 35px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: #666;
            margin-right: 5px;
        }
        
        .well {
            width: 35px;
            height: 35px;
            border: 2px solid #ccc;
            border-radius: 50%;
            margin: 1px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            font-weight: bold;
            user-select: none;
        }
        
        .well:hover {
            transform: scale(1.1);
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }
        
        .well-empty {
            background: linear-gradient(145deg, #f0f0f0, #e0e0e0);
            color: #999;
        }
        
        .well-filled {
            background: linear-gradient(145deg, #4CAF50, #45a049);
            border-color: #4CAF50;
            color: white;
            box-shadow: 0 2px 5px rgba(76, 175, 80, 0.3);
        }
        
        .controls {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.2s;
        }
        
        .btn-primary {
            background: #2196F3;
            color: white;
        }
        
        .btn-primary:hover {
            background: #1976D2;
        }
        
        .btn-success {
            background: #4CAF50;
            color: white;
        }
        
        .btn-success:hover {
            background: #45a049;
        }
        
        .btn-danger {
            background: #f44336;
            color: white;
        }
        
        .btn-danger:hover {
            background: #d32f2f;
        }
        
        .input-group {
            margin: 10px 0;
        }
        
        .input-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        
        .input-group input {
            width: 100%;
            padding: 8px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        
        .metrics {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 20px 0;
        }
        
        .metric {
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #2196F3;
        }
        
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #2196F3;
        }
        
        .metric-label {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
        
        .buffer-results {
            background: white;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }
        
        .buffer-item {
            display: flex;
            justify-content: between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        
        .buffer-item:last-child {
            border-bottom: none;
        }
        
        .buffer-name {
            font-weight: bold;
            flex: 1;
        }
        
        .buffer-volume {
            color: #2196F3;
            font-weight: bold;
        }
        
        .safety-margin {
            margin: 15px 0;
        }
        
        .instructions {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #2196F3;
        }
        
        .drag-info {
            position: absolute;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 12px;
            pointer-events: none;
            z-index: 1000;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Lab Buffer Calculator</h1>
            <p>Interactive 96-well plate buffer calculation tool</p>
        </div>
        
        <div class="instructions">
            <strong>Instructions:</strong>
            <ul>
                <li><strong>Click wells</strong> to toggle filled/empty status</li>
                <li><strong>Click column numbers</strong> to select/deselect entire columns</li>
                <li><strong>Hold and drag</strong> across wells to select multiple wells at once</li>
                <li>Use the control buttons below for quick operations</li>
            </ul>
        </div>
        
        <div class="main-content">
            <div class="plate-section">
                <h3>96-Well Plate Layout</h3>
                
                <div class="controls">
                    <button class="btn btn-success" onclick="fillAll()">Fill All</button>
                    <button class="btn btn-danger" onclick="clearAll()">Clear All</button>
                    <button class="btn btn-primary" onclick="fillPattern()">Fill Pattern</button>
                    <button class="btn btn-primary" onclick="toggleDragMode()">
                        <span id="dragModeText">Enable Drag Select</span>
                    </button>
                </div>
                
                <div class="input-group">
                    <label>Fill specific wells (e.g., A1,B2,C3-C5):</label>
                    <input type="text" id="wellInput" placeholder="A1,B2,C3-C5" onkeypress="if(event.key==='Enter') fillSpecific()">
                    <button class="btn btn-primary" onclick="fillSpecific()" style="margin-top: 5px;">Apply</button>
                </div>
                
                <div class="plate-container">
                    <div class="col-labels" id="colLabels"></div>
                    <div id="plateGrid"></div>
                </div>
            </div>
            
            <div class="results-section">
                <h3>Results</h3>
                
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-value" id="filledWells">0</div>
                        <div class="metric-label">Filled Wells</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value" id="totalReactions">0</div>
                        <div class="metric-label">Total Reactions</div>
                    </div>
                </div>
                
                <div class="input-group">
                    <label>Extra reactions:</label>
                    <input type="number" id="extraReactions" value="5" min="0" onchange="updateCalculations()">
                </div>
                
                <div class="safety-margin">
                    <label><strong>Safety margin:</strong></label>
                    <select id="safetyMargin" onchange="updateCalculations()">
                        <option value="1.1">10% extra</option>
                        <option value="1.2" selected>20% extra</option>
                        <option value="1.5">50% extra</option>
                    </select>
                </div>
                
                <div class="buffer-results">
                    <h4>Buffer Volumes Needed:</h4>
                    <div id="bufferCalculations"></div>
                </div>
                
                <button class="btn btn-success" onclick="exportResults()" style="width: 100%; margin-top: 15px;">
                    Export Results
                </button>
            </div>
        </div>
    </div>
    
    <div class="drag-info" id="dragInfo">Dragging...</div>
    
    <script>
        // Plate state: 8 rows (A-H) x 12 columns (1-12)
        let plateState = Array(8).fill().map(() => Array(12).fill(false));
        let isDragging = false;
        let dragMode = false;
        let dragStartState = null;
        
        // Buffer composition per reaction (in µl)
        const bufferComposition = {
            'Buffer VXL': 100,
            'Buffer ACB': 400,
            'MagAttract Suspension G': 25,
            'Carrier RNA': 1
        };
        
        function initializePlate() {
            // Create column labels
            const colLabels = document.getElementById('colLabels');
            colLabels.innerHTML = '<div style="width: 25px;"></div>'; // Space for row labels
            for (let col = 1; col <= 12; col++) {
                const colLabel = document.createElement('div');
                colLabel.className = 'col-label';
                colLabel.textContent = col;
                colLabel.onclick = () => toggleColumn(col - 1);
                colLabels.appendChild(colLabel);
            }
            
            // Create plate grid
            const plateGrid = document.getElementById('plateGrid');
            plateGrid.innerHTML = '';
            
            for (let row = 0; row < 8; row++) {
                const plateRow = document.createElement('div');
                plateRow.className = 'plate-row';
                
                // Row label
                const rowLabel = document.createElement('div');
                rowLabel.className = 'row-label';
                rowLabel.textContent = String.fromCharCode(65 + row);
                plateRow.appendChild(rowLabel);
                
                // Wells
                for (let col = 0; col < 12; col++) {
                    const well = document.createElement('div');
                    well.className = 'well well-empty';
                    well.id = `well-${row}-${col}`;
                    well.dataset.row = row;
                    well.dataset.col = col;
                    
                    // Mouse events for clicking and dragging
                    well.onmousedown = (e) => handleMouseDown(e, row, col);
                    well.onmouseover = (e) => handleMouseOver(e, row, col);
                    well.onmouseup = () => handleMouseUp();
                    
                    plateRow.appendChild(well);
                }
                
                plateGrid.appendChild(plateRow);
            }
            
            // Global mouse events
            document.onmouseup = () => {
                isDragging = false;
                dragStartState = null;
                document.getElementById('dragInfo').style.display = 'none';
            };
            
            updateCalculations();
        }
        
        function handleMouseDown(e, row, col) {
            e.preventDefault();
            if (dragMode) {
                isDragging = true;
                dragStartState = !plateState[row][col];
                toggleWell(row, col, dragStartState);
                
                const dragInfo = document.getElementById('dragInfo');
                dragInfo.style.display = 'block';
                dragInfo.style.left = e.pageX + 10 + 'px';
                dragInfo.style.top = e.pageY - 30 + 'px';
            } else {
                toggleWell(row, col);
            }
        }
        
        function handleMouseOver(e, row, col) {
            if (isDragging && dragMode) {
                toggleWell(row, col, dragStartState);
                
                const dragInfo = document.getElementById('dragInfo');
                dragInfo.style.left = e.pageX + 10 + 'px';
                dragInfo.style.top = e.pageY - 30 + 'px';
            }
        }
        
        function handleMouseUp() {
            isDragging = false;
            dragStartState = null;
            document.getElementById('dragInfo').style.display = 'none';
        }
        
        function toggleWell(row, col, forceState = null) {
            const newState = forceState !== null ? forceState : !plateState[row][col];
            plateState[row][col] = newState;
            
            const well = document.getElementById(`well-${row}-${col}`);
            well.className = newState ? 'well well-filled' : 'well well-empty';
            
            updateCalculations();
        }
        
        function toggleColumn(col) {
            // Check if column is fully filled
            const isColumnFilled = plateState.every(row => row[col]);
            const newState = !isColumnFilled;
            
            for (let row = 0; row < 8; row++) {
                plateState[row][col] = newState;
                const well = document.getElementById(`well-${row}-${col}`);
                well.className = newState ? 'well well-filled' : 'well well-empty';
            }
            
            updateCalculations();
        }
        
        function fillAll() {
            for (let row = 0; row < 8; row++) {
                for (let col = 0; col < 12; col++) {
                    plateState[row][col] = true;
                    const well = document.getElementById(`well-${row}-${col}`);
                    well.className = 'well well-filled';
                }
            }
            updateCalculations();
        }
        
        function clearAll() {
            for (let row = 0; row < 8; row++) {
                for (let col = 0; col < 12; col++) {
                    plateState[row][col] = false;
                    const well = document.getElementById(`well-${row}-${col}`);
                    well.className = 'well well-empty';
                }
            }
            updateCalculations();
        }
        
        function fillPattern() {
            const pattern = prompt("Enter pattern (e.g., 'rows:A,B,C' or 'cols:1,2,3' or 'checkerboard'):");
            if (!pattern) return;
            
            if (pattern.toLowerCase() === 'checkerboard') {
                for (let row = 0; row < 8; row++) {
                    for (let col = 0; col < 12; col++) {
                        const shouldFill = (row + col) % 2 === 0;
                        plateState[row][col] = shouldFill;
                        const well = document.getElementById(`well-${row}-${col}`);
                        well.className = shouldFill ? 'well well-filled' : 'well well-empty';
                    }
                }
            } else if (pattern.startsWith('rows:')) {
                const rows = pattern.substring(5).split(',').map(r => r.trim().toUpperCase());
                rows.forEach(rowLetter => {
                    const rowIndex = rowLetter.charCodeAt(0) - 65;
                    if (rowIndex >= 0 && rowIndex < 8) {
                        for (let col = 0; col < 12; col++) {
                            plateState[rowIndex][col] = true;
                            const well = document.getElementById(`well-${rowIndex}-${col}`);
                            well.className = 'well well-filled';
                        }
                    }
                });
            } else if (pattern.startsWith('cols:')) {
                const cols = pattern.substring(5).split(',').map(c => parseInt(c.trim()) - 1);
                cols.forEach(colIndex => {
                    if (colIndex >= 0 && colIndex < 12) {
                        for (let row = 0; row < 8; row++) {
                            plateState[row][colIndex] = true;
                            const well = document.getElementById(`well-${row}-${colIndex}`);
                            well.className = 'well well-filled';
                        }
                    }
                });
            }
            
            updateCalculations();
        }
        
        function fillSpecific() {
            const input = document.getElementById('wellInput').value.trim();
            if (!input) return;
            
            const wells = input.split(',').map(w => w.trim().toUpperCase());
            
            wells.forEach(wellRange => {
                if (wellRange.includes('-')) {
                    // Handle range like A1-A5
                    const [start, end] = wellRange.split('-');
                    const startRow = start.charCodeAt(0) - 65;
                    const startCol = parseInt(start.substring(1)) - 1;
                    const endRow = end.charCodeAt(0) - 65;
                    const endCol = parseInt(end.substring(1)) - 1;
                    
                    for (let row = Math.min(startRow, endRow); row <= Math.max(startRow, endRow); row++) {
                        for (let col = Math.min(startCol, endCol); col <= Math.max(startCol, endCol); col++) {
                            if (row >= 0 && row < 8 && col >= 0 && col < 12) {
                                plateState[row][col] = true;
                                const well = document.getElementById(`well-${row}-${col}`);
                                well.className = 'well well-filled';
                            }
                        }
                    }
                } else {
                    // Handle single well like A1
                    const row = wellRange.charCodeAt(0) - 65;
                    const col = parseInt(wellRange.substring(1)) - 1;
                    
                    if (row >= 0 && row < 8 && col >= 0 && col < 12) {
                        plateState[row][col] = true;
                        const well = document.getElementById(`well-${row}-${col}`);
                        well.className = 'well well-filled';
                    }
                }
            });
            
            document.getElementById('wellInput').value = '';
            updateCalculations();
        }
        
        function toggleDragMode() {
            dragMode = !dragMode;
            const dragModeText = document.getElementById('dragModeText');
            dragModeText.textContent = dragMode ? 'Disable Drag Select' : 'Enable Drag Select';
            
            // Change cursor style
            const plateContainer = document.querySelector('.plate-container');
            plateContainer.style.cursor = dragMode ? 'crosshair' : 'default';
        }
        
        function updateCalculations() {
            // Count filled wells
            let filledCount = 0;
            for (let row = 0; row < 8; row++) {
                for (let col = 0; col < 12; col++) {
                    if (plateState[row][col]) filledCount++;
                }
            }
            
            const extraReactions = parseInt(document.getElementById('extraReactions').value) || 0;
            const totalReactions = filledCount + extraReactions;
            const safetyMargin = parseFloat(document.getElementById('safetyMargin').value);
            
            // Update metrics
            document.getElementById('filledWells').textContent = filledCount;
            document.getElementById('totalReactions').textContent = totalReactions;
            
            // Calculate buffer volumes
            const bufferCalc = document.getElementById('bufferCalculations');
            bufferCalc.innerHTML = '';
            
            if (totalReactions > 0) {
                let totalVolume = 0;
                
                Object.entries(bufferComposition).forEach(([name, volumePerReaction]) => {
                    const baseVolume = volumePerReaction * totalReactions;
                    const finalVolume = Math.ceil(baseVolume * safetyMargin);
                    totalVolume += finalVolume;
                    
                    const item = document.createElement('div');
                    item.className = 'buffer-item';
                    item.innerHTML = `
                        <div class="buffer-name">${name}:</div>
                        <div class="buffer-volume">${finalVolume.toLocaleString()} µl (${(finalVolume/1000).toFixed(2)} ml)</div>
                    `;
                    bufferCalc.appendChild(item);
                });
                
                // Add total
                const totalItem = document.createElement('div');
                totalItem.className = 'buffer-item';
                totalItem.style.borderTop = '2px solid #2196F3';
                totalItem.style.marginTop = '10px';
                totalItem.style.paddingTop = '10px';
                totalItem.innerHTML = `
                    <div class="buffer-name"><strong>Total Volume:</strong></div>
                    <div class="buffer-volume"><strong>${totalVolume.toLocaleString()} µl (${(totalVolume/1000).toFixed(2)} ml)</strong></div>
                `;
                bufferCalc.appendChild(totalItem);
            } else {
                bufferCalc.innerHTML = '<p style="text-align: center; color: #666;">Select wells to see calculations</p>';
            }
        }
        
        function exportResults() {
            const filledCount = document.getElementById('filledWells').textContent;
            const totalReactions = document.getElementById('totalReactions').textContent;
            const safetyMargin = parseFloat(document.getElementById('safetyMargin').value);
            
            let csvContent = "data:text/csv;charset=utf-8,";
            csvContent += "Lab Buffer Calculator Results\n";
            csvContent += `Date,${new Date().toLocaleDateString()}\n`;
            csvContent += `Filled Wells,${filledCount}\n`;
            csvContent += `Total Reactions,${totalReactions}\n`;
            csvContent += `Safety Margin,${((safetyMargin - 1) * 100).toFixed(0)}%\n\n`;
            csvContent += "Reagent,Per Reaction (µl),Total Volume (µl),Total Volume (ml)\n";
            
            Object.entries(bufferComposition).forEach(([name, volumePerReaction]) => {
                const baseVolume = volumePerReaction * parseInt(totalReactions);
                const finalVolume = Math.ceil(baseVolume * safetyMargin);
                csvContent += `${name},${volumePerReaction},${finalVolume},${(finalVolume/1000).toFixed(2)}\n`;
            });
            
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", `buffer_calculation_${filledCount}_wells.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
        
        // Initialize the plate when page loads
        window.onload = initializePlate;
    </script>
</body>
</html>
