import boto3
import json
import logging
import os
from typing import Dict, List, Any

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
            
            # Test if Bedrock is available
            self._test_bedrock_connection()
            
        except Exception as e:
            self.logger.warning(f"Bedrock client initialization failed: {e}")
            self.bedrock_client = None
    
    def _test_bedrock_connection(self):
        """Test if Bedrock connection is working"""
        if not self.bedrock_client:
            return False
        
        # List of models to try in order of preference
        models_to_try = [
            "anthropic.claude-3-haiku-20240307-v1:0",  # More likely to be enabled by default
            "anthropic.claude-3-5-sonnet-20240620-v1:0",  # Newer Sonnet
            "anthropic.claude-3-sonnet-20240229-v1:0",  # Original Sonnet
            "amazon.titan-text-express-v1",  # Amazon's own model
            "amazon.nova-lite-v1:0"  # Newest Amazon model
        ]
        
        for model_id in models_to_try:
            try:
                self.logger.info(f"Testing model: {model_id}")
                
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
                elif "nova" in model_id:
                    # Nova models use messages format
                    test_body = {
                        "messages": [{"role": "user", "content": "test"}],
                        "inferenceConfig": {"maxTokens": 10}
                    }
                else:
                    continue
                
                self.bedrock_client.invoke_model(
                    modelId=model_id,
                    body=json.dumps(test_body)
                )
                
                # If successful, update our model_id and return
                self.model_id = model_id
                self.logger.info(f"Bedrock connection successful with model: {model_id}")
                return True
                
            except Exception as e:
                self.logger.warning(f"Model {model_id} failed: {e}")
                continue
        
        # If all models failed
        self.logger.warning("No Bedrock models are accessible. Models may need to be enabled in AWS console.")
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
            return self._parse_ai_response(response, 'server')
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
                return json.loads(json_str)
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
            "confidence_level": "medium"
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
