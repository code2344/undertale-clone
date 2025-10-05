#!/bin/bash
# Build script for WebAssembly version using Pygbag

set -e

echo "Building Undertale Clone for WebAssembly..."

# Check if pygbag is installed
if ! command -v pygbag &> /dev/null; then
    echo "Pygbag not found. Installing..."
    pip install pygbag
fi

# Create build directory
mkdir -p build/web

# Build the game using pygbag
echo "Building with pygbag..."
pygbag --build .

echo "Build complete! Output in build/web/"
echo ""
echo "To test locally, run:"
echo "  python3 -m http.server 8000 --directory build/web"
echo ""
echo "Then open http://localhost:8000 in your browser"
