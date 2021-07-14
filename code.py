import accelerometer
import buttoninputs
import screen
import time
import csvfile
import math

screen.showSplash(1)

usbConnected = False
try:
    csvfile.unlock()
except:
    usbConnected = True
    print("USB connected")

if not accelerometer.isConnected():
    print("Hisssss!\nNo accelerometer!\nCheck the cable!")
    screen.showNothing()
    while True:
        pass

screen.showMainMenu()

def rawDataViewLoop(length):
    accelList = []
    for i in range(length):
        accelList.append(0)
    mode = 1

    while True:
        if (mode == 1):
            accelList[length - 1] = accelerometer.getXAcceleration()
        if (mode == 2):
            accelList[length - 1] = accelerometer.getYAcceleration()
        if (mode == 4):
            accelList[length - 1] = accelerometer.getZAcceleration()
        j = 0
        for i in range(length - 1):
            accelList[j] = accelList[j + 1]
            j = j + 1
        screen.showGraph(accelList, mode, length)

        button = buttoninputs.nextButton()
        if (button):
            for i in range(length):
                accelList[i] = 0
            mode = button

def vectorLoop():
    while True:
        x = accelerometer.getXAcceleration() / 9.81
        y = -1 * accelerometer.getYAcceleration() / 9.81
        r = math.sqrt(math.pow(x, 2) + math.pow(y, 2))

        x1 = int((x + 1) * (128) / 2)
        #x1 = int((x + 1) * (64) / 2) + 32
        y1 = int((y + 1) * (64) / 2)
        #y1 = int((y + 1) * (128) / 2) - 32

        while (x1 > 0 and x1 < 128 and y1 > 0 and y1 < 64):
            x1 += (x1 > 64)
            x1 -= (x1 < 64)
            y1 += (y1 > 32)
            y1 -= (y1 < 32)
            if (x1 == 64 or y1 == 32):
                break

        screen.showVector(x1, y1, r)

def recordData():
    screen.countdown(3)
    datalist = []
    t = time.monotonic()
    dt = 0
    while (dt < recorderTime):
        datalist.append(dt)
        if (recorderMode & 1):
            datalist.append(accelerometer.getXAcceleration())
        if (recorderMode & 2):
            datalist.append(accelerometer.getYAcceleration())
        if (recorderMode & 4):
            datalist.append(accelerometer.getZAcceleration())
        dt = time.monotonic() - t
    screen.saveText(0, 0)
    savedFile = csvfile.saveFile(datalist, recorderMode)
    screen.saveText(1, savedFile)
    while True:
        pass

menuMode = 0 #Main Menu
recorderMode = 1
recorderTime = 1
sleepTime = time.monotonic()

while True:
    button = buttoninputs.nextButton()
    if (menuMode == 1):
        if (button == 1):
            recorderTime += 1
            screen.showRecorderMenu(recorderTime, recorderMode)
        if (button == 9):
            recorderTime = 1
            screen.showRecorderMenu(recorderTime, recorderMode)
        if (button == 2):
            if (recorderMode == 7):
                recorderMode = 1
            else:
                recorderMode += 1
            screen.showRecorderMenu(recorderTime, recorderMode)
        if (button == 4):
            recordData()

    if (menuMode == 0):
        if (button == 1):
            vectorLoop()
        if (button == 2):
            rawDataViewLoop(64)
        if (button == 10): #hold and release B
            rawDataViewLoop(128)
        if (button == 4):
            if (not usbConnected):
                screen.showRecorderMenu(recorderTime, recorderMode)
                menuMode = 1
            else:
                screen.errorText()
                time.sleep(3)
                screen.showMainMenu()
                sleepTime = time.monotonic()

    sleepCheck = time.monotonic() - sleepTime
    if (sleepCheck > 30 and menuMode == 0):
        print("30 seconds without input. Time to sleep.")
        screen.blankScreen()
        b = 0
        while (b == 0):
            b = buttoninputs.buttonState()
        print("Wake up!")
        screen.showMainMenu()
        sleepTime = time.monotonic()