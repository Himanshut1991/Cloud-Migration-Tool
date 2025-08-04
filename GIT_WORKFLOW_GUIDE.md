# Git Workflow Guide

## Problem: Push Rejected Due to Repository Rules

The repository `https://github.com/Himanshut1991/Cloud-Migration-Tool.git` has branch protection rules that prevent direct pushes to the `main` branch.

## Solution: Feature Branch Workflow

### Step 1: Install Git (if not already installed)
- Download from: https://git-scm.com/download/win
- Install with default settings
- Restart VS Code/Terminal

### Step 2: Create Feature Branch
```bash
# Navigate to project directory
cd "c:\Users\2313274\Cloud Migration Tool"

# Create and switch to new branch
git checkout -b feature/ai-integration-complete

# Or use a different branch name like:
# git checkout -b feature/cost-estimation
# git checkout -b feature/migration-strategy
```

### Step 3: Stage and Commit Changes
```bash
# Add all changes
git add .

# Commit with descriptive message
git commit -m "feat: Complete AI integration with AWS Bedrock

- Add comprehensive AI-powered cost estimation
- Implement migration strategy recommendations
- Fix TypeScript errors in frontend components
- Add comprehensive .gitignore file
- Include AWS Bedrock setup documentation"
```

### Step 4: Push Feature Branch
```bash
# Push new branch to GitHub
git push -u origin feature/ai-integration-complete
```

### Step 5: Create Pull Request
1. Go to: https://github.com/Himanshut1991/Cloud-Migration-Tool
2. Click "Compare & pull request" button
3. Add title: "Complete AI Integration with AWS Bedrock"
4. Add description of changes
5. Click "Create pull request"

### Step 6: Merge (after review)
1. Review the changes
2. Click "Merge pull request"
3. Choose "Squash and merge" if you want clean history
4. Delete the feature branch after merging

## Alternative: VS Code Git Integration

If command line doesn't work:

1. **Open Source Control**: `Ctrl+Shift+G`
2. **Create Branch**: Click branch name at bottom → "Create new branch"
3. **Name Branch**: `feature/ai-integration-complete`
4. **Stage Files**: Click `+` next to each file
5. **Commit**: Enter message and click "Commit"
6. **Publish Branch**: Click "Publish Branch" button

## Best Practices

- **Never push directly to main**: Use feature branches
- **Use descriptive commit messages**: Include what was changed and why
- **Keep branches focused**: One feature/fix per branch
- **Review before merging**: Use pull requests for code review

## Current Status

✅ Project is ready with:
- Complete AI integration (AWS Bedrock + Claude 3 Sonnet)
- Working cost estimation with AI insights
- Migration strategy recommendations
- Fixed TypeScript errors
- Comprehensive .gitignore file
- Documentation and setup guides
