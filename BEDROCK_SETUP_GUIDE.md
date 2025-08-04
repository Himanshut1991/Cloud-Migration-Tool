# Setting Up AWS Bedrock for Real AI Recommendations

## Step 1: AWS Account Setup
1. **Create AWS Account** (if you don't have one)
2. **Navigate to AWS Bedrock Console**
3. **Request Model Access**:
   - Go to "Model access" in Bedrock console
   - Request access to "Anthropic Claude 3 Sonnet"
   - Wait for approval (usually instant for most accounts)

## Step 2: Create IAM User
1. **Go to IAM Console**
2. **Create New User**:
   - Username: `bedrock-migration-tool`
   - Access type: Programmatic access
3. **Attach Policy**:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "bedrock:InvokeModel",
           "bedrock:ListModels",
           "bedrock:GetModel"
         ],
         "Resource": "*"
       }
     ]
   }
   ```
4. **Save Access Key & Secret Key**

## Step 3: Configure Environment
1. **Copy environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit .env file** with your credentials:
   ```bash
   # AWS Configuration for Bedrock
   AWS_REGION=us-east-1
   AWS_ACCESS_KEY_ID=AKIA...your-actual-key
   AWS_SECRET_ACCESS_KEY=your-actual-secret-key
   ```

## Step 4: Test the Integration
1. **Restart the backend server**
2. **Check logs** for "Bedrock connection successful"
3. **Test API**: `GET /api/cost-estimation`
4. **Verify AI insights** in the response

## Cost Considerations
- **Claude 3 Sonnet Pricing**: ~$15 per 1M input tokens
- **Typical Usage**: ~500-1000 tokens per recommendation
- **Estimated Cost**: $0.01-0.02 per full cost analysis
- **Monthly Usage**: For 100 analyses = ~$1-2/month

## Security Best Practices
1. **Use IAM roles** instead of access keys when possible
2. **Rotate keys regularly**
3. **Monitor usage** in AWS CloudWatch
4. **Set billing alerts** to avoid unexpected charges
5. **Use least privilege principle** for IAM permissions

## Troubleshooting
- **"Model not available"**: Request access in Bedrock console
- **"Credentials not found"**: Check .env file configuration
- **"Access denied"**: Verify IAM permissions
- **"Region not supported"**: Try us-east-1 or us-west-2
