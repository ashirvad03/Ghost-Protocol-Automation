@echo off
title SUPER POTATO FIXER 3000 🤡
color 0e

:: --- MAGIC CODE: AUTO ASK FOR POWER ---
:: Check if I have muscles (Admin Rights)
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :gotPower
) else (
    echo.
    echo [ERROR] I AM WEAK! NO MUSCLES! 😭
    echo [ACTION] Asking Boss for SUPER POWERS...
    echo.
    echo Please click "YES" on the popup... or I die.
    
    :: This creates a temporary script to relaunch ME as Admin
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B
)

:gotPower
:: Ab hum asli folder me aayenge (Kyunki Admin mode kabhi kabhi System32 me chala jata hai)
cd /d "%~dp0"

:start
cls
echo ==================================================
echo      HELLO BOSS! WELCOME TO POTATO FIXER
echo ==================================================
echo.
echo [1] EAT MY GARBAGE (Quick Clean)
echo [2] NUKE THE SYSTEM (Deep Clean)
echo [3] MAKE WIFI GO ZOOM (Internet Fix)
echo [4] BYE BYE (Exit)
echo.
echo ==================================================
set /p choice="WHAT YOU WANT? (Type Number): "

if "%choice%"=="1" goto quick
if "%choice%"=="2" goto deep
if "%choice%"=="3" goto netboost
if "%choice%"=="4" exit

:quick
cls
echo [MOOD] Hungry for trash... OM NOM NOM!
echo.
del /s /f /q %temp%\*.*
rd /s /q %temp%
md %temp%
echo [OK] Yummy! User temp files eaten.

del /s /f /q C:\Windows\Temp\*.*
echo [OK] Burp! System temp files gone.
echo.
echo ==================================================
echo   WOW! YOUR PC SO LIGHT LIKE FEATHER! 🪶
echo ==================================================
pause
goto start

:deep
cls
echo [WARNING] HOLD ON BRO! THIS TAKE TIME!
echo [MOOD] Cleaning your secrets... hehe...
echo.

del /s /f /q C:\Windows\Prefetch\*.*
echo [OK] Brain cache cleared!

net stop wuauserv
del /s /f /q C:\Windows\SoftwareDistribution\Download\*.*
net start wuauserv
echo [OK] Old Update Garbage = DELETED!

echo [ACTION] Looking inside Recycle Bin...
rd /s /q %systemdrive%\$Recycle.bin
echo [OK] POOF! Trash bin is empty!

echo.
echo ==================================================
echo   OMG! YOUR POTATO PC IS NOW A FERRARI! 🏎️
echo ==================================================
pause
goto start

:netboost
cls
echo [MOOD] Kicking the Router... HYAAA! 🥋
echo.
ipconfig /flushdns
echo [OK] Toilet... I mean DNS Flushed! 🚽

ipconfig /release
ipconfig /renew
echo [OK] New IP Address stolen from internet!

echo.
echo ==================================================
echo   INTERNET GO VROOM VROOM NOW! 🚀
echo ==================================================
pause
goto start