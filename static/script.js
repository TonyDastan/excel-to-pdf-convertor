const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const fileInfo = document.getElementById('file-info');
const form = document.getElementById('upload-form');
const resultDiv = document.getElementById('result');
const modeBtns = document.querySelectorAll('.mode-btn');
const stepTitle = document.getElementById('step-title');
const submitBtn = document.getElementById('submit-btn');

let currentMode = 'single';

// Mode selection
modeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        modeBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentMode = btn.dataset.mode;
        
        if (currentMode === 'batch') {
            stepTitle.textContent = 'Step 1: Upload Excel Files (Folder)';
            dropZone.textContent = 'Drag & Drop Your Excel Files Here or Click to Browse';
            fileInput.removeAttribute('multiple');
            fileInput.setAttribute('webkitdirectory', 'webkitdirectory');
            fileInput.setAttribute('directory', 'directory');
            submitBtn.textContent = 'Convert All to PDF';
        } else {
            stepTitle.textContent = 'Step 1: Upload Excel File';
            dropZone.textContent = 'Drag & Drop Your Excel File Here or Click to Browse';
            fileInput.removeAttribute('webkitdirectory');
            fileInput.removeAttribute('directory');
            fileInput.removeAttribute('multiple');
            submitBtn.textContent = 'Convert to PDF';
        }
        
        // Reset file input and UI
        fileInput.value = '';
        fileInfo.classList.add('hidden');
        fileInfo.textContent = '';
    });
});

dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');

    const files = Array.from(e.dataTransfer.files);
    const excelFiles = files.filter(file => 
        file.name.endsWith('.xlsx') || 
        file.name.endsWith('.xls') || 
        file.name.endsWith('.csv')
    );

    if (excelFiles.length > 0) {
        fileInput.files = e.dataTransfer.files;
        dropZone.classList.add('hidden');
        fileInfo.classList.remove('hidden');
        
        if (currentMode === 'batch') {
            fileInfo.textContent = `✅ ${excelFiles.length} Excel file(s) loaded`;
        } else {
            fileInfo.textContent = `✅ File loaded: ${excelFiles[0].name}`;
            // Auto-fill title for single file mode
            const titleWithoutExt = excelFiles[0].name.substring(0, excelFiles[0].name.lastIndexOf('.')) || excelFiles[0].name;
            document.getElementById('title').value = titleWithoutExt.toUpperCase();
            // Set today's date
            const today = new Date().toISOString().split('T')[0];
            document.getElementById('report-date').value = today;
        }
    } else {
        alert("Please drop Excel files (.xlsx, .xls, or .csv)");
    }
});

fileInput.addEventListener('change', () => {
    const files = fileInput.files;
    if (files.length > 0) {
        dropZone.classList.add('hidden');
        fileInfo.classList.remove('hidden');
        
        if (currentMode === 'batch') {
            // Count Excel files in the selection
            const excelFiles = Array.from(files).filter(f => 
                f.name.endsWith('.xlsx') || 
                f.name.endsWith('.xls') || 
                f.name.endsWith('.csv')
            );
            fileInfo.textContent = `✅ ${excelFiles.length} Excel file(s) loaded`;
        } else {
            fileInfo.textContent = `✅ File loaded: ${files[0].name}`;
            
            // Auto-fill title with filename (without extension)
            const filename = files[0].name;
            const titleWithoutExt = filename.substring(0, filename.lastIndexOf('.')) || filename;
            document.getElementById('title').value = titleWithoutExt.toUpperCase();
            
            // Set today's date as default
            const today = new Date().toISOString().split('T')[0];
            document.getElementById('report-date').value = today;
        }
    }
});

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const files = fileInput.files;
    if (!files.length) {
        alert("Please select Excel file(s)!");
        return;
    }

    const formData = new FormData();
    
    if (currentMode === 'batch') {
        // Batch mode - add all Excel files
        for (let file of files) {
            if (file.name.endsWith('.xlsx') || file.name.endsWith('.xls') || file.name.endsWith('.csv')) {
                formData.append('files[]', file);
            }
        }
    } else {
        // Single mode - add only the first file
        formData.append('file', files[0]);
        formData.append('title', document.getElementById('title').value);
    }
    
    formData.append('subtitle', document.getElementById('subtitle').value);
    formData.append('report_date', document.getElementById('report-date').value);

    resultDiv.innerHTML = "<p class='loading'>Converting to PDF... Please wait...</p>";
    
    try {
        const endpoint = currentMode === 'batch' ? '/batch-convert' : '/convert';
        const response = await fetch(endpoint, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            
            if (currentMode === 'batch') {
                a.download = "attendance_reports.zip";
                a.textContent = "📥 Download All PDFs (ZIP)";
            } else {
                // Get the filename from the input
                const filename = fileInput.files[0].name;
                const pdfFilename = filename.substring(0, filename.lastIndexOf('.')) + '.pdf';
                a.download = pdfFilename;
                a.textContent = "📥 Download PDF";
            }
            
            a.className = 'download-link';
            resultDiv.innerHTML = "";
            resultDiv.appendChild(a);
        } else {
            const error = await response.json();
            resultDiv.innerHTML = `<p class='error'>Error: ${error.error}</p>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<p class='error'>Error converting file(s): ${error.message}</p>`;
    }
});
