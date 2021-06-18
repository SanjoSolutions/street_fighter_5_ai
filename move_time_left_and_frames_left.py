from pymem import Pymem
import time

pm = Pymem('StreetFighterV.exe')

FPS = 60

while True:
    move_time_left = pm.read_int(0x28B850B791C)
    if move_time_left > 0:
        move_id = pm.read_int(0x28B850B79E8)
        frames_left = pm.read_int(0x28C05BB9774)
        print(str(move_id) + ': ' + str(move_time_left) + ', ' + str(frames_left))
        time.sleep(1 / FPS)
