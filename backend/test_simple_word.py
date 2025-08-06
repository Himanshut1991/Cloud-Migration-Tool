#!/usr/bin/env python3
"""Test simple Word exporter"""

import os
import sys
sys.path.append('.')

from services.simple_word_exporter import SimpleWordExporter
from models_new import init_models
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "migration_tool.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
    models = init_models(db)
    exporter = SimpleWordExporter(db, models)
    filepath = exporter.export_to_word()
    print(f"✅ Simple Word export completed: {filepath}")
