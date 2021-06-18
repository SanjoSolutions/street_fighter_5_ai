from pymem import Pymem
import time

pm = Pymem('StreetFighterV.exe')

while True:
    frames_left = pm.read_int(0x26D86053FF4)
    if frames_left > 0:
        move_id = pm.read_int(0x26D65EAE9E8)
        print(str(move_id) + ': ' + str(frames_left))
