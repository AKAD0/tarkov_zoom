@echo off
REM set current directory
set DIR=%~dp0
cd /d %DIR%


call .\venv\Scripts\activate.bat
"python.exe" ".\script2.py"
pause