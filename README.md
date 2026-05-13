# Tetris v terminálu (Curses)
Klon hry tetris v pythonu pomocí Curses knihovny

## O projektu
Verze se zaměřuje na "retro" zážitek. Kód běž v terminálu  


## Klíčové vlastnosti
**Dynamic UI:** Vše se vykresluje pomocí ASCII/Unicode znaků.
**Nastavení v realném čase:** Možnost zapnout/vypnout barvy nebo změnit počáteční úroveň.
**Leveling systém:** Hra se postupně zrychluje podle počtu smazaných řad.
**Dual Control:** Podpora pro šipky i WSAD.

## Instalace a spuštění

Hra vyžaduje **Python 3**. Knihovna 'curses' je v Lunuxu a mocOS standartem.  Pokud  jsi na Windows, je potřeeba doinstalovat podporu:

```bash
# Pouze pro uživatele Windows:
pip install windows-curses

