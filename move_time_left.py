from pymem import Pymem
import time

pm = Pymem('StreetFighterV.exe')

while True:
    value = pm.read_int(0x28B850B791C)
    if value > 0:
        move_id = pm.read_int(0x28B850B79E8)
        print(str(move_id) + ': ' + str(value))
    time.sleep(0.001)
