# Troubleshooting Guide

This guide helps resolve common issues when building or running the browser version of Undertale Clone.

## Table of Contents

1. [Build Issues](#build-issues)
2. [Runtime Issues](#runtime-issues)
3. [Deployment Issues](#deployment-issues)
4. [Performance Issues](#performance-issues)
5. [Save/Load Issues](#save-load-issues)
6. [Browser-Specific Issues](#browser-specific-issues)

---

## Build Issues

### ❌ "Pygbag command not found"

**Symptom:** Running `./build.sh` or `pygbag` gives "command not found"

**Solution:**
```bash
# Install pygbag
pip install --user pygbag

# If still not found, add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Or use python -m
python3 -m pygbag --build .
```

### ❌ "Permission denied: ./build.sh"

**Symptom:** Cannot execute build script

**Solution:**
```bash
chmod +x build.sh
./build.sh
```

### ❌ Build fails with "No module named 'pygame'"

**Symptom:** Build process complains about missing pygame

**Solution:**
This is actually OK! Pygbag bundles its own pygame-ce. However, if the build truly fails:

```bash
# For development/testing only
pip install pygame

# But pygbag will use its own version for the build
```

### ❌ "Asset directory not found"

**Symptom:** Build complains about missing assets

**Solution:**
```bash
# Check that required directories exist
ls -la sprites/ fonts/ mus/ sfx/

# Run compatibility check
python3 check_compatibility.py

# If directories are truly missing, the game won't work
# You need to obtain the asset files
```

### ❌ Build creates empty output

**Symptom:** `build/web/` exists but has no files

**Solution:**
```bash
# Clean and rebuild
rm -rf build/
rm -rf .pygbag/
./build.sh

# Check pygbag version
pip show pygbag

# Update if old
pip install --upgrade pygbag
```

---

## Runtime Issues

### ❌ Game doesn't load - blank screen

**Symptom:** Browser shows blank or loading screen forever

**Solutions:**

1. **Check browser console** (F12 → Console):
   - Look for error messages
   - Note any failed network requests

2. **Verify files are served correctly:**
   ```bash
   # Make sure you're in the right directory
   cd build/web
   python3 -m http.server 8000
   
   # Open http://localhost:8000 (not file://)
   ```

3. **Check browser compatibility:**
   - Use Chrome 90+, Firefox 88+, Edge 90+, or Safari 14+
   - Update browser to latest version
   - Try a different browser

4. **Disable browser extensions:**
   - Some extensions block WebAssembly
   - Try incognito/private mode

### ❌ "Failed to load Python runtime"

**Symptom:** Error about Python/Pyodide loading

**Solution:**
```javascript
// Check in browser console
// Look for CORS errors or network failures

// If using local server, make sure it's configured correctly
// Python's http.server should work fine

// If on deployment, check:
// - Files uploaded correctly
// - Server serves .wasm with correct MIME type
// - No CORS restrictions
```

### ❌ Graphics don't appear correctly

**Symptom:** Sprites missing, colors wrong, or distorted graphics

**Solutions:**

1. **Check asset loading:**
   - Open Network tab (F12)
   - Look for failed asset requests
   - Verify assets bundled in build

2. **Check canvas rendering:**
   ```javascript
   // In console
   document.querySelector('canvas')
   // Should show canvas element
   ```

3. **Clear browser cache:**
   - Hard reload: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
   - Or clear site data

### ❌ "TypeError: Cannot read property..."

**Symptom:** JavaScript errors in console

**Solution:**
```bash
# Rebuild with latest pygbag
pip install --upgrade pygbag
rm -rf build/
./build.sh

# Check that main_web.py has correct async structure
python3 check_compatibility.py
```

### ❌ Audio doesn't play

**Symptom:** No sound, even though graphics work

**Solutions:**

1. **Browser requires user interaction:**
   - Click on the page
   - Some browsers block audio until user interacts

2. **Check browser audio permissions:**
   - Look for blocked audio icon in address bar
   - Allow audio for the site

3. **Verify audio files:**
   ```bash
   # Check that music files exist
   ls -la mus/
   
   # Verify OGG format (most compatible)
   file mus/*.ogg
   ```

4. **Check browser console:**
   - Look for Web Audio API errors
   - Check for CORS issues with audio files

---

## Deployment Issues

### ❌ GitHub Actions build fails

**Symptom:** Workflow shows red X

**Solutions:**

1. **Check workflow logs:**
   - Go to Actions tab in GitHub
   - Click on failed run
   - Read error messages

2. **Common fixes:**
   ```yaml
   # Make sure deploy.yml has correct Python version
   python-version: '3.11'
   
   # Check that all files are committed
   git status
   git add .
   git commit -m "Fix deployment"
   git push
   ```

3. **Verify permissions:**
   - Repository Settings → Actions → General
   - Workflow permissions: Read and write
   - Pages → Source: GitHub Actions

### ❌ GitHub Pages shows 404

**Symptom:** Deployment succeeds but site not accessible

**Solutions:**

1. **Check Pages settings:**
   - Settings → Pages
   - Source should be "GitHub Actions"
   - Wait 2-3 minutes after deployment

2. **Verify URL:**
   ```
   # Correct format:
   https://username.github.io/repository-name/
   
   # Not:
   https://username.github.io/
   ```

3. **Check deployment:**
   - Actions tab → Latest workflow
   - Should show green checkmark
   - Look for deployment URL in logs

### ❌ "Site can't be reached"

**Symptom:** Deployed but URL doesn't work

**Solution:**
```bash
# Wait a few minutes - Pages can be slow
# Check status:
# Settings → Pages → should show "Your site is live at..."

# If still not working:
# - Re-run the workflow (Actions → Re-run jobs)
# - Check repository is public (or has Pages enabled for private)
# - Verify no typos in repository name/URL
```

---

## Performance Issues

### ⚠️ Slow initial load

**Symptom:** Takes 30+ seconds to load

**This is normal!** But you can optimize:

1. **Compress assets:**
   ```bash
   # Install optimization tools
   sudo apt install optipng
   
   # Optimize images
   find sprites -name "*.png" -exec optipng {} \;
   
   # Rebuild
   ./build.sh
   ```

2. **Reduce asset sizes:**
   - Use lower resolution (if acceptable)
   - Convert audio to lower bitrate
   - Remove unused assets

3. **Use CDN:**
   - GitHub Pages already uses CDN
   - Or use Cloudflare for custom domain

### ⚠️ Low FPS / Stuttering

**Symptom:** Game runs slowly or jerkily

**Solutions:**

1. **Check browser performance:**
   - Close other tabs
   - Disable extensions
   - Use Chrome (usually fastest)

2. **Enable hardware acceleration:**
   - Chrome: Settings → Advanced → System
   - Enable "Use hardware acceleration"

3. **Check system resources:**
   - Open Task Manager / Activity Monitor
   - Look for high CPU/memory usage
   - Close other applications

4. **Reduce graphics quality (if game supports it):**
   ```python
   # In game settings or globals.py
   # Reduce resolution or effects
   ```

---

## Save/Load Issues

### ❌ Saves don't persist

**Symptom:** Progress lost on reload

**Solutions:**

1. **Check browser storage:**
   - Not in private/incognito mode
   - Browser allows cookies/storage
   - Site not blocked

2. **Verify storage usage:**
   ```javascript
   // In browser console
   navigator.storage.estimate().then(e => console.log(e))
   ```

3. **Clear and retry:**
   ```javascript
   // Delete old saves
   indexedDB.deleteDatabase('EM_PRELOAD_CACHE')
   // Reload page
   ```

### ❌ "Save file corrupted"

**Symptom:** Error loading saved game

**Solution:**
```bash
# This usually means incompatible versions
# After updating the game, old saves might not work

# In browser console, reset:
localStorage.clear()
indexedDB.databases().then(dbs => {
    dbs.forEach(db => indexedDB.deleteDatabase(db.name))
})
```

---

## Browser-Specific Issues

### Chrome

**Issue:** High memory usage

**Solution:**
- Expected - WebAssembly uses more memory
- Close other tabs
- Restart browser periodically

### Firefox

**Issue:** Slower than Chrome

**Solution:**
- Normal - WebAssembly performance varies
- Update to latest Firefox
- Check `about:config` → `javascript.options.wasm_*` settings

### Safari

**Issue:** Some features don't work

**Solution:**
- Update to latest macOS/iOS
- Safari 14+ required
- Some features may have limited support

### Mobile Browsers

**Issue:** Touch controls don't work

**Solution:**
- Desktop keyboard required currently
- Bluetooth keyboard on mobile may work
- Touch support is a future enhancement

---

## Diagnostic Tools

### Browser Console Commands

```javascript
// Check if WebAssembly is supported
typeof WebAssembly !== 'undefined'

// Check canvas
document.querySelector('canvas')

// Check Pygame/Python loaded
// (Will show after game loads)
window.pyodide

// Storage info
navigator.storage.estimate()

// Performance
performance.memory
```

### Python Debugging (in game)

```python
# In main_web.py or main.py
import sys
print(f"Python version: {sys.version}")
print(f"Platform: {sys.platform}")

# Check if WebAssembly
try:
    import platform
    print(f"System: {platform.system()}")
except:
    pass
```

### Build Diagnostics

```bash
# Run compatibility check
python3 check_compatibility.py

# Verbose build
pygbag --build --verbose .

# Check build size
du -sh build/web/

# List build contents
ls -lah build/web/
```

---

## Getting Help

If none of these solutions work:

1. **Gather information:**
   - Browser and version
   - Operating system
   - Error messages (screenshots)
   - Console logs
   - Steps to reproduce

2. **Check existing issues:**
   - Search GitHub issues
   - Look for similar problems

3. **Create new issue:**
   - Include all gathered information
   - Describe what you tried
   - Provide minimal reproduction case

4. **Community resources:**
   - Pygbag GitHub: https://github.com/pygame-web/pygbag
   - Pygame Discord/Forums
   - Stack Overflow (tag: pygame, webassembly)

---

## Prevention

To avoid issues:

- ✅ Always run `check_compatibility.py` before building
- ✅ Test locally before deploying
- ✅ Keep dependencies updated
- ✅ Use recommended browser versions
- ✅ Read documentation before making changes
- ✅ Commit working code before experimenting

---

## Quick Reference

| Problem | Quick Fix |
|---------|-----------|
| Build fails | `rm -rf build/ .pygbag/ && ./build.sh` |
| Won't load | Check console, try different browser |
| No audio | Click page, check permissions |
| Slow | Use Chrome, close tabs, clear cache |
| No saves | Check not in private mode |
| Deploy fails | Re-run workflow, check permissions |

---

**Remember:** When in doubt, check the browser console (F12) - it usually tells you what's wrong!
