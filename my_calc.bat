@echo off
title Smart calculator
color 0b
:main_menu
cls
echo it's gonna real............
echo 1. sum
echo 2. minus
echo 3. multiply
echo 4. division
echo 5. exit
set /p choice="which one...."
if "%choice%"=="1" goto sum
if "%choice%"=="2" goto minus
if "%choice%"=="3" goto multiply
if "%choice%"=="4" goto division
if "%choice%"=="5"  exit
echo loop is exist
pause 
goto main_menu
:sum
cls
echo -----ADDITION MODE-------
echo enter 2 values.....
set /p v1="Enter first value : "
set /p v2="Enter second value : "
set /a result=v1+v2
echo sum is %result%
pause
goto main_menu
:minus
cls
echo -------SUBSTRACTION MODE----------
echo enter 2 values......
set /p v1="Enter first value : "
set /p v2="Enter second value : "
set /a result=v1-v2
echo Substraction is %result%
pause 
goto main_menu
:multiply
cls
echo -------MULTIPLICATION MODE---------
echo enter 2 values.....
set /p v1="Enter first value : "
set /p v2="Enter second value : "
set /a result=v1*v2
echo Multipication is %result%
pause
goto main_menu
:division
cls
echo --------DIVISION MODE--------------
echo enter 2 values........
set /p v1="Enter first value : "
set /p v2="Enter second value : "
set /a result=v1/v2
echo Division is %result%
pause
goto main_menu


