#!/usr/bin/env python3
"""Ensure database is populated with sample data"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db
from models_new import init_models

def populate_inventory_data():
    """Populate inventory with sample data"""
    print("Populating inventory data...")
    
    # Initialize models
    models = init_models(db)
    Server = models['Server']
    Database = models['Database']
    FileShare = models['FileShare']
    
    # Clear existing data
    db.session.query(Server).delete()
    db.session.query(Database).delete()
    db.session.query(FileShare).delete()
    
    # Add sample servers
    servers = [
        {
            'name': 'WEB-SERVER-01',
            'ip_address': '192.168.1.10',
            'operating_system': 'Windows Server 2019',
            'cpu_cores': 4,
            'memory_gb': 16,
            'storage_gb': 500,
            'environment': 'Production',
            'application': 'IIS Web Server',
            'dependencies': 'Database Server',
            'current_utilization': 65,
            'business_criticality': 'High'
        },
        {
            'name': 'DB-SERVER-01',
            'ip_address': '192.168.1.20',
            'operating_system': 'Windows Server 2019',
            'cpu_cores': 8,
            'memory_gb': 32,
            'storage_gb': 1000,
            'environment': 'Production',
            'application': 'SQL Server 2019',
            'dependencies': 'None',
            'current_utilization': 45,
            'business_criticality': 'Critical'
        },
        {
            'name': 'APP-SERVER-01',
            'ip_address': '192.168.1.30',
            'operating_system': 'Linux Ubuntu 20.04',
            'cpu_cores': 6,
            'memory_gb': 24,
            'storage_gb': 750,
            'environment': 'Production',
            'application': 'Node.js Application',
            'dependencies': 'Database Server',
            'current_utilization': 55,
            'business_criticality': 'High'
        }
    ]
    
    for server_data in servers:
        server = Server(**server_data)
        db.session.add(server)
    
    # Add sample databases
    databases = [
        {
            'name': 'CustomerDB',
            'type': 'SQL Server',
            'version': '2019',
            'size_gb': 250,
            'server_name': 'DB-SERVER-01',
            'port': 1433,
            'environment': 'Production',
            'backup_frequency': 'Daily',
            'business_criticality': 'Critical',
            'current_connections': 50,
            'performance_tier': 'High'
        },
        {
            'name': 'InventoryDB',
            'type': 'MySQL',
            'version': '8.0',
            'size_gb': 100,
            'server_name': 'APP-SERVER-01',
            'port': 3306,
            'environment': 'Production',
            'backup_frequency': 'Daily',
            'business_criticality': 'High',
            'current_connections': 25,
            'performance_tier': 'Standard'
        },
        {
            'name': 'LoggingDB',
            'type': 'PostgreSQL',
            'version': '13',
            'size_gb': 50,
            'server_name': 'APP-SERVER-01',
            'port': 5432,
            'environment': 'Production',
            'backup_frequency': 'Weekly',
            'business_criticality': 'Medium',
            'current_connections': 10,
            'performance_tier': 'Basic'
        }
    ]
    
    for db_data in databases:
        database = Database(**db_data)
        db.session.add(database)
    
    # Add sample file shares
    file_shares = [
        {
            'name': 'CompanyDocs',
            'path': '//fileserver/companydocs',
            'size_gb': 500,
            'file_count': 25000,
            'server_name': 'FILE-SERVER-01',
            'share_type': 'SMB',
            'access_frequency': 'High',
            'backup_status': 'Enabled',
            'business_criticality': 'High',
            'user_count': 150
        },
        {
            'name': 'UserProfiles',
            'path': '//fileserver/profiles',
            'size_gb': 200,
            'file_count': 5000,
            'server_name': 'FILE-SERVER-01',
            'share_type': 'SMB',
            'access_frequency': 'Medium',
            'backup_status': 'Enabled',
            'business_criticality': 'Medium',
            'user_count': 100
        },
        {
            'name': 'ProjectArchive',
            'path': '//fileserver/archive',
            'size_gb': 1000,
            'file_count': 50000,
            'server_name': 'FILE-SERVER-02',
            'share_type': 'NFS',
            'access_frequency': 'Low',
            'backup_status': 'Enabled',
            'business_criticality': 'Low',
            'user_count': 20
        }
    ]
    
    for share_data in file_shares:
        file_share = FileShare(**share_data)
        db.session.add(file_share)
    
    # Commit all changes
    db.session.commit()
    print(f"✓ Added {len(servers)} servers, {len(databases)} databases, {len(file_shares)} file shares")

def populate_configuration_data():
    """Populate configuration with sample data"""
    print("Populating configuration data...")
    
    # Initialize models
    models = init_models(db)
    CloudPreference = models['CloudPreference']
    BusinessConstraint = models['BusinessConstraint']
    ResourceRate = models['ResourceRate']
    
    # Clear existing data
    db.session.query(CloudPreference).delete()
    db.session.query(BusinessConstraint).delete()
    db.session.query(ResourceRate).delete()
    
    # Add cloud preferences
    cloud_prefs = [
        {
            'provider': 'AWS',
            'region': 'us-east-1',
            'preferred_services': 'EC2, RDS, S3',
            'deployment_model': 'Public Cloud',
            'compliance_requirements': 'SOC2, PCI DSS',
            'budget_constraints': 'Medium',
            'performance_requirements': 'High',
            'availability_requirements': '99.9%'
        }
    ]
    
    for pref_data in cloud_prefs:
        pref = CloudPreference(**pref_data)
        db.session.add(pref)
    
    # Add business constraints
    constraints = [
        {
            'constraint_type': 'Timeline',
            'description': 'Must complete migration within 6 months',
            'priority': 'High',
            'impact': 'Schedule',
            'mitigation_strategy': 'Parallel migration phases'
        },
        {
            'constraint_type': 'Budget',
            'description': 'Total budget not to exceed $500,000',
            'priority': 'Critical',
            'impact': 'Cost',
            'mitigation_strategy': 'Phased approach with cost monitoring'
        },
        {
            'constraint_type': 'Downtime',
            'description': 'Maximum 4 hours downtime per application',
            'priority': 'High',
            'impact': 'Availability',
            'mitigation_strategy': 'Blue-green deployment strategy'
        }
    ]
    
    for constraint_data in constraints:
        constraint = BusinessConstraint(**constraint_data)
        db.session.add(constraint)
    
    # Add resource rates
    rates = [
        {
            'resource_type': 'Compute',
            'service_name': 'EC2 t3.medium',
            'unit': 'hour',
            'rate': 0.0416,
            'currency': 'USD',
            'region': 'us-east-1'
        },
        {
            'resource_type': 'Storage',
            'service_name': 'EBS gp3',
            'unit': 'GB-month',
            'rate': 0.08,
            'currency': 'USD',
            'region': 'us-east-1'
        },
        {
            'resource_type': 'Database',
            'service_name': 'RDS SQL Server',
            'unit': 'hour',
            'rate': 0.48,
            'currency': 'USD',
            'region': 'us-east-1'
        }
    ]
    
    for rate_data in rates:
        rate = ResourceRate(**rate_data)
        db.session.add(rate)
    
    # Commit all changes
    db.session.commit()
    print(f"✓ Added {len(cloud_prefs)} cloud preferences, {len(constraints)} constraints, {len(rates)} resource rates")

if __name__ == '__main__':
    print("Populating Sample Data")
    print("=" * 30)
    
    with app.app_context():
        try:
            # Ensure tables exist
            db.create_all()
            print("✓ Database tables created/verified")
            
            # Populate data
            populate_inventory_data()
            populate_configuration_data()
            
            # Verify data
            models = init_models(db)
            Server = models['Server']
            Database = models['Database']
            FileShare = models['FileShare']
            CloudPreference = models['CloudPreference']
            BusinessConstraint = models['BusinessConstraint']
            ResourceRate = models['ResourceRate']
            
            print("\n" + "=" * 30)
            print("Database Status:")
            print(f"Servers: {Server.query.count()}")
            print(f"Databases: {Database.query.count()}")
            print(f"File Shares: {FileShare.query.count()}")
            print(f"Cloud Preferences: {CloudPreference.query.count()}")
            print(f"Business Constraints: {BusinessConstraint.query.count()}")
            print(f"Resource Rates: {ResourceRate.query.count()}")
            print("\n✓ Sample data populated successfully!")
            
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()
