@echo off
REM set current directory
set DIR=%~dp0
cd /d %DIR%

REM install libs
"python.exe" -m venv venv
call .\venv\Scripts\activate.bat
pip install pynput pyautogui wmi screen-brightness-control

REM add .gitignore file
cd /d %DIR%
echo. > .gitignore
echo venv/ >> .gitignore

pause