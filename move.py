class Move:
    def __init__(self, name: str, move_type: [str], damage: int, status: str, pp: int, to_self: bool):
        self.name = name
        self.move_type = move_type
        self.damage = damage
        self.status = status
        self.pp = pp
        self.to_selp = to_self

    def get_name(self):
        return self.name

    def get_move_type(self):
        return self.move_type

    def get_damage(self):
        return self.damage

    def get_status(self):
        return self.status

    def get_to_self(self):
        return self.to_selp
