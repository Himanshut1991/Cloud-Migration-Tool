#!/usr/bin/env python3
"""Direct test of PDF export functionality"""

import os
import sys
import traceback
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

def test_pdf_export():
    """Test PDF export directly"""
    try:
        print("Setting up Flask app...")
        app = Flask(__name__)
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "migration_tool.db")}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy(app)

        with app.app_context():
            print("Initializing models...")
            from models_new import init_models
            models = init_models(db)
            
            print("Available models:", list(models.keys()))
            
            print("Testing database access...")
            Server = models['Server']
            servers = Server.query.all()
            print(f"Found {len(servers)} servers in database")
            
            print("Initializing export service...")
            from services.export_service import ExportService
            export_service = ExportService(db, models)
            
            print("Testing summary data...")
            summary = export_service._get_summary_data()
            print(f"Summary data: {summary}")
            
            print("Generating PDF...")
            filepath = export_service.export_to_pdf()
            print(f"PDF generated at: {filepath}")
            
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                print(f"PDF file size: {size} bytes")
                if size > 0:
                    print("✅ PDF export successful!")
                else:
                    print("❌ PDF file is empty")
            else:
                print("❌ PDF file was not created")
                
    except Exception as e:
        print(f"❌ Error during PDF export: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    test_pdf_export()
