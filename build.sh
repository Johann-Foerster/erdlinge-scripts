#!/bin/bash
# Enhanced build script for creating standalone executables

echo "Building Erdlinge Scripts standalone executables..."

# Install PyInstaller and PyWebView if not already installed
pip install pyinstaller pywebview

# Create build directory
mkdir -p dist/

echo "Building standard standalone executable (browser-based)..."

# Build the standard executable using the spec file
pyinstaller build.spec --clean --noconfirm

echo "Building desktop executable (native window with PyWebView)..."

# Build the desktop executable using the desktop spec file
pyinstaller build_desktop.spec --clean --noconfirm

echo "Build completed!"
echo "Standard executable location: dist/ErdlingeScripts"
echo "Desktop executable location: dist/ErdlingeScriptsDesktop"

# Create run scripts for both versions
cat > dist/run_standard.sh << 'EOF'
#!/bin/bash
echo "Starting Erdlinge Scripts (Browser Version)..."
cd "$(dirname "$0")"
./ErdlingeScripts
EOF

cat > dist/run_desktop.sh << 'EOF'
#!/bin/bash
echo "Starting Erdlinge Scripts (Desktop Version)..."
cd "$(dirname "$0")"
./ErdlingeScriptsDesktop
EOF

chmod +x dist/run_standard.sh
chmod +x dist/run_desktop.sh

echo ""
echo "To run the applications:"
echo "  Standard (Browser) Version:"
echo "    - Windows: Double-click ErdlingeScripts.exe"
echo "    - Linux/Mac: ./ErdlingeScripts or ./run_standard.sh"
echo ""
echo "  Desktop (Native Window) Version:"
echo "    - Windows: Double-click ErdlingeScriptsDesktop.exe"  
echo "    - Linux/Mac: ./ErdlingeScriptsDesktop or ./run_desktop.sh"
echo ""
echo "The desktop version provides a native window experience!"