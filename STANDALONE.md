# Erdlinge Scripts - Standalone Application Guide

This guide explains how to create and use standalone executable applications for the Erdlinge Scripts PDF processing tool, including the new native desktop application using PyWebView.

## WSL2/Linux Installation Issues

### Common WSL2 Problems

**Problem: PyQt6 Installation Fails**
WSL2 and Linux systems require system-level GUI packages that pip cannot install.

**Solution:**
```bash
# For WSL2 (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3-gi python3-gi-cairo gir1.2-webkit2-4.0
sudo apt-get install python3-pyqt5 python3-pyqt5.qtwebkit

# Enable GUI forwarding
export DISPLAY=:0  # For X11 forwarding
# OR use WSLg on Windows 11 (no DISPLAY setup needed)

# Then install Python dependencies
pip install -r requirements.txt
```

**For other Linux distributions:**
```bash
# Fedora/RHEL
sudo dnf install python3-qt5 python3-qt5-devel python3-qt5-webkit

# Arch Linux
sudo pacman -S python-pyqt5 python-pyqt5-webkit

# Then install Python dependencies
pip install -r requirements.txt
```

### Display Setup for WSL2

**Option 1: Windows 11 WSLg (Recommended)**
Windows 11 includes built-in GUI support - no additional setup needed.

**Option 2: X11 Forwarding**
```bash
# Install X11 server on Windows (e.g., VcXsrv, Xming)
# Set DISPLAY variable in WSL2
export DISPLAY=:0
# Or add to ~/.bashrc for persistence
echo 'export DISPLAY=:0' >> ~/.bashrc
```

### Quick Start
Download the pre-built executable for your operating system:

**Native Desktop Applications (Recommended):**
- **Windows**: `ErdlingeScriptsDesktop.exe`
- **macOS**: `ErdlingeScriptsDesktop` (macOS app bundle)
- **Linux**: `ErdlingeScriptsDesktop` (Linux executable)

**Browser-Based Applications:**
- **Windows**: `ErdlingeScripts.exe`
- **macOS**: `ErdlingeScripts` (macOS app bundle)
- **Linux**: `ErdlingeScripts` (Linux executable)

### Usage
1. Double-click the executable file
2. **Desktop Version**: Opens in a native desktop window
3. **Browser Version**: Opens automatically in your default web browser
4. Use the interface to upload and process PDF files

### Features Comparison

| Feature | Desktop App | Browser App |
|---------|-------------|-------------|
| Native Window | ✅ | ❌ |
| Browser Required | ❌ | ✅ |
| Offline Operation | ✅ | ✅ |
| OS Integration | ✅ | ⚠️ |
| File Dialogs | Native | Web-based |
| Professional Look | ✅ | ⚠️ |
| Memory Usage | Lower | Higher |

## For Developers

### Building Standalone Applications

#### Prerequisites
```bash
# Full installation (recommended)
pip install -r requirements.txt

# If PyWebView fails, install GUI backend manually:
# Windows/Linux: pip install PyQt5
# Linux alternative: sudo apt-get install python3-gi python3-gi-cairo gir1.2-webkit2-4.0
# macOS: pip install pywebview (uses system WebView)
```

**Common PyWebView Installation Issues:**
- **Windows**: Install Visual C++ Redistributable if PyQt5/PyQt6 fails
- **Linux**: Install GTK development headers: `sudo apt-get install libgtk-3-dev`
- **macOS**: Ensure Xcode Command Line Tools are installed: `xcode-select --install`

#### Building for Your Platform
```bash
# Install all dependencies including PyWebView and GUI backends
pip install -r requirements.txt

# Build both versions
# On Windows
build.bat

# On Linux/macOS
chmod +x build.sh
./build.sh
```

This creates two executables:
- **Desktop Version**: Native window application using PyWebView
- **Browser Version**: Traditional web application that opens in browser

#### Manual PyInstaller Build
```bash
# Desktop version (PyWebView)
pyinstaller build_desktop.spec --clean --noconfirm

# Browser version (traditional)
pyinstaller build.spec --clean --noconfirm
```

### Development Mode
For development and testing, you can run the applications directly:

```bash
# Desktop application (PyWebView - native window)
python desktop_app.py

# Standard Gradio app (fixed port 7860)
python gradio_app.py

# Standalone app (random port + auto browser opening)
python standalone_app.py

# Using convenience scripts
# Windows:
start_desktop.bat  # Desktop version
start.bat          # Browser version

# Linux/macOS:
./start_desktop.sh # Desktop version
./start.sh         # Browser version
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