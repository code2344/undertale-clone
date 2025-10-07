# Web Build Enhancements

This document describes the loading bar and error console features added to the web version of the Undertale Clone.

## Features

### 🎯 Loading Bar with Progress Indicator

The web version now includes a beautiful, animated loading bar that shows the game's loading progress:

- **Visual Progress**: A green progress bar with percentage indicator
- **Status Messages**: Real-time updates on what's being loaded
- **Smooth Animations**: Shimmer effect and smooth transitions
- **Auto-hide**: Automatically disappears when loading is complete

**Loading Stages**:
1. Initializing game... (10%)
2. Loading game modules... (30%)
3. Initializing game systems... (70%)
4. Starting game loop... (95%)
5. Ready! (100%)

### 🔍 Error Console

An integrated error console that captures and displays errors during gameplay:

- **Auto-capture**: Automatically catches JavaScript errors, warnings, and Python exceptions
- **Categorized Messages**: Different colors for errors (red), warnings (orange), and info (blue)
- **Timestamps**: Each message includes when it occurred
- **Collapsible**: Toggle visibility with the error button in bottom-right corner
- **Error Counter**: Badge showing the number of errors
- **Auto-show**: Opens automatically when the first error occurs

**Error Levels**:
- **Error** (Red): Critical issues that may affect gameplay
- **Warning** (Orange): Non-critical issues or deprecations
- **Info** (Blue): General information messages

## How It Works

### Build Process

1. **Pygbag Build**: The standard Pygbag build creates the WebAssembly package
2. **Enhancement Script**: `enhance_web_build.py` post-processes the HTML to inject:
   - CSS styles for the loading bar and error console
   - HTML elements for the UI components
   - JavaScript for managing loading progress and errors

### Python Integration

The `main_web.py` file includes helper classes that integrate with the JavaScript UI:

```python
# Update loading progress
LoadingProgress.set_progress(50, "Loading assets...")

# Log errors to the console
WebConsole.log_error("An error occurred")
WebConsole.log_warning("This is a warning")
WebConsole.log_info("Informational message")
```

### JavaScript API

The web page exposes a global `gameAPI` object that Python can call:

```javascript
window.gameAPI.setLoadingProgress(percent, status)
window.gameAPI.completeLoading()
window.gameAPI.logError(message)
window.gameAPI.logWarning(message)
window.gameAPI.logInfo(message)
```

## Files

### Core Files

- **`enhance_web_build.py`**: Post-build script that injects the UI enhancements
- **`main_web.py`**: Enhanced with `LoadingProgress` and `WebConsole` classes
- **`build.sh`**: Updated to run the enhancement script after building
- **`.github/workflows/deploy.yml`**: Updated to enhance the build in CI/CD

### Generated Files (build/web/)

- **`index.html`**: Enhanced with loading bar and error console
  - Additional CSS styles
  - HTML elements for loading screen and error console
  - JavaScript for UI management

## Usage

### Building Locally

```bash
# Standard build (automatically includes enhancements)
./build.sh

# Manual enhancement (if needed)
python3 enhance_web_build.py
```

### Testing

```bash
cd build/web
python3 -m http.server 8000
# Open http://localhost:8000 in your browser
```

### Deployment

The GitHub Actions workflow automatically:
1. Builds the game with Pygbag
2. Runs the enhancement script
3. Deploys to GitHub Pages

## Customization

### Styling

Edit the CSS in `enhance_web_build.py` to customize:
- Loading bar colors and animations
- Error console appearance
- Font sizes and spacing

### Loading Messages

Modify the status messages in `main_web.py`:

```python
LoadingProgress.set_progress(30, "Your custom message...")
```

### Error Handling

Add custom error logging anywhere in the code:

```python
try:
    # Your code
except Exception as e:
    WebConsole.log_error(f"Custom error: {e}")
```

## Browser Compatibility

The enhanced UI works in all modern browsers:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Performance

The enhancements have minimal performance impact:
- **CSS**: ~3KB (compressed)
- **JavaScript**: ~2KB (compressed)
- **HTML**: ~1KB
- **Total overhead**: < 6KB

## Troubleshooting

### Loading Bar Not Showing

- Check browser console for JavaScript errors
- Ensure `enhance_web_build.py` ran successfully
- Verify `index.html` contains the enhanced UI code

### Errors Not Appearing

- Open browser DevTools (F12) to see if errors are logged
- Click the error button in bottom-right corner to toggle console
- Check that error console is not hidden behind other elements

### Build Issues

```bash
# Rebuild from scratch
rm -rf build/
./build.sh
```

## Future Improvements

Potential enhancements for future versions:
- [ ] Asset loading progress (individual files)
- [ ] Network status indicator
- [ ] Performance metrics display
- [ ] Save/load state visualization
- [ ] Sound effect on loading complete

## Credits

These enhancements were added to improve the user experience when playing the Undertale Clone in a web browser. They provide visual feedback during loading and help with debugging issues.
