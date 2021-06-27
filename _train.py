import re
from datetime import datetime, timedelta

import cv2 as cv
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.initializers import Zeros
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError
import numpy as np

from buttons import BUTTONS_COUNT, BUTTON_STATES_COUNT
from video import VIDEO_WIDTH, VIDEO_HEIGHT
from tensorflow_hub import KerasLayer


def open_video(path):
    return cv.VideoCapture(path)


def parse_video_creation_time(video_path):
    match = re.match(r'.*StreetFighterV (\d\d\d\d)-(\d\d)-(\d\d) (\d\d)-(\d\d)-(\d\d)-(\d\d\d)\.mp4', video_path)
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        hour = int(match.group(4))
        minute = int(match.group(5))
        second = int(match.group(6))
        millisecond = int(match.group(7))
        time = datetime(year, month, day, hour, minute, second, millisecond * 1000)
        return time
    else:
        raise ValueError('Failed to retrieve creation time from video path.')


def read_data(video, video_creation_time, actions):
    data = []
    last_frame_time = None
    first_action_index = 0
    while True:
        frame_time = video_creation_time + timedelta(milliseconds=video.get(cv.CAP_PROP_POS_MSEC))
        return_value, frame = video.read()
        if not return_value:
            return data
        if actions[first_action_index][0] <= frame_time:
            frame = cv.resize(frame, (VIDEO_WIDTH, VIDEO_HEIGHT))
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
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
            last_action_index = first_action_index
            while last_action_index < len(actions) - 1:
                action_index = last_action_index + 1
                action = actions[action_index]
                if (
                    action[0] <= frame_time and
                    (last_frame_time is None or action[0] > last_frame_time)
                ):
                    last_action_index = action_index
                else:
                    break
            frame_actions = actions[first_action_index:last_action_index+1]
            action = to_action(frame_actions)
            entry = (frame, action)
            data.append(entry)
            first_action_index = last_action_index + 1
            if first_action_index >= len(actions):
                return data
        last_frame_time = frame_time


def to_action(frame_actions):
    action = [0] * (BUTTONS_COUNT * 2)
    for frame_action in frame_actions:
        code = frame_action[1]
        state = frame_action[2]
        if code == 'ABS_HAT0Y' and state == 0:
            action[0] = 1
            action[4] = 1
        elif code == 'ABS_HAT0X' and state == 0:
            action[2] = 1
            action[6] = 1
        elif code in {'BTN_WEST', 'BTN_NORTH', 'BTN_TR', 'BTN_TL', 'BTN_SOUTH', 'BTN_EAST', 'ABS_RZ', 'ABS_Z'}:
            index = frame_action_to_action_index(frame_action)
            action[index + (0 if is_press(frame_action) else 1)] = 1
    return action


def frame_action_to_action_index(frame_action):
    code = frame_action[1]
    state = frame_action[2]
    if code in {'ABS_HAT0X', 'ABS_HAT0Y', 'ABS_RZ', 'ABS_Z'}:
        if code == 'ABS_HAT0X':
            if state == -1:
                action_index = 2
            elif state == 1:
                action_index = 6
            else:
                raise ValueError('Unexpected value for status: ' + str(state))
        elif code == 'ABS_HAT0Y':
            if state == -1:
                action_index = 0
            elif state == 1:
                action_index = 4
            else:
                raise ValueError('Unexpected value for state: ' + str(state))
        elif code == 'ABS_RZ':
            action_index = 20
        elif code == 'ABS_Z':
            action_index = 22
    else:
        mapping = {
            'BTN_WEST': 8,
            'BTN_NORTH': 10,
            'BTN_TR': 12,
            'BTN_TL': 14,
            'BTN_SOUTH': 16,
            'BTN_EAST': 18,
        }
        if code in mapping:
            action_index = mapping[code]
        else:
            raise ValueError('Unexpected value for code: ' + code)

    return action_index


def is_press(frame_action):
    code = frame_action[1]
    state = frame_action[2]
    if code in {'ABS_HAT0X', 'ABS_HAT0Y', 'ABS_RZ', 'ABS_Z'}:
        is_press = True if state != 0 else False
    else:
        is_press = True if state == 0 else False
    return is_press


def read_actions(file):
    actions = []
    line = file.readline()
    while line:
        action = parse_action_entry(line)
        actions.append(action)
        line = file.readline()
    return actions


def parse_action_entry(line):
    match = re.match(r'\((\d+\.\d+), \'(.+?)\', (-?\d+)\)', line)
    if match:
        timestamp = datetime.fromtimestamp(float(match.group(1)))
        code = match.group(2)
        state = int(match.group(3))
        action = (timestamp, code, state)
        return action
    else:
        raise ValueError('match failed')


actions_file = open('actions_3.txt')
actions = read_actions(actions_file)
actions_file.close()
video_path = 'D:\\StreetFighterV 2021-06-13 06-29-24-000.mp4'
video_creation_time = parse_video_creation_time(video_path)
video = open_video(video_path)
data = read_data(video, video_creation_time, actions)
video.release()

model = Sequential([
    KerasLayer(
        "https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4",
        input_shape=(224, 224, 3),
        trainable=False
    ),
    Dense(1048, activation='relu'),
    Dense(BUTTONS_COUNT * BUTTON_STATES_COUNT, kernel_initializer=Zeros()),
])

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss=MeanSquaredError(),
)
# model = load_model('model')

x = np.array([entry[0] for entry in data])
y = np.array([entry[1] for entry in data])
model.fit(
    x=x,
    y=y,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    callbacks=[
        EarlyStopping(patience=1)
    ]
)

model.save(r'D:\model_5')
