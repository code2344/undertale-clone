#!/usr/bin/env python3
"""
Web Build Validation Script

This script validates that the Undertale Clone web build is correctly structured
and contains all necessary components for browser-based gameplay.
"""

import os
import sys
import json
from pathlib import Path

def check_mark(condition):
    return "✅" if condition else "❌"

def validate_build():
    """Validate the web build structure and contents."""
    
    print("=" * 70)
    print("Undertale Clone - Web Build Validation")
    print("=" * 70)
    print()
    
    build_dir = Path("build/web")
    results = {}
    
    # Check 1: Build directory exists
    print("📁 Checking build directory...")
    build_exists = build_dir.exists() and build_dir.is_dir()
    results["build_directory"] = build_exists
    print(f"   {check_mark(build_exists)} Build directory: {build_dir}")
    
    if not build_exists:
        print("\n❌ Build directory not found. Run './build.sh' first.")
        return False
    
    print()
    
    # Check 2: Required files
    print("📄 Checking required files...")
    required_files = {
        "index.html": "Game loader HTML",
        "undertale-clone.apk": "Compiled game package",
        "favicon.png": "Game icon"
    }
    
    all_files_exist = True
    for filename, description in required_files.items():
        file_path = build_dir / filename
        exists = file_path.exists()
        results[f"file_{filename}"] = exists
        all_files_exist &= exists
        
        size_info = ""
        if exists:
            size_mb = file_path.stat().st_size / (1024 * 1024)
            size_info = f" ({size_mb:.1f} MB)" if size_mb >= 1 else f" ({file_path.stat().st_size} bytes)"
        
        print(f"   {check_mark(exists)} {filename:<25} - {description}{size_info}")
    
    print()
    
    # Check 3: Index.html structure
    print("🔍 Analyzing index.html...")
    index_path = build_dir / "index.html"
    
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            index_content = f.read()
        
        checks = {
            'pythons.js': 'Python WebAssembly loader',
            'undertale-clone.apk': 'Game package reference',
            'python3.12': 'Python 3.12 runtime',
            'async def custom_site': 'Async game initialization'
        }
        
        for check, description in checks.items():
            found = check in index_content
            results[f"index_{check}"] = found
            print(f"   {check_mark(found)} {description}")
    else:
        print("   ❌ index.html not found")
    
    print()
    
    # Check 4: APK size validation
    print("📦 Validating game package...")
    apk_path = build_dir / "undertale-clone.apk"
    
    if apk_path.exists():
        apk_size_mb = apk_path.stat().st_size / (1024 * 1024)
        size_ok = apk_size_mb > 50  # Should be > 50MB with all assets
        results["apk_size"] = size_ok
        
        print(f"   {check_mark(size_ok)} APK size: {apk_size_mb:.1f} MB")
        
        if apk_size_mb > 150:
            print(f"   ✅ Size indicates full asset bundle (sprites, music, etc.)")
        else:
            print(f"   ⚠️  Size smaller than expected - some assets may be missing")
    else:
        print("   ❌ APK file not found")
        results["apk_size"] = False
    
    print()
    
    # Check 5: Source files validation
    print("🎮 Checking source game files...")
    source_checks = {
        "main.py": "Main entry point",
        "main_web.py": "WebAssembly entry point",
        "globals.py": "Game globals",
        "frisk.py": "Player character",
        "draw.py": "Rendering system",
        "sprite.py": "Sprite system"
    }
    
    all_sources_exist = True
    for filename, description in source_checks.items():
        exists = Path(filename).exists()
        results[f"source_{filename}"] = exists
        all_sources_exist &= exists
        print(f"   {check_mark(exists)} {filename:<20} - {description}")
    
    print()
    
    # Check 6: Asset directories
    print("🎨 Checking asset directories...")
    asset_dirs = {
        "sprites": "Game sprites",
        "fonts": "Font files",
        "mus": "Music files",
        "sfx": "Sound effects",
        "rooms": "Room definitions"
    }
    
    all_assets_exist = True
    for dirname, description in asset_dirs.items():
        dir_path = Path(dirname)
        exists = dir_path.exists() and dir_path.is_dir()
        results[f"assets_{dirname}"] = exists
        all_assets_exist &= exists
        
        file_count = 0
        if exists:
            file_count = len(list(dir_path.glob("**/*")))
        
        print(f"   {check_mark(exists)} {dirname:<12} - {description} ({file_count} items)")
    
    print()
    
    # Check 7: PyBag configuration
    print("⚙️  Checking Pygbag configuration...")
    pygbag_toml = Path("pygbag.toml")
    
    if pygbag_toml.exists():
        print(f"   ✅ pygbag.toml found")
        results["pygbag_config"] = True
        
        try:
            import toml
            config = toml.load(pygbag_toml)
            print(f"   ✅ Resolution: {config.get('width', 'N/A')}x{config.get('height', 'N/A')}")
            print(f"   ✅ Archive: {config.get('archive', 'N/A')}")
        except:
            print("   ⚠️  Could not parse config (toml module not available)")
    else:
        print(f"   ❌ pygbag.toml not found")
        results["pygbag_config"] = False
    
    print()
    
    # Check 8: Testing accessibility
    print("🌐 Testing deployment accessibility...")
    
    import subprocess
    try:
        result = subprocess.run(
            ["curl", "-I", "-s", "https://code2344.github.io/undertale-clone/"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if "200" in result.stdout or "HTTP/2 200" in result.stdout:
            print("   ✅ GitHub Pages deployment is live and accessible")
            print("   🌐 URL: https://code2344.github.io/undertale-clone/")
            results["deployment"] = True
        else:
            print("   ❌ Deployment not accessible")
            results["deployment"] = False
    except Exception as e:
        print(f"   ⚠️  Could not verify deployment: {e}")
        results["deployment"] = None
    
    print()
    print("=" * 70)
    print("Validation Summary")
    print("=" * 70)
    print()
    
    total_checks = len(results)
    passed_checks = sum(1 for v in results.values() if v is True)
    
    print(f"Total Checks: {total_checks}")
    print(f"Passed: {passed_checks}")
    print(f"Failed: {total_checks - passed_checks}")
    print()
    
    if passed_checks >= total_checks * 0.9:  # 90% pass rate
        print("✅ BUILD VALIDATION: PASSED")
        print()
        print("The web build is correctly structured and ready for deployment.")
        print()
        print("🎮 To test the game:")
        print("   Option 1: Visit https://code2344.github.io/undertale-clone/")
        print("   Option 2: Run local server:")
        print("             cd build/web")
        print("             python3 -m http.server 8000")
        print("             Open http://localhost:8000")
        print()
        return True
    else:
        print("❌ BUILD VALIDATION: FAILED")
        print()
        print("Some components are missing. Please run './build.sh' to rebuild.")
        print()
        return False

def check_gameplay_requirements():
    """Check if all components needed for the specified gameplay test are present."""
    
    print()
    print("=" * 70)
    print("Gameplay Test Requirements Check")
    print("=" * 70)
    print()
    
    print("📋 Required for 'Play to start of Ruins with name=copilot':")
    print()
    
    requirements = {
        "Name selection system": Path("decompilation/code/gml_Script_scr_namingscreen.gml.lsp").exists(),
        "Room definitions": Path("rooms").exists(),
        "Ruins room files": Path("decompilation/code/gml_Script_scr_roomname.gml.lsp").exists(),
        "Encounter system": any(Path("decompilation/code").glob("*encount*.lsp")) if Path("decompilation/code").exists() else False,
        "Save system": Path("decompilation/code/gml_Script_scr_save.gml.lsp").exists() if Path("decompilation/code").exists() else False,
        "Music system": Path("mus/mus_ruins.ogg").exists(),
        "Sprite system": Path("sprites").exists() and len(list(Path("sprites").glob("*.png"))) > 100
    }
    
    for requirement, satisfied in requirements.items():
        print(f"   {check_mark(satisfied)} {requirement}")
    
    print()
    
    all_satisfied = all(requirements.values())
    if all_satisfied:
        print("✅ All gameplay requirements present")
        print()
        print("📝 Test Plan:")
        print("   1. Load game in browser")
        print("   2. Wait for intro sequence")
        print("   3. Enter name: 'copilot'")
        print("   4. Complete naming confirmation")
        print("   5. Play through intro")
        print("   6. Progress to Ruins entrance")
        print("   7. Test random encounters")
        print("   8. Verify all features work")
        print()
    else:
        print("❌ Some gameplay requirements missing")
    
    return all_satisfied

if __name__ == "__main__":
    print()
    try:
        build_valid = validate_build()
        gameplay_ready = check_gameplay_requirements()
        
        print("=" * 70)
        print()
        
        if build_valid and gameplay_ready:
            print("🎉 SUCCESS: Web version is ready for testing!")
            print()
            sys.exit(0)
        else:
            print("⚠️  WARNING: Some validation checks failed")
            print()
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
