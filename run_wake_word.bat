@echo off
title BUDDY WAKE WORD DAEMON
cd /d "c:\buddy"
echo Starting Buddy Hands-Free Wake Word Service...
python voice/wake_word_daemon.py
pause
