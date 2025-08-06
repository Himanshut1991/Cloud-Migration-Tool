#!/usr/bin/env python3
"""Direct Bedrock connection test"""

import os
import boto3
import json
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
print("Environment variables loaded")

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_direct_bedrock():
    """Test Bedrock directly"""
    print("🧪 Testing direct Bedrock connection...")
    
    # Check environment variables
    print(f"AWS_REGION: {os.getenv('AWS_REGION')}")
    print(f"AWS_ACCESS_KEY_ID: {os.getenv('AWS_ACCESS_KEY_ID')[:10]}..." if os.getenv('AWS_ACCESS_KEY_ID') else "AWS_ACCESS_KEY_ID: Not set")
    print(f"AWS_SECRET_ACCESS_KEY: {'Set' if os.getenv('AWS_SECRET_ACCESS_KEY') else 'Not set'}")
    print(f"BEDROCK_MODEL_ID: {os.getenv('BEDROCK_MODEL_ID')}")
    
    try:
        # Initialize Bedrock client
        bedrock_client = boto3.client(
            'bedrock-runtime',
            region_name=os.getenv('AWS_REGION', 'us-east-1'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        print("✅ Bedrock client created")
        
        # List of models to try in your preferred order
        models_to_try = [
            "anthropic.claude-3-5-sonnet-20240620-v1:0",  # 1. Claude 3.5 Sonnet
            "anthropic.claude-3-sonnet-20240229-v1:0",    # 2. Claude 3 Sonnet  
            "amazon.titan-text-express-v1"                # 3. Titan Text G1 - Express
        ]
        
        working_model = None
        
        for model_id in models_to_try:
            try:
                print(f"\n🧪 Testing model: {model_id}")
                
                if "anthropic" in model_id:
                    # Anthropic models use messages format
                    test_body = {
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 10,
                        "messages": [{"role": "user", "content": "Hello, can you respond with just 'OK'?"}]
                    }
                elif "titan" in model_id:
                    # Titan models use different format
                    test_body = {
                        "inputText": "Hello, can you respond with just 'OK'?",
                        "textGenerationConfig": {
                            "maxTokenCount": 10,
                            "temperature": 0.1
                        }
                    }
                else:
                    print(f"⚠️  Unknown model format for {model_id}")
                    continue
                
                # Try to invoke the model
                response = bedrock_client.invoke_model(
                    modelId=model_id,
                    body=json.dumps(test_body)
                )
                
                # Parse response
                response_body = json.loads(response['body'].read())
                print(f"✅ Model {model_id} responded successfully!")
                print(f"Response: {response_body}")
                
                working_model = model_id
                break
                
            except Exception as e:
                print(f"❌ Model {model_id} failed: {e}")
                if "ValidationException" in str(e):
                    print("   This model might need to be enabled in AWS Bedrock console")
                elif "AccessDenied" in str(e):
                    print("   Access denied - check IAM permissions")
                continue
        
        if working_model:
            print(f"\n🎉 SUCCESS! Working model found: {working_model}")
        else:
            print(f"\n❌ FAILED! No models are accessible")
            print("\nPossible solutions:")
            print("1. Enable models in AWS Bedrock console")
            print("2. Check IAM permissions")
            print("3. Verify AWS credentials")
            
    except Exception as e:
        print(f"❌ Bedrock client initialization failed: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_bedrock()
