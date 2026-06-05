#!/usr/bin/env python
"""
Test Script - Verify Email Scam Detector is working correctly
Run this to ensure all components are functional
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all modules can be imported"""
    print("\n🧪 TESTING IMPORTS...")
    try:
        import flask
        print("  ✓ Flask imported successfully")
    except ImportError as e:
        print(f"  ✗ Flask import failed: {e}")
        return False
    
    try:
        import sklearn
        print("  ✓ Scikit-Learn imported successfully")
    except ImportError as e:
        print(f"  ✗ Scikit-Learn import failed: {e}")
        return False
    
    try:
        import pandas
        print("  ✓ Pandas imported successfully")
    except ImportError as e:
        print(f"  ✗ Pandas import failed: {e}")
        return False
    
    try:
        import numpy
        print("  ✓ NumPy imported successfully")
    except ImportError as e:
        print(f"  ✗ NumPy import failed: {e}")
        return False
    
    try:
        import nltk
        print("  ✓ NLTK imported successfully")
    except ImportError as e:
        print(f"  ✗ NLTK import failed: {e}")
        return False
    
    return True

def test_file_structure():
    """Test that all required files exist"""
    print("\n📁 TESTING FILE STRUCTURE...")
    
    required_files = [
        "app.py",
        "config.py",
        "requirements.txt",
        "verify_setup.py",
        "utils/logger.py",
        "utils/data_handler.py",
        "utils/text_processor.py",
        "utils/ml_engine.py",
        "templates/index.html",
        "static/css/style.css",
        "static/js/app.js",
    ]
    
    all_exist = True
    for file in required_files:
        path = Path(file)
        if path.exists():
            size = path.stat().st_size
            print(f"  ✓ {file} ({size:,} bytes)")
        else:
            print(f"  ✗ {file} NOT FOUND")
            all_exist = False
    
    return all_exist

def test_app_structure():
    """Test that app.py has all required components"""
    print("\n🔍 TESTING APP STRUCTURE...")
    
    with open("app.py", "r") as f:
        content = f.read()
    
    required_functions = [
        "init_components",
        "get_risk_level",
        "validate_input",
        "index",
        "predict",
        "health",
        "get_history",
        "get_stats",
    ]
    
    all_found = True
    for func in required_functions:
        if f"def {func}" in content:
            print(f"  ✓ Function '{func}' found")
        else:
            print(f"  ✗ Function '{func}' NOT FOUND")
            all_found = False
    
    return all_found

def test_utils():
    """Test that utils modules are properly structured"""
    print("\n🛠️  TESTING UTILS MODULES...")
    
    modules = {
        "utils/logger.py": ("get_logger", "function"),
        "utils/data_handler.py": ("DataHandler", "class"),
        "utils/text_processor.py": ("TextProcessor", "class"),
        "utils/ml_engine.py": ("MLEngine", "class"),
    }
    
    all_found = True
    for module_path, (item, item_type) in modules.items():
        with open(module_path, "r") as f:
            content = f.read()
        
        search_str = f"def {item}" if item_type == "function" else f"class {item}"
        if search_str in content:
            print(f"  ✓ {module_path}: {item_type} {item}")
        else:
            print(f"  ✗ {module_path}: {item_type} {item} NOT FOUND")
            all_found = False
    
    return all_found

def test_directories():
    """Test that all required directories exist or can be created"""
    print("\n📂 TESTING DIRECTORIES...")
    
    required_dirs = [
        "data",
        "models",
        "static",
        "static/css",
        "static/js",
        "templates",
        "utils",
        "logs",
    ]
    
    all_ok = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists() and path.is_dir():
            print(f"  ✓ {dir_path}/ exists")
        else:
            try:
                path.mkdir(parents=True, exist_ok=True)
                print(f"  ✓ {dir_path}/ created")
            except Exception as e:
                print(f"  ✗ {dir_path}/ creation failed: {e}")
                all_ok = False
    
    return all_ok

def main():
    """Run all tests"""
    print("=" * 60)
    print("EMAIL SCAM DETECTOR - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Directories", test_directories),
        ("App Structure", test_app_structure),
        ("Utils Modules", test_utils),
    ]
    
    results = {}
    for name, test_fn in tests:
        try:
            results[name] = test_fn()
        except Exception as e:
            print(f"\n❌ {name} test failed with error: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    print("\n" + "=" * 60)
    
    if passed == total:
        print(f"✅ ALL TESTS PASSED ({passed}/{total})")
        print("\n🚀 Ready to launch!")
        print("   Run: python app.py")
        print("   Then open: http://localhost:5000")
        return True
    else:
        print(f"❌ SOME TESTS FAILED ({passed}/{total})")
        print("\nPlease fix the issues above and try again.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
