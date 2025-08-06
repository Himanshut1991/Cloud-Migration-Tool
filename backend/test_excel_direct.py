#!/usr/bin/env python3
"""Test Excel export directly"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.export_service_new import ExportService
from models_new import init_models
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def test_excel_export():
    """Test Excel export functionality directly"""
    print("🧪 Testing Excel Export...")
    
    try:
        # Set up Flask app and database (minimal setup)
        app = Flask(__name__)
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "migration_tool.db")}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db = SQLAlchemy(app)
        
        with app.app_context():
            # Initialize models
            models = init_models(db)
            
            # Create export service
            export_service = ExportService(db, models)
            
            print("📊 Creating Excel export...")
            
            # Test Excel export
            filepath = export_service.export_to_excel()
            
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                print(f"✅ Excel export successful!")
                print(f"📄 File: {os.path.basename(filepath)}")
                print(f"📊 Size: {file_size:,} bytes")
            else:
                print("❌ Excel file was not created")
                
    except Exception as e:
        print(f"❌ Excel export failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_excel_export()
