# 🕹️ Tetris v terminálu (Curses)
Vítejte v projektu klasické hry **Tetris** předělané do terminálového prostředí! Tento projekt kombinuje retro herní zážitek s moderním zázemím pro automatickou instalaci a aktualizaci. 

Hra běží plně v příkazové řádce díky knihovně `curses`, podporuje ukládání nejlepších skóre do SQL databáze a má stylové ozvučení.

![ukázka hry](/assets/Tetris3.gif)


##  ✨ Klíčové vlastnosti
* **Dynamic UI:** Vše se vykresluje pomocí ASCII/Unicode znaků.
* **Leveling systém:** Hra se postupně zrychluje podle počtu smazaných řad.
* **Dual Control:** Podpora pro šipky i WSAD.
* **High Score Tabulka:** Automatické ukládání nejlepších výsledků do lokální SQlite databáze.
* **Chytrý Launcher:** Soubor `launcher.bat`, který Windows automaticky připravý na kompletní spuštění hry.


### 🎛️ Možnosti nastavení v reálném čase

| Funkce v menu        | Popis | Výchozí stav |
|:---------------------| :--- | :--- |
| **Barvy**            | Zapne/vypne barevné terminálové kostky | Zapnuto |
| **Duch**             | Zobrazuje stín, kam kostka dopadne | Zapnuto |
| **Počáteční úroveň** | Volba startovní rychlosti hry (Level 1-10) | Level 1 |
| **Hudba**            | Zapne/vypne retro audio doprovod ze složky `music` | Zapnuto |

##  🚀 Instalace a spuštění
### 🪟 Windows (Nejjednodušší cesta)
Pro hraní není třeba žádných instalací ani nastavování. Stačí postupovat následně:
1. Stáhněte si z nejnovějšího [Releases](https://github.com/Badsoul01/Tetris/releases) balíček `instalator.zip` 
2. Rozbalte jej do prázdné složky.
3. Spusťte soubor **`launcher.bat`**

> ⚠️ **Poznámka k zabezpečení Windows:** Jelikož skript není digitálně podepsaný, Windows SmartScreen nebo Smart App Control ho může při prvním stažení zablokovat. V takovém případě klikněte na soubor `launcher.bat` pravým tlačítkem -> **Vlastnosti** -> zaškrtněte políčko **Odblokovat** (Unblock) a dejte OK.


### 🐧 Linux / 🍏 MacOS
```bash
# Nainstalujte potřebné knihovny
pip3 install pygame

# Spusťte hru
python3 main.py
```
## 🎮 Ovládání hry

Hra se kompletně ovládá pomocí klávesnice:

* <kbd>←</kbd> / <kbd>→</kbd> – Pohyb kostky
* <kbd>↑</kbd> – Otočení kostky
* <kbd>↓</kbd> – Zrychlené padání (Soft Drop)
* <kbd>Space</kbd> – Okamžitý pád dolů (Hard Drop)
* <kbd>P</kbd> – Pauza ve hře
* <kbd>Q</kbd> – Uložení hry a návrat do menu

---

### 👤 Autor

* **Badsoul01** - Kompletní vývoj, refaktoring kódu a správa distribuce.