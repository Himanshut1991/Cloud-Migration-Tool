#!/usr/bin/env python3

import json
import boto3
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SimpleAIService:
    """Simplified AI service focused on Claude 3.5 Sonnet only"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        console.setFormatter(formatter)
        self.logger.addHandler(console)
        self.logger.setLevel(logging.INFO)
        
        self.client = None
        self.model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Bedrock client"""
        try:
            self.logger.info("🚀 Initializing Bedrock client...")
            
            self.client = boto3.client(
                'bedrock-runtime',
                region_name='us-east-1',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )
            
            # Test the connection
            if self._test_connection():
                self.logger.info("✅ Bedrock client initialized successfully!")
            else:
                self.logger.error("❌ Bedrock client test failed")
                self.client = None
                
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Bedrock client: {e}")
            self.client = None
    
    def _test_connection(self):
        """Test if we can connect to Claude 3.5 Sonnet"""
        if not self.client:
            return False
        
        try:
            self.logger.info(f"🧪 Testing connection to {self.model_id}")
            
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 20,
                "messages": [{"role": "user", "content": "Hello"}]
            }
            
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body)
            )
            
            result = json.loads(response['body'].read())
            response_text = result['content'][0]['text']
            
            self.logger.info(f"✅ Test successful! Claude responded: {response_text}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Connection test failed: {e}")
            return False
    
    def get_recommendation(self, prompt):
        """Get a recommendation from Claude"""
        if not self.client:
            return {"error": "AI service not available", "fallback": True}
        
        try:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1
            }
            
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body)
            )
            
            result = json.loads(response['body'].read())
            response_text = result['content'][0]['text']
            
            return {"response": response_text, "success": True}
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get recommendation: {e}")
            return {"error": str(e), "fallback": True}
    
    def is_available(self):
        """Check if AI service is available"""
        return self.client is not None

def test_simple_ai():
    """Test the simple AI service"""
    print("🧪 Testing Simple AI Service...")
    
    ai = SimpleAIService()
    
    if ai.is_available():
        print("✅ AI Service is available!")
        
        # Test a simple recommendation
        result = ai.get_recommendation("What's the best EC2 instance for a web server?")
        
        if result.get('success'):
            print("✅ AI recommendation successful!")
            print(f"Response: {result['response'][:100]}...")
        else:
            print(f"❌ AI recommendation failed: {result}")
    else:
        print("❌ AI Service is not available")

if __name__ == "__main__":
    test_simple_ai()
