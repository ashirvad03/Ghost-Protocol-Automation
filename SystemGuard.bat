@echo off
title SYSTEM LOCKED - ACCESS DENIED ⛔
color 4f
:: 4f = Red Background, White Text (Scary look)

:: --- SETTINGS ---
set "GUEST_PASS=1234"
set "MASTER_PASS=king007"
set "LOG_FILE=C:\MyTools\history_logs.txt"
set "LOCK_FILE=C:\Windows\Temp\mytools_unlocked.flag"

:: Screen saaf aur full focus
cls
echo.
echo ==========================================================
echo        🛑  SYSTEM LOCKDOWN INITIATED  🛑
echo ==========================================================
echo.
echo        THIS COMPUTER IS PROCTECTED BY JOKER PROTOCOL.
echo.
echo        Identify yourself! Who are you?
echo        (Don't try to be smart, I am watching you)
echo.
echo ==========================================================

:check_pass
echo.
set /p "pass=ENTER PASSWORD: "

:: --- CHECK 1: MASTER PASSWORD (GOD MODE) ---
if "%pass%"=="%MASTER_PASS%" (
    cls
    color 0a
    echo.
    echo =================================================
    echo    ACCESS GRANTED - WELCOME BACK, MY KING! 👑
    echo =================================================
    echo.
    echo System Status: FULLY UNLOCKED.
    echo No more passwords will be asked today.
    
    :: Flag file banao taaki baaki tools ko pata chale King aa gaya hai
    echo UNLOCKED > "%LOCK_FILE%"
    
    :: History me likho
    echo [%date% %time%] [LOGIN] MASTER Login Successful (System Unlocked) >> "%LOG_FILE%"
    
    timeout /t 2 >nul
    exit
)

:: --- CHECK 2: GUEST PASSWORD (NORMAL MODE) ---
if "%pass%"=="%GUEST_PASS%" (
    cls
    color 0e
    echo.
    echo =================================================
    echo    ACCESS GRANTED - Hello Guest. 😐
    echo =================================================
    echo.
    echo Warning: Restricted Areas are still LOCKED.
    
    :: Flag file delete kar do (agar pehle se thi) taaki tools lock rahein
    if exist "%LOCK_FILE%" del "%LOCK_FILE%"
    
    :: History me likho
    echo [%date% %time%] [LOGIN] GUEST Login Successful (Restricted Mode) >> "%LOG_FILE%"
    
    timeout /t 2 >nul
    exit
)

:: --- CHECK 3: WRONG PASSWORD ---
echo.
echo [WRONG!] HAHA! Are you trying to hack me? 🤡
echo Try again or I will self-destruct (Just kidding... or am I?)
echo.
:: Log me likho ki koi galat password daal raha hai
echo [%date% %time%] [FAILED] WRONG Password attempted: '%pass%' >> "%LOG_FILE%"
goto :check_pass