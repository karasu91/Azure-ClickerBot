import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = ROOT_DIR + "\\imgs\\"

class Ships():
    def __init__(self):       
        #self.carrier720 = IMG_DIR + "carrier.png"
        #self.destroyer720 = IMG_DIR + "destroyer.png"
        #self.cruiser720 = IMG_DIR + "cruiser.png"
        self.destroyer1 = IMG_DIR + "destroyer1.png"
        self.destroyer2 = IMG_DIR + "destroyer2.png"
        self.destroyer3 = IMG_DIR + "destroyer3.png"
        self.cruiser1 = IMG_DIR + "cruiser1.png"
        self.cruiser2 = IMG_DIR + "cruiser2.png"
        self.cruiser3 = IMG_DIR + "cruiser3.png"
        self.cruiser4 = IMG_DIR + "cruiser4.png"
        self.carrier1 = IMG_DIR + "carrier1.png"
        #self.money1 =  IMG_DIR + "money1.png"
        self.money2 =  IMG_DIR + "money2.png"
        self.money3 =  IMG_DIR + "money3.png"
        #self.carrier2 = IMG_DIR + "carrier2.png"
        #self.carrier3 = IMG_DIR + "carrier3.png"

class Boss():
    def __init__(self): 
        self.boss1 = IMG_DIR + "boss1.png"
        self.boss2 = IMG_DIR + "boss2.png"
        self.boss3 = IMG_DIR + "boss3.png"
        self.boss4 = IMG_DIR + "boss4.png"
        self.boss5 = IMG_DIR + "boss7.png"

class States():
    def __init__(self):       
        #self.autoBattleManual = IMG_DIR + "modeManual1080.jpg"
        self.preBattle = IMG_DIR + "targets1.png"
        self.enemySelect = IMG_DIR + "retreat1.png"
        
        self.victory2 = IMG_DIR + "victory2.png"
        self.victory3 = IMG_DIR + "victory3.png"
        self.ambush1 = IMG_DIR + "evade1.png"  

        self.go1 = IMG_DIR + "go1.png"
        self.go2 = IMG_DIR + "go2.png"
        self.cancel1 = IMG_DIR + "cancel1.png"
        self.confirm2 = IMG_DIR + "confirm2.png"
        self.level_3_4 = IMG_DIR + "level_6_2.png"

class Buttons():
    def __init__(self):       
        self.battleStart = IMG_DIR + "battleb1.png"
        #self.battleStart = IMG_DIR + "battleb2.png"
        #self.battleStart = IMG_DIR + "battleb3.png"

        self.confirm1 = IMG_DIR + "confirm1.png"
        self.confirm2 = IMG_DIR + "confirm2.png"
        