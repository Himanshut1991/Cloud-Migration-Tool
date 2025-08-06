#!/usr/bin/env python3
"""
Test if the backend file has syntax errors
"""

try:
    print("Testing backend file...")
    exec(open('working_backend.py').read())
    print("✅ Backend file loaded successfully")
except Exception as e:
    print(f"❌ Backend error: {e}")
    print(f"Error type: {type(e)}")
