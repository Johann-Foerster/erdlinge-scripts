#!/bin/bash
"""
Build script for creating cross-platform binaries of the Erdlinge Scripts Gradio App.
Usage: ./build.sh [platform]
where platform can be: windows, linux, macos, all
"""

set -e

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🔧 Building Erdlinge Scripts Gradio App..."

# Install dependencies if not already installed
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/

# Build with PyInstaller
echo "🚀 Building executable..."
pyinstaller erdlinge-scripts.spec --clean

# Check if build was successful
if [ -d "dist/erdlinge-scripts" ]; then
    echo "✅ Build successful!"
    echo "📁 Binary location: dist/erdlinge-scripts/"
    echo ""
    echo "To run the application:"
    echo "  Linux/macOS: ./dist/erdlinge-scripts/erdlinge-scripts"
    echo "  Windows: dist\\erdlinge-scripts\\erdlinge-scripts.exe"
    echo ""
    echo "The application will start a web server accessible at http://localhost:7860"
else
    echo "❌ Build failed!"
    exit 1
fi