import json
from .ai_recommendations import AIRecommendationService

class CostCalculator:
    """Cost calculation service for cloud migration with AI-powered recommendations"""
    
    def __init__(self, db, models, bedrock_client=None):
        self.db = db
        self.bedrock_client = bedrock_client
        
        # Initialize AI recommendation service
        self.ai_service = AIRecommendationService()
        
        # Model classes
        self.Server = models['Server']
        self.Database = models['Database']
        self.FileShare = models['FileShare']
        self.CloudPreference = models['CloudPreference']
        self.ResourceRate = models['ResourceRate']
        
        # AWS Pricing (simplified - would typically use AWS Pricing API)
        self.aws_pricing = {
            'ec2': {
                't3.micro': {'cpu': 2, 'ram': 1, 'cost_per_hour': 0.0104},
                't3.small': {'cpu': 2, 'ram': 2, 'cost_per_hour': 0.0208},
                't3.medium': {'cpu': 2, 'ram': 4, 'cost_per_hour': 0.0416},
                't3.large': {'cpu': 2, 'ram': 8, 'cost_per_hour': 0.0832},
                't3.xlarge': {'cpu': 4, 'ram': 16, 'cost_per_hour': 0.1664},
                't3.2xlarge': {'cpu': 8, 'ram': 32, 'cost_per_hour': 0.3328},
                'm5.large': {'cpu': 2, 'ram': 8, 'cost_per_hour': 0.096},
                'm5.xlarge': {'cpu': 4, 'ram': 16, 'cost_per_hour': 0.192},
                'm5.2xlarge': {'cpu': 8, 'ram': 32, 'cost_per_hour': 0.384},
                'm5.4xlarge': {'cpu': 16, 'ram': 64, 'cost_per_hour': 0.768}
            },
            'rds': {
                'db.t3.micro': 0.017,
                'db.t3.small': 0.034,
                'db.t3.medium': 0.068,
                'db.t3.large': 0.136,
                'db.t3.xlarge': 0.272,
                'db.m5.large': 0.180,
                'db.m5.xlarge': 0.360,
                'db.m5.2xlarge': 0.720
            },
            's3': {
                'standard': 0.023,  # per GB/month
                'ia': 0.0125,       # Infrequent Access
                'glacier': 0.004   # Glacier
            },
            'ebs': {
                'gp3': 0.08,       # per GB/month
                'io2': 0.125       # per GB/month
            }
        }
    
    def calculate_server_costs(self):
        """Calculate costs for server migration with AI-powered recommendations"""
        servers = self.Server.query.all()
        total_monthly_cost = 0
        server_recommendations = []
        
        for server in servers:
            # Prepare server specifications for AI analysis
            server_specs = {
                'server_id': server.server_id,
                'os_type': server.os_type,
                'vcpu': server.vcpu,
                'ram': server.ram,
                'disk_size': server.disk_size,
                'disk_type': server.disk_type,
                'uptime_pattern': server.uptime_pattern,
                'current_hosting': server.current_hosting,
                'technology': server.technology
            }
            
            # Get AI-powered recommendation
            ai_recommendation = self.ai_service.get_server_recommendation(server_specs)
            recommended_instance = ai_recommendation.get('recommended_instance', 't3.medium')
            
            # Calculate costs using the recommended instance
            instance_cost = self.aws_pricing['ec2'].get(recommended_instance, {}).get('cost_per_hour', 0.0416)
            
            # Calculate monthly cost (24/7 * 30 days)
            monthly_cost = instance_cost * 24 * 30
            
            # Add EBS storage cost
            storage_cost = server.disk_size * self.aws_pricing['ebs']['gp3']
            monthly_cost += storage_cost
            
            total_monthly_cost += monthly_cost
            
            server_recommendations.append({
                'server_id': server.server_id,
                'current_specs': f"{server.vcpu} vCPU, {server.ram}GB RAM, {server.disk_size}GB Storage",
                'recommended_instance': recommended_instance,
                'monthly_cost': monthly_cost,
                'annual_cost': monthly_cost * 12,
                'ai_reasoning': ai_recommendation.get('reasoning', 'Standard sizing recommendation'),
                'cost_optimization_tips': ai_recommendation.get('cost_optimization_tips', []),
                'alternative_options': ai_recommendation.get('alternative_options', []),
                'confidence_level': ai_recommendation.get('confidence_level', 'medium')
            })
        
        return {
            'total_monthly_cost': total_monthly_cost,
            'total_annual_cost': total_monthly_cost * 12,
            'server_recommendations': server_recommendations
        }
    
    def calculate_database_costs(self):
        """Calculate costs for database migration with AI-powered recommendations"""
        databases = self.Database.query.all()
        total_monthly_cost = 0
        db_recommendations = []
        
        for database in databases:
            # Prepare database specifications for AI analysis
            db_specs = {
                'db_name': database.db_name,
                'db_type': database.db_type,
                'size_gb': database.size_gb,
                'ha_dr_required': database.ha_dr_required,
                'backup_frequency': database.backup_frequency,
                'performance_tier': getattr(database, 'performance_tier', 'Standard')
            }
            
            # Get AI-powered recommendation
            ai_recommendation = self.ai_service.get_database_recommendation(db_specs)
            recommended_instance = ai_recommendation.get('recommended_instance', 'db.t3.small')
            
            # Calculate costs using the recommended instance
            instance_cost = self.aws_pricing['rds'].get(recommended_instance, 0.034)
            
            # Calculate monthly cost
            monthly_cost = instance_cost * 24 * 30
            
            # Add storage cost
            storage_cost = database.size_gb * 0.115  # RDS storage cost per GB/month
            monthly_cost += storage_cost
            
            # Add backup storage cost
            if database.backup_frequency == 'Daily':
                backup_cost = database.size_gb * 0.095  # Backup storage cost
                monthly_cost += backup_cost
            
            total_monthly_cost += monthly_cost
            
            db_recommendations.append({
                'db_name': database.db_name,
                'db_type': database.db_type,
                'size_gb': database.size_gb,
                'recommended_instance': recommended_instance,
                'monthly_cost': monthly_cost,
                'annual_cost': monthly_cost * 12,
                'ai_reasoning': ai_recommendation.get('reasoning', 'Standard sizing recommendation'),
                'engine_recommendation': ai_recommendation.get('engine_recommendation', database.db_type),
                'performance_insights': ai_recommendation.get('performance_insights', 'Standard performance configuration'),
                'migration_complexity': ai_recommendation.get('migration_complexity', 'medium'),
                'confidence_level': ai_recommendation.get('confidence_level', 'medium')
            })
        
        return {
            'total_monthly_cost': total_monthly_cost,
            'total_annual_cost': total_monthly_cost * 12,
            'database_recommendations': db_recommendations
        }
    
    def calculate_storage_costs(self):
        """Calculate costs for file share migration with AI-powered recommendations"""
        file_shares = self.FileShare.query.all()
        total_monthly_cost = 0
        storage_recommendations = []
        
        for file_share in file_shares:
            # Prepare storage specifications for AI analysis
            storage_specs = {
                'share_name': file_share.share_name,
                'total_size_gb': file_share.total_size_gb,
                'file_count': getattr(file_share, 'file_count', 0),
                'access_pattern': file_share.access_pattern,
                'file_types': getattr(file_share, 'file_types', 'Mixed'),
                'access_frequency': getattr(file_share, 'access_frequency', 'Regular')
            }
            
            # Get AI-powered recommendation
            ai_recommendation = self.ai_service.get_storage_recommendation(storage_specs)
            recommended_storage = ai_recommendation.get('recommended_storage', 'S3 Standard')
            
            # Map AI recommendation to pricing
            if 'S3 Standard' in recommended_storage or file_share.access_pattern == 'Hot':
                storage_class = 'standard'
                cost_per_gb = self.aws_pricing['s3']['standard']
            elif 'S3 IA' in recommended_storage or file_share.access_pattern == 'Warm':
                storage_class = 'ia'
                cost_per_gb = self.aws_pricing['s3']['ia']
            else:  # Glacier or Cold
                storage_class = 'glacier'
                cost_per_gb = self.aws_pricing['s3']['glacier']
            
            monthly_cost = file_share.total_size_gb * cost_per_gb
            total_monthly_cost += monthly_cost
            
            storage_recommendations.append({
                'share_name': file_share.share_name,
                'size_gb': file_share.total_size_gb,
                'access_pattern': file_share.access_pattern,
                'recommended_storage': recommended_storage,
                'monthly_cost': monthly_cost,
                'annual_cost': monthly_cost * 12,
                'ai_reasoning': ai_recommendation.get('reasoning', 'Standard storage recommendation'),
                'lifecycle_policy': ai_recommendation.get('lifecycle_policy', 'Standard lifecycle'),
                'cost_optimization_tips': ai_recommendation.get('cost_optimization_tips', []),
                'performance_considerations': ai_recommendation.get('performance_considerations', 'Standard performance'),
                'confidence_level': ai_recommendation.get('confidence_level', 'medium')
            })
        
        return {
            'total_monthly_cost': total_monthly_cost,
            'total_annual_cost': total_monthly_cost * 12,
            'storage_recommendations': storage_recommendations
        }
    
    def calculate_migration_service_costs(self):
        """Calculate professional services costs"""
        resource_rates = self.ResourceRate.query.all()
        total_cost = 0
        resource_breakdown = []
        
        for rate in resource_rates:
            role_total_cost = rate.duration_weeks * rate.hours_per_week * rate.rate_per_hour
            total_cost += role_total_cost
            
            resource_breakdown.append({
                'role': rate.role,
                'duration_weeks': rate.duration_weeks,
                'hours_per_week': rate.hours_per_week,
                'rate_per_hour': rate.rate_per_hour,
                'total_hours': rate.duration_weeks * rate.hours_per_week,
                'total_cost': role_total_cost
            })
        
        return {
            'total_professional_services_cost': total_cost,
            'resource_breakdown': resource_breakdown
        }
    
    def calculate_total_costs(self):
        """Calculate comprehensive migration costs with AI insights"""
        server_costs = self.calculate_server_costs()
        database_costs = self.calculate_database_costs()
        storage_costs = self.calculate_storage_costs()
        service_costs = self.calculate_migration_service_costs()
        ai_analysis = self.get_ai_comprehensive_analysis()
        
        # Calculate total cloud infrastructure costs
        total_cloud_monthly = (
            server_costs['total_monthly_cost'] +
            database_costs['total_monthly_cost'] +
            storage_costs['total_monthly_cost']
        )
        
        return {
            'cloud_infrastructure': {
                'servers': server_costs,
                'databases': database_costs,
                'storage': storage_costs,
                'total_monthly_cost': total_cloud_monthly,
                'total_annual_cost': total_cloud_monthly * 12
            },
            'migration_services': service_costs,
            'grand_total': {
                'one_time_migration_cost': service_costs['total_professional_services_cost'],
                'annual_cloud_cost': total_cloud_monthly * 12,
                'total_first_year_cost': service_costs['total_professional_services_cost'] + (total_cloud_monthly * 12)
            },
            'ai_insights': ai_analysis
        }
    
    def _recommend_ec2_instance(self, vcpu, ram):
        """Recommend appropriate EC2 instance type"""
        # Simple logic - would be more sophisticated in production
        if vcpu <= 2 and ram <= 2:
            return 't3.small'
        elif vcpu <= 2 and ram <= 4:
            return 't3.medium'
        elif vcpu <= 2 and ram <= 8:
            return 't3.large'
        elif vcpu <= 4 and ram <= 16:
            return 't3.xlarge'
        elif vcpu <= 8 and ram <= 32:
            return 't3.2xlarge'
        elif vcpu <= 4 and ram <= 16:
            return 'm5.xlarge'
        elif vcpu <= 8 and ram <= 32:
            return 'm5.2xlarge'
        else:
            return 'm5.4xlarge'
    
    def _recommend_rds_instance(self, size_gb, ha_required):
        """Recommend appropriate RDS instance type"""
        if size_gb <= 20:
            return 'db.t3.micro'
        elif size_gb <= 100:
            return 'db.t3.small'
        elif size_gb <= 500:
            return 'db.t3.medium'
        elif size_gb <= 1000:
            return 'db.t3.large'
        else:
            return 'db.m5.large' if not ha_required else 'db.m5.xlarge'
    
    def get_ai_comprehensive_analysis(self):
        """Get AI-powered comprehensive migration analysis"""
        try:
            # Gather infrastructure summary
            servers = self.Server.query.all()
            databases = self.Database.query.all()
            file_shares = self.FileShare.query.all()
            
            infrastructure_summary = {
                'servers': [
                    {
                        'server_id': s.server_id,
                        'os_type': s.os_type,
                        'vcpu': s.vcpu,
                        'ram': s.ram,
                        'disk_size': s.disk_size,
                        'technology': s.technology,
                        'uptime_pattern': s.uptime_pattern
                    } for s in servers
                ],
                'databases': [
                    {
                        'db_name': d.db_name,
                        'db_type': d.db_type,
                        'size_gb': d.size_gb,
                        'ha_dr_required': d.ha_dr_required,
                        'backup_frequency': d.backup_frequency
                    } for d in databases
                ],
                'storage': [
                    {
                        'share_name': f.share_name,
                        'total_size_gb': f.total_size_gb,
                        'access_pattern': f.access_pattern
                    } for f in file_shares
                ],
                'totals': {
                    'server_count': len(servers),
                    'database_count': len(databases),
                    'storage_count': len(file_shares),
                    'total_servers_vcpu': sum(s.vcpu for s in servers),
                    'total_servers_ram': sum(s.ram for s in servers),
                    'total_storage_gb': sum(f.total_size_gb for f in file_shares)
                }
            }
            
            # Get AI comprehensive analysis
            analysis = self.ai_service.get_comprehensive_analysis(infrastructure_summary)
            return analysis
            
        except Exception as e:
            return {
                'error': f'AI analysis failed: {str(e)}',
                'analysis': 'Comprehensive AI analysis is currently unavailable'
            }
