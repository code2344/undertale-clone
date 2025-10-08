#!/bin/bash
# Build script for WebAssembly version using Pygbag

set -e

echo "================================"
echo "Undertale Clone - Browser Build"
echo "================================"
echo ""

# Check if pygbag is installed
if ! command -v pygbag &> /dev/null; then
    echo "❌ Pygbag not found."
    echo "Installing pygbag..."
    pip install --user pygbag
    echo "✅ Pygbag installed successfully"
    echo ""
fi

# Clean previous build
if [ -d "build" ]; then
    echo "🧹 Cleaning previous build..."
    rm -rf build
fi

# Create build directory
mkdir -p build/web

echo "🔨 Building with pygbag..."
echo "This may take a few minutes..."
echo ""

# Build the game using pygbag
# --build: Build mode (as opposed to dev/serve mode)
# --template: Use template for better compatibility
# --ume_block: Prevent blocking calls
# --can_close: Allow game to be closed
if pygbag --build --ume_block 0 --can_close 1 .; then
    echo "✅ Pygbag build successful"
else
    echo "❌ Pygbag build failed"
    echo "Try updating pygbag: pip install --upgrade pygbag"
    exit 1
fi

echo ""
echo "🎨 Enhancing web build with loading bar and error console..."
python3 enhance_web_build.py

echo ""
echo "🔧 Fixing CDN references and downloading runtime files..."
python3 fix_cdn_references.py

echo ""
echo "✅ Build complete!"
echo ""
echo "📁 Output directory: build/web/"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 To test locally:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  cd build/web"
echo "  python3 -m http.server 8000"
echo ""
echo "Then open http://localhost:8000 in your browser"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 To deploy to GitHub Pages:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  1. Push these changes to GitHub"
echo "  2. Enable GitHub Pages in repo settings"
echo "  3. Select 'GitHub Actions' as source"
echo "  4. The workflow will automatically deploy"
echo ""
echo "🎮 Enjoy the game!"
echo ""
