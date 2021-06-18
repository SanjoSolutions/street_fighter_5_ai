from ctypes import cdll

from mss import mss
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import cv2 as cv
from ctypes import *

from KeyPressing import KeyPressing, VirtualKeyCode
from buttons import BUTTONS_COUNT, BUTTON_STATES_COUNT
from video import VIDEO_WIDTH, VIDEO_HEIGHT


pressed_keys = [False] * BUTTONS_COUNT
key_bindings = (
    VirtualKeyCode.W,
    VirtualKeyCode.A,
    VirtualKeyCode.S,
    VirtualKeyCode.D,
    VirtualKeyCode.G,
    VirtualKeyCode.H,
    VirtualKeyCode.J,
    VirtualKeyCode.K,
    VirtualKeyCode.B,
    VirtualKeyCode.N,
    VirtualKeyCode.M,
    VirtualKeyCode.OEM_COMMA,
)


def release_keys(key_pressing):
    for key in key_bindings:
        key_pressing.release_key(key)


def do_action(key_pressing, action):
    for index in range(0, BUTTONS_COUNT, BUTTON_STATES_COUNT):
        press_index = index
        release_index = index + 1
        key_index = int(index / 2)
        key_binding = key_bindings[key_index]
        if action[press_index] > 0.5 and action[release_index] <= 0.5:
            if not pressed_keys[key_index]:
                key_pressing.press_key(key_binding)
                pressed_keys[key_index] = True
        elif action[release_index] > 0.5 and action[press_index] <= 0.5:
            if pressed_keys[key_index]:
                key_pressing.release_key(key_binding)
                pressed_keys[key_index] = False


class Rect(Structure):
    _fields_ = [
        ('left', c_long),
        ('top', c_long),
        ('right', c_long),
        ('bottom', c_long),
    ]


if __name__ == '__main__':
    model = load_model(r'D:\model_5')
    key_pressing = KeyPressing()
    release_keys(key_pressing)

    with mss() as screenshotter:
        hwnd = cdll.user32.FindWindowW(None, 'StreetFighterV')
        rect = Rect()
        succeeded = cdll.user32.GetWindowRect(hwnd, pointer(rect))
        title_bar_height = 32
        padding_left = 8
        padding_right = 8
        padding_bottom = 9
        window = {
            'left': rect.left + padding_left,
            'top': rect.top + title_bar_height,
            'width': rect.right - rect.left - padding_left - padding_right,
            'height': rect.bottom - rect.top - title_bar_height - padding_bottom,
        }
        while True:
            # RGB
            screenshot = screenshotter.grab(window)
            frame = np.array(screenshot.pixels, dtype=np.uint8)
            frame = cv.resize(frame, (VIDEO_WIDTH, VIDEO_HEIGHT))
            frame = np.array(frame, dtype=np.float32)
            frame /= 255.0
            frame = np.pad(
                frame,
                (
                    (0, VIDEO_WIDTH - frame.shape[0]),
                    (0, VIDEO_WIDTH - frame.shape[1]),
                    (0, 0)
                ),
                'constant',
                constant_values=0
            )
            frames = np.array([frame], dtype=np.float32)
            # action = model.predict(frames)[0]
            action = model(frames).numpy()[0]
            action[action > 0.5] = 1
            action[action <= 0.5] = 0
            # action = [0] * (BUTTONS_COUNT * BUTTON_STATES_COUNT)
            # action[0] = 1
            # action = np.array(action)
            print('action', action)
            do_action(key_pressing, action)
