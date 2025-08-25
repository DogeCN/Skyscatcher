::[Bat To Exe Converter]
::
::fBE1pAF6MU+EWHzeyGY1Ph5YQxS+DHKuDroS1Nvw9vmEo1keXOctRIvSyaCyE+sK+UblYZUl02g6
::YAwzoRdxOk+EWAjk
::fBw5plQjdCqDJH2B4kc8JwtofB2WNGS0OoYX8fv47v6EqkgPaOsyf7PS2buAbukQ5SU=
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF25
::cxAkpRVqdFKZSTk=
::cBs/ulQjdF25
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+IeA==
::cxY6rQJ7JhzQF1fEqQJgZkoaHErSXA==
::ZQ05rAF9IBncCkqN+0xwdVsEAlXMbCXqZg==
::ZQ05rAF9IAHYFVzEqQIDIwJHTwWWP2O/FNU=
::eg0/rx1wNQPfEVWB+kM9LVsJDDeJJXi5B6Ef4O3poe+fpy0=
::fBEirQZwNQPfEVWB+kM9LVsJDDeJJXi5B6Ef4O3pjw==
::cRolqwZ3JBvQF1fEqQIDIwJHTwWWP2O/FNU=
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATE100gMQldSwyWfFeiJ+xczOf86smp4h9NBrdxOK7X1vScKecb/lakZ5M+02hMnc9CbA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCqDJH2B4kc8JwtofB2WNGS0OoYX8fv47v6EqkgPaOY2a5vn6b+XM+MS/kbscIRj02Jf+A==
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
chcp >nul 65001
set arc=%PROCESSOR_ARCHITECTURE:AMD64=x64%
for /f "tokens=1-2 delims=." %%a in ('wmic os get version ^| findstr [0-9]') do set osver=%%a.%%b
set ver=0
if %osver% equ 10.0 set ver=1
if %osver% equ 6.3  set ver=1
if %arc% equ x86 goto err
if %ver% equ 0 goto err

cd "Skyscatcher\bin"
set exe=%~f0
for /f "tokens=2 delims==" %%i in ('wmic datafile where name^="%exe:\=\\%" get Version /value ^| findstr "="') do set release=%%i
echo Current Release: %release%
set exe=main.exe
for /f "tokens=2 delims==" %%i in ('wmic datafile where name^="%cd:\=\\%\\%exe%" get Version /value ^| findstr "="') do set version=%%i
echo File Ver: %version%
echo.
if %version% equ %release% (
echo Starting ...
%exe% "%1"
) else (
del >nul 2>nul /f %exe%
echo About to Release ...
%0
)
goto eof

:err
%extd% /getsystemlanguage
if "%result%" == "Chinese - China" (
set message="此程序无法在这台电脑上运行�?"
) else (
set message="This program cannot run on this computer"
)
%extd% /messagebox Error %message:�?=% 16

:eof