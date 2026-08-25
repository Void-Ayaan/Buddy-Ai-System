@echo off
title BUDDY AI - 1-CLICK AUTOMATED SETUP PROTOCOL
cls

echo ===================================================
echo   BUDDY AI - 1-CLICK AUTOMATED SETUP PROTOCOL
echo ===================================================
echo.

echo [ 1/2 ] Installing Python Dependencies from requirements.txt...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [ 2/2 ] Verifying & Auto-Downloading Local GGUF LLM Model...
python tools/model_downloader.py

echo.
echo ===================================================
echo   ✓ BUDDY AI SYSTEM FULLY INSTALLED & READY!
echo   Launching Buddy HUD...
echo ===================================================
echo.

start launch_hud.bat

echo Removing setup.bat installer...
(goto) 2>nul & del "%~f0"
