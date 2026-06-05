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
::5. odblokujeme import knihoven
echo import site >> python_env\python311._pth
::6. stahneme get-pip skript
echo [!] Stahuji instalátor pro správce balíčků (pip)...
curl -L -o get-pip.py https://bootstrap.pypa.io/get-pip.py
::7. Spustíme instalaci pipu naším lokálním Pythonem
echo[!] Instaluji pip do lokálního prostředí...
python_env\python.exe get-pip.py --no-warn-script-location
::8. Uklidíme stažený script
del get-pip.py

::----------------------------------------------------------------
set PYTHON_CMD=.\python_env\python.exe
echo [OK] Lokální python uspěšně připraven!
goto :KONTROLA_KNIHOVEN

:: ---------------------------------------------------------
:: OBLAST PRO KONTROLU KNIHOVEN A VERZÍ
:: ---------------------------------------------------------
:KONTROLA_KNIHOVEN
echo.
echo [2/4] Kontrola herních knihoven (pygame, curses)...

:: Pomoci našeho Pythonu zavolame pip a nainstalujeme requiments.txt
%PYTHON_CMD% -m pip install -r requirements.txt  >nul 2>&1
echo [OK] Všechny knihovny jsou připraveny!
echo.
echo [3/4] Kontroluji dostupnost aktualizací...

::1. Stáhneme online verzi z GitHubu
curl -L -o online_version.txt https://raw.githubusercontent.com/TVOJE_JMENO/TVUJ_REPO/main/version.txt >nul 2>&1

::2. Provonáme lokální verzi hráče s online verzi
fc version.txtt online_version.txt >nul

::3. Pokud se soubory nerovnají, odbočímen a aktualizaci
if %errorlevel% neq 0 (
    goto :AKTUALIZUJ_HRU
)

::4. Pokud se Rovnají, kod pokračuje
del online_version.txt
echo [OK] Hra je aktualní!
echo.
::---------------------------------------------------

echo [4/4] Hra se spouští...
echo ==================================================
:: Pauza 2vteřiny
timeout /t 2 >nul
:: zapínáme hru!
%PYTHON_CMD% main.py

:: ---------------------------------------------------------
:: OBLAST PRO AKTUALIZACE HRY
:: ---------------------------------------------------------
:AKTUALIZUJ_HRU
echo.
echo [!] Byla nalezena nová verze hry! Aktualizuji...

::1. curl -L -o update.zip https://github.com/TVOJE_JMENO/TVUJ_REPO/releases/latest/download/code.zip >nul 2>&1

echo [!] Instaluji novou verzi...
::2. Rozbalíme nové soubory přímo přes ty staré
tar -xf update.zip
::3. Smažeme stažený zip
del update.zip

::4. Aktualizujeme lokální číslo verze
:: Vezmeme "online_version.txt a přejmenujeme ho..
move /y online_version.txt version.txt >nul

echo [OK] Aktualizace byla dokončena!
echo.

::5. Spustíme hru.

echo [4/4] Hra se spouští...
echo ==================================================
:: Pauza 2vteřiny
timeout /t 2 >nul
:: zapínáme hru!
%PYTHON_CMD% main.py
