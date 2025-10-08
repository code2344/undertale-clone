# undertale-clone

[Undertale](undertale.net) is a video game released 15 September 2015 by Toby Fox.
This repository is an attempt to replicate the game to as close to pixel-level accuracy as possible using Python and Pygame.

The asset files were taken from [rawr.ws](rawr.ws/undertale)

## Play in Browser

This game can now be played directly in your web browser! A WebAssembly version is available via GitHub Pages.

**[Play Now](https://code2344.github.io/undertale-clone/)** (Once deployed)

The browser version is built using [Pygbag](https://github.com/pygame-web/pygbag) and Emscripten, which compiles the Python/Pygame code to WebAssembly.

## Installation

### Desktop Version

1. Install Python 3.11 or higher
2. Install dependencies:
   ```bash
   pip install pygame
   ```
3. Run the game:
   ```bash
   python3 main.py
   ```

### Browser Version

For instructions on building and deploying the browser version, see [BROWSER_BUILD.md](BROWSER_BUILD.md).

Quick build:
```bash
chmod +x build.sh
./build.sh
```

## Browser Compatibility

The WebAssembly version works on:
- Chrome/Chromium 90+
- Firefox 88+
- Edge 90+
- Safari 14+

### Troubleshooting

If you experience loading errors (including 1401 errors):

1. **Run the diagnostic tool:**
   ```bash
   python3 diagnose_1401_errors.py
   ```

2. **Common fixes:**
   - Clear browser cache (Ctrl+Shift+Delete)
   - Try a different browser
   - Check your internet connection
   - The game automatically uses CDN fallback for reliability

3. **For more help, see:**
   - [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Comprehensive troubleshooting guide
   - [Browser Console](https://developer.chrome.com/docs/devtools/open/) (F12) - Check for specific error messages

## Features

- Pixel-perfect recreation of Undertale gameplay
- Browser-compatible via WebAssembly
- Save/Load functionality (browser version uses local storage)
- Full Pygame implementation

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
