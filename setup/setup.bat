@echo off
cd /d %~dp0\..

if not exist setup\config.json (
  copy setup\config.example.json setup\config.json
  echo.
  echo Created setup\config.json from setup\config.example.json
  echo Edit setup\config.json, then run setup.bat again.
  pause
  exit /b 0
)

python setup\setup.py
pause
