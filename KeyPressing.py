from enum import IntEnum

from interception.interception import *
from ctypes import *

MAPVK_VK_TO_VSC = 0


class VirtualKeyCode(IntEnum):
    A = 0x41
    B = 0x42
    D = 0x44
    G = 0x47
    H = 0x48
    J = 0x4A
    K = 0x4B
    M = 0x4D
    N = 0x4E
    S = 0x53
    W = 0x57
    OEM_COMMA = 0xBC


class KeyPressing:
    def __init__(self):
        self.context = interception()
        self.keyboard = self.get_keyboard()

    def get_keyboard(self):
        for i in range(MAX_DEVICES):
            if interception.is_keyboard(i):
                return i
        return None

    def press_key(self, key):
        scan_code = windll.user32.MapVirtualKeyA(key, MAPVK_VK_TO_VSC)
        key_press = key_stroke(
            scan_code,
            interception_key_state.INTERCEPTION_KEY_DOWN.value,
            0
        )
        self.context.send(self.keyboard, key_press)

    def release_key(self, key):
        scan_code = windll.user32.MapVirtualKeyA(key, MAPVK_VK_TO_VSC)
        key_release = key_stroke(
            scan_code,
            interception_key_state.INTERCEPTION_KEY_UP.value,
            0
        )
        self.context.send(self.keyboard, key_release)
