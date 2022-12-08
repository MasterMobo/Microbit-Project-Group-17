#--SETUP--------------------------------------------------------------------------
valves = [DigitalPin.P8, DigitalPin.P12, DigitalPin.P16]    # List of valve pin objects
sensors = [AnalogPin.P0, AnalogPin.P1, AnalogPin.P2]    # List of sensor pin objects
sensorVal = [0, 0, 0]     # List of sensor values
currentShow = 1     # The pot currently being displayed on LCD
THRESHOLD = 500     # The value after which the valve will open

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

# List of LCD position (for progress bar display)
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

    # Check moisture, if too low then open valve
    for i in range(len(sensors)):
        if sensorVal[i] >= THRESHOLD:
            openValve(i)
        else:
            closeValve(i)

    #LCD Control
    if currentShow == 1:
        s1_percent = Math.ceil(Math.map(sensorVal[0], 800, 300, 0, 100))
        makerbit.show_string_on_lcd1602("Pot 1:", makerbit.position1602(LcdPosition1602.POS1), 6)
        makerbit.show_string_on_lcd1602("" + str(sensorVal[0]),
            makerbit.position1602(LcdPosition1602.POS8),
            3)
        makerbit.show_string_on_lcd1602("" + str(s1_percent) + "%",
            makerbit.position1602(LcdPosition1602.POS13),
            6)
        progressBar(s1_percent)
    if currentShow == 2:
        s2_percent = Math.ceil(Math.map(sensorVal[1], 800, 300, 0, 100))
        makerbit.show_string_on_lcd1602("Pot 2:", makerbit.position1602(LcdPosition1602.POS1), 6)
        makerbit.show_string_on_lcd1602("" + str(sensorVal[1]),
            makerbit.position1602(LcdPosition1602.POS8),
            3)
        makerbit.show_string_on_lcd1602("" + str(s2_percent) + "%",
            makerbit.position1602(LcdPosition1602.POS13),
            6)
        progressBar(s2_percent)
    if currentShow == 3:
        s3_percent = Math.ceil(Math.map(sensorVal[2], 800, 300, 0, 100))
        makerbit.show_string_on_lcd1602("Pot 3:", makerbit.position1602(LcdPosition1602.POS1), 6)
        makerbit.show_string_on_lcd1602("" + str(sensorVal[2]),
            makerbit.position1602(LcdPosition1602.POS8),
            3)
        makerbit.show_string_on_lcd1602("" + str(s3_percent) + "%",
            makerbit.position1602(LcdPosition1602.POS13),
            6)
        progressBar(s3_percent)
basic.forever(on_forever)
#---------------------------------------------------------------------------------------------------------

#-OTHER-FUNCIONS------------------------------------------------------------------------------------------
def updatePins():
    i = 0
    while i <= len(sensors) - 1:
        sensorVal[i] = pins.analog_read_pin(sensors[i])
        i += 1
        

def progressBar(val: number):
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


def closeValve(ind: number):
    pins.digital_write_pin(valves[ind], 0)


def openValve(ind2: number):
    pins.digital_write_pin(valves[ind2], 1)


def on_every_interval():
    global currentShow
    currentShow += 1
    if currentShow > 3:
        currentShow = 1
loops.every_interval(5000, on_every_interval)

#---------------------------------------------------------------------------------------------------------
