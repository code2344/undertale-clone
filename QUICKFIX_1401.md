# Quick Fix Guide for 1401 Errors

## If You're Experiencing 1401 Errors

### Step 1: Run the Diagnostic Tool
```bash
python3 diagnose_1401_errors.py
```

This will check:
- ✅ CDN availability
- ✅ Pygbag installation
- ✅ Build artifacts
- ✅ Asset files

### Step 2: Follow Recommendations

The tool will provide specific recommendations. Common fixes:

#### If CDN Issues:
```bash
# The game now has automatic fallback
# Just refresh your browser (Ctrl+R or Cmd+R)
```

#### If Pygbag Issues:
```bash
pip install --upgrade pygbag
```

#### If Build Issues:
```bash
rm -rf build/ .pygbag/
./build.sh
```

### Step 3: Clear Browser Cache
```
Chrome/Edge: Ctrl+Shift+Delete (Windows) or Cmd+Shift+Delete (Mac)
Firefox: Ctrl+Shift+Delete
Safari: Cmd+Option+E
```

### Step 4: Test in Browser
```bash
cd build/web
python3 -m http.server 8000
```

Then open: http://localhost:8000

## What We Fixed

✅ **Multi-CDN Fallback** - Game tries 3 different CDN sources automatically
✅ **Better Error Messages** - Clear, actionable error messages  
✅ **Retry Logic** - Automatic retries for failed loads
✅ **Diagnostic Tool** - Easy troubleshooting
✅ **Test Suite** - Verify fixes work

## Need More Help?

- 📖 Read [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- 🧪 Run [test_1401_fix.html](test_1401_fix.html) in your browser
- 📋 Check [1401_FIX_SUMMARY.md](1401_FIX_SUMMARY.md) for technical details

## Still Having Issues?

1. Check browser console (F12 → Console tab)
2. Look for specific error messages
3. Try a different browser
4. Ensure you have a stable internet connection
5. Disable browser extensions (try incognito mode)

## Technical Details

The 1401 errors were caused by:
- CDN (Content Delivery Network) loading failures
- No fallback mechanism when primary CDN was down
- Missing error handling for network issues

We fixed it by:
- Adding 3 CDN sources with automatic fallback
- Implementing comprehensive error handling
- Adding retry logic for failed loads
- Creating diagnostic and testing tools
