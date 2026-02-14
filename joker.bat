@echo off
cd /d "C:\MyTools"
title HACKER TOOLBOX (GHOST MODE)
color 0a

:: ==========================================
::       PHASE 1: INITIAL LOGIN
:: ==========================================

:: 1. Check Master Flag (Using User Temp folder now)
if exist "%TEMP%\mytools_unlocked.flag" goto menu

:login_screen
cls
color 0b
echo ==========================================
echo     IDENTITY VERIFICATION REQUIRED
echo ==========================================
echo.
set /p "pass=Enter Access Password: "

:: CASE A: MASTER PASSWORD
if "%pass%"=="king007" goto set_master

:: CASE B: GUEST PASSWORD
if "%pass%"=="1234" goto menu

:: CASE C: WRONG PASSWORD
echo.
echo [ACCESS DENIED] Incorrect Password.
pause
exit

:set_master
:: Using %TEMP% instead of Windows Temp to avoid Permission Error
echo UNLOCKED > "%TEMP%\mytools_unlocked.flag"
goto menu

:: ==========================================
::            MAIN MENU
:: ==========================================
:menu
cls
color 0a
echo ==================================================
echo           GHOST PROTOCOL ACTIVATED
echo ==================================================
echo.
echo    [1] YouTube Downloader
echo    [2] Digital Detective
echo    [3] Smart Folder Organizer
echo    [4] System Booster
echo    [5] Compressor
echo    [6] Secret Vault (Hidden)
echo    [7] View History Logs
echo    [8] Re-Lock System (Logout)
echo    [9] THE OFFICE HQ (PDF/Image/Video/Audio)
echo    [0] Exit
echo.
echo ==================================================

:: Status Update Logic
if exist "%TEMP%\mytools_unlocked.flag" (
    echo [STATUS] SYSTEM UNLOCKED (Master Mode)
) else (
    echo [STATUS] GUEST MODE (Restricted Access)
)
echo ==================================================
set /p opt="Select an option (0-9): "

:: --- SECURITY LOGIC ---
:: Note: 'call' command ensures we return here after checking
if "%opt%"=="1" call :check_access & goto downloader
if "%opt%"=="2" call :check_access & goto detective
if "%opt%"=="3" call :check_access & goto organizer
if "%opt%"=="4" call :check_access & goto booster
if "%opt%"=="5" call :check_access & goto compress
if "%opt%"=="6" call :check_access & goto secret_vault
if "%opt%"=="7" goto viewlogs
if "%opt%"=="8" goto relock
if "%opt%"=="9" call :check_access & goto office_hq
if "%opt%"=="0" exit

:: If wrong input
goto menu

:: ==========================================
::       SECURITY CHECKPOINT
:: ==========================================
:check_access
:: 1. If Master Flag exists in TEMP, proceed immediately (Unlock All)
if exist "%TEMP%\mytools_unlocked.flag" exit /b

:: 2. If Guest, halt and ask for password
cls
color 0c
echo ==========================================
echo     SECURITY ALERT: RESTRICTED MODE
echo ==========================================
echo.
echo You are attempting to access a restricted tool.
echo Authorization is required.
set /p "sec_pass=Enter Password: "

:: SCENARIO 1: Upgrade to Master
if "%sec_pass%"=="king007" (
    echo.
    echo [SUCCESS] Master Password Accepted.
    echo System is now FULLY UNLOCKED.
    echo UNLOCKED > "%TEMP%\mytools_unlocked.flag"
    timeout /t 1 >nul
    exit /b
)

:: SCENARIO 2: Guest Continue (One-time access)
if "%sec_pass%"=="1234" (
    echo.
    echo [OK] Temporary Access Granted.
    timeout /t 1 >nul
    exit /b
)

:: SCENARIO 3: Fail
echo.
echo [ERROR] Access Denied.
pause
goto menu

:: ==========================================
::            TOOLS SECTION
:: ==========================================

:downloader
cls
python youtube_downloader.py
goto menu

:detective
cls
python find.py
goto menu

:organizer
cls
python smart_folder_orgainizer.py
goto menu

:booster
cls
call booster.bat
goto menu

:compress
cls
python masscompressor.py
goto menu

:secret_vault
cls
call locker.bat
goto menu

:office_hq
cls
cd office
python office_hq.py
cd ..
goto menu

:viewlogs
cls
echo ==================================================
echo             SYSTEM ACTIVITY LOGS
echo ==================================================
if exist "history_logs.txt" (
    type "history_logs.txt"
) else (
    echo No logs available.
)
echo.
echo ==================================================
pause
goto menu

:relock
cls
echo [ACTION] Locking System...
if exist "%TEMP%\mytools_unlocked.flag" del "%TEMP%\mytools_unlocked.flag"
echo [OK] System Locked. Authentication required for next session.
pause
exit