import boto3
import json
import logging
import os
from typing import Dict, List, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIRecommendationService:
    """AI-powered recommendation service using AWS Bedrock"""
    
    def __init__(self, region_name=None):
        try:
            # Use environment variables for AWS configuration
            self.region_name = region_name or os.getenv('AWS_REGION', 'us-east-1')
            
            # Initialize Bedrock client with credentials from environment
            self.bedrock_client = boto3.client(
                'bedrock-runtime',
                region_name=self.region_name,
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )
            
            self.model_id = os.getenv('BEDROCK_MODEL_ID', "anthropic.claude-3-sonnet-20240229-v1:0")
            self.logger = logging.getLogger(__name__)
            
            # Skip connection test to avoid hanging
            # self._test_bedrock_connection()
            
        except Exception as e:
            self.logger.warning(f"Bedrock client initialization failed: {e}")
            self.bedrock_client = None
    
    def _test_bedrock_connection(self):
        """Test if Bedrock connection is working"""
        if not self.bedrock_client:
            return False
        
        # List of models to try in order of user preference
        models_to_try = [
            "anthropic.claude-3-5-sonnet-20240620-v1:0",  # 1. Claude 3.5 Sonnet
            "anthropic.claude-3-sonnet-20240229-v1:0",    # 2. Claude 3 Sonnet
            "amazon.titan-text-express-v1"               # 3. Titan Text G1 - Express
        ]
        
        for model_id in models_to_try:
            try:
                self.logger.info(f"🧪 Testing model: {model_id}")
                
                if "anthropic" in model_id:
                    # Anthropic models use the messages format
                    test_body = {
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 10,
                        "messages": [{"role": "user", "content": "test"}]
                    }
                elif "titan" in model_id:
                    # Titan models use different format
                    test_body = {
                        "inputText": "test",
                        "textGenerationConfig": {
                            "maxTokenCount": 10,
                            "temperature": 0.1
                        }
                    }
                else:
                    continue
                
                response = self.bedrock_client.invoke_model(
                    modelId=model_id,
                    body=json.dumps(test_body)
                )
                
                self.logger.info(f"✅ Model {model_id} is working!")
                self.model_id = model_id
                return True
                
            except Exception as e:
                self.logger.warning(f"❌ Model {model_id} failed: {e}")
                continue
        
        # If all models failed
        self.logger.error("❌ No Bedrock models are accessible. Models may need to be enabled in AWS console.")
        self.bedrock_client = None
        return False
    
    def get_server_recommendation(self, server_specs: Dict[str, Any]) -> Dict[str, Any]:
        """Get AI-powered EC2 instance recommendation"""
        if not self.bedrock_client:
            return self._fallback_server_recommendation(server_specs)
        
        prompt = f"""
        You are an AWS cloud migration expert. Based on the following server specifications, recommend the most suitable EC2 instance type and provide detailed reasoning.

        Server Details:
        - Server ID: {server_specs.get('server_id', 'N/A')}
        - OS Type: {server_specs.get('os_type', 'N/A')}
        - vCPUs: {server_specs.get('vcpu', 'N/A')}
        - RAM: {server_specs.get('ram', 'N/A')} GB
        - Disk Size: {server_specs.get('disk_size', 'N/A')} GB
        - Disk Type: {server_specs.get('disk_type', 'N/A')}
        - Uptime Pattern: {server_specs.get('uptime_pattern', 'N/A')}
        - Current Hosting: {server_specs.get('current_hosting', 'N/A')}
        - Technologies: {server_specs.get('technology', 'N/A')}

        Consider the following factors:
        1. Performance requirements based on vCPU and RAM
        2. Cost optimization opportunities
        3. Workload patterns and uptime requirements
        4. Technology stack compatibility
        5. Storage performance needs
        6. Potential for spot instances or reserved instances

        Provide your response in the following JSON format:
        {{
            "recommended_instance": "instance_type",
            "instance_family": "family_name",
            "reasoning": "detailed explanation",
            "cost_optimization_tips": ["tip1", "tip2"],
            "alternative_options": [
                {{"instance": "alternative1", "use_case": "description"}},
                {{"instance": "alternative2", "use_case": "description"}}
            ],
            "confidence_level": "high/medium/low"
        }}
        """
        
        try:
            response = self._call_bedrock(prompt)
            result = self._parse_ai_response(response, 'server')
            
            # Mark as AI-generated response
            if result and not result.get('fallback_used'):
                result['fallback_used'] = False
                result['ai_model'] = self.model_id
            
            return result
        except Exception as e:
            self.logger.error(f"AI recommendation failed for server: {e}")
            return self._fallback_server_recommendation(server_specs)
    
    def get_database_recommendation(self, db_specs: Dict[str, Any]) -> Dict[str, Any]:
        """Get AI-powered RDS instance recommendation"""
        if not self.bedrock_client:
            return self._fallback_database_recommendation(db_specs)
        
        prompt = f"""
        You are an AWS database migration expert. Based on the following database specifications, recommend the most suitable RDS instance type and configuration.

        Database Details:
        - Database Name: {db_specs.get('db_name', 'N/A')}
        - Database Type: {db_specs.get('db_type', 'N/A')}
        - Size: {db_specs.get('size_gb', 'N/A')} GB
        - HA/DR Required: {db_specs.get('ha_dr_required', 'N/A')}
        - Backup Frequency: {db_specs.get('backup_frequency', 'N/A')}
        - Performance Tier: {db_specs.get('performance_tier', 'N/A')}

        Consider the following factors:
        1. Database engine compatibility
        2. Performance requirements and IOPS needs
        3. High availability and disaster recovery needs
        4. Backup and retention requirements
        5. Cost optimization (Reserved Instances, Aurora Serverless)
        6. Security and compliance requirements
        7. Read replica needs

        Provide your response in the following JSON format:
        {{
            "recommended_instance": "instance_type",
            "engine_recommendation": "recommended_engine",
            "storage_type": "recommended_storage",
            "multi_az": true/false,
            "reasoning": "detailed explanation",
            "performance_insights": "recommendations",
            "cost_optimization_tips": ["tip1", "tip2"],
            "migration_complexity": "low/medium/high",
            "confidence_level": "high/medium/low"
        }}
        """
        
        try:
            response = self._call_bedrock(prompt)
            return self._parse_ai_response(response, 'database')
        except Exception as e:
            self.logger.error(f"AI recommendation failed for database: {e}")
            return self._fallback_database_recommendation(db_specs)
    
    def get_storage_recommendation(self, storage_specs: Dict[str, Any]) -> Dict[str, Any]:
        """Get AI-powered storage recommendation"""
        if not self.bedrock_client:
            return self._fallback_storage_recommendation(storage_specs)
        
        prompt = f"""
        You are an AWS storage migration expert. Based on the following file share specifications, recommend the most suitable AWS storage solution.

        Storage Details:
        - Share Name: {storage_specs.get('share_name', 'N/A')}
        - Total Size: {storage_specs.get('total_size_gb', 'N/A')} GB
        - File Count: {storage_specs.get('file_count', 'N/A')}
        - Access Pattern: {storage_specs.get('access_pattern', 'N/A')}
        - File Types: {storage_specs.get('file_types', 'N/A')}
        - Access Frequency: {storage_specs.get('access_frequency', 'N/A')}

        Consider the following factors:
        1. Access patterns and frequency
        2. File size distribution
        3. Performance requirements
        4. Cost optimization through storage classes
        5. Integration with other AWS services
        6. Backup and versioning needs
        7. Security and compliance requirements

        Recommend from these options: S3 Standard, S3 IA, S3 One Zone-IA, S3 Glacier Instant Retrieval, S3 Glacier Flexible Retrieval, S3 Glacier Deep Archive, EFS, FSx

        Provide your response in the following JSON format:
        {{
            "recommended_storage": "storage_type",
            "storage_class": "specific_class",
            "reasoning": "detailed explanation",
            "lifecycle_policy": "recommended_policy",
            "cost_optimization_tips": ["tip1", "tip2"],
            "performance_considerations": "recommendations",
            "alternative_options": [
                {{"storage": "alternative1", "use_case": "description"}},
                {{"storage": "alternative2", "use_case": "description"}}
            ],
            "confidence_level": "high/medium/low"
        }}
        """
        
        try:
            response = self._call_bedrock(prompt)
            return self._parse_ai_response(response, 'storage')
        except Exception as e:
            self.logger.error(f"AI recommendation failed for storage: {e}")
            return self._fallback_storage_recommendation(storage_specs)
    
    def get_comprehensive_analysis(self, infrastructure_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive migration strategy recommendations"""
        if not self.bedrock_client:
            return {"analysis": "AI analysis not available", "recommendations": []}
        
        prompt = f"""
        You are a senior cloud migration architect. Analyze the following infrastructure summary and provide comprehensive migration recommendations.

        Infrastructure Summary:
        {json.dumps(infrastructure_summary, indent=2)}

        Provide strategic recommendations covering:
        1. Overall migration approach (lift-and-shift vs. modernization)
        2. Priority and phasing recommendations
        3. Risk mitigation strategies
        4. Cost optimization opportunities
        5. Performance optimization suggestions
        6. Security and compliance considerations
        7. Timeline and resource planning

        Provide your response in the following JSON format:
        {{
            "migration_strategy": "overall_approach",
            "priority_phases": [
                {{"phase": 1, "components": ["item1", "item2"], "rationale": "reason"}},
                {{"phase": 2, "components": ["item3", "item4"], "rationale": "reason"}}
            ],
            "risk_assessment": {{"high": ["risk1"], "medium": ["risk2"], "low": ["risk3"]}},
            "cost_optimization": ["opportunity1", "opportunity2"],
            "modernization_opportunities": ["modernization1", "modernization2"],
            "timeline_estimate": "estimated_duration",
            "key_recommendations": ["recommendation1", "recommendation2"],
            "success_metrics": ["metric1", "metric2"]
        }}
        """
        
        try:
            response = self._call_bedrock(prompt)
            return self._parse_ai_response(response, 'analysis')
        except Exception as e:
            self.logger.error(f"AI comprehensive analysis failed: {e}")
            return {"analysis": "AI analysis failed", "recommendations": []}
    
    def get_cost_optimization_recommendations(self, inventory_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get AI-powered cost optimization recommendations"""
        if not self.bedrock_client:
            return self._fallback_cost_optimization(inventory_data)
        
        servers_count = len(inventory_data.get('servers', []))
        databases_count = len(inventory_data.get('databases', []))
        file_shares_count = len(inventory_data.get('file_shares', []))
        
        prompt = f"""
        You are a senior cloud cost optimization specialist. Analyze the following infrastructure inventory and provide specific cost optimization recommendations for AWS cloud migration.

        Infrastructure Inventory:
        - Servers: {servers_count} servers
        - Databases: {databases_count} databases  
        - File Shares: {file_shares_count} file shares
        
        Detailed inventory:
        {json.dumps(inventory_data, indent=2)}

        Provide specific, actionable cost optimization recommendations. Focus on:
        1. EC2 instance right-sizing and reserved instance opportunities
        2. Database optimization and managed service benefits
        3. Storage optimization and lifecycle policies
        4. Auto-scaling and resource scheduling
        5. Cost monitoring and governance

        Provide your response in the following JSON format:
        {{
            "confidence_level": 0.90,
            "recommendations": [
                "Specific recommendation 1 with expected savings",
                "Specific recommendation 2 with expected savings",
                "Specific recommendation 3 with expected savings"
            ],
            "cost_optimization_tips": [
                "Quick tip 1 with percentage savings",
                "Quick tip 2 with percentage savings",
                "Quick tip 3 with percentage savings"
            ],
            "expected_savings": {{
                "monthly_percentage": 25,
                "annual_amount": 50000
            }}
        }}
        """
        
        try:
            response = self._call_bedrock(prompt)
            result = self._parse_ai_response(response, 'cost_optimization')
            
            # Ensure we have the required fields
            if not result.get('recommendations'):
                return self._fallback_cost_optimization(inventory_data)
                
            # Mark as AI-generated response
            result['fallback_used'] = False
            result['ai_model'] = self.model_id
            
            return result
            
        except Exception as e:
            self.logger.error(f"AI cost optimization failed: {e}")
            return self._fallback_cost_optimization(inventory_data)
    
    def get_ai_cost_estimation(self, infrastructure_data: Dict[str, Any], cloud_provider: str = "AWS", target_region: str = "us-east-1") -> Dict[str, Any]:
        """Get AI-powered comprehensive cost estimation"""
        if not self.bedrock_client:
            return self._fallback_cost_estimation(infrastructure_data, cloud_provider, target_region)

        servers = infrastructure_data.get('servers', [])
        databases = infrastructure_data.get('databases', [])
        file_shares = infrastructure_data.get('file_shares', [])

        prompt = f"""
        You are a senior cloud cost optimization specialist with expertise in {cloud_provider} pricing models. Provide a comprehensive cost estimation for migrating the following infrastructure to {cloud_provider} in the {target_region} region.

        Infrastructure to Migrate:
        Servers ({len(servers)} total):
        {json.dumps(servers, indent=2)}

        Databases ({len(databases)} total):
        {json.dumps(databases, indent=2)}

        File Shares ({len(file_shares)} total):
        {json.dumps(file_shares, indent=2)}

        Consider these factors in your cost analysis:
        1. Current usage patterns and peak hours
        2. Reserved instance vs on-demand pricing
        3. Storage optimization opportunities
        4. Network transfer costs
        5. Backup and disaster recovery costs
        6. Management and monitoring costs
        7. Migration service costs
        8. Professional services required

        Provide your response in this exact JSON format:
        {{
            "grand_total": {{
                "annual_cloud_cost": <number>,
                "one_time_migration_cost": <number>,
                "total_first_year_cost": <number>
            }},
            "cloud_infrastructure": {{
                "servers": {{
                    "total_monthly_cost": <number>,
                    "total_annual_cost": <number>,
                    "server_recommendations": [
                        {{
                            "server_id": "string",
                            "current_specs": "string",
                            "recommended_instance": "string",
                            "monthly_cost": <number>,
                            "annual_cost": <number>,
                            "optimization_notes": "string"
                        }}
                    ]
                }},
                "databases": {{
                    "total_monthly_cost": <number>,
                    "total_annual_cost": <number>,
                    "database_recommendations": [
                        {{
                            "db_name": "string",
                            "db_type": "string",
                            "recommended_instance": "string",
                            "size_gb": <number>,
                            "monthly_cost": <number>,
                            "annual_cost": <number>,
                            "optimization_notes": "string"
                        }}
                    ]
                }},
                "storage": {{
                    "total_monthly_cost": <number>,
                    "total_annual_cost": <number>,
                    "storage_recommendations": [
                        {{
                            "share_name": "string",
                            "size_gb": <number>,
                            "recommended_storage": "string",
                            "access_pattern": "string",
                            "monthly_cost": <number>,
                            "annual_cost": <number>,
                            "optimization_notes": "string"
                        }}
                    ]
                }},
                "total_monthly_cost": <number>,
                "total_annual_cost": <number>
            }},
            "migration_services": {{
                "total_professional_services_cost": <number>,
                "resource_breakdown": [
                    {{
                        "role": "string",
                        "rate_per_hour": <number>,
                        "hours_per_week": <number>,
                        "duration_weeks": <number>,
                        "total_hours": <number>,
                        "total_cost": <number>
                    }}
                ]
            }},
            "ai_insights": {{
                "confidence_level": <number>,
                "cost_optimization_tips": ["string"],
                "potential_savings": {{
                    "percentage": <number>,
                    "annual_amount": <number>
                }},
                "recommendations": ["string"],
                "ai_model_used": "{self.model_id}",
                "fallback_used": false
            }}
        }}
        """

        try:
            response = self._call_bedrock(prompt)
            result = self._parse_ai_response(response, 'cost_estimation')
            
            if result and not result.get('fallback_used'):
                result['ai_insights']['ai_model_used'] = self.model_id
                result['ai_insights']['fallback_used'] = False
            
            return result
        except Exception as e:
            self.logger.error(f"AI cost estimation failed: {e}")
            return self._fallback_cost_estimation(infrastructure_data, cloud_provider, target_region)

    def get_ai_migration_strategy(self, infrastructure_data: Dict[str, Any], cloud_provider: str = "AWS", 
                                target_region: str = "us-east-1", complexity: str = "medium") -> Dict[str, Any]:
        """Get AI-powered comprehensive migration strategy"""
        if not self.bedrock_client:
            return self._fallback_migration_strategy(infrastructure_data, cloud_provider, complexity)

        servers = infrastructure_data.get('servers', [])
        databases = infrastructure_data.get('databases', [])
        file_shares = infrastructure_data.get('file_shares', [])
        complexity_score = len(servers) + len(databases) + len(file_shares)

        prompt = f"""
        You are a senior cloud migration architect with expertise in {cloud_provider} migration strategies. Create a comprehensive migration strategy for the following infrastructure with {complexity} complexity level.

        Infrastructure to Migrate:
        Servers ({len(servers)} total):
        {json.dumps(servers, indent=2)}

        Databases ({len(databases)} total):
        {json.dumps(databases, indent=2)}

        File Shares ({len(file_shares)} total):
        {json.dumps(file_shares, indent=2)}

        Migration Context:
        - Target Cloud: {cloud_provider}
        - Target Region: {target_region}
        - Complexity Level: {complexity}
        - Total Complexity Score: {complexity_score}

        Consider these migration approaches:
        1. Rehost (Lift and Shift) - Quick migration with minimal changes
        2. Replatform - Some optimization during migration
        3. Refactor/Rearchitect - Significant modernization
        4. Replace - Move to SaaS solutions
        5. Hybrid approaches for different components

        Provide your response in this exact JSON format:
        {{
            "migration_approach": {{
                "overall_strategy": "string",
                "estimated_duration": "string",
                "complexity_level": "Low/Medium/High",
                "rationale": "string"
            }},
            "component_strategies": {{
                "servers": [
                    {{
                        "server_id": "string",
                        "migration_type": "string",
                        "current_state": "string",
                        "target_state": "string",
                        "complexity": "string",
                        "estimated_effort": "string",
                        "rationale": "string"
                    }}
                ],
                "databases": [
                    {{
                        "db_name": "string",
                        "current_engine": "string",
                        "target_engine": "string",
                        "migration_type": "string",
                        "approach": "string",
                        "complexity": "string",
                        "data_migration_strategy": "string",
                        "downtime_estimate": "string"
                    }}
                ],
                "storage": [
                    {{
                        "share_name": "string",
                        "current_type": "string",
                        "target_type": "string",
                        "migration_method": "string",
                        "sync_strategy": "string",
                        "cutover_approach": "string"
                    }}
                ]
            }},
            "migration_phases": [
                {{
                    "phase": <number>,
                    "name": "string",
                    "duration": "string",
                    "components": ["string"],
                    "dependencies": ["string"],
                    "risks": ["string"],
                    "success_criteria": ["string"]
                }}
            ],
            "recommendations": {{
                "quick_wins": ["string"],
                "cost_optimization": ["string"],
                "performance_improvements": ["string"],
                "modernization_opportunities": ["string"]
            }},
            "risk_assessment": {{
                "high_risks": ["string"],
                "medium_risks": ["string"],
                "low_risks": ["string"],
                "mitigation_strategies": {{
                    "risk_name": "mitigation_strategy"
                }}
            }},
            "ai_insights": {{
                "confidence_level": <number>,
                "ai_model_used": "{self.model_id}",
                "fallback_used": false,
                "strategic_recommendations": ["string"]
            }}
        }}
        """

        try:
            response = self._call_bedrock(prompt)
            result = self._parse_ai_response(response, 'migration_strategy')
            
            if result and not result.get('fallback_used'):
                if 'ai_insights' not in result:
                    result['ai_insights'] = {}
                result['ai_insights']['ai_model_used'] = self.model_id
                result['ai_insights']['fallback_used'] = False
            
            return result
        except Exception as e:
            self.logger.error(f"AI migration strategy failed: {e}")
            return self._fallback_migration_strategy(infrastructure_data, cloud_provider, complexity)

    def _call_bedrock(self, prompt: str) -> str:
        """Call AWS Bedrock with the given prompt"""
        try:
            if "anthropic" in self.model_id:
                # Anthropic models (Claude) use messages format
                body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 4000,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.1,
                    "top_p": 0.9
                }
                
                response = self.bedrock_client.invoke_model(
                    modelId=self.model_id,
                    body=json.dumps(body)
                )
                
                response_body = json.loads(response['body'].read())
                return response_body['content'][0]['text']
                
            elif "titan" in self.model_id:
                # Amazon Titan models use different format
                body = {
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": 4000,
                        "temperature": 0.1,
                        "topP": 0.9
                    }
                }
                
                response = self.bedrock_client.invoke_model(
                    modelId=self.model_id,
                    body=json.dumps(body)
                )
                
                response_body = json.loads(response['body'].read())
                return response_body['results'][0]['outputText']
                
            elif "nova" in self.model_id:
                # Amazon Nova models use messages format but different structure
                body = {
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "inferenceConfig": {
                        "maxTokens": 4000,
                        "temperature": 0.1,
                        "topP": 0.9
                    }
                }
                
                response = self.bedrock_client.invoke_model(
                    modelId=self.model_id,
                    body=json.dumps(body)
                )
                
                response_body = json.loads(response['body'].read())
                return response_body['output']['message']['content'][0]['text']
                
            else:
                # Generic fallback - try Anthropic format
                body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 4000,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.1,
                    "top_p": 0.9
                }
                
                response = self.bedrock_client.invoke_model(
                    modelId=self.model_id,
                    body=json.dumps(body)
                )
                
                response_body = json.loads(response['body'].read())
                return response_body['content'][0]['text']
                
        except Exception as e:
            self.logger.error(f"Bedrock API call failed: {e}")
            raise
    
    def _parse_ai_response(self, response: str, response_type: str) -> Dict[str, Any]:
        """Parse AI response and extract JSON"""
        try:
            # Find JSON in the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                result = json.loads(json_str)
                
                # Normalize confidence level to decimal format (0.0-1.0)
                if 'confidence_level' in result:
                    confidence = result['confidence_level']
                    if isinstance(confidence, (int, float)) and confidence > 1:
                        # Convert percentage to decimal (85 -> 0.85)
                        result['confidence_level'] = confidence / 100.0
                
                return result
            else:
                raise ValueError("No JSON found in response")
        except Exception as e:
            self.logger.error(f"Failed to parse AI response for {response_type}: {e}")
            return {"error": "Failed to parse AI response", "raw_response": response}
    
    # Fallback methods for when AI is not available
    def _fallback_server_recommendation(self, server_specs: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback server recommendation logic"""
        vcpu = server_specs.get('vcpu', 2)
        ram = server_specs.get('ram', 4)
        
        if vcpu <= 2 and ram <= 2:
            instance = 't3.small'
        elif vcpu <= 2 and ram <= 4:
            instance = 't3.medium'
        elif vcpu <= 2 and ram <= 8:
            instance = 't3.large'
        elif vcpu <= 4 and ram <= 16:
            instance = 't3.xlarge'
        elif vcpu <= 8 and ram <= 32:
            instance = 't3.2xlarge'
        else:
            instance = 'm5.4xlarge'
        
        return {
            "recommended_instance": instance,
            "reasoning": "Basic sizing based on vCPU and RAM requirements",
            "confidence_level": "medium",
            "fallback_used": True,
            "fallback_reason": "AI service not available - using rule-based recommendation"
        }
    
    def _fallback_database_recommendation(self, db_specs: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback database recommendation logic"""
        size_gb = db_specs.get('size_gb', 100)
        ha_required = db_specs.get('ha_dr_required', False)
        
        if size_gb <= 20:
            instance = 'db.t3.micro'
        elif size_gb <= 100:
            instance = 'db.t3.small'
        elif size_gb <= 500:
            instance = 'db.t3.medium'
        elif size_gb <= 1000:
            instance = 'db.t3.large'
        else:
            instance = 'db.m5.large' if not ha_required else 'db.m5.xlarge'
        
        return {
            "recommended_instance": instance,
            "reasoning": "Basic sizing based on database size and HA requirements",
            "confidence_level": "medium"
        }
    
    def _fallback_storage_recommendation(self, storage_specs: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback storage recommendation logic"""
        access_pattern = storage_specs.get('access_pattern', 'Hot')
        
        if access_pattern == 'Hot':
            storage = 'S3 Standard'
        elif access_pattern == 'Warm':
            storage = 'S3 IA'
        else:
            storage = 'S3 Glacier'
        
        return {
            "recommended_storage": storage,
            "reasoning": f"Basic recommendation based on {access_pattern} access pattern",
            "confidence_level": "medium"
        }
    
    def _fallback_cost_optimization(self, inventory_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback cost optimization recommendations"""
        servers_count = len(inventory_data.get('servers', []))
        databases_count = len(inventory_data.get('databases', []))
        file_shares_count = len(inventory_data.get('file_shares', []))
        
        return {
            "confidence_level": 0.85,
            "recommendations": [
                f"Consider reserved instances for {servers_count} servers - save 20-72% vs on-demand pricing",
                f"Evaluate managed database services for {databases_count} databases to reduce operational costs",
                f"Implement S3 intelligent tiering for {file_shares_count} file shares to optimize storage costs",
                "Use auto-scaling groups to match compute capacity with actual demand",
                "Implement resource tagging and cost allocation for better cost visibility"
            ],
            "cost_optimization_tips": [
                "Reserved instances offer 20-72% savings over on-demand pricing",
                "S3 Intelligent Tiering can reduce storage costs by 30-68%",
                "Auto-scaling can reduce compute costs by 10-50% during low usage periods",
                "Spot instances can provide up to 90% savings for fault-tolerant workloads",
                "Right-sizing instances can reduce costs by 10-30% on average"
            ],
            "expected_savings": {
                "monthly_percentage": 25,
                "annual_amount": max(10000, (servers_count + databases_count) * 2000)
            },
            "fallback_used": True,
            "fallback_reason": "AI service not available - using rule-based recommendations"
        }
    
    def _fallback_cost_estimation(self, infrastructure_data: Dict[str, Any], cloud_provider: str, target_region: str) -> Dict[str, Any]:
        """Fallback cost estimation when AI is not available"""
        servers = infrastructure_data.get('servers', [])
        databases = infrastructure_data.get('databases', [])
        file_shares = infrastructure_data.get('file_shares', [])
        
        # Simple cost calculation based on resource count
        server_monthly_cost = len(servers) * 200  # Approximate $200/server/month
        db_monthly_cost = len(databases) * 300    # Approximate $300/db/month
        storage_monthly_cost = len(file_shares) * 50  # Approximate $50/share/month
        
        total_monthly = server_monthly_cost + db_monthly_cost + storage_monthly_cost
        total_annual = total_monthly * 12
        migration_cost = (len(servers) + len(databases)) * 1000  # $1000 per major component
        
        return {
            "grand_total": {
                "annual_cloud_cost": total_annual,
                "one_time_migration_cost": migration_cost,
                "total_first_year_cost": total_annual + migration_cost
            },
            "cloud_infrastructure": {
                "servers": {
                    "total_monthly_cost": server_monthly_cost,
                    "total_annual_cost": server_monthly_cost * 12,
                    "server_recommendations": [
                        {
                            "server_id": f"Server-{i+1}",
                            "current_specs": "Standard server",
                            "recommended_instance": "t3.medium",
                            "monthly_cost": 200,
                            "annual_cost": 2400,
                            "optimization_notes": "Basic estimation - requires detailed analysis"
                        } for i in range(len(servers))
                    ]
                },
                "databases": {
                    "total_monthly_cost": db_monthly_cost,
                    "total_annual_cost": db_monthly_cost * 12,
                    "database_recommendations": [
                        {
                            "db_name": f"Database-{i+1}",
                            "db_type": "MySQL",
                            "recommended_instance": "db.t3.medium",
                            "size_gb": 100,
                            "monthly_cost": 300,
                            "annual_cost": 3600,
                            "optimization_notes": "Basic estimation - requires detailed analysis"
                        } for i in range(len(databases))
                    ]
                },
                "storage": {
                    "total_monthly_cost": storage_monthly_cost,
                    "total_annual_cost": storage_monthly_cost * 12,
                    "storage_recommendations": [
                        {
                            "share_name": f"FileShare-{i+1}",
                            "size_gb": 500,
                            "recommended_storage": "EFS",
                            "access_pattern": "General Purpose",
                            "monthly_cost": 50,
                            "annual_cost": 600,
                            "optimization_notes": "Basic estimation - requires detailed analysis"
                        } for i in range(len(file_shares))
                    ]
                },
                "total_monthly_cost": total_monthly,
                "total_annual_cost": total_annual
            },
            "migration_services": {
                "total_professional_services_cost": migration_cost,
                "resource_breakdown": [
                    {
                        "role": "Cloud Architect",
                        "rate_per_hour": 150,
                        "hours_per_week": 20,
                        "duration_weeks": 4,
                        "total_hours": 80,
                        "total_cost": migration_cost * 0.6
                    },
                    {
                        "role": "Migration Specialist",
                        "rate_per_hour": 125,
                        "hours_per_week": 20,
                        "duration_weeks": 4,
                        "total_hours": 80,
                        "total_cost": migration_cost * 0.4
                    }
                ]
            },
            "ai_insights": {
                "confidence_level": 0.65,
                "cost_optimization_tips": [
                    "Consider reserved instances for 20-72% savings",
                    "Use auto-scaling to optimize costs",
                    "Implement S3 Intelligent Tiering for storage",
                    "Right-size instances based on actual usage"
                ],
                "potential_savings": {
                    "percentage": 25,
                    "annual_amount": total_annual * 0.25
                },
                "recommendations": [
                    "Detailed assessment needed for accurate pricing",
                    "Consider phased migration approach",
                    "Implement cost monitoring from day one"
                ],
                "ai_model_used": "fallback",
                "fallback_used": True
            }
        }

    def _fallback_migration_strategy(self, infrastructure_data: Dict[str, Any], cloud_provider: str, complexity: str) -> Dict[str, Any]:
        """Fallback migration strategy when AI is not available"""
        servers = infrastructure_data.get('servers', [])
        databases = infrastructure_data.get('databases', [])
        file_shares = infrastructure_data.get('file_shares', [])
        
        total_components = len(servers) + len(databases) + len(file_shares)
        duration_weeks = max(8, total_components * 2)
        
        return {
            "migration_approach": {
                "overall_strategy": "Lift and Shift",
                "estimated_duration": f"{duration_weeks} weeks",
                "complexity_level": complexity.title(),
                "rationale": f"Based on {total_components} components requiring migration"
            },
            "component_strategies": {
                "servers": [
                    {
                        "server_id": f"Server-{i+1}",
                        "migration_type": "Rehost (Lift and Shift)",
                        "current_state": "On-premise server",
                        "target_state": "AWS EC2 instance",
                        "complexity": "Medium",
                        "estimated_effort": "4-8 hours",
                        "rationale": "Standard lift and shift approach"
                    } for i in range(len(servers))
                ],
                "databases": [
                    {
                        "db_name": f"Database-{i+1}",
                        "current_engine": "MySQL",
                        "target_engine": "RDS MySQL",
                        "migration_type": "Database Migration Service",
                        "approach": "Online migration with minimal downtime",
                        "complexity": "Medium",
                        "data_migration_strategy": "Initial sync + CDC",
                        "downtime_estimate": "1-2 hours"
                    } for i in range(len(databases))
                ],
                "storage": [
                    {
                        "share_name": f"FileShare-{i+1}",
                        "current_type": "Windows File Share",
                        "target_type": "Amazon FSx",
                        "migration_method": "AWS DataSync",
                        "sync_strategy": "Initial copy + incremental sync",
                        "cutover_approach": "DNS cutover"
                    } for i in range(len(file_shares))
                ]
            },
            "migration_phases": [
                {
                    "phase": 1,
                    "name": "Assessment & Planning",
                    "duration": "4 weeks",
                    "components": ["Infrastructure Discovery", "Dependency Mapping", "Risk Assessment"],
                    "dependencies": [],
                    "risks": ["Incomplete inventory", "Missing dependencies"],
                    "success_criteria": ["Complete infrastructure catalog", "Migration plan approved"]
                },
                {
                    "phase": 2,
                    "name": "Foundation Setup",
                    "duration": "3 weeks",
                    "components": ["AWS Account Setup", "Network Configuration", "Security Baseline"],
                    "dependencies": ["Phase 1"],
                    "risks": ["Network connectivity", "Security compliance"],
                    "success_criteria": ["Landing zone ready", "Security controls validated"]
                },
                {
                    "phase": 3,
                    "name": "Data Migration",
                    "duration": f"{max(4, len(databases) * 2)} weeks",
                    "components": ["Database Migration", "File Share Migration", "Data Validation"],
                    "dependencies": ["Phase 2"],
                    "risks": ["Data corruption", "Extended sync time"],
                    "success_criteria": ["Data sync established", "Validation complete"]
                },
                {
                    "phase": 4,
                    "name": "Application Migration",
                    "duration": f"{max(4, len(servers) * 1)} weeks",
                    "components": ["Server Migration", "Application Testing", "Performance Tuning"],
                    "dependencies": ["Phase 2", "Phase 3"],
                    "risks": ["Application compatibility", "Performance issues"],
                    "success_criteria": ["Applications operational", "Performance validated"]
                },
                {
                    "phase": 5,
                    "name": "Cutover & Validation",
                    "duration": "2 weeks",
                    "components": ["Production Cutover", "User Acceptance Testing", "Go-Live Support"],
                    "dependencies": ["Phase 4"],
                    "risks": ["User adoption", "Rollback scenarios"],
                    "success_criteria": ["Production stable", "Users trained", "Support documented"]
                }
            ],
            "recommendations": {
                "quick_wins": [
                    "Start with non-critical systems for proof of concept",
                    "Implement AWS cost optimization tools early",
                    "Establish monitoring and alerting from day one"
                ],
                "cost_optimization": [
                    "Right-size instances based on actual usage",
                    "Implement reserved instances for predictable workloads",
                    "Use spot instances for development environments"
                ],
                "performance_improvements": [
                    "Leverage AWS-native services for better performance",
                    "Implement CDN for web applications",
                    "Optimize database configurations for cloud environment"
                ],
                "modernization_opportunities": [
                    "Consider containerization for legacy applications",
                    "Implement auto-scaling for variable workloads",
                    "Evaluate serverless options for specific functions"
                ]
            },
            "risk_assessment": {
                "high_risks": [
                    "Data loss during migration",
                    "Extended downtime during cutover",
                    "Application compatibility issues"
                ],
                "medium_risks": [
                    "Network performance degradation",
                    "User training requirements",
                    "Cost overruns"
                ],
                "low_risks": [
                    "Minor configuration adjustments",
                    "Documentation updates",
                    "Monitoring setup"
                ],
                "mitigation_strategies": {
                    "Data loss": "Implement comprehensive backup and validation procedures",
                    "Extended downtime": "Plan rollback procedures and conduct dress rehearsals",
                    "Application compatibility": "Thorough testing in staging environment"
                }
            },
            "ai_insights": {
                "confidence_level": 0.70,
                "ai_model_used": "fallback",
                "fallback_used": True,
                "strategic_recommendations": [
                    "Consider phased approach to minimize risk",
                    "Invest in team training for cloud technologies",
                    "Establish cloud governance early"
                ]
            }
        }
