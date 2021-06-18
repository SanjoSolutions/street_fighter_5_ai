class State:
    def __init__(self):
        self.players = [
            Player(),
            Player()
        ]
        self.time_left


class Player:
    def __init__(self):
        self.hp
        self.stun_meter
        self.v_skill
        self.v_trigger_meter
        self.v_trigger_active
        self.crtitical_art_meter
        self.move
        self.position

# Move database with:
# * damage
# * start up frames count
# * active frames count
# * recovery frames count
