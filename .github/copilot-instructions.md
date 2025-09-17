# Copilot Instructions for Erdlinge Scripts

This repository contains PDF processing scripts for German payroll and reimbursement documents. The codebase includes both CLI scripts and a Gradio web interface.

## Repository Overview

### Purpose
- Process various types of German payroll-related PDF documents
- Extract structured data from PDFs using Apache Tika
- Generate CSV and Excel reports
- Provide both command-line and web interfaces

### Key Document Types
1. **AAG Erstattungen** - AAG reimbursement documents (outputs CSV with U1/U2 categorization)
2. **Abrechnungen** - Payroll documents (outputs Excel with allowances, working hours, salary groups)
3. **AG Belastung** - Employer burden documents (outputs Excel with cost breakdowns)
4. **Lohnjournal** - Payroll journal documents (outputs Excel with gross salary data)

## Architecture

### Core Components
- `core_logic.py` - Shared processing functions extracted from CLI scripts
- `gradio_app.py` - German-localized web interface using Gradio
- `aag_erstattungen.py`, `abrechnungen.py`, `ag_belastung.py`, `lohnjournal.py` - CLI scripts
- `requirements.txt` - Python dependencies

### Design Principles
- **Code Reusability**: Core logic is shared between CLI and web interfaces
- **No Breaking Changes**: CLI scripts maintain backward compatibility
- **German Localization**: All UI elements and documentation in German
- **Single Source of Truth**: Identical processing logic for both interfaces

## Development Guidelines

### Language and Localization
- **Primary Language**: German for all user-facing content
- **UI Elements**: All buttons, labels, messages in German
- **Documentation**: README and comments in German
- **Error Messages**: User-facing errors in German, technical logs can be English

### PDF Processing
- Use Apache Tika for PDF text extraction
- Handle German number formats (comma as decimal separator)
- Process structured payroll data with regex patterns
- Extract employee names, amounts, dates, and classifications

### Data Formats
- **Input**: PDF files with specific German payroll document structures
- **Output**: 
  - CSV with semicolon separators (German standard)
  - Excel files with multiple sheets and German column headers
  - German number formatting (comma decimal separator)

### File Structure Expectations
```
aag_erstattungen/2024/*.pdf
abrechnungen/2024/*.pdf
ag_belastung/2024/Jan-Dez.pdf
lohnjournal/12.2024.pdf
```

## Coding Standards

### Code Style
- Use descriptive German variable names for domain-specific concepts
- Keep English for technical programming terms
- Follow Python PEP 8 conventions
- Use type hints where appropriate

### Error Handling
- Graceful handling of malformed PDFs
- Clear German error messages for users
- Fallback values for missing data fields
- Validation of expected PDF structures

### Dependencies
- **Core**: tika, pandas, openpyxl, numpy
- **Web Interface**: gradio
- Avoid adding unnecessary dependencies
- Pin versions for stability

## Testing and Validation

### Manual Testing
- Test CLI scripts with sample PDF files
- Verify web interface functionality
- Check German number formatting in outputs
- Validate Excel/CSV structure and content

### Expected Behavior
- CLI scripts should work independently
- Web interface should provide identical results to CLI
- Error handling should be user-friendly in German
- File uploads should support drag-and-drop

## Common Patterns

### PDF Text Extraction
```python
def get_pages(filename):
    raw_xml = parser.from_file(filename, xmlContent=True)
    # Clean HTML tags and extract page content
```

### German Number Parsing
```python
def parse_float(float_str_eu: str):
    return float(float_str_eu.replace(".", "").replace(",", "."))
```

### Excel Generation
```python
with ExcelWriter(filename, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Sheet", index=True)
```

## When Making Changes

### Preserve Compatibility
- CLI scripts must continue working without changes
- Maintain expected file input/output locations
- Keep existing function signatures stable

### Update Both Interfaces
- Changes to processing logic should be made in `core_logic.py`
- Both CLI and web interfaces will automatically benefit
- Test both interfaces after any changes

### German Localization
- All new UI elements must be in German
- Use appropriate German terminology for payroll concepts
- Maintain consistent translation style

### Documentation
- Update German README for user-facing changes
- Add German comments for complex business logic
- Keep architecture documentation current

## Domain Knowledge

### German Payroll Context
- **U1/U2**: German social security categories (sickness/maternity)
- **TVöD**: German public sector pay scale
- **Arbeitsmarktzulage**: Labor market allowance
- **Münchenzulage**: Munich cost-of-living allowance
- **Fahrtkostenzuschuss**: Travel cost subsidy

### PDF Structure Expectations
- Documents contain structured text with employee data
- Multiple employees per document common
- German date formats (DD.MM.YYYY)
- Euro amounts with German formatting

This repository serves German payroll administrators who need to process PDF documents efficiently while maintaining accuracy and compliance with German payroll standards.