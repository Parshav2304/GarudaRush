@echo off
title GarudaRush Agent (Real Capture)
color 0C

REM Check if config.json exists
if not exist "config.json" (
    echo [ERROR] config.json not found!
    echo.
    echo Please run setup-config.bat first to create config.json
    echo.
    pause
    exit /b
)

echo Reading credentials from config.json...

REM Read values from config.json
for /f "tokens=2 delims=:," %%a in ('findstr "email" config.json') do set EMAIL=%%a
for /f "tokens=2 delims=:," %%a in ('findstr "password" config.json') do set PASSWORD=%%a
for /f "tokens=2 delims=:," %%a in ('findstr "agent_id" config.json') do set AGENT_ID=%%a
for /f "tokens=2 delims=:," %%a in ('findstr "interface" config.json') do set INTERFACE=%%a

REM Clean up the values
set EMAIL=%EMAIL:"=%
set EMAIL=%EMAIL: =%
set PASSWORD=%PASSWORD:"=%
set PASSWORD=%PASSWORD: =%
set AGENT_ID=%AGENT_ID:"=%
set AGENT_ID=%AGENT_ID: =%
set INTERFACE=%INTERFACE:"=%
set INTERFACE=%INTERFACE: =%

echo.
echo Starting Real Agent: %AGENT_ID%
echo Interface: %INTERFACE%
echo.
echo NOTE: This requires Wireshark to be installed!
echo.

cd /d %~dp0backend
call venv\Scripts\activate
python agent.py --agent-id %AGENT_ID% --interface "%INTERFACE%" --api-url http://localhost:5000/api --username %EMAIL% --password %PASSWORD%

pause
