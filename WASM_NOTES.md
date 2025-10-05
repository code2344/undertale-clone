# WebAssembly Compatibility Notes

This document outlines the changes made to support WebAssembly/browser deployment and known compatibility considerations.

## Architecture Overview

```
┌─────────────────────────────────────────┐
│         Browser (Chrome/Firefox)        │
│  ┌───────────────────────────────────┐  │
│  │      JavaScript/HTML Interface     │  │
│  └───────────────┬───────────────────┘  │
│                  │                       │
│  ┌───────────────▼───────────────────┐  │
│  │   Pyodide/Emscripten Runtime      │  │
│  │   (Python 3.11 in WebAssembly)    │  │
│  └───────────────┬───────────────────┘  │
│                  │                       │
│  ┌───────────────▼───────────────────┐  │
│  │         Pygame-ce Library         │  │
│  └───────────────┬───────────────────┘  │
│                  │                       │
│  ┌───────────────▼───────────────────┐  │
│  │    Undertale Clone Game Code      │  │
│  │         (main_web.py)             │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## Key Changes for Browser Compatibility

### 1. Async Main Loop (`main_web.py`)

**Why**: WebAssembly requires yielding control back to the browser's event loop to prevent freezing.

**Implementation**:
```python
async def async_maincycle():
    while globals.running:
        if globals.room:
            globals.room.draw()
        if IS_WASM:
            await asyncio.sleep(0)  # Yield to browser
```

**Impact**: Minimal - the game loop runs the same way, just with async support.

### 2. Platform Detection

**Why**: Different behavior needed for native vs browser environments.

**Implementation**:
```python
import platform
IS_WASM = platform.system() == "Emscripten"
```

**Usage**: Used to conditionally enable browser-specific features.

### 3. File System Handling

**Current State**: The game uses standard Python file I/O.

**Browser Behavior**: 
- Emscripten provides an in-memory file system (MEMFS)
- Files persist in browser LocalStorage via IndexedDB
- Save files work but are isolated per browser/domain

**No Changes Needed**: Python's standard file operations work transparently.

## Compatibility Matrix

| Feature | Native | Browser | Notes |
|---------|--------|---------|-------|
| Pygame rendering | ✅ | ✅ | Full support |
| Audio playback | ✅ | ✅ | May have slight delay on first play |
| Keyboard input | ✅ | ✅ | Full support |
| File I/O | ✅ | ✅ | Browser uses virtual FS |
| Save/Load | ✅ | ✅ | Persists in LocalStorage |
| Threading | ✅ | ⚠️ | Limited; avoid complex threading |
| Mouse input | ✅ | ✅ | Blocked by game design |
| Fullscreen | ✅ | ✅ | Via browser API |

✅ = Fully supported
⚠️ = Partially supported / Has limitations
❌ = Not supported

## Known Limitations

### Performance
- **Initial Load**: 10-30 seconds for Python runtime + assets
- **Runtime Performance**: 80-95% of native speed
- **Memory**: Higher memory usage due to browser overhead

### Threading
The game uses `threading.Thread` for room initialization:
```python
threading.Thread(target=globals.room.on_enter, name='on_enter runner for first room').start()
```

**Browser Impact**: 
- Emscripten supports threading via SharedArrayBuffer
- Most browsers require special headers to enable
- Current implementation should work but may have timing differences

**Recommendation**: Monitor for any race conditions in browser testing.

### Audio
- First audio playback may have ~100ms delay (browser limitation)
- Some browsers require user interaction before playing audio
- OGG format is well-supported

### Clipboard
- Browser clipboard access requires special permissions
- Paste operations may need user confirmation
- Not critical for this game

## Pygbag Build Process

### What Pygbag Does

1. **Bundles Assets**: Packages sprites, music, fonts into the build
2. **Compiles Python**: Converts Python bytecode to WebAssembly
3. **Generates HTML/JS**: Creates loader and runtime environment
4. **Optimizes**: Compresses assets and code for faster loading

### Build Outputs

```
build/web/
├── index.html          # Main entry point
├── pygame.js           # Pygame runtime
├── python.wasm         # Python interpreter
├── undertale-clone.zip # Bundled game + assets
└── [various .data files]
```

### Customization Options

In `pygbag.toml`:
- Canvas size (width/height)
- Asset inclusion/exclusion
- Compression level
- Caching options

## Testing Checklist

Before deploying, test these scenarios in browser:

- [ ] Game loads without errors
- [ ] Graphics render correctly
- [ ] Keyboard controls work
- [ ] Audio plays (after user interaction)
- [ ] Save/Load functionality works
- [ ] No console errors
- [ ] Works in incognito/private mode
- [ ] Tested on multiple browsers
- [ ] Tested on mobile (if applicable)
- [ ] Performance is acceptable

## Debugging Tips

### Browser Console

Access with F12 → Console tab. Look for:
- Python exceptions (shown as JavaScript errors)
- Asset loading failures
- Missing file warnings

### Common Issues

**"Module not found"**
- Check that all imports are available in Pygbag's Python distribution
- Some native extensions may not be available

**"File not found"**
- Ensure asset paths are relative, not absolute
- Check `pygbag.toml` includes the right directories

**Performance issues**
- Reduce asset sizes (compress images/audio)
- Check for infinite loops or heavy computations
- Use browser profiler (Performance tab)

**Save files not persisting**
- Check browser allows LocalStorage
- Not in private browsing mode
- Clear site data to reset

### Verbose Logging

Enable debug output in browser console:
```javascript
// In browser console
localStorage.setItem('PYGBAG_DEBUG', '1');
```

## Future Enhancements

Potential improvements for browser version:

1. **Progressive Loading**: Load assets on-demand rather than upfront
2. **Service Worker**: Enable offline play
3. **Cloud Saves**: Sync saves across devices
4. **Touch Controls**: Mobile support
5. **Gamepad API**: Controller support
6. **WebGL Acceleration**: Better performance via WebGL backend

## Resources

- **Pygbag**: https://github.com/pygame-web/pygbag
- **Pygame-ce**: https://pyga.me/
- **Emscripten**: https://emscripten.org/
- **WebAssembly**: https://webassembly.org/

## Contributing

If you make improvements to browser compatibility:

1. Update this document
2. Test across multiple browsers
3. Update compatibility matrix
4. Add notes about any limitations discovered
