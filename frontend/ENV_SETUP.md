# Frontend Environment Setup

## Create .env File

Create a file named `.env` in the `frontend` directory with this content:

```
REACT_APP_API_URL=http://localhost:5000/api
```

## Steps:

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Create `.env` file:
   - **Windows PowerShell:**
     ```powershell
     echo "REACT_APP_API_URL=http://localhost:5000/api" > .env
     ```
   
   - **Or manually:**
     - Create a new file named `.env` (no extension)
     - Add: `REACT_APP_API_URL=http://localhost:5000/api`
     - Save the file

3. Restart React app:
   - Stop the React app (Ctrl+C)
   - Start again: `npm start`

## Verify

After creating `.env` and restarting, check browser console - it should connect to `http://localhost:5000/api`
