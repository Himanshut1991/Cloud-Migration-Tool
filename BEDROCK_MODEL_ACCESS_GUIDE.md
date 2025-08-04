# AWS Bedrock Model Access Setup Guide

## Overview
AWS Bedrock requires explicit model access to be granted before you can use foundation models. By default, most models are not accessible even with proper IAM permissions.

## Steps to Enable Model Access

### 1. Access AWS Console
1. Log in to the AWS Console
2. Navigate to the **Amazon Bedrock** service
3. Make sure you're in the correct region (us-east-1 recommended)

### 2. Request Model Access
1. In the Bedrock console, go to **Model access** in the left sidebar
2. Click **Request model access** or **Manage model access**
3. You'll see a list of all available foundation models

### 3. Enable Recommended Models
For this migration tool, we recommend enabling these models in order of priority:

#### High Priority (Choose at least one):
- **Anthropic Claude 3 Haiku** (`anthropic.claude-3-haiku-20240307-v1:0`)
  - Fast and cost-effective
  - Good for structured analysis
  - Usually approved quickly

- **Amazon Nova Lite** (`amazon.nova-lite-v1:0`)
  - Amazon's newest lightweight model
  - Fast approval as it's Amazon's own model
  - Good performance for migration analysis

#### Medium Priority:
- **Anthropic Claude 3.5 Sonnet** (`anthropic.claude-3-5-sonnet-20240620-v1:0`)
  - Better reasoning capabilities
  - More detailed analysis
  - May require business justification

- **Amazon Titan Text Express** (`amazon.titan-text-express-v1`)
  - Amazon's proven text model
  - Reliable and cost-effective
  - Usually approved quickly

### 4. Submit Access Request
1. Select the models you want to access
2. For each model, you may need to provide:
   - **Use case description**: "Cloud migration planning and cost estimation tool"
   - **Expected usage**: "Moderate - analyzing server configurations and providing migration recommendations"
   - **Business justification**: "Internal tool for pre-sales and migration planning activities"

3. Click **Request model access**

### 5. Wait for Approval
- **Amazon models**: Usually approved within minutes to hours
- **Third-party models (Anthropic, etc.)**: May take 1-3 business days
- You'll receive email notifications when access is granted

### 6. Verify Access
Once approved, you can verify access by running our test script:

```bash
cd backend
python test_bedrock.py
```

## Alternative: Use Free Tier Models
If you're on AWS Free Tier or want to minimize costs, start with:
1. **Amazon Nova Lite** - New and free tier eligible
2. **Amazon Titan Text Express** - Reliable and cost-effective

## Troubleshooting

### Common Issues:

#### "AccessDeniedException: You don't have access to the model"
- **Solution**: The model hasn't been enabled in Bedrock console
- **Action**: Follow steps 1-4 above to request access

#### "ValidationException: The model ID is not valid"
- **Solution**: Model may not be available in your region
- **Action**: Try a different region or different model

#### "ResourceNotFoundException: The request failed"
- **Solution**: Bedrock service may not be available in your region
- **Action**: Switch to us-east-1, us-west-2, or eu-west-1

### IAM Permissions Required:
Your AWS user/role needs these permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:ListFoundationModels"
            ],
            "Resource": "*"
        }
    ]
}
```

## Cost Considerations
- **Nova Lite**: ~$0.0002 per 1K input tokens
- **Titan Text Express**: ~$0.0008 per 1K tokens
- **Claude 3 Haiku**: ~$0.00025 per 1K input tokens

For typical migration analysis (1000 servers), expect $5-20 in AI costs.

## Fallback Mode
If no models are accessible, the tool automatically falls back to rule-based recommendations. You'll see:
- ✅ Rule-based recommendations (still useful!)
- ⚠️ "AI Unavailable - Using Fallback" status
- All functionality still works, just without AI insights

## Support
If you continue having issues after following this guide:
1. Check AWS CloudTrail logs for detailed error messages
2. Contact your AWS administrator for account-level permissions
3. Consider using the rule-based fallback mode while resolving access issues
