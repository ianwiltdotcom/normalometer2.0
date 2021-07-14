import board
import displayio
import adafruit_displayio_sh1107
import time
import math

import terminalio
from adafruit_display_text import label
from adafruit_display_shapes import rect
from adafruit_display_shapes import line

displayio.release_displays()

i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

WIDTH = 128
HEIGHT = 64

display = adafruit_displayio_sh1107.SH1107(display_bus, width=WIDTH, height=HEIGHT)
font = terminalio.FONT
display.auto_refresh = False

plotter = displayio.Group()
palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xFFFFFF
plotter.append(displayio.Group())
plot_label = label.Label(font, text=" ", y=8)
plotter.append(plot_label)

def errorText():
    error_group = displayio.Group()
    usb_label = label.Label(font, text="Can't save to disk", y=8)
    usb_label2 = label.Label(font, text="when USB is connected", y=18)
    usb_label3 = label.Label(font, text="Unplug, press reset", y=28)
    usb_label4 = label.Label(font, text="button and try again", y=38)
    error_group.append(usb_label)
    error_group.append(usb_label2)
    error_group.append(usb_label3)
    error_group.append(usb_label4)
    display.show(error_group)
    display.refresh()

def saveText(saved, saveNum):
    if (saved):
        saved_group = displayio.Group(scale=1)
        saved_label = label.Label(font, text="Saved to:", y=16, x=2)
        saved_label2 = label.Label(font, text="/records/record{}.csv".format(saveNum), y=26, x=2)
        saved_label3 = label.Label(font, text="Please press reset.", y=46, x=2)
        saved_group.append(saved_label2)
        saved_group.append(saved_label3)
    else:
        saved_group = displayio.Group(scale=2)
        saved_label = label.Label(font, text="Saving...", y=15, x=2)
    saved_group.append(saved_label)
    display.show(saved_group)
    display.refresh()

def countdown(t):
    countdown_group = displayio.Group(scale=3)
    number_label = label.Label(font, text=str(t), y=10, x=20)
    countdown_group.append(number_label)
    display.show(countdown_group)
    for i in range(t):
        display.refresh()
        t -= 1
        number_label.text = str(t)
        time.sleep(1)
    recording_group = displayio.Group(scale=2)
    recording_label = label.Label(font, text="Recording!", y=15, x=2)
    recording_group.append(recording_label)
    display.show(recording_group)
    display.refresh()

def showMainMenu():
    mainmenu_group = displayio.Group()
    title_label = label.Label(font, text="Normalometer 2.0", y=8, x=16)
    title_rect = rect.Rect(0, 0, 128, 18, outline=palette[1])
    label_a = label.Label(font, text="A: Normal Vectors", y=38)
    label_b = label.Label(font, text="B: Raw Data Viewer", y=48)
    label_c = label.Label(font, text="C: Recorder Mode", y=58)
    label_info = label.Label(font, text="<-- (Click a button)", y=24)
    mainmenu_group.append(label_info)
    mainmenu_group.append(title_label)
    mainmenu_group.append(title_rect)
    mainmenu_group.append(label_a)
    mainmenu_group.append(label_b)
    mainmenu_group.append(label_c)
    display.show(mainmenu_group)
    display.refresh()

def showRecorderMenu(time, mode):
    recordermenu_group = displayio.Group()
    title_label = label.Label(font, text="Recorder Mode", y=8, x=24)
    title_rect = rect.Rect(0, 0, 128, 18, outline=palette[1])
    label_info = label.Label(font, text=" ", y=24)
    label_a = label.Label(font, text="A: Record Time: " + str(time) + "s", y=38)
    bLabelText = "B: Columns [T"
    if (mode & 1):
        bLabelText += " X"
    if (mode & 2):
        bLabelText += " Y"
    if (mode & 4):
        bLabelText += " Z"
    bLabelText += "]"
    label_b = label.Label(font, text=bLabelText, y=48)
    label_c = label.Label(font, text="C: Start Recording", y=58)
    recordermenu_group.append(title_label)
    recordermenu_group.append(title_rect)
    recordermenu_group.append(label_a)
    recordermenu_group.append(label_b)
    recordermenu_group.append(label_c)
    recordermenu_group.append(label_info)
    display.show(recordermenu_group)
    display.refresh()

def showNothing():
    display.show(None)
    display.refresh()

def blankScreen():
    blankScreen_group = displayio.Group()
    blankScreen = rect.Rect(0, 0, 128, 64, fill=0x000000)
    blankScreen_group.append(blankScreen)
    display.show(blankScreen_group)
    display.refresh()

def showSplash(timeout):
    with open("/splash.bmp", "rb") as splashfile:
        bitmap = displayio.OnDiskBitmap(splashfile)
        tilegrid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())
        splash_group = displayio.Group()
        splash_group.append(tilegrid)
        display.show(splash_group)
        display.refresh()

        time.sleep(timeout)

def showVector(xval, yval, length):
    newLength = math.sqrt(math.pow(xval - 64, 2) + math.pow(yval - 32, 2)) * length
    try:
        slope = (yval - 32) / (xval - 64)
    except:
        slope = None
    print((xval, yval, slope, newLength))

    newXVal = xval
    newYVal = yval
    curLength = math.sqrt(math.pow(xval - newXVal, 2) + math.pow(yval - newYVal, 2))

    while (curLength < newLength):
        newXVal -= 1
        newYVal -= slope
        curLength = math.sqrt(math.pow(xval - newXVal, 2) + math.pow(yval - newYVal, 2))

    plotter[0] = line.Line(xval, yval, int(newXVal), int(newYVal), palette[1])

    display.show(plotter)
    display.refresh()


def showGraph(accelList, mode, length):
    if (mode == 1):
        plot_label.text = "X:"
    if (mode == 2):
        plot_label.text = "Y:"
    if (mode == 4):
        plot_label.text = "Z:"

    yValues = []
    for i in accelList:
        mapped = int((i + 10) * (64) / 20)
        yValues.append(mapped)

    yRange = max(yValues) - min(yValues) + 1

    plot = displayio.Bitmap(length, yRange, 2)
    plot.fill(0)

    for x in range(length):
        newMap = int((yValues[x]) * yRange / 64)
        try:
            plot[x, newMap] = 1
        except:
            pass

    plotter[0] = displayio.TileGrid(plot, pixel_shader=palette)
    plotter[0].y = int(32 - yRange/2)
    display.show(plotter)
    display.refresh()