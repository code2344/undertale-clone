#!/usr/bin/env python3
"""
Compatibility check script for WebAssembly/Pygbag build.
This script verifies that the codebase is ready for browser deployment.
"""

import sys
import os
import importlib.util

def check_file_exists(filepath, description):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} not found: {filepath}")
        return False

def check_import(module_name):
    """Check if a module can be imported."""
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            print(f"✅ Module '{module_name}' can be imported")
            return True
        else:
            print(f"⚠️  Module '{module_name}' not found (may be optional)")
            return False
    except Exception as e:
        print(f"❌ Error checking module '{module_name}': {e}")
        return False

def check_syntax(filepath):
    """Check if a Python file has valid syntax."""
    try:
        with open(filepath, 'r') as f:
            compile(f.read(), filepath, 'exec')
        print(f"✅ Syntax valid: {filepath}")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in {filepath}: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Could not check {filepath}: {e}")
        return False

def main():
    print("=" * 60)
    print("WebAssembly Compatibility Check")
    print("=" * 60)
    print()
    
    issues = []
    
    # Check essential files
    print("Checking essential files...")
    print("-" * 60)
    if not check_file_exists("main_web.py", "WebAssembly entry point"):
        issues.append("main_web.py is missing")
    if not check_file_exists("build.sh", "Build script"):
        issues.append("build.sh is missing")
    if not check_file_exists("pygbag.toml", "Pygbag configuration"):
        issues.append("pygbag.toml is missing")
    if not check_file_exists("BROWSER_BUILD.md", "Browser build documentation"):
        issues.append("BROWSER_BUILD.md is missing")
    print()
    
    # Check Python syntax
    print("Checking Python syntax...")
    print("-" * 60)
    python_files = [
        "main.py",
        "main_web.py",
        "globals.py",
        "frisk.py",
        "draw.py",
    ]
    for pf in python_files:
        if os.path.exists(pf):
            if not check_syntax(pf):
                issues.append(f"Syntax error in {pf}")
    print()
    
    # Check directory structure
    print("Checking asset directories...")
    print("-" * 60)
    asset_dirs = ["sprites", "fonts", "mus", "sfx"]
    for d in asset_dirs:
        if os.path.isdir(d):
            print(f"✅ Asset directory exists: {d}")
        else:
            print(f"⚠️  Asset directory not found: {d} (may affect gameplay)")
    print()
    
    # Check for problematic patterns
    print("Checking for potential compatibility issues...")
    print("-" * 60)
    
    # Check for absolute paths
    found_issues = False
    for root, dirs, files in os.walk("."):
        # Skip .git and build directories
        dirs[:] = [d for d in dirs if d not in ['.git', 'build', '__pycache__', 'decompilation']]
        
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                        # Check for absolute paths (simple heuristic)
                        if '"/home/' in content or '"/usr/' in content or '"C:\\' in content:
                            print(f"⚠️  Possible absolute path in {filepath}")
                            found_issues = True
                except Exception:
                    pass
    
    if not found_issues:
        print("✅ No obvious absolute paths found")
    print()
    
    # Summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    if issues:
        print(f"❌ Found {len(issues)} issue(s):")
        for issue in issues:
            print(f"   - {issue}")
        print()
        print("Please fix these issues before building for browser.")
        return 1
    else:
        print("✅ All checks passed!")
        print()
        print("Your codebase appears ready for WebAssembly build.")
        print("Run './build.sh' to build for browser.")
        return 0

if __name__ == "__main__":
    sys.exit(main())
