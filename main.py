import math
import os
import pickle
import sys
from enum import IntEnum

from pymem import Pymem

from ActionSpaceRyu import ActionSpaceRyu, Condition, Input
from KeyPressing import KeyPressing, VirtualKeyCode
from a import A
from ctypes import *
import time


class Rect(Structure):
    _fields_ = [
        ('left', c_long),
        ('top', c_long),
        ('right', c_long),
        ('bottom', c_long),
    ]


class ActionType(IntEnum):
    PrimaryMouseClickAt = 1
    KeyPress = 2
    Idle = 3


class Environment:
    def __init__(self):
        self.key_pressing = KeyPressing()
        self.process = Pymem('StreetFighterV.exe')
        self.hwnd = cdll.user32.FindWindowW(None, 'StreetFighterV')
        rect = Rect()
        succeeded = cdll.user32.GetWindowRect(self.hwnd, pointer(rect))
        title_bar_height = 32
        padding_left = 8
        padding_right = 8
        padding_bottom = 9
        self.window = {
            'left': rect.left + padding_left,
            'top': rect.top + title_bar_height,
            'width': rect.right - rect.left - padding_left - padding_right,
            'height': rect.bottom - rect.top - title_bar_height - padding_bottom,
        }

    def do_action(self, action):
        if self.is_done():
            raise AssertionError(
                '"do_action" was called when environment was done. ' +
                'Please make sure to reset the environment first.'
            )
        while windll.user32.GetForegroundWindow() != self.hwnd:
            time.sleep(1)

        state = self.get_state()

        input_to_keys = {
            Input.Forward: lambda: (VirtualKeyCode.D,) if self.is_character_on_left(state) else (VirtualKeyCode.A,),
            Input.Backward: lambda: (VirtualKeyCode.A,) if self.is_character_on_left(state) else (VirtualKeyCode.D,),
            Input.Up: VirtualKeyCode.W,
            Input.Down: VirtualKeyCode.S,
            Input.LP: VirtualKeyCode.G,
            Input.MP: VirtualKeyCode.H,
            Input.HP: VirtualKeyCode.J,
            Input.LMHP: VirtualKeyCode.K,
            Input.LK: VirtualKeyCode.B,
            Input.MK: VirtualKeyCode.N,
            Input.HK: VirtualKeyCode.M,
            Input.LMHK: VirtualKeyCode.OEM_COMMA
        }

        input_to_keys = dict(self.convert_input_to_key_mapping_to_lambda_function(input, key) for input, key in input_to_keys.items())

        print('Doing action: ' + action.name)

        inputs, conditions = action.value
        for inputs_entry in inputs:
            for input in inputs_entry:
                keys = input_to_keys[input]()
                for key in keys:
                    self.key_pressing.press_key(key)
            time.sleep(0.1)
            for input in inputs_entry:
                keys = input_to_keys[input]()
                for key in keys:
                    self.key_pressing.release_key(key)

    def convert_input_to_key_mapping_to_lambda_function(self, input, key):
        if isinstance(key, VirtualKeyCode):
            return input, lambda: (key,)
        elif isinstance(key, tuple):
            return input, lambda: key
        else:
            return input, key

    def is_character_on_left(self, state):
        character_1_x = state[0]
        character_2_x = state[9]
        return character_1_x <= character_2_x

    def reset(self):
        pass

    def is_done(self):
        state = self.get_state()
        character_1_health_points = state[8]
        character_2_health_points = state[17]
        return character_1_health_points == 0 or character_2_health_points == 0

    def get_available_actions(self):
        state = self.get_state()
        character_1_move_time_left = state[2]
        if character_1_move_time_left > 0:  # TODO: Implement cancelables
            return {ActionSpaceRyu.Idle}
        else:
            return set(filter(self.is_action_available, ActionSpaceRyu))

    def is_action_available(self, action):
        inputs, conditions = action.value
        condition_checkers = {
            Condition.Jumping: self.is_jumping,
            Condition.VGaugeAtOrAbove300: self.is_v_gauge_at_or_above_300,
            Condition.VGaugeAtOrAbove600: self.is_v_gauge_at_or_above_600,
            Condition.VGaugeAtOrAbove900: self.is_v_gauge_at_or_above_900,
            Condition.AfterEvadingWithVShift: self.is_after_evading_with_v_shift,
            Condition.DuringVTrigger: self.is_during_v_trigger,
            Condition.DuringGuard: self.is_during_guard
        }
        return all(
            condition_checkers[condition]() for condition in conditions
        )

    def is_jumping(self):
        state = self.get_state()
        character_1_standing_crouching_jumping = state[4]
        return character_1_standing_crouching_jumping == 4

    def is_v_gauge_at_or_above_300(self):
        return self.is_v_gauge_at_or_above(300)

    def is_v_gauge_at_or_above_600(self):
        return self.is_v_gauge_at_or_above(600)

    def is_v_gauge_at_or_above_900(self):
        return self.is_v_gauge_at_or_above(900)

    def is_v_gauge_at_or_above(self, value):
        state = self.get_state()
        character_1_v_bar = state[6]
        return character_1_v_bar >= value

    def is_after_evading_with_v_shift(self):
        return False  # TODO: Implement

    def is_during_v_trigger(self):
        state = self.get_state()
        character_1_v_trigger_active_time_left = state[7]
        return character_1_v_trigger_active_time_left > 0

    def is_during_guard(self):
        return False  # TODO: Implement

    def get_state(self):
        character_1_x_base_address = read_pointer(self.process, self.process.base_address + 0x03CFDCD0, (
            0x288,
            0x1F0,
            0x58,
            0x18,
            0x290,
            0x50
        ))
        character_1_x = self.process.read_float(character_1_x_base_address + 0xC0)

        character_1_y_base_address = read_pointer(self.process, self.process.base_address + 0x03CFDCD0, (
            0x288,
            0x1F0,
            0x58,
            0x18,
            0x290,
            0x50
        ))
        character_1_y = self.process.read_float(character_1_y_base_address + 0xC8)

        character_1_move_time_left_base_address = read_pointer(self.process, self.process.base_address + 0x03CFDCD0, (
            0x288,
            0x1F0,
            0x20,
            0x998,
            0x1B8,
            0x18
        ))
        character_1_move_time_left = self.process.read_int(character_1_move_time_left_base_address + 0x914)

        character_1_move_id_base_address = read_pointer(self.process, self.process.base_address + 0x03CFDCD0, (
            0x288,
            0x1F0,
            0x20,
            0x998,
            0x1B8,
            0x18
        ))
        character_1_move_id = self.process.read_int(character_1_move_id_base_address + 0x9E0)

        character_1_standing_crouching_jumping_base_address = read_pointer(self.process, self.process.base_address + 0x03CFDCD0, (
            0x288,
            0x1F0,
            0x20,
            0x998,
            0x1B8,
            0x18
        ))
        character_1_standing_crouching_jumping = self.process.read_int(character_1_standing_crouching_jumping_base_address + 0xCBC)

        character_1_critical_art_bar_base_address = read_pointer(self.process,
            self.process.base_address + 0x03CFDCD0, (
                0x288,
                0x1F0,
                0x20,
                0x998,
                0x1B8,
                0x18
            )
        )
        character_1_critical_art_bar = self.process.read_int(character_1_critical_art_bar_base_address + 0xCE4)

        character_1_v_bar_base_address = read_pointer(self.process,
            self.process.base_address + 0x03CFDCD0, (
                0x288,
                0x1F0,
                0x20,
                0x998,
                0x1B8,
                0x18
            )
        )
        character_1_v_bar = self.process.read_int(character_1_v_bar_base_address + 0xCEC)

        character_1_v_trigger_active_time_left_base_address = read_pointer(self.process, self.process.base_address + 0x03CFDCD0, (
            0x288,
            0x1F0,
            0x20,
            0x998,
            0x1B8,
            0x18
        ))
        character_1_v_trigger_active_time_left = self.process.read_int(
            character_1_v_trigger_active_time_left_base_address + 0xCF0
        )

        character_1_health_points_base_address = read_pointer(self.process, self.process.base_address + 0x03CFDCD0, (
            0x170,
            0x0,
            0x70,
            0x50,
            0x258,
            0x30
        ))
        character_1_health_points = self.process.read_int(
            character_1_health_points_base_address + 0x47C
        )

        character_2_x_base_address = read_pointer(self.process, self.process.base_address + 0x03CFDCD0, (
            0x288,
            0x200,
            0x58,
            0x18,
            0x3E0,
            0x10
        ))
        character_2_x = self.process.read_float(character_2_x_base_address + 0xC0)

        character_2_y_base_address = read_pointer(self.process, self.process.base_address + 0x03CFDCD0, (
            0x288,
            0x200,
            0x58,
            0x18,
            0x3E0,
            0x10
        ))
        character_2_y = self.process.read_float(character_2_y_base_address + 0xC8)

        character_2_move_time_left_base_address = read_pointer(self.process, self.process.base_address + 0x03A15660, (
            0x8,
            0x48,
            0x28,
            0x10,
            0x98,
            0xF0
        ))
        character_2_move_time_left = self.process.read_int(character_2_move_time_left_base_address + 0x91C)

        character_2_move_id_base_address = read_pointer(self.process, self.process.base_address + 0x03A15660, (
            0x8,
            0x48,
            0x28,
            0x10,
            0x98,
            0xF0
        ))
        character_2_move_id = self.process.read_int(character_2_move_id_base_address + 0x9E8)

        character_2_standing_crouching_jumping_base_address = read_pointer(
            self.process,
            self.process.base_address + 0x03A15660, (
                0x8,
                0x48,
                0x28,
                0x10,
                0x98,
                0xF0
            )
        )
        character_2_standing_crouching_jumping = self.process.read_int(
            character_2_standing_crouching_jumping_base_address + 0xCC4
        )

        character_2_critical_art_bar_base_address = read_pointer(self.process,
            self.process.base_address + 0x03A15660, (
                0x8,
                0x48,
                0x28,
                0x10,
                0x98,
                0xF0
            )
        )
        character_2_critical_art_bar = self.process.read_int(character_2_critical_art_bar_base_address + 0xCEC)

        character_2_v_bar_base_address = read_pointer(self.process,
            self.process.base_address + 0x03A15660, (
                0x8,
                0x48,
                0x28,
                0x10,
                0x98,
                0xF0
            )
        )
        character_2_v_bar = self.process.read_int(character_2_v_bar_base_address + 0xCF4)

        character_2_v_trigger_active_time_left_base_address = read_pointer(
            self.process,
            self.process.base_address + 0x03A15660, (
                0x8,
                0x48,
                0x28,
                0x10,
                0x98,
                0xF0
            )
        )
        character_2_v_trigger_active_time_left = self.process.read_int(
            character_2_v_trigger_active_time_left_base_address + 0xCF8
        )

        character_2_health_points_base_address = read_pointer(self.process, self.process.base_address + 0x03CFDCD0, (
            0x170,
            0x0,
            0x70,
            0x50,
            0x98,
            0xA8
        ))
        character_2_health_points = self.process.read_int(
            character_2_health_points_base_address + 0x11C
        )

        state = (
            character_1_x,
            character_1_y,
            character_1_move_time_left,
            character_1_move_id,
            character_1_standing_crouching_jumping,
            character_1_critical_art_bar,
            character_1_v_bar,
            character_1_v_trigger_active_time_left,
            character_1_health_points,
            character_2_x,
            character_2_y,
            character_2_move_time_left,
            character_2_move_id,
            character_2_standing_crouching_jumping,
            character_2_critical_art_bar,
            character_2_v_bar,
            character_2_v_trigger_active_time_left,
            character_2_health_points
        )

        return state


def read_pointer(process: Pymem, base_address, offsets):
    address = process.read_ulonglong(base_address)
    for offset in offsets:
        address += offset
        address = process.read_ulonglong(address)
    return address


class Database:
    def __init__(self):
        self.state_to_explored_actions = dict()
        self.state_and_action_to_state = dict()
        self.state_to_state_and_action_pairs_that_lead_to_it = dict()
        self.state_to_unexplored_actions_count = dict()

    def store(self, state_before_action, action, state_after_action):
        state_before_action = tuple(state_before_action)
        state_after_action = tuple(state_after_action)
        if state_before_action not in self.state_to_explored_actions:
            self.state_to_explored_actions[state_before_action] = set()
        self.state_to_explored_actions[state_before_action].add(action)

        self.state_and_action_to_state[(state_before_action, action)] = \
            state_after_action

        if state_after_action not in self.state_to_state_and_action_pairs_that_lead_to_it:
            self.state_to_state_and_action_pairs_that_lead_to_it[state_after_action] = set()
        self.state_to_state_and_action_pairs_that_lead_to_it[state_after_action].add(
            (state_before_action, action)
        )

    def query_explored_actions(self, state):
        state = tuple(state)
        return self.state_to_explored_actions[state] if state in self.state_to_explored_actions else set()

    def query_action_that_lead_to_state_with_highest_metric_value(self, state, determine_metric_value):
        state = tuple(state)
        explored_actions = self.state_to_explored_actions[state]
        return max(
            determine_metric_value(self.state_and_action_to_state[(state, action)])
            for action
            in explored_actions
        )

    def query_state_with_highest_metric_value(self, determine_metric_value):
        return max(self.state_and_action_to_state.values(), key=lambda state: determine_metric_value(state))

    def query_state_and_action_pairs_which_lead_to_state(self, state):
        state = tuple(state)
        return (
            self.state_to_state_and_action_pairs_that_lead_to_it[state]
            if state in self.state_to_state_and_action_pairs_that_lead_to_it
            else set()
        )

    def store_unexplored_actions_count(self, state, unexplored_actions_count):
        state = tuple(state)
        self.state_to_unexplored_actions_count[state] = unexplored_actions_count

    def query_total_known_unexplored_actions_count(self, state):
        visited_states = set()
        state = tuple(state)
        count = 0
        states = [state]
        while len(states) >= 1:
            next_states = []
            for state in states:
                if state not in visited_states:
                    unexplored_actions_count = self.query_unexplored_actions_count(state)
                    if unexplored_actions_count is not None:
                        count += unexplored_actions_count
                    if state in self.state_to_explored_actions:
                        actions = self.state_to_explored_actions[state]
                        next_states += [self.state_and_action_to_state[(state, action)] for action in actions]
                    visited_states.add(state)
            states = next_states
        return count

    def query_unexplored_actions_count(self, state):
        return (
            self.state_to_unexplored_actions_count[state]
            if state in self.state_to_unexplored_actions_count
            else None
        )

    def query_state(self, state, action):
        state = tuple(state)
        state_and_action_pair = (state, action)
        return (
            self.state_and_action_to_state[state_and_action_pair]
            if state_and_action_pair in self.state_and_action_to_state
            else None
        )

    def query_closest_state_with_explored_actions(self, state):
        return min(
            self.state_to_explored_actions.keys(),
            key=lambda state_b: state_distance(state, state_b)
        )


# def distance(state_a, state_b):
#     result = 0
#     for index in range(len(state_a)):
#         result += (state_b[index] - state_a[index]) ** 2
#     return result

def state_distance(state_a, state_b):
    character_1_x_a = state_a[0]
    character_1_y_a = state_a[1]
    character_2_x_a = state_a[9]
    character_2_y_a = state_a[10]
    character_1_x_b = state_b[0]
    character_1_y_b = state_b[1]
    character_2_x_b = state_b[9]
    character_2_y_b = state_b[10]
    return (
        distance((character_1_x_a, character_1_y_a), (character_2_x_a, character_2_y_a)) -
        distance((character_1_x_b, character_1_y_b), (character_2_x_b, character_2_y_b))
    ) ** 2


def distance(a, b):
    return math.sqrt(
        (b[0] - a[0]) ** 2 +
        (b[1] - a[1]) ** 2
    )


def determine_metric_value(state):
    character_1_health_points = state[8]
    character_2_health_points = state[17]
    return character_1_health_points - character_2_health_points


database_path = 'D:/street_fighter_v/database.pickle'


def save_database(database):
    with open(database_path, 'wb') as file:
        pickle.dump(database, file, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    if os.path.isfile(database_path):
        with open(database_path, 'rb') as file:
            database = pickle.load(file)
    else:
        database = Database()
    environment = Environment()
    a = A()
    try:
        # a.explore(environment, database, 100000)
        # print('explored states: ' + str(len(database.state_to_explored_actions)))
        #
        # save_database(database)

        # # environment.reset()
        # path_to_outcome = a.evaluate(environment, database, determine_metric_value)
        # print(path_to_outcome)

        while True:
            state = database.query_closest_state_with_explored_actions(environment.get_state())
            # state = environment.get_state()
            actions = database.query_explored_actions(state)
            if len(actions) >= 1:
                action = max(
                    actions,
                    key=lambda action: determine_metric_value(database.query_state(state, action))
                )
                environment.do_action(action)
                print(action.name)
    except KeyboardInterrupt:
        print('Interrupted')

        save_database(database)

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
