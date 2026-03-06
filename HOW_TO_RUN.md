# 🚀 How to Run Both Backend and Frontend

## Method 1: Using Batch Script (Easiest - Windows)

### Option A: Run Both Automatically
1. Double-click `start-all.bat`
2. Two windows will open:
   - One for Backend (port 5000)
   - One for Frontend (port 3000)
3. Wait for both to start
4. Open browser: `http://localhost:3000`

### Option B: Run Separately
1. Double-click `start-backend.bat` (opens Backend)
2. Double-click `start-frontend.bat` (opens Frontend)

## Method 2: Using PowerShell Script

1. Right-click `start-all.ps1`
2. Select "Run with PowerShell"
3. If you get an execution policy error, run this first:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
4. Then run: `.\start-all.ps1`

## Method 3: Manual (Two Terminal Windows)

### Terminal Window 1 - Backend:
```bash
cd backend
venv\Scripts\activate
python app.py
```

### Terminal Window 2 - Frontend:
```bash
cd frontend
npm start
```

## Method 4: Using VS Code (Recommended for Development)

1. Open VS Code in the project root
2. Install "Terminal Tabs" extension (optional)
3. Open two terminals:
   - Terminal 1: `cd backend && venv\Scripts\activate && python app.py`
   - Terminal 2: `cd frontend && npm start`

## Quick Start Checklist

- [ ] MongoDB is running
- [ ] Backend server started (port 5000)
- [ ] Frontend server started (port 3000)
- [ ] Browser opens to `http://localhost:3000`

## Stopping the Servers

- **Backend**: Press `Ctrl+C` in the backend terminal
- **Frontend**: Press `Ctrl+C` in the frontend terminal
- **Or**: Close the terminal windows

## Troubleshooting

### Port Already in Use?
- Backend (5000): Change `PORT=5001` in `backend/.env`
- Frontend (3000): It will ask to use a different port automatically

### MongoDB Not Connected?
- Start MongoDB service first
- Then start the backend

### Frontend Can't Connect?
- Make sure backend is running first
- Check `frontend/.env` has: `REACT_APP_API_URL=http://localhost:5000/api`
- Restart frontend after creating `.env`

## Expected Output

### Backend Terminal:
```
✓ MongoDB connection established
╔═══════════════════════════════════════╗
║     🦅 GarudaRush Backend Started     ║
║                                       ║
║  Port: 5000                          ║
║  Debug: True                         ║
║  MongoDB: Connected                  ║
╚═══════════════════════════════════════╝
```

### Frontend Terminal:
```
Compiled successfully!

You can now view garudarush-frontend in the browser.

  Local:            http://localhost:3000
```
