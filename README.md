# 🏢 Erdlinge Scripts - Document Processing Tool

A comprehensive document processing tool that converts various types of payroll and administrative PDF documents to Excel/CSV files. Available as both command-line interface (CLI) and web application (Gradio).

## 📋 Features

### Document Types Supported

1. **📊 Abrechnungen (Gehaltsabrechnungen)** - Payroll Documents
   - Processes multiple PDF files
   - Extracts salary information, allowances, and benefits
   - Outputs Excel file with multiple sheets for different categories

2. **💰 AG Belastung (Arbeitgeber-Belastung)** - Employer Burden
   - Processes single PDF file
   - Calculates employer costs and social security contributions
   - Outputs Excel file with detailed breakdown

3. **📄 AAG Erstattungen** - Reimbursements
   - Processes multiple PDF files
   - Handles U1 (sick leave) and U2 (maternity/disability) reimbursements
   - Outputs CSV file with categorized data

4. **📋 Lohnjournal** - Payroll Journal
   - Processes single PDF file
   - Extracts tax and gross salary information
   - Outputs Excel file with employee data

## 🚀 Quick Start

### Web Interface (Gradio App)

1. **Run the Web Application:**
   ```bash
   python gradio_app.py
   ```

2. **Access the Interface:**
   Open your browser to `http://localhost:7860`

3. **Use the Tool:**
   - Select the appropriate tab for your document type
   - Upload PDF file(s)
   - Configure year/month settings
   - Click "🚀 Verarbeiten" (Process)
   - Download the generated Excel/CSV file

### Command Line Interface

Each script can be run independently:

```bash
# Process payroll documents
python abrechnungen.py

# Process employer burden documents  
python ag_belastung.py

# Process reimbursement documents
python aag_erstattungen.py

# Process payroll journal
python lohnjournal.py
```

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Dependencies Include

- `gradio==5.49.1` - Web interface framework
- `pandas>=2.0.0` - Data manipulation and Excel/CSV export
- `tika>=2.6.0` - PDF text extraction
- `openpyxl>=3.1.0` - Excel file handling
- `numpy>=1.24.0` - Numerical operations
- `pyinstaller>=6.0.0` - Binary compilation

## 🔧 Building Standalone Binaries

### Quick Build

```bash
./build.sh
```

### Manual Build

```bash
# Install PyInstaller if not already installed
pip install pyinstaller

# Build the application
pyinstaller erdlinge-scripts.spec --clean
```

### Binary Locations

After building:
- **Linux/macOS:** `./dist/erdlinge-scripts/erdlinge-scripts`
- **Windows:** `dist\erdlinge-scripts\erdlinge-scripts.exe`

The binary will start a web server at `http://localhost:7860`

## 📁 Directory Structure

```
erdlinge-scripts/
├── gradio_app.py              # Main Gradio web application
├── core_processors.py         # Core processing logic
├── abrechnungen.py            # CLI script for payroll processing
├── ag_belastung.py            # CLI script for employer burden
├── aag_erstattungen.py        # CLI script for reimbursements
├── lohnjournal.py             # CLI script for payroll journal
├── requirements.txt           # Python dependencies
├── erdlinge-scripts.spec      # PyInstaller specification
├── build.sh                   # Build script for binaries
└── README.md                  # This file
```

## 🖼️ Screenshots

![Gradio App Interface](https://github.com/user-attachments/assets/542cf798-48e2-4489-ba00-0531f10b9870)

*The web interface provides an intuitive tabbed layout for different document types*

## 💻 Usage Examples

### Web Interface

1. **Processing Payroll Documents:**
   - Go to "📊 Abrechnungen" tab
   - Upload multiple PDF files
   - Set the year (e.g., "2024")
   - Click "🚀 Verarbeiten"
   - Download the generated Excel file

2. **Processing Employer Burden:**
   - Go to "💰 AG Belastung" tab
   - Upload a single PDF file
   - Set year (e.g., "2025") and month (e.g., "AUGUST")
   - Click "🚀 Verarbeiten"
   - Download the generated Excel file

### CLI Interface

The CLI scripts expect specific directory structures:

```bash
# For abrechnungen.py
abrechnungen/2024/*.pdf

# For ag_belastung.py  
ag_belastung/2025/August.pdf

# For aag_erstattungen.py
aag_erstattungen/2024/*.pdf

# For lohnjournal.py
lohnjournal/12.2024.pdf
```

## 🛠️ Development

### Architecture

- **core_processors.py:** Contains refactored processing logic extracted from original CLI scripts
- **gradio_app.py:** Web interface that uses the core processors
- **CLI scripts:** Preserved original functionality while using shared core logic

### Key Features

- **Minimal Changes:** Preserved all original CLI functionality
- **Shared Logic:** Core processing extracted to reusable functions
- **Modern Dependencies:** Uses Gradio 5.49.1 and latest package versions
- **Cross-Platform:** PyInstaller support for Windows, Linux, and macOS binaries
- **User Friendly:** Intuitive web interface with clear instructions

## 🔒 Security

- All file processing happens locally
- No data is sent to external services
- Temporary files are automatically cleaned up
- PDF processing uses the secure Tika library

## 📝 Notes

- **File Format:** Only PDF files are supported for input
- **Output Formats:** Excel (.xlsx) and CSV files
- **Language:** Interface is in German (German payroll processing tool)
- **Tika Dependency:** Requires Java runtime for PDF processing

## 🔧 Developed for Erdlinge-Verwaltung

This tool was specifically developed for the Erdlinge administration to streamline document processing workflows.