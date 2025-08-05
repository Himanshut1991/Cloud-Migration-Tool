#!/usr/bin/env python3
"""Test script to check timeline generation functionality"""

import os
import sys
import json
from datetime import datetime

# Add the backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from models_new import init_models
    from services.timeline_generator import TimelineGenerator
    
    print("Setting up test environment...")
    
    # Create Flask app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///migration_tool.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db = SQLAlchemy(app)
    
    # Initialize models
    models = init_models(db)
    
    print("✓ Flask app & models initialized")
    
    with app.app_context():
        # Test TimelineGenerator
        print("Testing TimelineGenerator...")
        generator = TimelineGenerator(db, models)
        timeline_data = generator.generate_migration_timeline()
        
        print("✓ Timeline generated successfully!")
        print(f"✓ Timeline has {len(timeline_data.get('phases', []))} phases")
        print(f"✓ Project duration: {timeline_data.get('project_overview', {}).get('total_duration_weeks', 'N/A')} weeks")
        
        # Pretty print first phase as sample
        if timeline_data.get('phases'):
            print("\n📋 Sample Phase:")
            print(json.dumps(timeline_data['phases'][0], indent=2))
        
        print("\n🎯 Timeline generation test PASSED!")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
