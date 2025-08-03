import json
import boto3
from models import Server, Database, FileShare, CloudPreference

class MigrationAdvisor:
    """AI-powered migration strategy advisor using AWS Bedrock"""
    
    def __init__(self, db, bedrock_client):
        self.db = db
        self.bedrock_client = bedrock_client
        
        # Technology mapping for different cloud providers
        self.technology_mappings = {
            'aws': {
                'mysql': 'Amazon RDS for MySQL',
                'postgresql': 'Amazon RDS for PostgreSQL',
                'sql_server': 'Amazon RDS for SQL Server',
                'oracle': 'Amazon RDS for Oracle',
                'apache': 'Amazon EC2 with Apache',
                'nginx': 'Amazon EC2 with Nginx / Application Load Balancer',
                'tomcat': 'AWS Elastic Beanstalk',
                'jboss': 'Amazon EC2 with JBoss',
                'iis': 'Amazon EC2 with IIS',
                'redis': 'Amazon ElastiCache for Redis',
                'mongodb': 'Amazon DocumentDB',
                'elasticsearch': 'Amazon OpenSearch Service',
                'rabbitmq': 'Amazon MQ for RabbitMQ',
                'activemq': 'Amazon MQ for ActiveMQ'
            }
        }
    
    def generate_data_migration_strategy(self, component_id, component_type):
        """Generate AI-powered data migration strategy"""
        try:
            if component_type == 'database':
                component = Database.query.get(component_id)
                if not component:
                    return {'error': 'Database not found'}
                
                context = self._build_database_context(component)
            elif component_type == 'file_share':
                component = FileShare.query.get(component_id)
                if not component:
                    return {'error': 'File share not found'}
                
                context = self._build_file_share_context(component)
            else:
                return {'error': 'Invalid component type'}
            
            # Get AI recommendation using AWS Bedrock
            ai_recommendation = self._get_ai_recommendation(context, 'data_migration')
            
            # Generate specific migration tools and methods
            migration_tools = self._recommend_migration_tools(component, component_type)
            
            # Calculate estimated costs and timelines
            cost_estimate = self._estimate_migration_cost(component, component_type)
            timeline = self._estimate_migration_timeline(component, component_type)
            
            return {
                'component_id': component_id,
                'component_type': component_type,
                'ai_recommendation': ai_recommendation,
                'migration_tools': migration_tools,
                'cost_estimate': cost_estimate,
                'timeline': timeline,
                'risk_assessment': self._assess_migration_risks(component, component_type)
            }
            
        except Exception as e:
            return {'error': f'Failed to generate migration strategy: {str(e)}'}
    
    def generate_server_migration_strategy(self, server_id):
        """Generate comprehensive server migration strategy"""
        try:
            server = Server.query.filter_by(server_id=server_id).first()
            if not server:
                return {'error': 'Server not found'}
            
            # Build context for AI analysis
            context = self._build_server_context(server)
            
            # Get AI recommendation
            ai_recommendation = self._get_ai_recommendation(context, 'server_migration')
            
            # Technology mapping recommendations
            tech_mappings = self._map_technologies_to_cloud(server.technology)
            
            # Migration strategy (Rehost vs Replatform)
            migration_strategy = self._determine_migration_strategy(server)
            
            # Recommended tools
            migration_tools = self._recommend_server_migration_tools(server, migration_strategy)
            
            return {
                'server_id': server_id,
                'current_technologies': server.technology.split(',') if server.technology else [],
                'ai_recommendation': ai_recommendation,
                'technology_mappings': tech_mappings,
                'migration_strategy': migration_strategy,
                'migration_tools': migration_tools,
                'estimated_downtime': self._estimate_server_downtime(server, migration_strategy),
                'cost_benefit_analysis': self._analyze_cost_benefits(server, migration_strategy)
            }
            
        except Exception as e:
            return {'error': f'Failed to generate server migration strategy: {str(e)}'}
    
    def _build_database_context(self, database):
        """Build context for database migration analysis"""
        cloud_pref = CloudPreference.query.first()
        
        return {
            'database_type': database.db_type,
            'size_gb': database.size_gb,
            'write_frequency': database.write_frequency,
            'downtime_tolerance': database.downtime_tolerance,
            'real_time_sync_required': database.real_time_sync,
            'ha_dr_required': database.ha_dr_required,
            'backup_frequency': database.backup_frequency,
            'licensing_model': database.licensing_model,
            'target_cloud': cloud_pref.cloud_provider if cloud_pref else 'aws'
        }
    
    def _build_file_share_context(self, file_share):
        """Build context for file share migration analysis"""
        cloud_pref = CloudPreference.query.first()
        
        return {
            'size_gb': file_share.total_size_gb,
            'access_pattern': file_share.access_pattern,
            'write_frequency': file_share.write_frequency,
            'downtime_tolerance': file_share.downtime_tolerance,
            'real_time_sync_required': file_share.real_time_sync,
            'snapshot_required': file_share.snapshot_required,
            'retention_days': file_share.retention_days,
            'target_cloud': cloud_pref.cloud_provider if cloud_pref else 'aws'
        }
    
    def _build_server_context(self, server):
        """Build context for server migration analysis"""
        cloud_pref = CloudPreference.query.first()
        
        return {
            'os_type': server.os_type,
            'vcpu': server.vcpu,
            'ram': server.ram,
            'disk_size': server.disk_size,
            'technologies': server.technology.split(',') if server.technology else [],
            'current_hosting': server.current_hosting,
            'uptime_pattern': server.uptime_pattern,
            'target_cloud': cloud_pref.cloud_provider if cloud_pref else 'aws'
        }
    
    def _get_ai_recommendation(self, context, migration_type):
        """Get AI-powered recommendation using AWS Bedrock"""
        if not self.bedrock_client:
            return self._get_fallback_recommendation(context, migration_type)
        
        try:
            if migration_type == 'data_migration':
                prompt = self._build_data_migration_prompt(context)
            elif migration_type == 'server_migration':
                prompt = self._build_server_migration_prompt(context)
            else:
                return "Invalid migration type"
            
            # Call AWS Bedrock (using Claude or another model)
            response = self.bedrock_client.invoke_model(
                modelId='anthropic.claude-3-sonnet-20240229-v1:0',
                body=json.dumps({
                    'anthropic_version': 'bedrock-2023-05-31',
                    'max_tokens': 1000,
                    'messages': [
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ]
                })
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except Exception as e:
            return self._get_fallback_recommendation(context, migration_type)
    
    def _build_data_migration_prompt(self, context):
        """Build AI prompt for data migration strategy"""
        return f"""
        As a cloud migration expert, analyze the following data migration scenario and provide a comprehensive strategy:

        Component Details:
        - Type: {context.get('database_type', 'File Share')}
        - Size: {context.get('size_gb')} GB
        - Write Frequency: {context.get('write_frequency')}
        - Downtime Tolerance: {context.get('downtime_tolerance')}
        - Real-time Sync Required: {context.get('real_time_sync_required')}
        - Target Cloud: {context.get('target_cloud')}

        Please provide:
        1. Recommended migration approach (online vs offline)
        2. Optimal migration tools and services
        3. Step-by-step migration process
        4. Risk mitigation strategies
        5. Expected timeline and effort
        6. Rollback plan

        Focus on minimizing downtime and ensuring data integrity.
        """
    
    def _build_server_migration_prompt(self, context):
        """Build AI prompt for server migration strategy"""
        return f"""
        As a cloud migration expert, analyze the following server migration scenario:

        Server Details:
        - OS: {context.get('os_type')}
        - Resources: {context.get('vcpu')} vCPU, {context.get('ram')} GB RAM
        - Technologies: {', '.join(context.get('technologies', []))}
        - Current Hosting: {context.get('current_hosting')}
        - Target Cloud: {context.get('target_cloud')}

        Please provide:
        1. Migration strategy recommendation (Rehost vs Replatform vs Refactor)
        2. Cloud service mappings for each technology component
        3. Recommended migration tools (e.g., AWS MGN, Azure Migrate)
        4. Architecture optimization opportunities
        5. Security and compliance considerations
        6. Performance optimization recommendations
        7. Cost optimization strategies

        Prioritize minimal disruption and maximum cloud-native benefits.
        """
    
    def _get_fallback_recommendation(self, context, migration_type):
        """Provide fallback recommendation when AI service is unavailable"""
        if migration_type == 'data_migration':
            if context.get('size_gb', 0) > 1000:
                return "Large dataset migration - Consider AWS DataSync or Snowball family for initial data transfer, followed by AWS DMS for ongoing synchronization."
            else:
                return "Medium dataset migration - AWS DMS with CDC (Change Data Capture) for minimal downtime migration."
        else:  # server_migration
            technologies = context.get('technologies', [])
            if any('database' in tech.lower() for tech in technologies):
                return "Server with database components - Recommend Replatform approach with managed database services for better scalability and reduced operational overhead."
            else:
                return "Application server - Rehost approach using AWS MGN for quick migration, then evaluate Replatform opportunities."
    
    def _recommend_migration_tools(self, component, component_type):
        """Recommend specific migration tools"""
        tools = []
        
        if component_type == 'database':
            if component.size_gb > 1000:
                tools.extend(['AWS Snowball Edge', 'AWS DMS'])
            else:
                tools.append('AWS DMS')
            
            if component.real_time_sync:
                tools.append('AWS DMS with CDC')
            
            if component.db_type.lower() in ['mysql', 'postgresql']:
                tools.append('AWS Schema Conversion Tool')
        
        elif component_type == 'file_share':
            if component.total_size_gb > 10000:  # > 10 TB
                tools.extend(['AWS Snowball Edge', 'AWS DataSync'])
            elif component.total_size_gb > 1000:  # > 1 TB
                tools.append('AWS DataSync')
            else:
                tools.extend(['AWS CLI', 'AWS DataSync'])
            
            if component.real_time_sync:
                tools.append('AWS File Gateway')
        
        return tools
    
    def _map_technologies_to_cloud(self, technologies_str):
        """Map on-premise technologies to cloud services"""
        if not technologies_str:
            return {}
        
        cloud_pref = CloudPreference.query.first()
        provider = cloud_pref.cloud_provider.lower() if cloud_pref else 'aws'
        
        mappings = {}
        technologies = [tech.strip().lower() for tech in technologies_str.split(',')]
        
        for tech in technologies:
            if tech in self.technology_mappings.get(provider, {}):
                mappings[tech] = self.technology_mappings[provider][tech]
            else:
                # Generic mapping
                mappings[tech] = f"Amazon EC2 with {tech.title()}"
        
        return mappings
    
    def _determine_migration_strategy(self, server):
        """Determine optimal migration strategy"""
        technologies = server.technology.split(',') if server.technology else []
        
        # Simple logic - would be more sophisticated in production
        if any('database' in tech.lower() for tech in technologies):
            return {
                'strategy': 'Replatform',
                'rationale': 'Server contains database components that would benefit from managed cloud services'
            }
        elif len(technologies) > 3:
            return {
                'strategy': 'Replatform',
                'rationale': 'Complex technology stack would benefit from cloud-native services'
            }
        else:
            return {
                'strategy': 'Rehost',
                'rationale': 'Simple application server suitable for lift-and-shift migration'
            }
    
    def _recommend_server_migration_tools(self, server, strategy):
        """Recommend tools for server migration"""
        tools = []
        
        if strategy['strategy'] == 'Rehost':
            tools.extend(['AWS Application Migration Service (MGN)', 'AWS EC2'])
        else:  # Replatform
            tools.extend(['AWS Elastic Beanstalk', 'Amazon ECS', 'AWS Lambda'])
            
            if 'database' in server.technology.lower():
                tools.extend(['AWS DMS', 'Amazon RDS'])
        
        return tools
    
    def _estimate_migration_cost(self, component, component_type):
        """Estimate migration costs"""
        # Simplified cost estimation
        if component_type == 'database':
            base_cost = component.size_gb * 0.1  # $0.10 per GB
            if component.real_time_sync:
                base_cost *= 1.5
        else:  # file_share
            base_cost = component.total_size_gb * 0.05  # $0.05 per GB
            if component.real_time_sync:
                base_cost *= 1.3
        
        return {
            'estimated_cost_usd': round(base_cost, 2),
            'cost_breakdown': {
                'data_transfer': round(base_cost * 0.6, 2),
                'tools_and_services': round(base_cost * 0.3, 2),
                'professional_services': round(base_cost * 0.1, 2)
            }
        }
    
    def _estimate_migration_timeline(self, component, component_type):
        """Estimate migration timeline"""
        if component_type == 'database':
            base_days = max(1, component.size_gb / 100)  # 100 GB per day baseline
            if component.real_time_sync:
                base_days += 2  # Additional setup time
        else:  # file_share
            base_days = max(1, component.total_size_gb / 500)  # 500 GB per day baseline
        
        return {
            'estimated_days': round(base_days, 1),
            'phases': {
                'planning_and_setup': round(base_days * 0.2, 1),
                'initial_data_transfer': round(base_days * 0.6, 1),
                'synchronization_and_cutover': round(base_days * 0.2, 1)
            }
        }
    
    def _assess_migration_risks(self, component, component_type):
        """Assess migration risks"""
        risks = []
        
        if component_type == 'database':
            if component.size_gb > 1000:
                risks.append('Large dataset may require extended transfer time')
            if component.downtime_tolerance == 'Zero':
                risks.append('Zero downtime requirement increases complexity')
            if component.real_time_sync:
                risks.append('Real-time sync adds technical complexity')
        else:  # file_share
            if component.total_size_gb > 5000:
                risks.append('Large file share may impact network bandwidth')
            if component.write_frequency == 'High':
                risks.append('High write frequency may cause sync delays')
        
        return {
            'risk_level': 'High' if len(risks) > 2 else 'Medium' if len(risks) > 0 else 'Low',
            'identified_risks': risks,
            'mitigation_strategies': [
                'Comprehensive testing in non-production environment',
                'Phased migration approach',
                'Rollback plan preparation',
                'Performance monitoring during migration'
            ]
        }
    
    def _estimate_server_downtime(self, server, strategy):
        """Estimate server migration downtime"""
        if strategy['strategy'] == 'Rehost':
            # Lift and shift typically requires less downtime
            base_hours = 2 + (server.disk_size / 100)  # 2 hours + 1 hour per 100GB
        else:  # Replatform
            # Replatform requires more downtime for reconfiguration
            base_hours = 4 + (server.disk_size / 50)   # 4 hours + 1 hour per 50GB
        
        return {
            'estimated_downtime_hours': round(base_hours, 1),
            'downtime_breakdown': {
                'preparation': round(base_hours * 0.2, 1),
                'data_migration': round(base_hours * 0.6, 1),
                'testing_and_validation': round(base_hours * 0.2, 1)
            }
        }
    
    def _analyze_cost_benefits(self, server, strategy):
        """Analyze cost benefits of migration strategy"""
        return {
            'strategy': strategy['strategy'],
            'benefits': {
                'operational_cost_reduction': '20-30%' if strategy['strategy'] == 'Replatform' else '10-15%',
                'scalability_improvement': 'High' if strategy['strategy'] == 'Replatform' else 'Medium',
                'maintenance_reduction': 'Significant' if strategy['strategy'] == 'Replatform' else 'Moderate',
                'security_enhancement': 'High',
                'disaster_recovery': 'Improved'
            },
            'investment_required': {
                'migration_effort': 'High' if strategy['strategy'] == 'Replatform' else 'Medium',
                'training_required': 'Medium' if strategy['strategy'] == 'Replatform' else 'Low',
                'code_changes': 'Some' if strategy['strategy'] == 'Replatform' else 'Minimal'
            }
        }
