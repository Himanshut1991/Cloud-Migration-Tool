@echo off
echo Setting up Git workflow for Cloud Migration Tool
echo.

echo Step 1: Check if Git is installed
git --version
if %errorlevel% neq 0 (
    echo Git is not installed. Please install Git from https://git-scm.com/download/win
    pause
    exit /b 1
)

echo.
echo Step 2: Check current branch
git branch --show-current

echo.
echo Step 3: Create and switch to feature branch
set /p branch_name="Enter branch name (e.g., feature/ai-integration): "
git checkout -b %branch_name%

echo.
echo Step 4: Add all changes
git add .

echo.
echo Step 5: Commit changes
set /p commit_msg="Enter commit message: "
git commit -m "%commit_msg%"

echo.
echo Step 6: Push feature branch
git push -u origin %branch_name%

echo.
echo Success! Now you can create a Pull Request on GitHub.
echo Go to: https://github.com/Himanshut1991/Cloud-Migration-Tool
echo.
pause
