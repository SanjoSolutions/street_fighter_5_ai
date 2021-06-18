from enum import IntEnum, Enum


class Condition(IntEnum):
    Jumping = 1
    VGaugeAtOrAbove300 = 2
    VGaugeAtOrAbove600 = 3
    VGaugeAtOrAbove900 = 4
    AfterEvadingWithVShift = 5
    DuringVTrigger = 6
    DuringGuard = 7


class Input(IntEnum):
    Forward = 1
    Backward = 2
    Up = 3
    Down = 4
    LP = 5
    MP = 6
    HP = 7
    LMHP = 8
    LK = 9
    MK = 10
    HK = 11
    LMHK = 12


class ActionSpaceRyu(Enum):
    # (inputs, conditions)
    Idle = (tuple(), tuple())
    StandingBlock = (((Input.Backward,),), tuple())
    CrouchingBlock = (((Input.Down, Input.Backward),), tuple())
    Jump = (((Input.Up,),), tuple())
    ForwardJump = (((Input.Up, Input.Forward),), tuple())
    BackwardJump = (((Input.Up, Input.Backward),), tuple())
    StandingLP = (((Input.LP,),), tuple())
    StandingMP = (((Input.MP,),), tuple())
    StandingHP = (((Input.HP,),), tuple())
    StandingLK = (((Input.LK,),), tuple())
    StandingMK = (((Input.MK,),), tuple())
    StandingHK = (((Input.HK,),), tuple())
    CrouchingLP = (((Input.Down, Input.LP),), tuple())
    CrouchingMP = (((Input.Down, Input.MP),), tuple())
    CrouchingHP = (((Input.Down, Input.HP),), tuple())
    CrouchingLK = (((Input.Down, Input.LK),), tuple())
    CrouchingMK = (((Input.Down, Input.MK),), tuple())
    CrouchingHK = (((Input.Down, Input.HK),), tuple())
    JumpingLP = (((Input.LP,),), (Condition.Jumping,))
    JumpingMP = (((Input.MP,),), (Condition.Jumping,))
    JumpingHP = (((Input.HP,),), (Condition.Jumping,))
    JumpingLK = (((Input.LK,),), (Condition.Jumping,))
    JumpingMK = (((Input.MK,),), (Condition.Jumping,))
    JumpingHK = (((Input.HK,),), (Condition.Jumping,))
    CollarboneBreaker = (((Input.Forward, Input.MP),), tuple())
    SolarPlexusStrike = (((Input.Forward, Input.HP),), tuple())
    AxeKick = (((Input.Backward, Input.HK),), tuple())
    ShoulderThrow = (((Input.LP, Input.LK),), tuple())
    SomersaultThrow = (((Input.Backward, Input.LP, Input.LK),), tuple())
    MindsEye = (((Input.MP, Input.MK),), tuple())
    DenjinRenki = (((Input.HP, Input.HK),), (Condition.VGaugeAtOrAbove600,))
    Hashogeki = (((Input.Forward, Input.LMHP),), (Condition.DuringGuard, Condition.VGaugeAtOrAbove300))
    VShift = (((Input.HP, Input.MK),), (Condition.VGaugeAtOrAbove300,))
    FumikomiJodanKagizuki = (((Input.HP, Input.MK),), (Condition.AfterEvadingWithVShift,))
    LHadoken = (((Input.Down,), (Input.Down, Input.Forward), (Input.Forward, Input.LP)), tuple())
    MHadoken = (((Input.Down,), (Input.Down, Input.Forward), (Input.Forward, Input.MP)), tuple())
    HHadoken = (((Input.Down,), (Input.Down, Input.Forward), (Input.Forward, Input.HP)), tuple())
    # Open: V Hadoken with holding buttons
    ExHadoken = (((Input.Down,), (Input.Down, Input.Forward), (Input.Forward, Input.LMHP)), tuple())
    LShoryuken = (((Input.Forward,), (Input.Down,), (Input.Forward, Input.LP)), tuple())
    MShoryuken = (((Input.Forward,), (Input.Down,), (Input.Forward, Input.MP)), tuple())
    HShoryuken = (((Input.Forward,), (Input.Down,), (Input.Forward, Input.HP)), tuple())
    ExShoryuken = (((Input.Forward,), (Input.Down,), (Input.Forward, Input.LMHP)), tuple())
    LTatsumakiSenpukyaku = (((Input.Down,), (Input.Backward, Input.LK)), tuple())
    MTatsumakiSenpukyaku = (((Input.Down,), (Input.Backward, Input.MK)), tuple())
    HTatsumakiSenpukyaku = (((Input.Down,), (Input.Backward, Input.HK)), tuple())
    ExTatsumakiSenpukyaku = (((Input.Down,), (Input.Backward, Input.LMHK)), tuple())
    AirborneTatsumakiSenpukyaku = (((Input.Down,), (Input.Backward, Input.LK)), (Condition.Jumping,))
    ExAirborneTatsumakiSenpukyaku = (((Input.Down,), (Input.Backward, Input.LMHK)), (Condition.Jumping,))
    LJodanSokutouGeri = (((Input.Backward,), (Input.Down,), (Input.Forward, Input.LK)), tuple())
    MJodanSokutouGeri = (((Input.Backward,), (Input.Down,), (Input.Forward, Input.MK)), tuple())
    HJodanSokutouGeri = (((Input.Backward,), (Input.Down,), (Input.Forward, Input.HK)), tuple())
    ExJodanSokutouGeri = (((Input.Backward,), (Input.Down,), (Input.Forward, Input.LMHK)), tuple())
    LShinkuHadoken = (((Input.Down,), (Input.Down, Input.Forward), (Input.Forward,), (Input.Down,), (Input.Down, Input.Forward), (Input.Forward, Input.LP)), (Condition.VGaugeAtOrAbove900,))
    MShinkuHadoken = (((Input.Down,), (Input.Down, Input.Forward), (Input.Forward,), (Input.Down,), (Input.Down, Input.Forward), (Input.Forward, Input.MP)), (Condition.VGaugeAtOrAbove900,))
    HShinkuHadoken = (((Input.Down,), (Input.Down, Input.Forward), (Input.Forward,), (Input.Down,), (Input.Down, Input.Forward), (Input.Forward, Input.HP)), (Condition.VGaugeAtOrAbove900,))
    ExShinkuHadoken = (((Input.Down,), (Input.Down, Input.Forward), (Input.Forward,), (Input.Down,), (Input.Down, Input.Forward), (Input.Forward, Input.LMHP)), (Condition.VGaugeAtOrAbove900,))
    LDenjinHadoken = (((Input.Down,), (Input.Down, Input.Forward), (Input.Forward,), (Input.Down,), (Input.Down, Input.Forward), (Input.Forward, Input.LP)), (Condition.DuringVTrigger, Condition.VGaugeAtOrAbove900))
    MDenjinHadoken = (((Input.Down,), (Input.Down, Input.Forward), (Input.Forward,), (Input.Down,), (Input.Down, Input.Forward), (Input.Forward, Input.MP)), (Condition.DuringVTrigger, Condition.VGaugeAtOrAbove900))
    HDenjinHadoken = (((Input.Down,), (Input.Down, Input.Forward), (Input.Forward,), (Input.Down,), (Input.Down, Input.Forward), (Input.Forward, Input.HP)), (Condition.DuringVTrigger, Condition.VGaugeAtOrAbove900))
    ExDenjinHadoken = (((Input.Down,), (Input.Down, Input.Forward), (Input.Forward,), (Input.Down,), (Input.Down, Input.Forward), (Input.Forward, Input.LMHP)), (Condition.DuringVTrigger, Condition.VGaugeAtOrAbove900))
