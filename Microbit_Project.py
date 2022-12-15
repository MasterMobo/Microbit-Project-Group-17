#--SETUP--------------------------------------------------------------------------
pumps = [DigitalPin.P8, DigitalPin.P12, DigitalPin.P16]    # List of pump pin objects
sensors = [AnalogPin.P0, AnalogPin.P1, AnalogPin.P2]        # List of sensor pin objects
sensorVal = [0, 0, 0]                                       # List of sensor values
currentShow = 1                                             # The pot currently being displayed on LCD
manualMode = False                                          # Whether the system is in manual mode or not
manualModeTimeElapsed = 0                                   # How many seconds the system has been in manual mode (refreshes after any user input)
manualModeTimeWindow = 10                                   # How many seconds the system can be in manual mode
settingThreshold = False                                    # Whether the user is setting the threshold
MAX_VAL = 700                                               # Maximum value read from moisture sensor
MIN_VAL = 500                                               # Minimum value read from moisture sensor
THRESHOLD = 580                                             # The value after which the pump will open

# Initialize I2C adress of LCD
makerbit.connect_lcd(39)
makerbit.clear_lcd1602()

# Custom characters for LCD display
makerbit.lcd_make_character(LcdChar.C1,
    makerbit.lcd_character_pixels("""
        # # # # #
            . . . . .
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            . . . . .
            # # # # #
    """))
makerbit.lcd_make_character(LcdChar.C2,
    makerbit.lcd_character_pixels("""
        # # # # #
            . . . . .
            . . . . .
            . . . . .
            . . . . .
            . . . . .
            . . . . .
            # # # # #
    """))
makerbit.lcd_make_character(LcdChar.C3,
    makerbit.lcd_character_pixels("""
        . . # # #
            . # . . .
            # . # # #
            # . # # #
            # . # # #
            # . # # #
            . # . . .
            . . # # #
    """))
makerbit.lcd_make_character(LcdChar.C4,
    makerbit.lcd_character_pixels("""
        # # # . .
            . . . # .
            . . . . #
            . . . . #
            . . . . #
            . . . . #
            . . . # .
            # # # . .
    """))
makerbit.lcd_make_character(LcdChar.C5,
    makerbit.lcd_character_pixels("""
        # # # . .
            . . . # .
            # # # . #
            # # # . #
            # # # . #
            # # # . #
            . . . # .
            # # # . .
    """))

# List of LCD positions (for progress bar display)
lcdPos = [LcdPosition1602.POS17,
    LcdPosition1602.POS18,
    LcdPosition1602.POS19,
    LcdPosition1602.POS20,
    LcdPosition1602.POS21,
    LcdPosition1602.POS22,
    LcdPosition1602.POS23,
    LcdPosition1602.POS24,
    LcdPosition1602.POS25,
    LcdPosition1602.POS26,
    LcdPosition1602.POS27,
    LcdPosition1602.POS28,
    LcdPosition1602.POS29,
    LcdPosition1602.POS30,
    LcdPosition1602.POS31,
    LcdPosition1602.POS32]

#-------------------------------------------------------------------------------------------

#--MAIN-LOOP--------------------------------------------------------------------------------

def on_forever():
    # Update values of sensors
    updatePins()

    if settingThreshold == True:
        setThresholdWindow()
    else:
        if manualMode == False:
            for i in range(len(sensors)):
                # Check moisture, if too low then open pump
                if sensorVal[i] >= THRESHOLD:
                    openPump(i)
                else:
                    closePump(i)

        #LCD Control
        showStats(currentShow)

basic.forever(on_forever)

#---------------------------------------------------------------------------------------------------------

#-OTHER-FUNCIONS------------------------------------------------------------------------------------------

def updatePins():
    """Update the values of sensors"""
    for i in range(len(sensors)):
        sensorVal[i] = pins.analog_read_pin(sensors[i])

def calculatePercent(val):
    """Calculate the percentage value of given moisture reading"""
    global MAX_VAL
    global MIN_VAL

    res = Math.ceil(Math.map(val, MAX_VAL, MIN_VAL, 0, 100))
    if res > 100:
        return 100
    elif res < 0:
        return 0
    return res

def setThresholdWindow():
    """Shows the window for setting threshold"""
    makerbit.clear_lcd1602()
    makerbit.show_string_on_lcd1602("Set Threshold:", makerbit.position1602(LcdPosition1602.POS1), 16)
    makerbit.show_string_on_lcd1602(str(THRESHOLD) + " (" + str(calculatePercent(THRESHOLD)) + "%)", makerbit.position1602(LcdPosition1602.POS17), 16)

def showStatsDetailed(showNum):
    global manualMode

    percent_val = calculatePercent(sensorVal[showNum-1])
    makerbit.show_string_on_lcd1602("P" + str(showNum), makerbit.position1602(LcdPosition1602.POS1), 2)
    makerbit.show_string_on_lcd1602("" + str(sensorVal[showNum-1]),
        makerbit.position1602(LcdPosition1602.POS4),
        3)
    makerbit.show_string_on_lcd1602(str(percent_val) + "%",
        makerbit.position1602(LcdPosition1602.POS8),
        3)
    progressBar(percent_val)

    if manualMode == True:
        makerbit.show_string_on_lcd1602("MANUAL", makerbit.position1602(LcdPosition1602.POS12), 6)
        
    else:
        makerbit.show_string_on_lcd1602("AUTO", makerbit.position1602(LcdPosition1602.POS12), 4)
        

def showStats(showNum):
    """Display statistics of the given pot"""
    global manualMode

    percent_val = calculatePercent(sensorVal[showNum-1])
    makerbit.show_string_on_lcd1602("Pot" + str(showNum) + ": ", makerbit.position1602(LcdPosition1602.POS1), 6)
    makerbit.show_string_on_lcd1602(str(percent_val) + "% ",
        makerbit.position1602(LcdPosition1602.POS7),
        4)
    progressBar(percent_val)

    if manualMode == True:
        makerbit.show_string_on_lcd1602("Manual", makerbit.position1602(LcdPosition1602.POS11), 6)
    else:
        makerbit.show_string_on_lcd1602("  Auto", makerbit.position1602(LcdPosition1602.POS11), 6)


def progressBar(val: number):
    """Display progrerss bar based on moisture level"""
    # First bit of bar
    makerbit.lcd_show_character1602(LcdChar.C3, makerbit.position1602(LcdPosition1602.POS17))
    
    #Middle part of bar
    for j in range(1, 15):
        if j / 16 <= val / 100:
            makerbit.lcd_show_character1602(LcdChar.C1, makerbit.position1602(lcdPos[j]))
        else:
            makerbit.lcd_show_character1602(LcdChar.C2, makerbit.position1602(lcdPos[j]))
    
    # Last bit of bar
    if val >= 100:
        makerbit.lcd_show_character1602(LcdChar.C5, makerbit.position1602(LcdPosition1602.POS32))
    else:
        makerbit.lcd_show_character1602(LcdChar.C4, makerbit.position1602(LcdPosition1602.POS32))


def closePump(ind: number):
    """Turns off given pump (indexed from 0)"""
    pins.digital_write_pin(pumps[ind], 0)


def openPump(ind: number):
    """Turns on given pump (indexed from 0)"""
    pins.digital_write_pin(pumps[ind], 1)


def showNext():
    """Changes the currently displayed plant pot to the next one"""
    if manualMode == False:
        global currentShow
        currentShow += 1
        if currentShow > 3:
            currentShow = 1
loops.every_interval(5000, showNext)

def startManualMode():
    """Initializes the manual mode"""
    global manualMode

    # Turn off pumps before going into manual mode
    for i in range(len(sensors)):
        closePump(i)

    manualMode = True

#--Button-control------------------------------------------------------------

def on_button_pressed_a():
    """Called when button A is pressed"""
    global currentShow
    global manualMode
    global manualModeTimeElapsed
    global THRESHOLD
    global MIN_VAL

    # Decrease threshold if user is setting threshold
    if settingThreshold:
        THRESHOLD = THRESHOLD - 5
        if THRESHOLD < MIN_VAL:     # Clamp THRESHOLD above MIN_VAL
            THRESHOLD = MIN_VAL
        return

    # Change to previous plant pot if in manual mode
    if manualMode == True:
        currentShow -= 1
        if currentShow < 1:
            currentShow = 3
        manualModeTimeElapsed = 0   # Refresh manual mode timer
    else:
        startManualMode()
input.on_button_pressed(Button.A, on_button_pressed_a)


def on_button_pressed_b():
    """Called when button B is pressed"""
    global currentShow
    global manualMode
    global manualModeTimeElapsed
    global THRESHOLD
    global MAX_VAL

    # Increase threshold if user is setting threshold
    if settingThreshold:
        THRESHOLD = THRESHOLD + 5
        if THRESHOLD > MAX_VAL:
            THRESHOLD = MAX_VAL     # Clamp THRESHOLD bellow MAX_VAL
        return

    # Change to next plant pot if in manual mode
    if manualMode == True:
        currentShow += 1
        if currentShow > 3:
            currentShow = 1
        manualModeTimeElapsed = 0   # Refresh manual mode timer
    else:
        startManualMode()
input.on_button_pressed(Button.B, on_button_pressed_b)


def on_button_pressed_ab():
    """Called when buttons A and B are pressed together"""
    global currentShow
    global manualMode
    global manualModeTimeElapsed
    global settingThreshold

    # Turn on plant pot for 2 seconds in manual mode
    if manualMode == True:
        openPump(currentShow - 1)
        basic.pause(2000)
        closePump(currentShow - 1)
        manualModeTimeElapsed = 0   # Refresh manual mode timer
    
    # Activate/Deactivate setting threshold mode
    else:
        if settingThreshold == False:
            settingThreshold = True
        else:
            settingThreshold = False

input.on_button_pressed(Button.AB, on_button_pressed_ab)


def manualModeTimer():
    """Timer function to reset manual mode"""
    global manualMode
    global manualModeTimeWindow
    global manualModeTimeElapsed
    
    if manualMode == True:
        manualModeTimeElapsed = manualModeTimeElapsed + 1
    
    if manualModeTimeElapsed > manualModeTimeWindow:
        manualMode = False
        manualModeTimeElapsed = 0
    
loops.every_interval(1000, manualModeTimer)

#---------------------------------------------------------------------------------------------------------
