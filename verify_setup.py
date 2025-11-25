#!/usr/bin/env python3
"""
Setup verification script to ensure all components work together.
Run this after installation to verify everything is configured correctly.
"""
import os
import sys
import json

def check_file_exists(filepath, description):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: NOT FOUND - {filepath}")
        return False

def check_import(module_name, description):
    """Check if a Python module can be imported."""
    try:
        __import__(module_name)
        print(f"✅ {description}: {module_name}")
        return True
    except ImportError as e:
        print(f"❌ {description}: {module_name} - {str(e)}")
        return False

def check_json_file(filepath, description):
    """Check if a JSON file is valid."""
    try:
        with open(filepath) as f:
            json.load(f)
        print(f"✅ {description}: {filepath}")
        return True
    except FileNotFoundError:
        print(f"❌ {description}: NOT FOUND - {filepath}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ {description}: INVALID JSON - {str(e)}")
        return False

def main():
    """Run all verification checks."""
    print("\n" + "="*70)
    print("    TELEGRAM-IMAGE-OCR SETUP VERIFICATION")
    print("="*70 + "\n")
    
    checks_passed = 0
    checks_total = 0
    
    # Check Python version
    print("📋 Python Environment")
    print("-" * 70)
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    if sys.version_info >= (3, 7):
        print(f"✅ Python version: {py_version} (3.7+ required)")
        checks_passed += 1
    else:
        print(f"❌ Python version: {py_version} (3.7+ required)")
    checks_total += 1
    
    # Check core modules
    print("\n📦 Core Modules")
    print("-" * 70)
    modules = [
        ("config", "Configuration module"),
        ("triggers", "Trigger system"),
        ("trigger_config_loader", "Config loader"),
        ("alert_handlers", "Alert handlers"),
        ("phone_call", "Phone call handler"),
        ("process_image", "Image processing"),
        ("process_check_visa_slots", "Visa slots checker"),
        ("monitor_telegram", "Main application"),
    ]
    
    for module, desc in modules:
        if check_import(module, desc):
            checks_passed += 1
        checks_total += 1
    
    # Check dependencies
    print("\n📚 External Dependencies")
    print("-" * 70)
    dependencies = [
        ("telethon", "Telethon (Telegram client)"),
        ("PIL", "Pillow (Image processing)"),
        ("pytesseract", "Tesseract (OCR)"),
        ("requests", "Requests (HTTP library)"),
        ("pytz", "Pytz (Timezone)"),
    ]
    
    for module, desc in dependencies:
        if check_import(module, desc):
            checks_passed += 1
        checks_total += 1
    
    # Check configuration files
    print("\n⚙️  Configuration Files")
    print("-" * 70)
    configs = [
        ("session.conf", "Telegram session config"),
        ("trigger_configs.json", "Trigger configurations"),
    ]
    
    for config_file, desc in configs:
        if config_file.endswith(".json"):
            if check_json_file(config_file, desc):
                checks_passed += 1
            else:
                checks_passed += 0
        else:
            if check_file_exists(config_file, desc):
                checks_passed += 1
            else:
                checks_passed += 0
        checks_total += 1
    
    # Check other files
    print("\n📄 Project Files")
    print("-" * 70)
    files = [
        ("requirements.txt", "Python requirements"),
        ("README.md", "README"),
        ("INDEX.md", "Documentation index"),
    ]
    
    for filepath, desc in files:
        if check_file_exists(filepath, desc):
            checks_passed += 1
        checks_total += 1
    
    # Check tesseract installation
    print("\n🔍 System Dependencies")
    print("-" * 70)
    try:
        import pytesseract
        from PIL import Image
        # Try to get tesseract version
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✅ Tesseract OCR: Installed - {version}")
            checks_passed += 1
        except Exception as e:
            print(f"⚠️  Tesseract: Detected but could not verify - {str(e)}")
            checks_passed += 1
    except ImportError:
        print(f"❌ Tesseract/Pillow: Not available")
    checks_total += 1
    
    # Summary
    print("\n" + "="*70)
    print(f"    VERIFICATION RESULTS: {checks_passed}/{checks_total} checks passed")
    print("="*70 + "\n")
    
    if checks_passed == checks_total:
        print("✅ All checks passed! Your setup is ready to use.\n")
        print("Next steps:")
        print("  1. Read: README.md")
        print("  2. Review: INDEX.md for documentation")
        print("  3. Try: Examples in QUICK_START.md")
        print("  4. Run: python3 monitor_telegram.py\n")
        return 0
    else:
        print(f"⚠️  {checks_total - checks_passed} check(s) failed.\n")
        print("Please address the issues above:")
        print("  • Install missing dependencies: pip3 install -r requirements.txt")
        print("  • Create config files: cp sample_* .")
        print("  • Install tesseract: See https://github.com/tesseract-ocr/tesseract\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
