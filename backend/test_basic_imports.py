#!/usr/bin/env python3
print("Testing basic imports...")

try:
    import flask
    print("✅ Flask OK")
except Exception as e:
    print(f"❌ Flask error: {e}")

try:
    from reportlab.lib.pagesizes import letter
    print("✅ ReportLab OK")
except Exception as e:
    print(f"❌ ReportLab error: {e}")

try:
    from openpyxl import Workbook
    print("✅ openpyxl OK")
except Exception as e:
    print(f"❌ openpyxl error: {e}")

try:
    from docx import Document
    print("✅ python-docx OK")  
except Exception as e:
    print(f"❌ python-docx error: {e}")

print("Basic import test done.")
