#!/usr/bin/env python3
"""Test the timeline API endpoint"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models_new import init_models
from services.timeline_generator import TimelineGenerator

# Create Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///migration_tool.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize models
models = init_models(db)

with app.app_context():
    try:
        print("Testing Timeline Generation...")
        
        # Count inventory
        servers = models['Server'].query.all()
        databases = models['Database'].query.all()
        file_shares = models['FileShare'].query.all()
        
        print(f"Found: {len(servers)} servers, {len(databases)} databases, {len(file_shares)} file shares")
        
        # Generate timeline
        generator = TimelineGenerator(db, models)
        timeline = generator.generate_migration_timeline()
        
        print(f"✓ Timeline generated successfully!")
        print(f"✓ {len(timeline.get('phases', []))} phases created")
        print(f"✓ Total duration: {timeline.get('project_overview', {}).get('total_duration_weeks', 'N/A')} weeks")
        
        # Show phase titles
        for phase in timeline.get('phases', []):
            print(f"  - Phase {phase.get('phase')}: {phase.get('title')} ({phase.get('duration_weeks')} weeks)")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
