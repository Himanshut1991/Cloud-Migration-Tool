#!/usr/bin/env python3
"""Test script to debug AWS Bedrock connection"""

import boto3
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_bedrock_connection():
    """Test Bedrock connection with detailed error reporting"""
    try:
        print("Testing AWS Bedrock Connection...")
        print(f"AWS Region: {os.getenv('AWS_REGION')}")
        print(f"AWS Access Key ID: {os.getenv('AWS_ACCESS_KEY_ID')[:10]}..." if os.getenv('AWS_ACCESS_KEY_ID') else "No Access Key")
        print(f"AWS Secret Key: {'Set' if os.getenv('AWS_SECRET_ACCESS_KEY') else 'Not Set'}")
        
        # Initialize Bedrock client
        bedrock_client = boto3.client(
            'bedrock-runtime',
            region_name=os.getenv('AWS_REGION', 'us-east-1'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        
        print("Bedrock client created successfully")
        
        # Test model access
        model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
        
        test_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 50,
            "messages": [{"role": "user", "content": "Hello, can you respond with 'Connection successful'?"}]
        }
        
        print(f"Testing model: {model_id}")
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps(test_body)
        )
        
        response_body = json.loads(response['body'].read())
        print("SUCCESS: Bedrock connection working!")
        print(f"Response: {response_body}")
        return True
        
    except Exception as e:
        print(f"ERROR: Bedrock connection failed: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Additional debugging
        if "AccessDeniedException" in str(e):
            print("Access denied - check IAM permissions for Bedrock")
        elif "ValidationException" in str(e):
            print("Validation error - check model availability in region")
        elif "ResourceNotFoundException" in str(e):
            print("Resource not found - model may not be available in this region")
        elif "UnauthorizedOperation" in str(e):
            print("Unauthorized - check AWS credentials")
        
        return False

if __name__ == "__main__":
    test_bedrock_connection()
