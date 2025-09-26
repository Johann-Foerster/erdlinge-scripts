# Erdlinge Scripts - Standalone Application Guide

This guide explains how to create and use standalone executable applications for the Erdlinge Scripts PDF processing tool.

## For End Users (Non-Developers)

### Quick Start
1. Download the pre-built executable for your operating system:
   - **Windows**: `ErdlingeScripts.exe`
   - **macOS**: `ErdlingeScripts` (macOS app bundle)
   - **Linux**: `ErdlingeScripts` (Linux executable)

2. Double-click the executable file
3. The application will automatically:
   - Find a free port on your system
   - Start the web server
   - Open your default web browser
   - Display the PDF processing interface

4. Use the web interface to upload and process PDF files

### Features
- **No Python Installation Required**: All dependencies are bundled
- **Auto-Browser Opening**: Automatically opens in your default browser
- **Random Port Selection**: Avoids conflicts with other applications
- **German Interface**: Fully localized German user interface
- **File Processing**: Same functionality as CLI scripts but with GUI

## For Developers

### Building Standalone Applications

#### Prerequisites
```bash
pip install -r requirements.txt
```

#### Building for Your Platform
```bash
# On Windows
build.bat

# On Linux/macOS
chmod +x build.sh
./build.sh
```

#### Manual PyInstaller Build
```bash
pyinstaller build.spec --clean --noconfirm
```

### Development Mode
For development and testing, you can run the standalone app directly:

```bash
# Standard Gradio app (fixed port 7860)
python gradio_app.py

# Standalone app (random port + auto browser opening)
python standalone_app.py

# Using convenience scripts
# Windows:
start.bat

# Linux/macOS:
./start.sh
```

## Technical Details

### Differences from Standard Gradio App
- **Port Selection**: Uses `find_free_port()` to avoid conflicts
- **Browser Control**: Automatically opens browser after 1.5 second delay
- **Error Handling**: Better error messages for standalone usage
- **Console Output**: User-friendly German messages

### File Structure
```
erdlinge-scripts/
├── standalone_app.py       # Main standalone application
├── build.spec             # PyInstaller specification
├── build.sh              # Linux/macOS build script
├── build.bat             # Windows build script
├── start.sh              # Linux/macOS convenience launcher
├── start.bat             # Windows convenience launcher
├── core_logic.py         # Shared processing functions
├── gradio_app.py         # Original web interface
└── dist/                 # Build output directory (created after build)
    ├── ErdlingeScripts    # Executable (Linux/macOS)
    ├── ErdlingeScripts.exe # Executable (Windows)
    └── run.sh            # Unix run script
```

### Included Dependencies
The standalone executable includes:
- Python runtime
- Gradio web framework
- Apache Tika for PDF processing
- Pandas for data manipulation
- OpenPyXL for Excel generation
- NumPy for numerical operations
- All other required libraries

### Platform-Specific Notes

#### Windows
- Executable: `ErdlingeScripts.exe`
- Console window shows status messages
- Windows Defender may require approval for first run

#### macOS
- Application bundle or single executable
- May require "Allow apps downloaded from anywhere" setting
- Gatekeeper approval needed for unsigned builds

#### Linux
- Single executable file
- Requires execute permissions: `chmod +x ErdlingeScripts`
- May need additional libraries on minimal distributions

## Troubleshooting

### Common Issues
1. **Port Already in Use**: The app automatically finds a free port
2. **Browser Doesn't Open**: Check firewall settings, manually navigate to displayed URL
3. **Antivirus Warnings**: Add executable to antivirus whitelist
4. **Missing Libraries**: Standalone version includes all dependencies

### Manual Browser Access
If the browser doesn't open automatically, look for this message in the console:
```
Anwendung läuft auf: http://localhost:[PORT]
```

Navigate to that URL manually in your browser.

### Performance
- First startup may be slower due to unpacking
- Processing speed is identical to Python version
- Temporary files are cleaned automatically

## Distribution

### Creating Distribution Packages

#### Windows
```bash
# Create installer (requires Inno Setup)
iscc erdlinge-scripts-installer.iss
```

#### macOS
```bash
# Create DMG package
hdiutil create -volname "Erdlinge Scripts" -srcfolder dist/ -ov erdlinge-scripts.dmg
```

#### Linux
```bash
# Create AppImage (requires appimagetool)
appimagetool dist/ erdlinge-scripts.AppImage
```

### File Sizes
- Windows executable: ~150-200 MB
- macOS executable: ~150-200 MB  
- Linux executable: ~150-200 MB

Large size due to bundled Python runtime and dependencies.

## Support

For issues with the standalone application:
1. Check that you're using the correct version for your OS
2. Verify that no antivirus software is blocking execution
3. Check console output for error messages
4. Try running from command line for detailed error information