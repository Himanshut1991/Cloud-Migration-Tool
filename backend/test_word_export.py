#!/usr/bin/env python3
"""Test enhanced Word export functionality"""

import os
import sys
sys.path.append('.')

print('🚀 Starting Word export test...')

try:
    from services.export_service_new import ExportService
    print('✅ Imported ExportService')
    
    from models_new import init_models
    print('✅ Imported init_models')
    
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    print('✅ Imported Flask components')

    app = Flask(__name__)
    basedir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(basedir, "migration_tool.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print(f'✅ Database path: {db_path}')

    db = SQLAlchemy(app)
    print('✅ Database initialized')

    with app.app_context():
        print('🔧 Initializing models...')
        models = init_models(db)
        print('✅ Models initialized')
        
        print('🔧 Creating export service...')
        export_service = ExportService(db, models)
        print('✅ Export service created')
        
        print('🧪 Testing enhanced Word export...')
        word_path = export_service.export_to_word()
        print(f'✅ Word export completed: {word_path}')
        
        # Check file exists and size
        if os.path.exists(word_path):
            size_kb = os.path.getsize(word_path) / 1024
            print(f'📄 File size: {size_kb:.1f} KB')
            print('🎉 Test completed successfully!')
        else:
            print('❌ File not found!')
            
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
