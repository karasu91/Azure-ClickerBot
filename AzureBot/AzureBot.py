# Window size must be 1280 x 720 for image reconginiton to work!
from PIL import Image, ImageGrab
#from defines import STATETABLE
import queue
import pyautogui
import ImagePaths
import defines as STATES
import win32api #pywin32
import win32con
import win32gui
import time
import threading
import numpy as np
import cv2
from threading import RLock
from itertools import chain
import random

mutex = RLock()
CONFIDENCE_GLOBAL = 0.7
runEnabled = True
autoGameFrequency = 1 # second
gameStateParserFrequency = 1
GLOBAL_X_COORD = 0
GLOBAL_Y_COORD = 0
imgCoords_tick_1s = 0
stateParser_tick_1s = 0
GAME_STATE = 0
start_tick_imgCoords = False
start_tick_stateParser = False
IMAGECOORD_MAX_TICKS = 5
STATEPARSER_MAX_TICKS = 5
CONFIDENCE_STATEPARSER = 0.93

def lClick(x, y):
    x_prev, y_prev = win32gui.GetCursorPos()
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    win32api.SetCursorPos((x_prev,y_prev))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x_prev,y_prev,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x_prev,y_prev,0,0)


def getImgCoords(obj, delay):
    global imgCoords_tick_1s
    global start_tick_imgCoords

    coordinates = None
    coordinateList = []
    if hasattr(obj, '__class__') and not isinstance(obj, str): # or isinstance(obj, ):  
        
        imgCoords_tick_1s = 0
        start_tick_imgCoords = True

        #if imgCoords_tick_1s < IMAGECOORD_MAX_TICKS:
        for attr, path in obj.__dict__.items(): # Cycle through all instances   
            coordinates = pyautogui.locateOnScreen(path, confidence=CONFIDENCE_GLOBAL)  
            print(attr, path, coordinates)
            if coordinates: 
                im = Image.open(path)
                width, height = im.size
                # Add offset so that click goes to center    
                xcoord = coordinates[0] + width / 2
                ycoord = coordinates[1] + height / 2
                coordinateList.append(int(xcoord))
                coordinateList.append(int(ycoord))
                                      
        return coordinateList

        if imgCoords_tick_1s > IMAGECOORD_MAX_TICKS:
            imgCoords_tick_1s = 0  
            
        if coordinates:
            print(attr, path)
            im = Image.open(path)
            width, height = im.size
            # Add offset so that click goes to center    
            xcoord = coordinates[0] + width / 2
            ycoord = coordinates[1] + height / 2
            return int(xcoord), int(ycoord)

    if isinstance(obj, str): # Get single image coordinates
        value = obj
        coordinates = pyautogui.locateOnScreen(value, confidence=CONFIDENCE_GLOBAL)
        print(obj, coordinates)
        if coordinates:
            im = Image.open(value)
            width, height = im.size
            # Add offset so that click goes to center    
            xcoord = coordinates[0] + width / 2
            ycoord = coordinates[1] + height / 2
            return int(xcoord), int(ycoord)


#def returnGameState(attr):
#    if str(attr) == "preBattle":
#        return STATES.STATETABLE[STATES.PRE_BATTLE]

def gameStateParser(num, q):
    global GLOBAL_X_COORD
    global GLOBAL_Y_COORD
    global GAME_STATE
    global stateParser_tick_1s
    global start_tick_stateParser
    setNewState = False
    stateObj = ImagePaths.States()
    prevState = 0
    newState = 0
    global runEnabled
    print("In StateParserThread")


    coordinates = None

    while True:
        try:
            if runEnabled:
                stateParser_tick_1s = 0
                start_tick_stateParser = True
                stateList = []
                for attr, value in stateObj.__dict__.items(): # Cycle through all instances                   
                    coordinates = pyautogui.locateOnScreen(value, confidence = CONFIDENCE_STATEPARSER) 
                    #print(attr, value, coordinates)
                    if coordinates:
                        setNewState = True
                        stateList.append([str(attr), coordinates[0], coordinates[1]])
                
                if stateParser_tick_1s > STATEPARSER_MAX_TICKS:
                    stateParser_tick_1s = 0

                if setNewState:

                    for state, x, y in stateList:     
                        print("stateXY: ",state, x, y)
                        if state == "preBattle":                
                            GAME_STATE = STATES.PRE_BATTLE   
                
                        if state == "ambush1":
                            lClick(x, y)
                            stateList = []
                            break

                        if state == "confirm2":    
                            lClick(x, y)
                            stateList = []
                            break

                        if state == "cancel1":    
                            lClick(x, y)
                            stateList = []
                            break

                        if state == "enemySelect":
                            GAME_STATE = STATES.SHIP_SEARCH   

                        if state == "go1":
                            lClick(x, y)
                            stateList = []
                            break

                        if state == "go2":
                            lClick(x, y)
                            stateList = []
                            break

                        if state == "level_3_4":
                            lClick(x, y)  
                            stateList = []
                            break

                        if state == "victory3" or state == "victory2":
                            GAME_STATE = STATES.POST_BATTLE  
                            GLOBAL_X_COORD = int(1920/2)
                            GLOBAL_Y_COORD = int(1080/4)          
            
                    preState = newState
                    newState = GAME_STATE

                    #if newState != preState: # State differs from previous
                    print("Queuing", newState)
                    q.put(newState)
                    #print(STATES.STATETABLE[GAME_STATE])
                    setNewState = False

                stateList = []
                coordinates = []
                time.sleep(0.1)

        except Exception as e:
            print(str(e))
            stateList = []
            coordinates = []

def tickHandler():

    global stateParser_tick_1s
    global imgCoords_tick_1s
    global start_tick_imgCoords
    global start_tick_stateParser
    global runEnabled

    globalSleepTimer = 0
    waitToRun = False

    while True: 
        if start_tick_stateParser:
            stateParser_tick_1s += 1        

        if start_tick_imgCoords:
            imgCoords_tick_1s += 1
        
        if not waitToRun: # Running
            globalSleepTimer += 1
            if globalSleepTimer >= 60*45:
                runEnabled = False
                waitToRun = True
                globalSleepTimer = 0

        if waitToRun: # Sleeping
            globalSleepTimer += 1
            if globalSleepTimer >= 60*random.randint(5, 15): # Sleep between 5 and 15 minutes
                runEnabled = True
                waitToRun = False
                globalSleepTimer = 0

       #time.sleep(1)
    

def autoGame(num, q):
    global GAME_STATE
    global GLOBAL_X_COORD
    global GLOBAL_Y_COORD
    global runEnabled
    ships = ImagePaths.Ships()
    buttons = ImagePaths.Buttons()
    boss = ImagePaths.Boss()
    coords = []
    bossFound = False  
    GAMESTATE = 0
    print("autoGameControllerThread")

    while True:
        try:
            if runEnabled:
                if q.qsize() != 0:
                    GAMESTATE = q.get()  
                    q.task_done();

                if(GAMESTATE == STATES.SHIP_SEARCH):
                    print("Searching ships..")

                    if not bossFound:
                        # Search for boss node for 5 seconds    
                        print("Searching for boss node..")        
                        coords = getImgCoords(boss, 0)  
                        if len(coords) > 0:
                            print("Boss found.") 

                    coords_t = getImgCoords(ships, 0)     
                    for val in coords_t:
                        coords.append(val)


                    if len(coords) > 0:
                        print("Proceeding..")
                        t = 0
                        # Get x and y from single value list and click
                        while t < len(coords):
                            x = coords[t]
                            y = coords[t+1]
                            lClick(x,y)
                            t += 2   
                            time.sleep(3)

                    coords = []
                    coords_t = []
                    bossFound = False

                if (GAMESTATE == STATES.PRE_BATTLE):
                    coords = []
                    coords = getImgCoords(buttons.battleStart, 0)  
                    if coords:
                        lClick(coords[0], coords[1])
                        GAMESTATE = 999;
        
                if (GAMESTATE == STATES.POST_BATTLE):  
                    coords = []
                    lClick(GLOBAL_X_COORD, GLOBAL_Y_COORD)
                    coords = getImgCoords(buttons.confirm1, 0) 
                    if coords:
                        lClick(coords[0], coords[1])
                        GAMESTATE = 999;
                    time.sleep(1)
                    

                bossFound = 0        
                coords = []
                time.sleep(0.1)

        except Exception as e:
            print(str(e))
            coords = []
            GAMESTATE = 0

if __name__ == "__main__":

    q = queue.Queue()
    num = 2
    autoGameThread = threading.Thread(target = autoGame, args = (num,q))
    autoGameThread.start()
    stateThread = threading.Thread(target = gameStateParser, args = (num,q))
    stateThread.start()
    tickHandlerThread = threading.Thread(target = tickHandler)
    tickHandlerThread.start()
    #stateThread.join()
    #autoGameThread.join()
    #tickHandlerThread.join()

    i = 0   