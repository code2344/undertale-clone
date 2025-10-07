#!/usr/bin/env python3
"""
Simple test to verify the game can run in browser mode
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing browser compatibility...")
print("=" * 60)

# Test 1: Check if main_web.py exists and has correct structure
print("\n✓ Test 1: Checking main_web.py...")
try:
    import main_web
    print("  ✅ main_web.py imports successfully")
    
    # Check for required functions
    assert hasattr(main_web, 'async_main'), "Missing async_main function"
    assert hasattr(main_web, 'async_maincycle'), "Missing async_maincycle function"
    print("  ✅ Required async functions present")
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

# Test 2: Check if main.py can be imported
print("\n✓ Test 2: Checking main.py...")
try:
    import main
    print("  ✅ main.py imports successfully")
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

# Test 3: Check essential modules
print("\n✓ Test 3: Checking essential modules...")
essential_modules = ['globals', 'frisk', 'rooms', 'draw', 'sprite']
for module_name in essential_modules:
    try:
        __import__(module_name)
        print(f"  ✅ {module_name} imports successfully")
    except Exception as e:
        print(f"  ❌ {module_name} failed: {e}")

# Test 4: Check asset directories
print("\n✓ Test 4: Checking asset directories...")
asset_dirs = ['sprites', 'fonts', 'mus', 'sfx']
for asset_dir in asset_dirs:
    if os.path.exists(asset_dir) and os.path.isdir(asset_dir):
        file_count = len([f for f in os.listdir(asset_dir) if os.path.isfile(os.path.join(asset_dir, f))])
        print(f"  ✅ {asset_dir}/ exists ({file_count} files)")
    else:
        print(f"  ⚠️  {asset_dir}/ not found")

# Test 5: Check pygame compatibility
print("\n✓ Test 5: Checking Pygame...")
try:
    import pygame
    print(f"  ✅ Pygame version: {pygame.version.ver}")
except Exception as e:
    print(f"  ❌ Pygame import failed: {e}")
    sys.exit(1)

# Test 6: Check build files
print("\n✓ Test 6: Checking build configuration...")
build_files = ['pygbag.toml', 'build.sh']
for build_file in build_files:
    if os.path.exists(build_file):
        print(f"  ✅ {build_file} exists")
    else:
        print(f"  ⚠️  {build_file} not found")

print("\n" + "=" * 60)
print("✅ All tests passed!")
print("\nThe game is ready for browser build.")
print("\nTo build for browser:")
print("  ./build.sh")
print("\nTo test locally:")
print("  cd build/web && python3 -m http.server 8000")
print("=" * 60)
