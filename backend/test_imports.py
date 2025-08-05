#!/usr/bin/env python3
"""Simple export test"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("Testing export imports...")

try:
    from services.export_service_new import ExportService
    print("✓ ExportService imported successfully")
    
    # Test creating an instance
    service = ExportService(None, {})
    print("✓ ExportService instance created")
    print(f"Output directory: {service.output_dir}")
    
    # Check if output directory exists
    if os.path.exists(service.output_dir):
        print("✓ Output directory exists")
    else:
        print("✗ Output directory does not exist, creating...")
        os.makedirs(service.output_dir, exist_ok=True)
        print("✓ Output directory created")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting pandas import...")
try:
    import pandas as pd
    print("✓ Pandas imported successfully")
except Exception as e:
    print(f"✗ Pandas error: {e}")

print("\nTesting openpyxl import...")
try:
    import openpyxl
    print("✓ Openpyxl imported successfully")
except Exception as e:
    print(f"✗ Openpyxl error: {e}")

print("\nTesting reportlab import...")
try:
    import reportlab
    print("✓ Reportlab imported successfully")
except Exception as e:
    print(f"✗ Reportlab error: {e}")

print("\nTesting docx import...")
try:
    from docx import Document
    print("✓ Python-docx imported successfully")
except Exception as e:
    print(f"✗ Python-docx error: {e}")

print("\nAll import tests completed!")
