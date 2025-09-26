#!/bin/bash
# Build script for creating standalone executables

echo "Building Erdlinge Scripts standalone executables..."

# Install PyInstaller if not already installed
pip install pyinstaller

# Create build directory
mkdir -p dist/

echo "Building standalone executable..."

# Build the executable using the spec file
pyinstaller build.spec --clean --noconfirm

echo "Build completed!"
echo "Executable location: dist/ErdlingeScripts"

# Create a simple run script for Unix systems
cat > dist/run.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
./ErdlingeScripts
EOF

chmod +x dist/run.sh

echo "To run the application:"
echo "  - On Windows: Double-click ErdlingeScripts.exe"
echo "  - On Linux/Mac: Run ./ErdlingeScripts or use ./run.sh"