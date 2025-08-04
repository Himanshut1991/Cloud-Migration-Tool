# Cloud Migration Tool - Startup Guide

## 🚀 Quick Start

### Option 1: Using Batch Files (Recommended)
1. **Backend**: Double-click `start_backend.bat` in the project root
2. **Frontend**: Double-click `start_frontend.bat` in the project root

### Option 2: Manual Command Line
```powershell
# Terminal 1 - Backend
cd "c:\Users\2313274\Cloud Migration Tool\backend"
python app.py

# Terminal 2 - Frontend  
cd "c:\Users\2313274\Cloud Migration Tool\frontend"
npm run dev
```

### Option 3: VS Code Tasks
1. Press `Ctrl+Shift+P`
2. Type "Tasks: Run Task" 
3. Select "Start Backend Server"

## 🔗 Access URLs

- **Frontend**: http://localhost:3000 (React App)
- **Backend API**: http://localhost:5000 (Flask API)
- **AI Status**: http://localhost:5000/api/ai-status

## ✅ Verification Steps

1. **Backend Running**: Check http://localhost:5000/api/ai-status
   - Should show: `"ai_enabled": true`
   - Model: `anthropic.claude-3-sonnet-20240229-v1:0`

2. **Frontend Running**: Check http://localhost:3000
   - Should load the Cloud Migration Tool dashboard

3. **Full Integration**: 
   - Navigate to Analysis > Cost Estimation
   - Click "Calculate Costs" 
   - Should see AI-powered recommendations

## 🔧 Troubleshooting

### Backend Issues
- **Port 5000 in use**: Stop other Flask apps or change port in `app.py`
- **Python not found**: Ensure Python 3.7+ is installed and in PATH
- **Missing packages**: Run `pip install -r requirements.txt` in backend folder
- **AWS credentials**: Check `.env` file has valid AWS keys

### Frontend Issues  
- **Port 3000 in use**: Frontend will auto-assign next available port
- **Node not found**: Install Node.js 16+ from nodejs.org
- **Dependencies missing**: Run `npm install` in frontend folder
- **Build errors**: Check TypeScript errors in terminal output

### Network Issues
- **CORS errors**: Backend includes CORS headers for localhost:3000
- **API connection failed**: Ensure backend is running on port 5000
- **Firewall**: Allow Python and Node through Windows Firewall

## 📊 Features to Test

1. **Dashboard**: Real-time metrics and inventory summary
2. **Inventory**: CRUD operations for servers, databases, file shares
3. **Configuration**: Cloud preferences, business constraints, resource rates
4. **Analysis**: AI-powered cost estimation and migration strategy
5. **AI Integration**: AWS Bedrock with Claude 3 Sonnet model

## 🔑 Environment Variables

Backend requires these in `.env` file:
```
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
SECRET_KEY=your-flask-secret-key
```

## 📝 Development Status

✅ **Working Features**:
- Full CRUD for all inventory types
- Real-time dashboard updates  
- AI-powered cost estimation
- Migration strategy recommendations
- AWS Bedrock integration (Claude 3 Sonnet)
- Professional services cost calculation

🔄 **In Development**:
- Timeline visualization
- Export to PDF/Excel/Word
- Advanced reporting features

## 💡 Tips

- **Use Chrome/Edge**: Best compatibility with React DevTools
- **Check Console**: F12 → Console for any JavaScript errors  
- **Monitor Network**: F12 → Network to see API calls
- **Use Incognito**: If seeing cached/stale data

---

**Need Help?** Check the logs in both terminal windows for detailed error messages.
