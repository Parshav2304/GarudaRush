@echo off
title GarudaRush Backend
cd /d %~dp0backend
call venv\Scripts\activate
python app.py
pause
