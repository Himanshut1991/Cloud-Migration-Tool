#!/usr/bin/env python3
"""Populate database with sample inventory data"""

from app import app, db
from models_new import init_models
from datetime import datetime

def populate_sample_data():
    """Add sample inventory data to the database"""
    
    with app.app_context():
        # Initialize models
        models = init_models(db)
        Server = models['Server']
        Database = models['Database']
        FileShare = models['FileShare']
        CloudPreference = models['CloudPreference']
        BusinessConstraint = models['BusinessConstraint']
        ResourceRate = models['ResourceRate']
        
        # Create tables
        db.create_all()
        
        print("=== Adding Sample Servers ===")
        servers_data = [
            {
                'server_id': 'SRV-WEB-001',
                'os_type': 'Windows Server 2019',
                'vcpu': 4,
                'ram': 16,
                'disk_size': 500,
                'disk_type': 'SSD',
                'uptime_pattern': '24/7',
                'current_hosting': 'On-premises',
                'technology': 'IIS, .NET Framework 4.8',
                'technology_version': '4.8'
            },
            {
                'server_id': 'SRV-DB-001',
                'os_type': 'Linux Ubuntu 20.04',
                'vcpu': 8,
                'ram': 32,
                'disk_size': 1000,
                'disk_type': 'SSD',
                'uptime_pattern': '24/7',
                'current_hosting': 'On-premises',
                'technology': 'MySQL, Apache',
                'technology_version': '8.0'
            },
            {
                'server_id': 'SRV-APP-001',
                'os_type': 'Windows Server 2016',
                'vcpu': 2,
                'ram': 8,
                'disk_size': 250,
                'disk_type': 'HDD',
                'uptime_pattern': 'Business hours',
                'current_hosting': 'On-premises',
                'technology': 'Java, Tomcat',
                'technology_version': '9.0'
            },
            {
                'server_id': 'SRV-FILE-001',
                'os_type': 'Windows Server 2019',
                'vcpu': 2,
                'ram': 16,
                'disk_size': 2000,
                'disk_type': 'HDD',
                'uptime_pattern': '24/7',
                'current_hosting': 'On-premises',
                'technology': 'File Server, SMB',
                'technology_version': '3.0'
            }
        ]
        
        for server_data in servers_data:
            existing = Server.query.filter_by(server_id=server_data['server_id']).first()
            if not existing:
                server = Server(**server_data)
                db.session.add(server)
                print(f"Added server: {server_data['server_id']}")
        
        print("\n=== Adding Sample Databases ===")
        databases_data = [
            {
                'db_name': 'ProductionDB',
                'db_type': 'MySQL',
                'size_gb': 500,
                'ha_dr_required': True,
                'backup_frequency': 'Daily',
                'licensing_model': 'Open Source',
                'server_id': 'SRV-DB-001',
                'write_frequency': 'High',
                'downtime_tolerance': 'Low',
                'real_time_sync': True
            },
            {
                'db_name': 'AnalyticsDB',
                'db_type': 'PostgreSQL',
                'size_gb': 200,
                'ha_dr_required': False,
                'backup_frequency': 'Weekly',
                'licensing_model': 'Open Source',
                'server_id': 'SRV-DB-001',
                'write_frequency': 'Medium',
                'downtime_tolerance': 'Medium',
                'real_time_sync': False
            },
            {
                'db_name': 'UserDB',
                'db_type': 'SQL Server',
                'size_gb': 100,
                'ha_dr_required': True,
                'backup_frequency': 'Daily',
                'licensing_model': 'Licensed',
                'server_id': 'SRV-WEB-001',
                'write_frequency': 'High',
                'downtime_tolerance': 'Low',
                'real_time_sync': True
            }
        ]
        
        for db_data in databases_data:
            existing = Database.query.filter_by(db_name=db_data['db_name']).first()
            if not existing:
                database = Database(**db_data)
                db.session.add(database)
                print(f"Added database: {db_data['db_name']}")
        
        print("\n=== Adding Sample File Shares ===")
        file_shares_data = [
            {
                'share_name': 'CompanyFiles',
                'share_type': 'SMB',
                'total_size_gb': 2000,
                'active_users': 150,
                'growth_rate_monthly': 5.0,
                'backup_enabled': True,
                'server_id': 'SRV-FILE-001',
                'access_frequency': 'Regular',
                'access_pattern': 'Hot'
            },
            {
                'share_name': 'ArchiveData',
                'share_type': 'NFS',
                'total_size_gb': 5000,
                'active_users': 20,
                'growth_rate_monthly': 2.0,
                'backup_enabled': True,
                'server_id': 'SRV-FILE-001',
                'access_frequency': 'Rare',
                'access_pattern': 'Cold'
            },
            {
                'share_name': 'ProjectFiles',
                'share_type': 'SMB',
                'total_size_gb': 750,
                'active_users': 75,
                'growth_rate_monthly': 10.0,
                'backup_enabled': True,
                'server_id': 'SRV-APP-001',
                'access_frequency': 'Regular',
                'access_pattern': 'Hot'
            }
        ]
        
        for share_data in file_shares_data:
            existing = FileShare.query.filter_by(share_name=share_data['share_name']).first()
            if not existing:
                file_share = FileShare(**share_data)
                db.session.add(file_share)
                print(f"Added file share: {share_data['share_name']}")
        
        print("\n=== Adding Sample Configuration ===")
        
        # Cloud Preferences
        cloud_pref = CloudPreference.query.first()
        if not cloud_pref:
            cloud_pref = CloudPreference(
                preferred_cloud='AWS',
                preferred_regions='us-east-1,us-west-2',
                compute_preferences='General Purpose',
                storage_preferences='Standard',
                network_requirements='Standard'
            )
            db.session.add(cloud_pref)
            print("Added cloud preferences")
        
        # Business Constraints
        business_constraint = BusinessConstraint.query.first()
        if not business_constraint:
            business_constraint = BusinessConstraint(
                budget_limit=500000.0,
                timeline_months=12,
                compliance_requirements='SOC2, HIPAA',
                downtime_tolerance='Low',
                data_residency_requirements='US Only'
            )
            db.session.add(business_constraint)
            print("Added business constraints")
        
        # Resource Rates
        rates_data = [
            {'resource_type': 'Migration Engineer', 'rate_per_hour': 145.0, 'currency': 'USD'},
            {'resource_type': 'Cloud Architect', 'rate_per_hour': 175.0, 'currency': 'USD'},
            {'resource_type': 'Database Specialist', 'rate_per_hour': 155.0, 'currency': 'USD'},
            {'resource_type': 'Security Consultant', 'rate_per_hour': 165.0, 'currency': 'USD'}
        ]
        
        for rate_data in rates_data:
            existing = ResourceRate.query.filter_by(resource_type=rate_data['resource_type']).first()
            if not existing:
                rate = ResourceRate(**rate_data)
                db.session.add(rate)
                print(f"Added rate: {rate_data['resource_type']}")
        
        # Commit all changes
        db.session.commit()
        
        print("\n=== Final Inventory Count ===")
        print(f"Servers: {Server.query.count()}")
        print(f"Databases: {Database.query.count()}")
        print(f"File Shares: {FileShare.query.count()}")
        print(f"Cloud Preferences: {CloudPreference.query.count()}")
        print(f"Business Constraints: {BusinessConstraint.query.count()}")
        print(f"Resource Rates: {ResourceRate.query.count()}")
        
        print("\n✅ Sample data populated successfully!")

if __name__ == "__main__":
    populate_sample_data()
