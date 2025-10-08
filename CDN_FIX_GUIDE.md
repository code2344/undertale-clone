# CDN Blocking Fix Guide

## Overview

This guide explains the fix for the game loading issue where external CDN resources were being blocked, causing the game to fail to load in the browser.

## Problem

The Undertale Clone was experiencing loading failures due to:
- **External CDN Dependency**: Pygbag runtime files hosted on `pygame-web.github.io` were being blocked
- **ERR_BLOCKED_BY_CLIENT Errors**: Browser security/network policies prevented loading external resources
- **Missing Runtime Files**: ~25MB of Python interpreter and support files couldn't be loaded

## Solution

An automated fix has been implemented that:
1. Downloads all required pygbag runtime files to `build/web/pygbag/`
2. Modifies generated HTML/JS to use local paths instead of remote CDN
3. Creates stub package index files for Python package management

## How It Works

### Build Process
When you run `./build.sh`, the following happens automatically:

```bash
./build.sh
├── 1. Run pygbag build (generates build/web/)
├── 2. Run enhance_web_build.py (adds loading bar & error console)
└── 3. Run fix_cdn_references.py (fixes CDN dependencies) ✨ NEW
```

### Fix Script (`fix_cdn_references.py`)

The script performs these steps:

1. **Downloads Runtime Files** (~25MB total):
   ```
   build/web/pygbag/
   ├── pythons.js          # Main loader script
   ├── browserfs.min.js    # Filesystem implementation
   ├── vtx.js, fs.js, snd.js, gui.js  # Feature modules
   ├── cpythonrc.py        # Python runtime configuration
   ├── cpython312/
   │   ├── main.js         # Python interpreter
   │   ├── main.wasm       # WebAssembly binary
   │   └── main.data       # Python stdlib
   ├── vt/
   │   ├── xterm.js        # Terminal emulator
   │   ├── xterm.css       # Terminal styles
   │   └── xterm-addon-image.js
   └── xtermjsixel/
       └── xterm-addon-image-worker.js
   ```

2. **Replaces CDN URLs**:
   - In `index.html`: `https://pygame-web.github.io/archives/0.9/` → `pygbag/`
   - In `vtx.js`: Updates xterm CDN path
   - In `pythons.js`: Adds URL rewriting for package repository

3. **Creates Stub Files**:
   - `pygbag/repo/index-090-cp312.json` (empty package index)
   - `pygbag/repo/repodata.json` (empty repository data)

## Usage

### Normal Build
```bash
# Build the game
./build.sh

# Serve locally
cd build/web
python3 -m http.server 8000

# Open in browser
# Navigate to http://localhost:8000
```

### Manual Fix (if needed)
If you've already built the game and need to apply the fix:

```bash
# Run the fix script manually
python3 fix_cdn_references.py

# Serve and test
cd build/web && python3 -m http.server 8000
```

## Technical Details

### Files Modified
- **`fix_cdn_references.py`**: New automated fix script
- **`build.sh`**: Updated to run fix script after build
- **`.gitignore`**: Excludes `build/` and `pygbag-cdn/` directories

### CDN Files Downloaded
The script downloads these files from `https://pygame-web.github.io/archives/0.9/`:

| File | Size | Purpose |
|------|------|---------|
| `main.wasm` | ~13MB | Python interpreter WebAssembly binary |
| `main.data` | ~7MB | Python standard library |
| `main.js` | ~5MB | Python interpreter JavaScript wrapper |
| `browserfs.min.js` | ~246KB | Virtual filesystem |
| `xterm.js` | ~276KB | Terminal emulator |
| `pythons.js` | ~74KB | Pygbag loader |
| Others | ~100KB | Support files |

### URL Rewriting Logic
The script modifies `pythons.js` to intercept and rewrite package repository URLs:

```javascript
window.cross_file = function * cross_file(url, store, flags) {
    // Redirect remote package repo to local stub
    if (url.includes('pygame-web.github.io/archives/repo/')) {
        url = url.replace('https://pygame-web.github.io/archives/repo/', 'pygbag/repo/');
    }
    // ... rest of function
}
```

## Troubleshooting

### Issue: Script fails to download files
**Solution**: Check your internet connection. Some files may 404 (expected) - the script will use existing files if available.

### Issue: Game still won't load
**Solution**: 
1. Clear browser cache (Ctrl+Shift+Delete)
2. Check browser console (F12) for specific errors
3. Ensure all files in `build/web/pygbag/` exist
4. Rebuild: `rm -rf build/ && ./build.sh`

### Issue: "File not found" errors for pygbag files
**Solution**: Re-run the fix script:
```bash
python3 fix_cdn_references.py
```

## Comparison: Before vs After

### Before (❌ Broken)
- External CDN: `https://pygame-web.github.io/archives/0.9/`
- Status: ERR_BLOCKED_BY_CLIENT
- Errors: ~1000 failed resource loads
- Result: Game fails to load

### After (✅ Fixed)
- Local hosting: `build/web/pygbag/`
- Status: HTTP 200 (all files loaded)
- Errors: 0 (no blocked resources)
- Result: Game loads successfully

## Notes

- **Build artifacts** (`build/` and `pygbag-cdn/`) are excluded from git via `.gitignore`
- **Runtime files** (~25MB) are downloaded once and reused for subsequent builds (cached)
- **No code changes** required to the game itself - fix is applied post-build
- **Compatible** with existing pygbag builds - script is safe to run multiple times

## References

- [Pygbag Documentation](https://pygame-web.github.io/wiki/pygbag/)
- [Original Issue: Nearly 1000 errors during game execution](https://github.com/code2344/undertale-clone/issues/)
- [WebAssembly Security](https://webassembly.org/docs/security/)
