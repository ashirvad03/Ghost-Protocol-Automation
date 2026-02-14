@echo off
cd /d "%~dp0"
title SECRET VAULT MANAGER 🔒
color 0b

:: --- SETTINGS ---
set "FOLDER_NAME=private"
set "ACCESS_PASS=king007"

:: --- CHECK: KYA FOLDER EXIST KARTA HAI? ---
if not exist "%FOLDER_NAME%" (
    echo [ERROR] 'private' folder nahi mila!
    echo Main naya bana raha hu...
    md "%FOLDER_NAME%"
    echo Folder created. Ab isme apna data rakho aur lock kar do.
    pause
    goto end
)

:: --- LOGIC: AGAR FOLDER KHULA HAI TO LOCK KARO ---
:: Hum check karenge ki kya folder hidden hai ya nahi
for %%A in ("%FOLDER_NAME%") do set "attr=%%~aA"

:: Agar attribute me 'h' (hidden) nahi hai, matlab khula hai -> LOCK IT
if "%attr:h=%"=="%attr%" (
    goto :lock_folder
) else (
    goto :unlock_folder
)

:lock_folder
cls
echo [ACTION] Locking the Vault... 🔒
:: +h = Hidden, +s = System (Super Hidden)
attrib +h +s "%FOLDER_NAME%"
echo.
echo [OK] Folder Gayab ho gaya hai!
echo Kisi ko pata bhi nahi chalega ki yahan kuch tha.
timeout /t 2 >nul
goto end

:unlock_folder
cls
echo =========================================
echo      🔓 UNLOCKING SECRET VAULT 🔓
echo =========================================

:: --- DUAL PASSWORD SYSTEM ---
:: 1. Check if MASTER is already logged in (Flag Check)
if exist "C:\Windows\Temp\mytools_unlocked.flag" (
    echo [AUTO] Master Login Detected. Access Granted! 👑
    goto :do_unlock
)

:: 2. If Guest, Ask for Password
echo.
echo System is in GUEST MODE.
echo Enter Password to view hidden files.
set /p "pass=Password: "

if "%pass%"=="%ACCESS_PASS%" (
    echo [SUCCESS] Password Accepted!
    goto :do_unlock
) else (
    color 0c
    echo.
    echo [WRONG] Galat Password! Access Denied. 🤡
    echo Folder will remain hidden.
    pause
    goto end
)

:do_unlock
:: -h = Unhide, -s = Remove System tag
attrib -h -s "%FOLDER_NAME%"
echo.
echo [OK] Folder is now VISIBLE.
echo Opening folder...
start "" "%FOLDER_NAME%"
goto end

:end
:: Script band
exit /b