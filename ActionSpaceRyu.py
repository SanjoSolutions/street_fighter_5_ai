from enum import IntEnum


class Condition(IntEnum):
    Jumping


class Input(IntEnum):
    Forward
    Backward
    Up
    Down
    LP
    MP
    HP
    LMHP
    LK
    MK
    HK
    LMHK


class ActionSpaceRyu():
    StandingLP = Input.LP
    StandingMP = Input.MP
    StandingHP = Input.HP
    StandingLK = Input.LK
    StandingMK = Input.MK
    StandingHK = Input.HK
    CrouchingLP = {Input.Down, Input.LP}
    CrouchingMP = {Input.Down, Input.MP}
    CrouchingHP = {Input.Down, Input.HP}
    CrouchingLK = {Input.Down, Input.LK}
    CrouchingMK = {Input.Down, Input.MK}
    CrouchingHK = {Input.Down, Input.HK}
    JumpingLP = {
        'conditions': {Condition.Jumping},
        'inputs': Input.LP
    },
    JumpingMP = {
        'conditions': {Condition.Jumping},
        'inputs': Input.MP
    },
    JumpingHP = {
        'conditions': {Condition.Jumping},
        'inputs': Input.HP
    },
    JumpingLK = {
        'conditions': {Condition.Jumping},
        'inputs': Input.LK
    },
    JumpingMK = {
        'conditions': {Condition.Jumping},
        'inputs': Input.MK
    },
    JumpingHK = {
        'conditions': {Condition.Jumping},
        'inputs': Input.HK
    }
