#!/usr/bin/env python3
"""
Diagnostic script for identifying and resolving 1401 errors.
This script checks common causes of loading failures in the browser build.
"""

import sys
import urllib.request
import urllib.error
import json
from pathlib import Path

def check_mark(passed):
    return "✅" if passed else "❌"

def check_cdn_availability():
    """Check if CDN sources are reachable."""
    print("🌐 Checking CDN availability...")
    
    cdn_urls = [
        ("jsDelivr v0.26.2", "https://cdn.jsdelivr.net/pyodide/v0.26.2/full/pyodide.js"),
        ("cdnjs v0.26.2", "https://cdnjs.cloudflare.com/ajax/libs/pyodide/0.26.2/pyodide.js"),
        ("jsDelivr v0.24.1", "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"),
    ]
    
    results = {}
    for name, url in cdn_urls:
        try:
            req = urllib.request.Request(url, method='HEAD')
            req.add_header('User-Agent', 'Mozilla/5.0')
            with urllib.request.urlopen(req, timeout=10) as response:
                status = response.status
                results[name] = (status == 200)
                print(f"   {check_mark(status == 200)} {name}: HTTP {status}")
        except urllib.error.HTTPError as e:
            results[name] = False
            print(f"   {check_mark(False)} {name}: HTTP {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            results[name] = False
            print(f"   {check_mark(False)} {name}: Network error - {e.reason}")
        except Exception as e:
            results[name] = False
            print(f"   {check_mark(False)} {name}: {str(e)}")
    
    print()
    return all(results.values())

def check_pygbag_version():
    """Check pygbag version."""
    print("📦 Checking pygbag installation...")
    
    try:
        import subprocess
        result = subprocess.run(
            ['pip', 'show', 'pygbag'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('Version:'):
                    version = line.split(':', 1)[1].strip()
                    print(f"   ✅ Pygbag version: {version}")
                    
                    # Check if version is recent (0.8.0+)
                    try:
                        major, minor, *_ = version.split('.')
                        if int(major) == 0 and int(minor) >= 8:
                            print(f"   ✅ Version is recent (0.8.0+)")
                            return True
                        else:
                            print(f"   ⚠️  Version is old. Recommended: 0.8.0+")
                            print(f"   Run: pip install --upgrade pygbag")
                            return False
                    except:
                        print(f"   ⚠️  Could not parse version")
                        return True
            return True
        else:
            print(f"   ❌ Pygbag not installed")
            print(f"   Run: pip install pygbag")
            return False
    except Exception as e:
        print(f"   ❌ Error checking pygbag: {e}")
        return False

def check_build_artifacts():
    """Check if build artifacts exist and are valid."""
    print("🔍 Checking build artifacts...")
    
    build_dir = Path('build/web')
    
    if not build_dir.exists():
        print(f"   ❌ Build directory not found: {build_dir}")
        print(f"   Run: ./build.sh")
        return False
    
    required_files = [
        'index.html',
    ]
    
    all_exist = True
    for filename in required_files:
        filepath = build_dir / filename
        exists = filepath.exists()
        all_exist &= exists
        
        if exists:
            size = filepath.stat().st_size
            print(f"   ✅ {filename} ({size} bytes)")
        else:
            print(f"   ❌ {filename} missing")
    
    # Check for .apk file (pygbag package)
    apk_files = list(build_dir.glob('*.apk'))
    if apk_files:
        for apk in apk_files:
            size_mb = apk.stat().st_size / (1024 * 1024)
            print(f"   ✅ {apk.name} ({size_mb:.1f} MB)")
    else:
        print(f"   ⚠️  No .apk package found")
    
    print()
    return all_exist

def check_asset_files():
    """Check if asset directories exist."""
    print("🎨 Checking asset directories...")
    
    asset_dirs = ['sprites', 'fonts', 'mus', 'sfx']
    all_exist = True
    
    for dirname in asset_dirs:
        dirpath = Path(dirname)
        exists = dirpath.exists() and dirpath.is_dir()
        all_exist &= exists
        
        if exists:
            file_count = len(list(dirpath.glob('**/*')))
            print(f"   ✅ {dirname}/ ({file_count} items)")
        else:
            print(f"   ❌ {dirname}/ not found")
    
    print()
    return all_exist

def check_python_files():
    """Check critical Python files."""
    print("🐍 Checking Python files...")
    
    required_files = [
        'main.py',
        'main_web.py',
        '__init__.py',
        'pygbag.toml'
    ]
    
    all_exist = True
    for filename in required_files:
        filepath = Path(filename)
        exists = filepath.exists()
        all_exist &= exists
        print(f"   {check_mark(exists)} {filename}")
    
    print()
    return all_exist

def provide_recommendations(cdn_ok, pygbag_ok, build_ok, assets_ok, files_ok):
    """Provide recommendations based on diagnostic results."""
    print("=" * 70)
    print("📋 RECOMMENDATIONS")
    print("=" * 70)
    print()
    
    if not cdn_ok:
        print("⚠️  CDN Issues Detected:")
        print("   • The game uses CDN fallback to handle unavailable sources")
        print("   • Check your internet connection")
        print("   • Try disabling VPN/proxy")
        print("   • The browser will automatically try alternative CDNs")
        print()
    
    if not pygbag_ok:
        print("⚠️  Pygbag Issues:")
        print("   • Install or update pygbag: pip install --upgrade pygbag")
        print()
    
    if not build_ok:
        print("⚠️  Build Issues:")
        print("   • Run ./build.sh to create the web build")
        print("   • If build fails, check TROUBLESHOOTING.md")
        print()
    
    if not assets_ok:
        print("⚠️  Asset Issues:")
        print("   • Some asset directories are missing")
        print("   • Game may not function properly without assets")
        print()
    
    if not files_ok:
        print("⚠️  Missing Files:")
        print("   • Critical Python files are missing")
        print("   • Ensure you have the complete repository")
        print()
    
    if all([cdn_ok, pygbag_ok, build_ok, assets_ok, files_ok]):
        print("✅ All checks passed!")
        print()
        print("If you're still experiencing 1401 errors:")
        print("   1. Clear browser cache (Ctrl+Shift+Delete)")
        print("   2. Try a different browser")
        print("   3. Check browser console (F12) for specific errors")
        print("   4. Rebuild: rm -rf build/ && ./build.sh")
        print()

def main():
    """Main diagnostic routine."""
    print("=" * 70)
    print("Undertale Clone - 1401 Error Diagnostic Tool")
    print("=" * 70)
    print()
    
    # Run all checks
    cdn_ok = check_cdn_availability()
    pygbag_ok = check_pygbag_version()
    print()
    build_ok = check_build_artifacts()
    assets_ok = check_asset_files()
    files_ok = check_python_files()
    
    # Provide recommendations
    provide_recommendations(cdn_ok, pygbag_ok, build_ok, assets_ok, files_ok)
    
    # Return exit code
    if all([cdn_ok, pygbag_ok, build_ok, assets_ok, files_ok]):
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main())
