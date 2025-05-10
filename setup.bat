@echo off
REM set current directory
set DIR=%~dp0
cd /d %DIR%

REM install libs
"python.exe" -m venv venv
call .\venv\Scripts\activate.bat

REM add .gitignore file
cd /d %DIR%
echo. > .gitignore
echo venv/ >> .gitignore

pause