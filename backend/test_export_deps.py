#!/usr/bin/env python3
"""Test export service dependencies and functionality"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_export_dependencies():
    """Test if all export dependencies are available"""
    print("🧪 Testing Export Service Dependencies...")
    
    dependencies = [
        ('openpyxl', 'Excel export'),
        ('reportlab', 'PDF export'),
        ('python-docx', 'Word export'),
        ('pandas', 'Data processing')
    ]
    
    missing_deps = []
    
    for dep_name, description in dependencies:
        try:
            __import__(dep_name.replace('-', '_'))
            print(f"✅ {dep_name} - {description}")
        except ImportError:
            print(f"❌ {dep_name} - {description} - MISSING")
            missing_deps.append(dep_name)
    
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        print("   Please install them with: pip install " + " ".join(missing_deps))
        return False
    
    print("\n✅ All export dependencies are available!")
    return True

def test_export_service():
    """Test export service initialization"""
    print("\n🧪 Testing Export Service Initialization...")
    
    try:
        from services.export_service_new import ExportService
        print("✅ Export service imported successfully")
        
        # Test with dummy data
        export_service = ExportService(None, {})
        print("✅ Export service initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Export service failed: {str(e)}")
        return False

if __name__ == "__main__":
    deps_ok = test_export_dependencies()
    service_ok = test_export_service()
    
    if deps_ok and service_ok:
        print("\n🎉 Export service is ready to use!")
    else:
        print("\n❌ Export service has issues that need to be resolved.")
