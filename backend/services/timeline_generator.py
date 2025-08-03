from datetime import datetime, timedelta
from models import Server, Database, FileShare, BusinessConstraint, ResourceRate

class TimelineGenerator:
    """Generate comprehensive migration timeline"""
    
    def __init__(self, db):
        self.db = db
    
    def generate_migration_timeline(self):
        """Generate complete migration timeline with milestones"""
        try:
            # Get business constraints
            constraints = BusinessConstraint.query.first()
            cutover_date = constraints.cutover_date if constraints else None
            
            # Calculate phases
            phases = self._calculate_migration_phases()
            
            # Generate timeline
            timeline = self._build_timeline(phases, cutover_date)
            
            # Add resource allocation
            resource_timeline = self._generate_resource_timeline(phases)
            
            # Add milestones and dependencies
            milestones = self._define_milestones(timeline)
            dependencies = self._define_dependencies()
            
            return {
                'total_duration_weeks': sum(phase['duration_weeks'] for phase in phases),
                'phases': phases,
                'timeline': timeline,
                'resource_timeline': resource_timeline,
                'milestones': milestones,
                'dependencies': dependencies,
                'critical_path': self._identify_critical_path(phases),
                'risk_buffer': self._calculate_risk_buffer(),
                'cutover_schedule': self._generate_cutover_schedule()
            }
            
        except Exception as e:
            return {'error': f'Failed to generate timeline: {str(e)}'}
    
    def _calculate_migration_phases(self):
        """Calculate duration for each migration phase"""
        servers = Server.query.all()
        databases = Database.query.all()
        file_shares = FileShare.query.all()
        
        phases = [
            {
                'phase': 'Assessment and Planning',
                'duration_weeks': 2,
                'tasks': [
                    'Infrastructure assessment',
                    'Dependency mapping',
                    'Risk assessment',
                    'Migration plan finalization',
                    'Team training'
                ],
                'deliverables': [
                    'Migration plan document',
                    'Risk mitigation plan',
                    'Resource allocation plan'
                ]
            },
            {
                'phase': 'Environment Setup',
                'duration_weeks': 2,
                'tasks': [
                    'Cloud account setup',
                    'Network configuration',
                    'Security setup',
                    'Monitoring setup',
                    'Tool configuration'
                ],
                'deliverables': [
                    'Cloud environment ready',
                    'Security policies implemented',
                    'Monitoring dashboards'
                ]
            },
            {
                'phase': 'Pilot Migration',
                'duration_weeks': 3,
                'tasks': [
                    'Select pilot workloads',
                    'Execute pilot migration',
                    'Performance testing',
                    'Process refinement',
                    'Stakeholder approval'
                ],
                'deliverables': [
                    'Pilot migration report',
                    'Refined migration process',
                    'Performance benchmarks'
                ]
            }
        ]
        
        # Calculate data migration duration
        total_data_size = sum(db.size_gb for db in databases) + sum(fs.total_size_gb for fs in file_shares)
        data_migration_weeks = max(2, total_data_size / 2000)  # 2TB per week baseline
        
        phases.append({
            'phase': 'Data Migration',
            'duration_weeks': round(data_migration_weeks, 1),
            'tasks': [
                'Database migration setup',
                'Initial data sync',
                'File share migration',
                'Data validation',
                'Incremental sync'
            ],
            'deliverables': [
                'Data successfully migrated',
                'Data integrity verified',
                'Sync processes established'
            ]
        })
        
        # Calculate server migration duration
        server_migration_weeks = max(2, len(servers) / 5)  # 5 servers per week baseline
        
        phases.append({
            'phase': 'Server Migration',
            'duration_weeks': round(server_migration_weeks, 1),
            'tasks': [
                'Server assessment',
                'Migration tool setup',
                'Replication setup',
                'Application migration',
                'Testing and validation'
            ],
            'deliverables': [
                'Servers migrated',
                'Applications functional',
                'Performance validated'
            ]
        })
        
        phases.extend([
            {
                'phase': 'Testing and Validation',
                'duration_weeks': 3,
                'tasks': [
                    'End-to-end testing',
                    'Performance testing',
                    'Security testing',
                    'User acceptance testing',
                    'Documentation update'
                ],
                'deliverables': [
                    'Test results report',
                    'Performance benchmarks',
                    'Updated documentation'
                ]
            },
            {
                'phase': 'Cutover and Go-Live',
                'duration_weeks': 2,
                'tasks': [
                    'Final data sync',
                    'DNS cutover',
                    'Traffic routing',
                    'Monitoring activation',
                    'Go-live verification'
                ],
                'deliverables': [
                    'Production cutover complete',
                    'All systems operational',
                    'Monitoring active'
                ]
            },
            {
                'phase': 'Post-Migration Support',
                'duration_weeks': 4,
                'tasks': [
                    'Hypercare support',
                    'Performance monitoring',
                    'Issue resolution',
                    'Optimization',
                    'Knowledge transfer'
                ],
                'deliverables': [
                    'Stable operations',
                    'Optimized performance',
                    'Team trained'
                ]
            }
        ])
        
        return phases
    
    def _build_timeline(self, phases, cutover_date):
        """Build detailed timeline with dates"""
        timeline = []
        current_date = datetime.now()
        
        # If cutover date is specified, work backwards
        if cutover_date:
            cutover_phase_index = next(i for i, phase in enumerate(phases) if phase['phase'] == 'Cutover and Go-Live')
            total_weeks_before_cutover = sum(phase['duration_weeks'] for phase in phases[:cutover_phase_index])
            current_date = cutover_date - timedelta(weeks=total_weeks_before_cutover)
        
        for phase in phases:
            start_date = current_date
            end_date = current_date + timedelta(weeks=phase['duration_weeks'])
            
            timeline.append({
                'phase': phase['phase'],
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'duration_weeks': phase['duration_weeks'],
                'tasks': phase['tasks'],
                'deliverables': phase['deliverables'],
                'status': 'Not Started'
            })
            
            current_date = end_date
        
        return timeline
    
    def _generate_resource_timeline(self, phases):
        """Generate resource allocation timeline"""
        resource_rates = ResourceRate.query.all()
        resource_timeline = []
        
        # Map roles to phases
        role_phase_mapping = {
            'Cloud Architect': ['Assessment and Planning', 'Environment Setup', 'Testing and Validation'],
            'Migration Engineer': ['Data Migration', 'Server Migration', 'Cutover and Go-Live'],
            'DBA': ['Data Migration', 'Testing and Validation'],
            'Project Manager': ['Assessment and Planning', 'Pilot Migration', 'Testing and Validation', 'Cutover and Go-Live', 'Post-Migration Support'],
            'DevOps Engineer': ['Environment Setup', 'Server Migration', 'Post-Migration Support']
        }
        
        for rate in resource_rates:
            role_phases = role_phase_mapping.get(rate.role, [])
            
            for phase in phases:
                if phase['phase'] in role_phases:
                    resource_timeline.append({
                        'role': rate.role,
                        'phase': phase['phase'],
                        'hours_per_week': rate.hours_per_week,
                        'duration_weeks': phase['duration_weeks'],
                        'total_hours': rate.hours_per_week * phase['duration_weeks'],
                        'total_cost': rate.hours_per_week * phase['duration_weeks'] * rate.rate_per_hour
                    })
        
        return resource_timeline
    
    def _define_milestones(self, timeline):
        """Define key project milestones"""
        milestones = []
        
        for entry in timeline:
            if entry['phase'] in ['Assessment and Planning', 'Pilot Migration', 'Data Migration', 'Testing and Validation', 'Cutover and Go-Live']:
                milestones.append({
                    'milestone': f"{entry['phase']} Complete",
                    'date': entry['end_date'],
                    'description': f"Completion of {entry['phase']} phase with all deliverables",
                    'critical': entry['phase'] in ['Data Migration', 'Cutover and Go-Live']
                })
        
        return milestones
    
    def _define_dependencies(self):
        """Define phase dependencies"""
        return [
            {
                'predecessor': 'Assessment and Planning',
                'successor': 'Environment Setup',
                'type': 'Finish-to-Start',
                'lag_days': 0
            },
            {
                'predecessor': 'Environment Setup',
                'successor': 'Pilot Migration',
                'type': 'Finish-to-Start',
                'lag_days': 0
            },
            {
                'predecessor': 'Pilot Migration',
                'successor': 'Data Migration',
                'type': 'Finish-to-Start',
                'lag_days': 0
            },
            {
                'predecessor': 'Data Migration',
                'successor': 'Server Migration',
                'type': 'Start-to-Start',
                'lag_days': 7  # Can start server migration 1 week after data migration starts
            },
            {
                'predecessor': 'Server Migration',
                'successor': 'Testing and Validation',
                'type': 'Finish-to-Start',
                'lag_days': 0
            },
            {
                'predecessor': 'Testing and Validation',
                'successor': 'Cutover and Go-Live',
                'type': 'Finish-to-Start',
                'lag_days': 0
            },
            {
                'predecessor': 'Cutover and Go-Live',
                'successor': 'Post-Migration Support',
                'type': 'Finish-to-Start',
                'lag_days': 0
            }
        ]
    
    def _identify_critical_path(self, phases):
        """Identify critical path through the project"""
        critical_phases = [
            'Assessment and Planning',
            'Environment Setup',
            'Data Migration',
            'Testing and Validation',
            'Cutover and Go-Live'
        ]
        
        total_critical_weeks = sum(
            phase['duration_weeks'] for phase in phases 
            if phase['phase'] in critical_phases
        )
        
        return {
            'critical_phases': critical_phases,
            'total_duration_weeks': total_critical_weeks,
            'buffer_weeks': sum(phase['duration_weeks'] for phase in phases) - total_critical_weeks
        }
    
    def _calculate_risk_buffer(self):
        """Calculate recommended risk buffer"""
        servers = Server.query.count()
        databases = Database.query.count()
        file_shares = FileShare.query.count()
        
        # Calculate complexity score
        complexity_score = (servers * 0.5) + (databases * 1.0) + (file_shares * 0.3)
        
        # Risk buffer percentage based on complexity
        if complexity_score > 50:
            buffer_percentage = 0.25  # 25% buffer for high complexity
        elif complexity_score > 20:
            buffer_percentage = 0.20  # 20% buffer for medium complexity
        else:
            buffer_percentage = 0.15  # 15% buffer for low complexity
        
        return {
            'complexity_score': complexity_score,
            'recommended_buffer_percentage': buffer_percentage * 100,
            'risk_factors': self._identify_risk_factors()
        }
    
    def _identify_risk_factors(self):
        """Identify project risk factors"""
        risk_factors = []
        
        # Check for high-risk scenarios
        large_databases = Database.query.filter(Database.size_gb > 1000).count()
        if large_databases > 0:
            risk_factors.append(f"{large_databases} large databases (>1TB) may require extended migration time")
        
        zero_downtime_dbs = Database.query.filter(Database.downtime_tolerance == 'Zero').count()
        if zero_downtime_dbs > 0:
            risk_factors.append(f"{zero_downtime_dbs} databases require zero downtime migration")
        
        realtime_sync = Database.query.filter(Database.real_time_sync == True).count()
        if realtime_sync > 0:
            risk_factors.append(f"{realtime_sync} components require real-time synchronization")
        
        total_servers = Server.query.count()
        if total_servers > 20:
            risk_factors.append(f"Large number of servers ({total_servers}) increases coordination complexity")
        
        return risk_factors
    
    def _generate_cutover_schedule(self):
        """Generate detailed cutover schedule"""
        constraints = BusinessConstraint.query.first()
        migration_window = constraints.migration_window if constraints else 'Weekends'
        
        cutover_tasks = [
            {
                'task': 'Pre-cutover verification',
                'duration_hours': 2,
                'responsible': 'Migration Engineer',
                'description': 'Verify all systems ready for cutover'
            },
            {
                'task': 'Stop source applications',
                'duration_hours': 0.5,
                'responsible': 'Application Team',
                'description': 'Gracefully stop source applications'
            },
            {
                'task': 'Final data synchronization',
                'duration_hours': 1,
                'responsible': 'DBA',
                'description': 'Complete final data sync to target'
            },
            {
                'task': 'DNS cutover',
                'duration_hours': 0.5,
                'responsible': 'Network Team',
                'description': 'Update DNS to point to new environment'
            },
            {
                'task': 'Start target applications',
                'duration_hours': 1,
                'responsible': 'Application Team',
                'description': 'Start applications in target environment'
            },
            {
                'task': 'Smoke testing',
                'duration_hours': 2,
                'responsible': 'Testing Team',
                'description': 'Verify critical functionality'
            },
            {
                'task': 'Go/No-go decision',
                'duration_hours': 0.5,
                'responsible': 'Project Manager',
                'description': 'Final go-live decision'
            }
        ]
        
        total_cutover_hours = sum(task['duration_hours'] for task in cutover_tasks)
        
        return {
            'migration_window': migration_window,
            'total_cutover_duration_hours': total_cutover_hours,
            'cutover_tasks': cutover_tasks,
            'rollback_time_limit': 4,  # hours
            'communication_plan': {
                'stakeholder_notification': '24 hours before cutover',
                'progress_updates': 'Every 30 minutes during cutover',
                'completion_notification': 'Within 1 hour of go-live'
            }
        }
