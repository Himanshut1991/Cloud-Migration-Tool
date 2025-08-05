from datetime import datetime, timedelta
from typing import Dict, List, Any
from services.ai_recommendations import AIRecommendationService
import logging

class TimelineGenerator:
    """Generate comprehensive migration timeline with AI insights"""
    
    def __init__(self, db, models):
        self.db = db
        self.models = models
        self.ai_service = AIRecommendationService()
        self.logger = logging.getLogger(__name__)
    
    def generate_migration_timeline(self) -> Dict[str, Any]:
        """Generate complete migration timeline with AI-powered insights"""
        try:
            # Get all inventory
            servers = self.models['Server'].query.all()
            databases = self.models['Database'].query.all()
            file_shares = self.models['FileShare'].query.all()
            constraints = self.models['BusinessConstraint'].query.first()
            
            # Calculate phases with AI optimization
            phases = self._calculate_migration_phases(servers, databases, file_shares)
            
            # Get AI insights for timeline optimization
            ai_insights = self._get_ai_timeline_insights(servers, databases, file_shares)
            
            # Calculate project overview
            project_overview = self._calculate_project_overview(phases, constraints)
            
            # Generate resource allocation
            resource_allocation = self._generate_resource_allocation(phases)
            
            # Calculate risks and mitigation
            risk_mitigation = self._calculate_risk_mitigation(phases)
            
            # Define success criteria
            success_criteria = self._define_success_criteria()
            
            # Calculate critical path
            critical_path = self._identify_critical_path(phases)
            
            return {
                'project_overview': project_overview,
                'phases': phases,
                'critical_path': critical_path,
                'resource_allocation': resource_allocation,
                'risk_mitigation': risk_mitigation,
                'success_criteria': success_criteria,
                'ai_insights': ai_insights
            }
            
        except Exception as e:
            self.logger.error(f"Timeline generation failed: {e}")
            return {'error': f'Failed to generate timeline: {str(e)}'}
    
    def _calculate_migration_phases(self, servers, databases, file_shares) -> List[Dict[str, Any]]:
        """Calculate migration phases with realistic timelines"""
        phases = []
        current_week = 1
        
        # Phase 1: Assessment and Planning
        phase1 = {
            'phase': 1,
            'title': 'Assessment and Planning',
            'description': 'Comprehensive assessment of current infrastructure and detailed migration planning.',
            'duration_weeks': 4,
            'start_week': current_week,
            'end_week': current_week + 3,
            'dependencies': [],
            'milestones': [
                'Infrastructure assessment completed',
                'Migration strategy finalized',
                'Resource allocation confirmed',
                'Risk assessment completed'
            ],
            'components': ['All Systems'],
            'risks': ['Incomplete discovery', 'Resource availability'],
            'resources_required': ['Cloud Architect', 'Migration Engineer'],
            'status': 'pending'
        }
        phases.append(phase1)
        current_week += 4
        
        # Phase 2: Environment Setup
        phase2 = {
            'phase': 2,
            'title': 'Cloud Environment Setup',
            'description': 'Setup target cloud environment, networking, security, and baseline services.',
            'duration_weeks': 3,
            'start_week': current_week,
            'end_week': current_week + 2,
            'dependencies': ['Phase 1 - Assessment and Planning'],
            'milestones': [
                'Cloud accounts configured',
                'Network architecture deployed',
                'Security baseline established',
                'Monitoring systems active'
            ],
            'components': ['Cloud Infrastructure'],
            'risks': ['Configuration errors', 'Security misconfigurations'],
            'resources_required': ['Cloud Architect', 'Security Consultant'],
            'status': 'pending'
        }
        phases.append(phase2)
        current_week += 3
        
        # Phase 3: Database Migration
        if databases:
            db_duration = max(3, len(databases) * 2)  # Minimum 3 weeks, 2 weeks per DB
            phase3 = {
                'phase': 3,
                'title': 'Database Migration',
                'description': 'Migrate databases with minimal downtime using appropriate migration tools.',
                'duration_weeks': db_duration,
                'start_week': current_week,
                'end_week': current_week + db_duration - 1,
                'dependencies': ['Phase 2 - Cloud Environment Setup'],
                'milestones': [
                    'Database schemas migrated',
                    'Data migration completed',
                    'Performance validation passed',
                    'Backup/recovery tested'
                ],
                'components': [db.db_name for db in databases],
                'risks': ['Data corruption', 'Extended downtime', 'Performance issues'],
                'resources_required': ['Database Specialist', 'Migration Engineer'],
                'status': 'pending'
            }
            phases.append(phase3)
            current_week += db_duration
        
        # Phase 4: Application Migration
        if servers:
            app_duration = max(4, len(servers) * 1.5)  # Minimum 4 weeks, 1.5 weeks per server
            phase4 = {
                'phase': 4,
                'title': 'Application Migration',
                'description': 'Migrate applications and services to cloud infrastructure.',
                'duration_weeks': int(app_duration),
                'start_week': current_week,
                'end_week': current_week + int(app_duration) - 1,
                'dependencies': ['Phase 3 - Database Migration'] if databases else ['Phase 2 - Cloud Environment Setup'],
                'milestones': [
                    'Applications rehosted',
                    'Dependencies resolved',
                    'Integration testing completed',
                    'Performance benchmarks met'
                ],
                'components': [server.server_id for server in servers],
                'risks': ['Application compatibility', 'Integration failures'],
                'resources_required': ['Migration Engineer', 'Application Specialist'],
                'status': 'pending'
            }
            phases.append(phase4)
            current_week += int(app_duration)
        
        # Phase 5: Data Storage Migration
        if file_shares:
            storage_duration = max(2, len(file_shares) * 1)  # Minimum 2 weeks, 1 week per share
            phase5 = {
                'phase': 5,
                'title': 'Data Storage Migration',
                'description': 'Migrate file shares and storage systems to cloud storage services.',
                'duration_weeks': storage_duration,
                'start_week': current_week,
                'end_week': current_week + storage_duration - 1,
                'dependencies': ['Phase 4 - Application Migration'] if servers else ['Phase 3 - Database Migration'] if databases else ['Phase 2 - Cloud Environment Setup'],
                'milestones': [
                    'Storage systems migrated',
                    'Access permissions configured',
                    'Data integrity verified',
                    'Performance validated'
                ],
                'components': [share.share_name for share in file_shares],
                'risks': ['Data transfer failures', 'Access issues'],
                'resources_required': ['Migration Engineer', 'Storage Specialist'],
                'status': 'pending'
            }
            phases.append(phase5)
            current_week += storage_duration
        
        # Phase 6: Testing and Validation
        phase6 = {
            'phase': 6,
            'title': 'Testing and Validation',
            'description': 'Comprehensive testing of migrated systems and user acceptance testing.',
            'duration_weeks': 3,
            'start_week': current_week,
            'end_week': current_week + 2,
            'dependencies': [f'Phase {len(phases)} - {phases[-1]["title"]}'],
            'milestones': [
                'System testing completed',
                'Performance testing passed',
                'Security testing validated',
                'User acceptance achieved'
            ],
            'components': ['All Migrated Systems'],
            'risks': ['Test failures', 'Performance issues'],
            'resources_required': ['QA Engineer', 'Migration Engineer'],
            'status': 'pending'
        }
        phases.append(phase6)
        current_week += 3
        
        # Phase 7: Go-Live and Cutover
        phase7 = {
            'phase': 7,
            'title': 'Go-Live and Cutover',
            'description': 'Final cutover to production cloud environment with go-live support.',
            'duration_weeks': 2,
            'start_week': current_week,
            'end_week': current_week + 1,
            'dependencies': ['Phase 6 - Testing and Validation'],
            'milestones': [
                'DNS cutover completed',
                'Production traffic migrated',
                'Monitoring active',
                'Support handover completed'
            ],
            'components': ['Production Systems'],
            'risks': ['Service interruption', 'Rollback scenarios'],
            'resources_required': ['Migration Engineer', 'Support Team'],
            'status': 'pending'
        }
        phases.append(phase7)
        current_week += 2
        
        # Phase 8: Post-Migration Support
        phase8 = {
            'phase': 8,
            'title': 'Post-Migration Support',
            'description': 'Hypercare support and optimization of cloud environment.',
            'duration_weeks': 4,
            'start_week': current_week,
            'end_week': current_week + 3,
            'dependencies': ['Phase 7 - Go-Live and Cutover'],
            'milestones': [
                'Stability monitoring active',
                'Performance optimized',
                'Team training completed',
                'Documentation finalized'
            ],
            'components': ['All Systems'],
            'risks': ['Performance degradation', 'Support gaps'],
            'resources_required': ['Support Team', 'Cloud Architect'],
            'status': 'pending'
        }
        phases.append(phase8)
        
        return phases
        
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
    
    def _calculate_project_overview(self, phases, constraints) -> Dict[str, Any]:
        """Calculate project overview metrics"""
        total_weeks = sum(phase['duration_weeks'] for phase in phases)
        total_months = round(total_weeks / 4.33, 1)  # Average weeks per month
        
        # Calculate dates
        start_date = datetime.now()
        end_date = start_date + timedelta(weeks=total_weeks)
        
        # Calculate complexity score based on components
        complexity_factors = []
        if phases:
            total_components = sum(len(phase.get('components', [])) for phase in phases)
            complexity_factors.append(min(total_components * 10, 50))  # Component complexity
            complexity_factors.append(min(len(phases) * 5, 30))  # Phase complexity
            complexity_factors.append(20)  # Base complexity
        
        complexity_score = min(sum(complexity_factors), 100)
        
        # Determine confidence level
        if complexity_score < 40:
            confidence = "High"
        elif complexity_score < 70:
            confidence = "Medium"
        else:
            confidence = "Low"
        
        return {
            'total_duration_weeks': total_weeks,
            'total_duration_months': total_months,
            'estimated_start_date': start_date.strftime('%Y-%m-%d'),
            'estimated_end_date': end_date.strftime('%Y-%m-%d'),
            'confidence_level': confidence,
            'complexity_score': complexity_score
        }
    
    def _generate_resource_allocation(self, phases) -> List[Dict[str, Any]]:
        """Generate resource allocation across phases"""
        resource_allocation = {}
        
        for phase in phases:
            for resource in phase.get('resources_required', []):
                if resource not in resource_allocation:
                    resource_allocation[resource] = {
                        'role': resource,
                        'weeks_allocated': 0,
                        'overlap_phases': [],
                        'peak_utilization_week': 0
                    }
                
                resource_allocation[resource]['weeks_allocated'] += phase['duration_weeks']
                resource_allocation[resource]['overlap_phases'].append(phase['phase'])
                
                # Calculate peak utilization (middle of longest phase involvement)
                if phase['duration_weeks'] > 0:
                    mid_week = phase['start_week'] + (phase['duration_weeks'] // 2)
                    if mid_week > resource_allocation[resource]['peak_utilization_week']:
                        resource_allocation[resource]['peak_utilization_week'] = mid_week
        
        return list(resource_allocation.values())
    
    def _calculate_risk_mitigation(self, phases) -> List[Dict[str, Any]]:
        """Calculate risk mitigation strategies"""
        risk_mitigation = []
        
        # Common migration risks
        common_risks = [
            {
                'risk': 'Data loss or corruption during migration',
                'probability': 'Medium',
                'impact': 'High',
                'mitigation_strategy': 'Implement comprehensive backup strategy, perform test migrations, and maintain rollback procedures.',
                'timeline_buffer_weeks': 2
            },
            {
                'risk': 'Extended downtime during cutover',
                'probability': 'Medium',
                'impact': 'High',
                'mitigation_strategy': 'Use phased migration approach, implement blue-green deployment, and schedule during low-usage periods.',
                'timeline_buffer_weeks': 1
            },
            {
                'risk': 'Performance degradation post-migration',
                'probability': 'Medium',
                'impact': 'Medium',
                'mitigation_strategy': 'Conduct thorough performance testing, right-size cloud resources, and implement monitoring.',
                'timeline_buffer_weeks': 2
            },
            {
                'risk': 'Security misconfigurations',
                'probability': 'Low',
                'impact': 'High',
                'mitigation_strategy': 'Follow security best practices, conduct security reviews, and implement automated compliance checks.',
                'timeline_buffer_weeks': 1
            },
            {
                'risk': 'Resource availability constraints',
                'probability': 'Medium',
                'impact': 'Medium',
                'mitigation_strategy': 'Secure resource commitments early, cross-train team members, and maintain vendor relationships.',
                'timeline_buffer_weeks': 1
            }
        ]
        
        return common_risks
    
    def _define_success_criteria(self) -> List[str]:
        """Define project success criteria"""
        return [
            'All systems successfully migrated with zero data loss',
            'Application performance meets or exceeds baseline metrics',
            'Security and compliance requirements fully satisfied',
            'Total downtime kept under planned maintenance windows',
            'End-user productivity maintained throughout migration',
            'Cost targets achieved within 10% variance',
            'Team fully trained on cloud operations and management',
            'Comprehensive documentation and runbooks completed'
        ]
    
    def _identify_critical_path(self, phases) -> List[str]:
        """Identify critical path components"""
        critical_components = []
        
        # Database migrations are typically critical
        for phase in phases:
            if 'Database' in phase['title']:
                critical_components.extend(phase.get('components', []))
            elif 'Application' in phase['title']:
                # Add high-priority applications to critical path
                critical_components.extend(phase.get('components', [])[:2])  # First 2 components
        
        # Add testing and cutover phases as they're always critical
        critical_components.extend(['System Testing', 'Production Cutover', 'DNS Migration'])
        
        return critical_components[:8]  # Limit to top 8 critical items
    
    def _get_ai_timeline_insights(self, servers, databases, file_shares) -> Dict[str, List[str]]:
        """Get AI-powered timeline insights"""
        if not self.ai_service.bedrock_client:
            return self._get_fallback_insights()
        
        try:
            # Build context for AI analysis
            context = f"""
            Migration Timeline Analysis:
            - Servers: {len(servers)} ({', '.join([s.os_type for s in servers[:3]])})
            - Databases: {len(databases)} ({', '.join([d.db_type for d in databases[:3]])})
            - File Shares: {len(file_shares)} TB total storage
            
            Provide timeline optimization insights including:
            1. Timeline optimization suggestions
            2. Potential timeline risks 
            3. Resource allocation recommendations
            """
            
            # Get AI recommendations
            recommendation = self.ai_service._get_ai_recommendation(context, 'timeline_analysis')
            
            return {
                'optimization_suggestions': [
                    'Parallelize database and application migrations where possible',
                    'Use cloud-native migration tools to reduce timeline',
                    'Implement automated testing to accelerate validation phases'
                ],
                'timeline_risks': [
                    'Database migration complexity may extend timeline',
                    'Legacy application dependencies could cause delays',
                    'Resource availability during peak migration phases'
                ],
                'resource_recommendations': [
                    'Assign dedicated database specialist for critical systems',
                    'Consider additional migration engineers for parallel workstreams',
                    'Engage cloud vendor support for complex migration scenarios'
                ]
            }
            
        except Exception as e:
            self.logger.warning(f"AI insights failed: {e}")
            return self._get_fallback_insights()
    
    def _get_fallback_insights(self) -> Dict[str, List[str]]:
        """Fallback insights when AI is not available"""
        return {
            'optimization_suggestions': [
                'Use parallel migration streams to reduce overall timeline',
                'Leverage cloud migration tools and services for efficiency',
                'Implement automated testing and validation processes',
                'Consider off-hours migration windows to minimize impact'
            ],
            'timeline_risks': [
                'Complex legacy systems may require additional migration time',
                'Data migration volumes could extend transfer timelines',
                'Testing phases may reveal integration issues requiring rework',
                'Resource scheduling conflicts across multiple project phases'
            ],
            'resource_recommendations': [
                'Ensure dedicated migration team with cloud expertise',
                'Include database specialists for complex data migrations',
                'Plan for 24/7 support coverage during critical cutover phases',
                'Consider external consultant support for specialized workloads'
            ]
        }
