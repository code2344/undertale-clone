# Quick Start Guide - Browser Version

## For Users: Playing the Game

### Online (After Deployment)
Simply visit: `https://code2344.github.io/undertale-clone/`

### Controls
- **Arrow Keys**: Move character
- **Z / Enter**: Accept/Confirm actions
- **X / Shift**: Cancel/Back
- **C / Ctrl**: Open menu

## For Developers: Building the Browser Version

### Prerequisites
```bash
# Install Python 3.11 or higher
python3 --version

# Install Pygbag
pip install pygbag
```

### Quick Build
```bash
# Clone the repository
git clone https://github.com/code2344/undertale-clone.git
cd undertale-clone

# Run the build script
chmod +x build.sh
./build.sh

# Test locally
cd build/web
python3 -m http.server 8000
```

Then open http://localhost:8000 in your browser.

### What Gets Built?

The build process:
1. ✅ Compiles Python code to WebAssembly
2. ✅ Bundles all game assets (sprites, music, fonts)
3. ✅ Generates HTML/JavaScript loader
4. ✅ Creates optimized package for web

Output: `build/web/` directory with all files needed for deployment.

### Deployment Options

#### Option 1: GitHub Pages (Automatic)
1. Push code to GitHub
2. Enable GitHub Pages in repository settings
3. Select "GitHub Actions" as source
4. Done! The workflow automatically builds and deploys

#### Option 2: Manual Upload
1. Build locally with `./build.sh`
2. Upload contents of `build/web/` to any static host:
   - GitHub Pages
   - Netlify
   - Vercel
   - Your own server

#### Option 3: Custom Domain
After deploying to GitHub Pages, you can add a custom domain:
1. Add a `CNAME` file to `build/web/` with your domain
2. Configure DNS to point to GitHub Pages
3. Enable HTTPS in repository settings

## Troubleshooting

### Build fails?
```bash
# Check compatibility first
python3 check_compatibility.py

# Install dependencies
pip install -r requirements.txt
pip install pygbag
```

### Game doesn't load?
- Open browser console (F12) to see errors
- Check that you're using a modern browser
- Try clearing browser cache
- Ensure JavaScript is enabled

### Performance issues?
- Use Chrome for best WebAssembly performance
- Close other tabs to free memory
- Check browser hardware acceleration is enabled

## File Structure

```
undertale-clone/
├── main_web.py          # WebAssembly entry point
├── main.py              # Original desktop entry point
├── globals.py           # Game globals
├── build.sh             # Build script
├── pygbag.toml          # Build configuration
├── index.html           # Local test HTML
├── sprites/             # Game sprites
├── fonts/               # Game fonts
├── mus/                 # Music files
├── sfx/                 # Sound effects
└── build/               # Generated build output
    └── web/             # Deploy this directory
```

## Development Workflow

1. **Edit Code**: Make changes to Python files
2. **Check Compatibility**: Run `./check_compatibility.py`
3. **Build**: Run `./build.sh`
4. **Test**: Open `build/web/index.html` in browser
5. **Debug**: Use browser console for errors
6. **Deploy**: Push to GitHub or upload to hosting

## Advanced

### Custom Build Options

Edit `pygbag.toml` to customize:
- Canvas dimensions
- Asset inclusion/exclusion
- Compression settings
- Template selection

### Optimize for Production

```bash
# Compress assets before building
optipng sprites/**/*.png
oggenc --quality 6 mus/**/*.ogg

# Build with optimization
pygbag --build --optimize .
```

## Resources

- 📖 Full documentation: [BROWSER_BUILD.md](BROWSER_BUILD.md)
- 🔧 Technical notes: [WASM_NOTES.md](WASM_NOTES.md)
- 🐛 Issues: [GitHub Issues](https://github.com/code2344/undertale-clone/issues)

## Support

Having trouble? Check:
1. [BROWSER_BUILD.md](BROWSER_BUILD.md) - Detailed build instructions
2. [WASM_NOTES.md](WASM_NOTES.md) - Technical compatibility info
3. GitHub Issues - Search existing issues or create new one

---

**Happy gaming! 🎮**
