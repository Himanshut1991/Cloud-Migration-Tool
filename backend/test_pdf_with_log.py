#!/usr/bin/env python3
"""Test PDF export and write results to a file"""

import os
import sys
import traceback
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

def write_log(message):
    """Write message to log file"""
    with open('pdf_test_log.txt', 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now()}: {message}\n")

def test_pdf_export():
    """Test PDF export and log results"""
    try:
        write_log("Starting PDF export test...")
        
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        
        write_log("Setting up Flask app...")
        app = Flask(__name__)
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "migration_tool.db")}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy(app)

        with app.app_context():
            write_log("Initializing models...")
            from models_new import init_models
            models = init_models(db)
            
            write_log(f"Available models: {list(models.keys())}")
            
            # Test basic model access
            Server = models.get('Server')
            if Server:
                servers = Server.query.all()
                write_log(f"Found {len(servers)} servers in database")
            else:
                write_log("Server model not found!")
            
            write_log("Initializing export service...")
            from services.export_service import ExportService
            export_service = ExportService(db, models)
            
            write_log("Testing summary data...")
            summary = export_service._get_summary_data()
            write_log(f"Summary data: {summary}")
            
            write_log("Testing cost summary...")
            cost_summary = export_service._get_cost_summary()
            write_log(f"Cost summary: {cost_summary}")
            
            write_log("Testing timeline summary...")
            timeline_summary = export_service._get_timeline_summary()
            write_log(f"Timeline summary: {timeline_summary}")
            
            write_log("Generating PDF...")
            filepath = export_service.export_to_pdf()
            write_log(f"PDF generated at: {filepath}")
            
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                write_log(f"PDF file size: {size} bytes")
                if size > 0:
                    write_log("✅ PDF export successful!")
                else:
                    write_log("❌ PDF file is empty")
            else:
                write_log("❌ PDF file was not created")
                
    except Exception as e:
        write_log(f"❌ Error during PDF export: {str(e)}")
        write_log(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    # Clear previous log
    if os.path.exists('pdf_test_log.txt'):
        os.remove('pdf_test_log.txt')
    
    test_pdf_export()
    write_log("Test completed.")
