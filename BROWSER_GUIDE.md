# 🎮 Undertale Clone - Browser Version Guide

## Quick Start

### Play Online
Visit: **https://code2344.github.io/undertale-clone/** (once deployed)

### Controls
- **Arrow Keys**: Move character
- **Z / Enter**: Accept/Confirm actions
- **X / Shift**: Cancel/Back
- **C / Ctrl**: Open menu

---

## For Developers: Building the Browser Version

### Prerequisites
```bash
# Install Python 3.11 or higher
python3 --version

# Install Pygbag (WebAssembly compiler for Pygame)
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
```

The build process:
1. ✅ Compiles Python code to WebAssembly  
2. ✅ Bundles all game assets (sprites, music, fonts)
3. ✅ Generates HTML/JavaScript loader
4. ✅ Creates optimized package for web

**Output:** `build/web/` directory with all files needed for deployment.

### Test Locally
```bash
cd build/web
python3 -m http.server 8000
```

Then open **http://localhost:8000** in your browser.

---

## Deployment to GitHub Pages

### Option 1: Automatic Deployment (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Update game"
   git push origin main
   ```

2. **Enable GitHub Pages**
   - Go to repository **Settings** → **Pages**
   - Source: **GitHub Actions**
   - The workflow in `.github/workflows/deploy.yml` will automatically:
     - Build the game with pygbag
     - Deploy to GitHub Pages

3. **Access your game**
   - Visit: `https://yourusername.github.io/undertale-clone/`
   - The game is now playable in any modern browser!

### Option 2: Manual Deployment

1. **Build the game**
   ```bash
   ./build.sh
   ```

2. **Deploy the `build/web` folder**
   - Use any static hosting service (Netlify, Vercel, GitHub Pages, etc.)
   - Upload the contents of `build/web/`

---

## How It Works

### Architecture

```
Original Pygame Game
        ↓
    main.py (desktop version)
        ↓
    main_web.py (WebAssembly wrapper)
        ↓
    Pygbag Compiler
        ↓
    WebAssembly + JavaScript
        ↓
    Runs in Browser!
```

### Key Files

- **`main_web.py`**: WebAssembly entry point with async/await support
- **`pygbag.toml`**: Build configuration (resolution, assets, etc.)
- **`build.sh`**: Automated build script
- **`main.py`**: Original game code (unchanged)

### What's Different in Browser Version?

**Nothing!** The game logic is identical to the desktop version. The browser version:
- ✅ Same gameplay
- ✅ Same graphics  
- ✅ Same music
- ✅ Same saves (stored in browser localStorage)
- ✅ Works on mobile devices too!

The only difference is `main_web.py` adds async/await wrappers required for WebAssembly.

---

## Troubleshooting

### Build fails with "pygbag not found"
```bash
pip install --user pygbag
# Add ~/.local/bin to PATH if needed
```

### Game doesn't load in browser
- Check browser console (F12) for errors
- Ensure you're serving from `build/web/` not the root directory
- Try a different browser (Chrome/Firefox recommended)

### Assets not loading
- Check that `pygbag.toml` includes your asset directories
- Ensure asset files are in the correct directories
- Rebuild: `./build.sh`

### Performance issues
- The first load may be slow (downloading WebAssembly)
- Subsequent loads are faster (browser caching)
- Try adjusting `compression` in `pygbag.toml`

---

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

---

## Development Workflow

1. **Edit Code**: Make changes to Python files
2. **Check Compatibility**: Run `./check_compatibility.py`
3. **Build**: Run `./build.sh`
4. **Test**: Open `build/web/index.html` in browser
5. **Debug**: Use browser console for errors
6. **Deploy**: Push to GitHub or upload to hosting

---

## Browser Compatibility

**Supported Browsers:**
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

**Mobile Support:**
- ✅ iOS Safari 14+
- ✅ Chrome Mobile 90+

**Note:** Internet Explorer is not supported (no WebAssembly support).

---

## Credits

This is a Pygame port of Undertale, made browser-compatible using Pygbag.

**Technologies:**
- [Python](https://python.org) - Programming language
- [Pygame](https://pygame.org) - Game framework
- [Pygbag](https://pygame-web.github.io/) - WebAssembly compiler
- [Emscripten](https://emscripten.org/) - C/C++ to WebAssembly

---

## License

See LICENSE file for details.

---

**Enjoy the game! 🎮**
