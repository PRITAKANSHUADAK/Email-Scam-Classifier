#!/usr/bin/env python
"""
Startup verification script - Ensures all dependencies and components are ready
"""

import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required (you have {version.major}.{version.minor})")
        return False
    print(f"✓ Python {version.major}.{version.minor} detected")
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    required = [
        "flask",
        "sklearn",
        "pandas",
        "numpy",
        "nltk",
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            missing.append(package)
    
    if missing:
        print(f"\nInstalling missing packages: {', '.join(missing)}")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        return True
    
    return True

def check_directories():
    """Check and create necessary directories"""
    dirs = [
        Path("data"),
        Path("models"),
        Path("static"),
        Path("static/css"),
        Path("static/js"),
        Path("templates"),
        Path("logs"),
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"✓ Directory {d} ready")
    
    return True

def main():
    """Run all startup checks"""
    print("\n" + "="*60)
    print("EMAIL SCAM DETECTOR - STARTUP VERIFICATION")
    print("="*60 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Directories", check_directories),
    ]
    
    for name, check_fn in checks:
        try:
            if not check_fn():
                print(f"\n❌ {name} check failed")
                return False
        except Exception as e:
            print(f"\n❌ {name} check error: {e}")
            return False
    
    print("\n" + "="*60)
    print("✓ ALL CHECKS PASSED - SYSTEM READY")
    print("="*60)
    print("\nStart the application with:")
    print("  python app.py")
    print("\nThen open browser to:")
    print("  http://localhost:5000")
    print()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
