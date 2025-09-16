# Erdlinge Scripts - PDF Processing Tool

This repository contains scripts to process various types of PDF documents related to payroll and reimbursements.

## Features

- **AAG Erstattungen**: Process AAG reimbursement PDFs and generate CSV reports with U1/U2 data
- **Abrechnungen**: Process payroll PDFs and generate Excel reports with allowances, working hours, and salary groups  
- **AG Belastung**: Process employer burden PDFs and generate Excel reports with cost breakdowns
- **Lohnjournal**: Process payroll journal PDFs and generate Excel reports with gross salary data

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface (CLI)

The original CLI scripts are preserved and can be used as before:

```bash
# Process AAG Erstattungen
python aag_erstattungen.py

# Process Abrechnungen  
python abrechnungen.py

# Process AG Belastung
python ag_belastung.py

# Process Lohnjournal
python lohnjournal.py
```

Each script expects PDF files to be placed in specific directory structures:
- `aag_erstattungen/2024/*.pdf`
- `abrechnungen/2024/*.pdf`
- `ag_belastung/2024/Jan-Dez.pdf`
- `lohnjournal/12.2024.pdf`

### Web Interface (Gradio App)

For a more user-friendly experience, use the Gradio web interface:

```bash
python gradio_app.py
```

This will start a web server at `http://localhost:7860` with tabs for each document type. You can:

1. Upload PDF files through the web interface
2. Specify the year for processing  
3. Click the process button
4. Download the generated CSV/Excel results

#### Features of the Web Interface:

- **Tabbed Interface**: Separate tabs for each document type
- **File Upload**: Drag-and-drop or click to upload PDF files
- **Real-time Processing**: See processing status and download results immediately
- **Multiple File Support**: Upload multiple files where supported (AAG, Abrechnungen)
- **Single File Support**: Upload single file where required (AG Belastung, Lohnjournal)

## File Formats

### Input
- PDF files containing the respective document types

### Output
- **AAG Erstattungen**: CSV file with semicolon-separated values
- **Abrechnungen**: Excel file with multiple sheets for different data categories
- **AG Belastung**: Excel file with employer cost breakdown
- **Lohnjournal**: Excel file with payroll summary data

## Dependencies

- `gradio` - Web interface framework
- `tika` - PDF text extraction  
- `pandas` - Data manipulation and Excel export
- `openpyxl` - Excel file handling
- `numpy` - Numerical computations

## Architecture

The code is structured to maximize reusability:

- `core_logic.py` - Contains the core processing functions extracted from the original CLI scripts
- `gradio_app.py` - Web interface implementation using the core logic
- `aag_erstattungen.py`, `abrechnungen.py`, `ag_belastung.py`, `lohnjournal.py` - CLI scripts that use the core logic

This design ensures that:
1. The original CLI functionality is preserved
2. Code is not duplicated
3. Bug fixes and improvements benefit both CLI and web interfaces
4. The core logic can be easily tested and maintained