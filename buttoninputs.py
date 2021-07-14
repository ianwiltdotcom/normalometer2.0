import board
import digitalio
import time

buttonA = digitalio.DigitalInOut(board.D9)
buttonA.direction = digitalio.Direction.INPUT
buttonA.pull = digitalio.Pull.UP

buttonB = digitalio.DigitalInOut(board.D6)
buttonB.direction = digitalio.Direction.INPUT
buttonB.pull = digitalio.Pull.UP

buttonC = digitalio.DigitalInOut(board.D5)
buttonC.direction = digitalio.Direction.INPUT
buttonC.pull = digitalio.Pull.UP

def buttonState():
    state = 0
    if buttonA.value == False:
        state += 1
    if buttonB.value == False:
        state += 2
    if buttonC.value == False:
        state += 4
    return state

def nextButton():
    b = buttonState()
    if (b > 0):
        t = time.monotonic()
        while (buttonState()):
            dT = time.monotonic() - t
        if (dT > 1):
            b += 8
        return b
