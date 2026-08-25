@echo off
title Buddy AI Assistant
cls
echo [ Starting Buddy AI Core Engine... ]
echo.
python main.py
if errorlevel 1 (
    echo.
    echo Buddy closed with an error.
    pause
)
