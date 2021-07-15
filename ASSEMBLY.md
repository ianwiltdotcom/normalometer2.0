# Assembly
Want to build your own Normalometer 2.0? Follow these assembly instructions.

## Bill of Materials
Most parts can be ordered from [Adafruit](https://adafruit.com).

- [Adafruit Feather RP2040](https://www.adafruit.com/product/4884)
- [128x64 OLED FeatherWing](https://www.adafruit.com/product/4650)
- [Adafruit LIS3DH Accelerometer](https://www.adafruit.com/product/2809)
- [100mAh LiPoly Battery](https://www.adafruit.com/product/1570)
- [Adafruit Feather Female Headers](https://www.adafruit.com/product/2886)
- [JST-SH STEMMA QT cable (50mm)](https://www.adafruit.com/product/4399)
- 3D printed housing (see below)

## 3D Printing
The housing for the device can be 3D printed. The model is located under `extras/BatteryHolder12mm USBC.stl` Print in a sturdy material such as PLA with no supports and a higher (>50%) infill density.

## Assembly

1. Solder male headers onto the pins of the OLED FeatherWing, and solder the female headers onto the pins of the Feather RP2040.
2. Using the STEMMA QT cable, connect the accelerometer to the QT connector on the OLED FeatherWing.
3. Place the accelerometer face-up in the housing. Allow the cable to go through the "U" shaped hole on the side of the housing.
4. Place the battery between the female headers of the Feather RP2040, routing the wires around the side of the battery connector.
5. Place the housing on top of the battery, ensuring the accelerometer goes between the female headers.
6. Snap the screen on top of the female headers, making sure the STEMMA QT cable's slack is inside of the device.