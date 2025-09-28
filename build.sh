#!/bin/bash
# Simple build script for creating standalone executable

echo "Building Erdlinge Scripts standalone executable..."

# Install PyInstaller if not already installed
pip install pyinstaller

# Create build directory
mkdir -p dist/

echo "Building standalone executable (browser-based)..."

# Build the executable using the spec file
pyinstaller build.spec --clean --noconfirm

echo "Build completed!"
echo "Executable location: dist/ErdlingeScripts"

# Create run script
cat > dist/run.sh << 'EOL'
#!/bin/bash
echo "Starting Erdlinge Scripts..."
cd "$(dirname "$0")"
./ErdlingeScripts
EOL

chmod +x dist/run.sh

echo ""
echo "To run the application:"
echo "  - Windows: Double-click ErdlingeScripts.exe"
echo "  - Linux/Mac: ./ErdlingeScripts or ./run.sh"
echo ""
echo "The application will automatically open in your default browser!"
