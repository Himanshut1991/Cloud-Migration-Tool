#!/usr/bin/env python3
"""Test script to check if timeline imports work"""

try:
    print("Testing imports...")
    
    # Test basic imports
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    print("✓ Flask imports successful")
    
    # Test models
    from models_new import init_models
    print("✓ Models import successful")
    
    # Test services
    from services.timeline_generator import TimelineGenerator
    print("✓ TimelineGenerator import successful")
    
    from services.migration_advisor import MigrationAdvisor
    print("✓ MigrationAdvisor import successful")
    
    print("All imports successful!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
