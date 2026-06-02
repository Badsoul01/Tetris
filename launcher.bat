@echo off

:: Nastavení UTF-8 kodovani pro spravne zobrazeni cestiny
chcp 65001 > nul
title Tetris Launcher
cls

echo =========================================
echo     TETRIS - SPUŠTĚNÍ A KONTROLA HRY
echo =========================================
echo.
echo [1/4] Kontrola instalace Pythonu...

:: Pokus o zjištění verzi Pythonu
python --version >nul 2>&1

:: Zkontrolujeme, jeslti prikaz prosel (errorlevel 0) nebo selhal

if %errorlevel% neg 0(
    echo [!] Systémový Python nebyl nalezen!
    echo Zahajuji záchrannou operaci...
    goto :STAHUJ_PYTHON
) else (
    echo [OK] Python je v systému nainstalován.
    set PYTHON_CMD=python
    goto :KONTROLA_KNIHOVEN

:: ---------------------------------------------------------
:: ZÁCHRANNÁ OBLAST PRO STAHOVÁNÍ PYTHONU
:: ---------------------------------------------------------

:STAHUJ_PYTHON
echo.
echo [!] Stahuji přenosovou verzi Pythonu...
::1. Vytvoříme novou složku pro nas lokalní Python
mkdir python_env
:: 2.Stahneme zip archiv z officialních stranek
curl -L -o python_env.zip https://www.python.org/ftp/python/3.11.8/python-3.11.8-embed-amd64.zip

echo [!] Rozbaluji prostředí...
:: 3. rozbalíme zip primo do nasi slozky:
tar -xf python_env.zip -C python_env
:: 4. Smazeme puvodni stazeny zip
del python_env.zip
::5. přesměrujeme nasi promennou na tento novy soubor
set PYTHON_CMD=.\python_env\python.exe

echo [OK] Lokální python uspěšně připraven!
goto :KONTROLA_KNIHOVEN

:: ---------------------------------------------------------
:: OBLAST PRO KONTROLU KNIHOVEN (PIP)
:: ---------------------------------------------------------
:KONTROLA_KNIHOVEN
echo.
echo [2/4] Kontrola herních knihoven (pygame, curses)...

:: Pomoci našeho Pythonu zavolame pip a nainstalujeme requiments.txt
%PYTHON_CMD% -m pip install -r requiments.txt  >nul 2>&1
echo [OK] Všechny knihovny jsou připraveny!
echo.
echo [3/4] Hra se spouští...
echo ==================================================

:: Pauza 2vteřiny
timeout /t 2 >nul

:: zapínáme hru!
%PYTHON_CMD% main.py


echo Spouštím hru přes příkaz: %PYTHON_CMD%
pause
exit

