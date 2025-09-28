# Erdlinge Scripts - Standalone Application Guide

This guide explains how to create and use standalone executable applications for the Erdlinge Scripts PDF processing tool.

## Quick Start

### Building Standalone Application

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Build executable:**
```bash
# Windows
build.bat

# Linux/macOS
./build.sh
```

3. **Run the application:**
- **Windows**: Double-click `dist/ErdlingeScripts.exe`
- **Linux/macOS**: Run `./dist/ErdlingeScripts` or `./dist/run.sh`

The application will automatically open in your default web browser.

## How It Works

The standalone application:
- Bundles Python runtime and all dependencies
- Starts a local web server on a random port
- Automatically opens the interface in your default browser
- Provides the same functionality as the CLI scripts
- Requires no Python installation on target machines

## Supported Platforms

- **Windows**: Creates `.exe` executable
- **Linux**: Creates standalone binary
- **macOS**: Creates standalone application

## File Sizes

The standalone executable will be approximately:
- **Windows**: ~150-200MB (includes Python runtime and all libraries)
- **Linux**: ~150-200MB
- **macOS**: ~150-200MB

## Distribution

The built executable can be distributed as a single file that includes:
- Python runtime
- All Python dependencies (Gradio, Tika, pandas, etc.)
- Application code and resources

End users simply need to:
1. Download the executable
2. Double-click to run
3. Use the web interface that opens automatically

## Troubleshooting

### Build Issues

**Problem**: PyInstaller not found
**Solution**: `pip install pyinstaller`

**Problem**: Build fails with import errors  
**Solution**: Ensure all dependencies are installed with `pip install -r requirements.txt`

### Runtime Issues

**Problem**: Application doesn't start
**Solution**: Run from command line to see error messages

**Problem**: Browser doesn't open automatically
**Solution**: Manually open browser and navigate to the URL shown in the console

**Problem**: Port already in use
**Solution**: The application automatically finds a free random port

## Advanced Usage

### Custom Build Configuration

The build process uses `build.spec` which can be customized:
- Add additional files to bundle
- Exclude unnecessary modules
- Change executable name or icon
- Modify console/windowed mode

### Manual Building

```bash
# Build using PyInstaller directly
pyinstaller build.spec --clean --noconfirm
```

### Development Mode

For testing during development:
```bash
python standalone_app.py  # Browser-based version
python gradio_app.py      # Fixed port version (7860)
```

## Architecture

The standalone application architecture:
1. **Entry Point**: `standalone_app.py`
2. **Core Logic**: `core_logic.py` (shared with CLI scripts)
3. **Web Interface**: Gradio-based tabbed interface
4. **PDF Processing**: Apache Tika for text extraction
5. **Output Generation**: pandas/openpyxl for CSV/Excel files

This ensures identical functionality between CLI scripts, web interface, and standalone application.