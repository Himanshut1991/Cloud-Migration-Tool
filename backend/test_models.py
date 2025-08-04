#!/usr/bin/env python3
"""Test available Bedrock models"""

import boto3
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_available_models():
    """Test which models are available"""
    try:
        # Initialize Bedrock client
        bedrock_client = boto3.client(
            'bedrock',  # Use bedrock, not bedrock-runtime for listing models
            region_name=os.getenv('AWS_REGION', 'us-east-1'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        
        print("Listing available foundation models...")
        response = bedrock_client.list_foundation_models()
        
        available_models = []
        for model in response['modelSummaries']:
            if model['modelLifecycle']['status'] == 'ACTIVE':
                available_models.append({
                    'modelId': model['modelId'],
                    'modelName': model['modelName'],
                    'providerName': model['providerName'],
                    'inputModalities': model['inputModalities'],
                    'outputModalities': model['outputModalities']
                })
        
        print(f"Found {len(available_models)} active models:")
        for model in available_models:
            print(f"  - {model['modelId']} ({model['providerName']}: {model['modelName']})")
            
        return available_models
        
    except Exception as e:
        print(f"ERROR listing models: {e}")
        return []

def test_simple_model():
    """Test with Amazon Titan Text model which should be more readily available"""
    try:
        bedrock_runtime = boto3.client(
            'bedrock-runtime',
            region_name=os.getenv('AWS_REGION', 'us-east-1'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        
        # Try Amazon Titan Text model
        model_id = "amazon.titan-text-express-v1"
        
        test_body = {
            "inputText": "Hello, can you respond with 'Connection successful'?",
            "textGenerationConfig": {
                "maxTokenCount": 50,
                "temperature": 0.1
            }
        }
        
        print(f"Testing model: {model_id}")
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(test_body)
        )
        
        response_body = json.loads(response['body'].read())
        print("SUCCESS: Bedrock connection working with Titan!")
        print(f"Response: {response_body}")
        return True
        
    except Exception as e:
        print(f"ERROR with Titan model: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Available Models ===")
    available = test_available_models()
    
    print("\n=== Testing Simple Model ===")
    test_simple_model()
