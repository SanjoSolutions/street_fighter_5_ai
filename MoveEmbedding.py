from enum import IntEnum


class MoveEmbedding(IntEnum):
    StandingLP = 2304
    StandingMP = 2560
    StandingHP = 3072
    StandingLK = 4352
    StandingMK = 4608
    StandingHK = 5120
    CrouchingLP = 2304
    CrouchingMP = 2560
    CrouchingHP = 3072
    CrouchingLK = 4352
    CrouchingMK = 4608
    CrouchingHK = 5120
    CollarboneBreaker = 2562
    SolarPlexusStrike = 3074
    AxeKick = 5122
    ShoulderThrow = 8192
    SomersaultThrow = 2105344
    MindsEye = 32
    DenjinRenki = 128
    Hashogeki = 64
    VShift = 2147483648
    LHadoken = 16644
    MHadoken = 16900
    HHadoken = 17412
    ExHadoken = 16392
    LShoryuken = 260
    MShoryuken = 516
    HShoryuken = 1028
    ExShoryuken = 8
    ShinkuHadoken = 272
    ShinkuHadoken2 = 528
    ShinkuHadoken3 = 1040


move_to_index = dict((move, index) for index, move in enumerate(MoveEmbedding))


def move_to_embedding(move):
    index = move_to_index[move]
    return generate_move_embedding(index)


def generate_move_embedding(move_index):
    embedding = [0] * len(MoveEmbedding)
    embedding[move_index] = 1
    return embedding
