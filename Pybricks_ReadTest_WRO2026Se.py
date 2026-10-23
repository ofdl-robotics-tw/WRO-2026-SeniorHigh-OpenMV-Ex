# OFDL Robotics Lab Taiwan = Anthony 2026
# WRO 2026 SeniorHigh OpenMV Example

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

from pybricks.iodevices import PUPDevice # For OpenMV Cam
Camera = PUPDevice(Port.B) # OpenMV Cam Object

while True:
    val = Camera.read(0)
    digits = []
    for num in val[:4]:  # Only read index 0-3
        hundreds = num // 100
        tens = (num % 100) // 10
        ones = num % 10
        digits.extend([hundreds, tens, ones])
    
    # Print 12 Digits
    print("Digits: %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d" % tuple(digits))
    wait(30)