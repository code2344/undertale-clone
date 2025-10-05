# Browser Build Instructions

This document provides instructions for building and running the browser-compatible version of the Undertale Clone.

## Overview

The browser version is built using [Pygbag](https://github.com/pygame-web/pygbag), which compiles Python/Pygame code to WebAssembly using Emscripten. This allows the game to run directly in modern web browsers without any additional plugins.

## Requirements

- Python 3.11 or higher
- pip (Python package installer)
- Modern web browser (Chrome, Firefox, Edge, or Safari)

## Building for Browser

### Method 1: Using the Build Script (Recommended)

1. Make the build script executable:
   ```bash
   chmod +x build.sh
   ```

2. Run the build script:
   ```bash
   ./build.sh
   ```

3. The built files will be in the `build/web/` directory.

### Method 2: Manual Build

1. Install Pygbag:
   ```bash
   pip install pygbag
   ```

2. Build the game:
   ```bash
   pygbag --build .
   ```

3. The output will be in `build/web/`.

## Testing Locally

After building, you can test the game locally:

```bash
python3 -m http.server 8000 --directory build/web
```

Then open your browser and navigate to:
```
http://localhost:8000
```

## Deployment to GitHub Pages

### Automatic Deployment

The repository includes a GitHub Actions workflow that automatically builds and deploys the game to GitHub Pages when you push to the `master` or `main` branch.

To enable this:

1. Go to your repository settings on GitHub
2. Navigate to "Pages" in the left sidebar
3. Under "Source", select "GitHub Actions"
4. Push your changes to trigger the deployment

The game will be available at:
```
https://<username>.github.io/<repository-name>/
```

### Manual Deployment

You can also manually deploy the built files to any static hosting service:

1. Build the game as described above
2. Upload the contents of `build/web/` to your hosting service
3. Ensure the `index.html` file is served as the root

## Browser Compatibility

The browser version has been tested on:
- ✅ Chrome/Chromium (version 90+)
- ✅ Firefox (version 88+)
- ✅ Edge (version 90+)
- ✅ Safari (version 14+)

## Known Limitations

Due to the nature of running Python in the browser via WebAssembly, there are some limitations:

1. **Loading Time**: Initial load may take 10-30 seconds as the Python runtime and game assets are downloaded.

2. **File System**: The browser version uses an in-memory file system. Save files are stored in browser local storage and may not persist across different browsers or in private browsing mode.

3. **Performance**: While generally smooth, performance may be slightly lower than the native desktop version, especially on older devices.

4. **Audio**: Some audio features may have limited support depending on the browser's WebAssembly audio implementation.

5. **Threading**: Some threading operations may behave differently in the browser environment.

## Troubleshooting

### Build Errors

**Problem**: `pygbag` installation fails
```bash
# Try installing with user flag
pip install --user pygbag
```

**Problem**: Build fails with missing dependencies
```bash
# Install all Python dependencies first
pip install -r requirements.txt
pip install pygbag
```

### Runtime Errors

**Problem**: Game doesn't load in browser
- Check browser console for error messages (F12 → Console)
- Ensure you're using a modern browser version
- Try clearing browser cache and reloading

**Problem**: Slow performance
- Close other browser tabs to free up memory
- Try a different browser (Chrome typically has the best WebAssembly performance)
- Ensure hardware acceleration is enabled in browser settings

**Problem**: Save files not persisting
- Check browser settings to ensure local storage is enabled
- Note that private/incognito mode may not persist data
- Try exporting save files if the game supports it

## Advanced Configuration

### Custom Build Options

Pygbag supports various build options:

```bash
# Build with specific template
pygbag --template noctx.tmpl --build .

# Build with custom dimensions
pygbag --width 640 --height 480 --build .

# Build with custom icon
pygbag --icon path/to/icon.png --build .
```

### Optimizing Assets

For better loading performance:

1. **Compress images**: Use tools like `optipng` or `pngcrush` for PNG files
2. **Reduce audio file sizes**: Convert to OGG format with appropriate bitrates
3. **Remove unused assets**: Clean up any files not needed for gameplay

## Development Notes

### Code Changes for Browser Compatibility

The main code changes for browser compatibility are in `main_web.py`:

1. **Async Main Loop**: The game loop is wrapped in an async function to allow the browser to handle events.
2. **Platform Detection**: Checks if running in WebAssembly environment.
3. **Event Loop Integration**: Uses `asyncio.sleep(0)` to yield control to the browser.

### Testing Changes

When developing for the browser version:

1. Test both native and browser versions
2. Use browser developer tools to debug
3. Check console for Python/JavaScript errors
4. Monitor network tab for asset loading issues

## Additional Resources

- [Pygbag Documentation](https://github.com/pygame-web/pygbag)
- [Pygame-ce Documentation](https://pyga.me/)
- [WebAssembly Documentation](https://webassembly.org/)
- [Emscripten Documentation](https://emscripten.org/)

## Contributing

If you encounter issues with the browser build or have suggestions for improvements, please:

1. Check existing issues on GitHub
2. Create a new issue with:
   - Browser and version
   - Steps to reproduce
   - Error messages/screenshots
   - System information

## License

Same as the main project. See LICENSE file for details.
