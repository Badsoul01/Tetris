import curses

COLOR_MAP = {"I":1,"O":2,"T":3,"S":4,"Z":5,"J":6,"L":7}

CURSES_COLORS = [curses.COLOR_CYAN, curses.COLOR_YELLOW, curses.COLOR_MAGENTA,
         curses.COLOR_GREEN, curses.COLOR_RED, curses.COLOR_BLUE, curses.COLOR_WHITE]
MAIN_MENU = ["NOVÁ HRA","TUTORIÁL","NASTAVENÍ","STATISTIKY","EXIT"]

SETTINGS_MENU = ["BARVY", "DUCH KOSTKY","POČÁTEČNÍ LEVEL", "ZPĚT"]

TUTORIAL_TEXT = [
    "OVLÁDÁNÍ:",
    "",
    "Šipky / WASD  -> Pohyb a rotace",
    "Mezerník      -> Hard Drop",
    "P             -> Pauza",
    "Q             -> QUIT",
    "",
    "ZPĚT"
]


ACTION_KEYS ={
                "UP" : [ord("w"), ord("W"), curses.KEY_UP],
                "DOWN":[ord("s"), ord("S"), curses.KEY_DOWN],
                "LEFT":[ord("a"), ord("A"), curses.KEY_LEFT],
                "RIGHT":[ord("d"), ord("D"), curses.KEY_RIGHT],
                "QUIT":[ord("q"), ord("Q")],
                "ENTER":[ord(" "),10],
                "PAUSE":[ord("p"), ord("P")]
}


SHAPES = {
    'O': [(0, 0), (1, 0), (0, 1), (1, 1)],
    'I': [(0, 0), (-1, 0), (1, 0), (2, 0)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)],
    'L': [(0, 0), (-1, 0), (1, 0), (1, -1)],
    'J': [(0, 0), (-1, 0), (1, 0), (-1, -1)],
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)]
}

LOGO_DATA = {
            "I":[(5,5),(6,5),(7,5),(8,5), #Písmenko T
                 (13,6),(13,7),(13,8),(13,9), #Písmenko E
                 (13,12),(14,12),(15,12),(16,12), #Písmenko E
                 (21,5),(22,5),(23,5),(24,5), #Druhé písmenko T
                 (32,9),(32,10),(32,11),(32,12), #Písmenko R
                 (40,5),(41,5),(42,5),(43,5), #Písmenko S
                 (39,9),(40,9),(41,9),(42,9), #Písmenko S
                 (38,12),(39,12),(40,12),(41,12) #Písmenko S
            ],
            "O":[(9,5),(10,5),(9,6),(10,6), #Písmenko T
                 (13,10),(14,10),(13,11),(14,11), #Písmenko E
                 (22,11),(23,11),(22,12),(23,12), #Druhé písmenko T
                 (28,11),(29,11),(28,12),(29,12), #Písmenko R
                 (35,5),(36,5),(35,6),(36,6), #Písmenko I
                 (39,7),(40,7),(39,8),(40,8), #Písmenko S
                 (42,11),(43,11),(42,12),(43,12) #Písmenko S

            ],
            "J":[(5,6),(6,6),(7,6),(7,7), #Písmenko T
                 (20,5),(20,6),(21,6),(22,6), #Druhé písmenko T
                 (30,5),(31,5),(32,5),(32,6), #Písmenko R
                 (30,7),(31,7),(32,7),(32,8), #Písmenko R
                 (29,8),(30,8),(29,9),(29,10), #Písmenko R
                 (39,5),(39,6),(40,6),(41,6) #Písmenko S
            ],
            "T":[(8,6),(8,7),(8,8),(9,7), #Písmenko T
                 (7,8),(7,9),(7,10),(8,9), #Písmenko T
                 (14,7),(14,8),(14,9),(15,8), #Písmenko E
                 (28,5),(28,6),(28,7),(29,6), #Písmenko R
            ],
            "Z":[(8,10),(7,11),(8,11),(7,12), #Písmenko T
                 (23,8),(22,9),(23,9),(22,10), #Druhé písmenko T
                 (36,7),(35,8),(36,8),(35,9), #Písmenko I
            ],
            "L":[(14,5),(15,5),(16,5),(14,6), #Písmenko E
                 (15,11),(16,11),(17,11),(17,10), #Písmenko E
                 (25,5),(23,6),(24,6),(25,6), #Druhé písmenko T
                 (27,8),(28,8),(28,9),(28,10),#Písmenko R
                 (43,9),(41,10),(42,10),(43,10) #Písmenko S
            ],
            "S":[(22,7),(23,7),(21,8),(22,8), #Druhé písmenko T
                 (35,10),(35,11),(36,11),(36,12), #Písmenko I

            ],
            "══":[(x,13) for x in range(4,45)], #podlaha
            "╚":[(4,13)], #podlaha
            "╝":[(45,13)] #podlaha

        }

