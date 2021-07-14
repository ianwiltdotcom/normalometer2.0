import board
import adafruit_lis3dh
import math

i2c = board.I2C()

try:
    lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)
except:
    lis3dh = None

def getXAcceleration():
    return lis3dh.acceleration.x

def getYAcceleration():
    return lis3dh.acceleration.y

def getZAcceleration():
    return lis3dh.acceleration.z

def isConnected():
    if (lis3dh):
        return True
    else:
        return False