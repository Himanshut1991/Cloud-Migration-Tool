#!/usr/bin/env python3

import os
import sys
import json
import boto3
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Simple test to check Claude 3.5 Sonnet access
def check_claude_access():
    print(f"🕐 {datetime.now().strftime('%H:%M:%S')} - Checking Claude 3.5 Sonnet access...")
    
    try:
        # Test with hardcoded values from .env
        client = boto3.client(
            'bedrock-runtime',
            region_name='us-east-1',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        
        # Test Claude 3.5 Sonnet specifically
        model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 50,
            "messages": [
                {
                    "role": "user", 
                    "content": "Respond with exactly: 'Claude 3.5 Sonnet is working'"
                }
            ]
        }
        
        print(f"🧪 Testing model: {model_id}")
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(body)
        )
        
        result = json.loads(response['body'].read())
        response_text = result['content'][0]['text'].strip()
        
        print(f"✅ SUCCESS! Response: {response_text}")
        
        # Check if we got the expected response
        if "Claude 3.5 Sonnet is working" in response_text:
            print("🎉 Claude 3.5 Sonnet is fully functional!")
            return True
        else:
            print("⚠️  Claude responded but not as expected")
            return True  # Still working, just different response
            
    except Exception as e:
        error_str = str(e)
        print(f"❌ ERROR: {error_str}")
        
        # Check for specific error types
        if "ValidationException" in error_str:
            print("🔍 This looks like a model access issue")
        elif "UnauthorizedOperation" in error_str or "AccessDenied" in error_str:
            print("🔍 This looks like a permissions issue")
        elif "throttling" in error_str.lower():
            print("🔍 This looks like a rate limiting issue")
        else:
            print("🔍 This looks like a general API/configuration issue")
            
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 CLAUDE 3.5 SONNET ACCESS TEST")
    print("=" * 60)
    
    success = check_claude_access()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ RESULT: Claude 3.5 Sonnet is accessible!")
        print("   The AI service should be working now.")
    else:
        print("❌ RESULT: Claude 3.5 Sonnet is NOT accessible")
        print("   Check model access in AWS Bedrock console.")
    print("=" * 60)
