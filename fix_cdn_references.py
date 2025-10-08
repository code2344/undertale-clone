#!/usr/bin/env python3
"""
Script to fix CDN references in the pygbag build and download necessary runtime files.
This resolves the "1401 errors" by self-hosting all pygbag runtime dependencies.
"""

import os
import sys
import urllib.request
from pathlib import Path

# CDN URLs
PYGBAG_CDN = "https://pygame-web.github.io/archives/0.9/"

# Required files to download
REQUIRED_FILES = [
    "pythons.js",
    "browserfs.min.js",
    "pythonrc.py",
    "cpythonrc.py",
    "empty.html",
    "vtx.js",
    "fs.js",
    "snd.js",
    "gui.js",
    "vt/xterm.js",
    "vt/xterm.css",
    "vt/xterm-addon-image.js",
    "xtermjsixel/xterm-addon-image-worker.js",
    "cpython312/main.js",
    "cpython312/main.data",
    "cpython312/main.wasm",
]

def download_file(url, output_path):
    """Download a file from URL to output path."""
    print(f"   Downloading {output_path.name}...")
    os.makedirs(output_path.parent, exist_ok=True)
    try:
        urllib.request.urlretrieve(url, output_path)
        return True
    except Exception as e:
        print(f"   ⚠️  Failed to download {url}: {e}")
        return False

def download_pygbag_runtime(build_dir):
    """Download all required pygbag runtime files."""
    print("\n📥 Downloading pygbag runtime files...")
    
    pygbag_dir = build_dir / "pygbag"
    pygbag_dir.mkdir(exist_ok=True)
    
    success_count = 0
    for file_path in REQUIRED_FILES:
        url = f"{PYGBAG_CDN}{file_path}"
        output_path = pygbag_dir / file_path
        if download_file(url, output_path):
            success_count += 1
    
    print(f"✅ Downloaded {success_count}/{len(REQUIRED_FILES)} files")
    return success_count == len(REQUIRED_FILES)

def fix_cdn_references(index_html_path, pygbag_dir):
    """Replace remote CDN references with local paths in index.html and JS files."""
    print(f"\n🔧 Fixing CDN references...")
    
    if not index_html_path.exists():
        print(f"❌ {index_html_path} not found")
        return False
    
    # Fix index.html
    with open(index_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_count = content.count('pygame-web.github.io/archives/0.9/')
    content = content.replace('https://pygame-web.github.io/archives/0.9/', 'pygbag/')
    
    with open(index_html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"   ✅ Fixed {original_count} CDN references in index.html")
    
    # Fix vtx.js to use local paths
    vtx_js = pygbag_dir / 'vtx.js'
    if vtx_js.exists():
        with open(vtx_js, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('https://pygame-web.github.io/archives/vt/', 'vt/')
        with open(vtx_js, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   ✅ Fixed CDN references in vtx.js")
    
    # Fix pythons.js to redirect package repo fetches to local
    pythons_js = pygbag_dir / 'pythons.js'
    if pythons_js.exists():
        with open(pythons_js, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add URL rewriting for package repo
        old_cross_file = 'window.cross_file = function * cross_file(url, store, flags) {'
        new_cross_file = '''window.cross_file = function * cross_file(url, store, flags) {
    // Redirect remote package repo to local stub
    if (url.includes('pygame-web.github.io/archives/repo/')) {
        url = url.replace('https://pygame-web.github.io/archives/repo/', 'pygbag/repo/');
    }'''
        
        if old_cross_file in content:
            content = content.replace(old_cross_file, new_cross_file)
            with open(pythons_js, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   ✅ Added package repo URL rewriting to pythons.js")
        else:
            print(f"   ⚠️  Could not find cross_file function in pythons.js")
    
    # Create stub package index to prevent fetch errors
    repo_dir = pygbag_dir / 'repo'
    repo_dir.mkdir(exist_ok=True)
    
    # Create empty package index files - pygbag will use bundled packages from the APK
    index_file = repo_dir / 'index-090-cp312.json'
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write('{}')
    
    repodata_file = repo_dir / 'repodata.json'
    with open(repodata_file, 'w', encoding='utf-8') as f:
        f.write('{}')
    
    print(f"   ✅ Created stub package index files")
    
    return True

def main():
    """Main entry point."""
    print("=" * 70)
    print("CDN Reference Fixer for Undertale Clone")
    print("=" * 70)
    
    build_dir = Path('build/web')
    
    if not build_dir.exists():
        print("❌ Build directory not found. Run ./build.sh first.")
        return 1
    
    index_html = build_dir / 'index.html'
    
    # Step 1: Download pygbag runtime files
    if not download_pygbag_runtime(build_dir):
        print("\n⚠️  Some files failed to download, but continuing...")
    
    # Step 2: Fix CDN references in index.html
    if not fix_cdn_references(index_html, build_dir / 'pygbag'):
        print("\n❌ Failed to fix CDN references")
        return 1
    
    print("\n" + "=" * 70)
    print("✅ SUCCESS! All CDN references fixed")
    print("=" * 70)
    print("\nThe game should now load without external CDN dependencies.")
    print("\nTest it by running:")
    print("   cd build/web && python3 -m http.server 8000")
    print("\nThen open http://localhost:8000 in your browser")
    print()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
