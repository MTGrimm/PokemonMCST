class Stats:
    def __init__(self, hp: int, attack: int, defence: int, sp_attack: int,
                 sp_defence: int, speed: int):
        self.hp = hp
        self.attack = attack
        self.defence = defence
        self.sp_attack = sp_attack
        self.sp_defence = sp_defence
        self.speed = speed

        self.hp_mod = 0
        self.attack_mod = 0
        self.defence_mod = 0
        self.sp_attack_mod = 0
        self.sp_defence_mod = 0
        self.speed_mod = 0

        self.stat_mod = {
                "attack":       self.set_attack_mod,
                "defence":      self.set_defence_mod,
                "sp attack":    self.set_sp_attack_mod,
                "sp defence":   self.set_sp_defence_mod,
                "speed":        self.set_speed_mod
                }

    def get_speed_mod(self):
        if self.speed_mod < 0:
            return 2/(2 + abs(self.speed_mod))
        return (2 + self.speed_mod)/2

    def set_speed_mod(self, speed_mod):
        prev_mod = self.speed_mod
        self.speed_mod = min(6, max(-6, self.speed_mod + speed_mod))
        if prev_mod == self.speed_mod:
            return False
        return True

    def get_sp_defence_mod(self):
        if self.sp_defence_mod < 0:
            return 2/(2 + abs(self.sp_defence_mod))
        return (2 + self.sp_defence_mod)/2

    def set_sp_defence_mod(self, sp_defence_mod):
        prev_mod = self.sp_defence_mod
        self.sp_defence_mod = min(6, max(-6, self.sp_defence_mod + sp_defence_mod))
        if prev_mod == self.sp_defence_mod:
            return False
        return True

    def get_sp_attack_mod(self):
        if self.sp_attack_mod < 0:
            return 2/(2 + abs(self.sp_attack_mod))
        return (2 + self.sp_attack_mod)/2

    def set_sp_attack_mod(self, sp_attack_mod):
        prev_mod = self.sp_attack_mod
        self.sp_attack_mod = min(6, max(-6, self.sp_attack_mod + sp_attack_mod))
        if prev_mod == self.sp_attack_mod:
            return False
        return True

    def get_defence_mod(self):
        if self.defence_mod < 0:
            return 2/(2 + abs(self.defence_mod))
        return (2 + self.defence_mod)/2

    def set_defence_mod(self, defence_mod):
        prev_mod = self.defence_mod
        self.defence_mod = min(6, max(-6, self.defence_mod + defence_mod))
        if prev_mod == self.defence_mod:
            return False
        return True

    def get_attack_mod(self):
        if self.attack_mod < 0:
            return 2/(2 + abs(self.attack_mod))
        return (2 + self.attack_mod)/2

    def set_attack_mod(self, attack_mod):
        prev_mod = self.attack_mod
        self.attack_mod = min(6, max(-6, self.attack_mod + attack_mod))
        if prev_mod == self.attack_mod:
            return False
        return True

    def get_hp_mod(self):
        if self.hp_mod < 0:
            return 2/(2 + abs(self.hp_mod))
        return (2 + self.hp_mod)/2

    def set_hp_mod(self, hp_mod):
        prev_mod = self.hp_mod
        self.hp_mod = min(6, max(-6, self.hp_mod + hp_mod))
        if prev_mod == self.hp_mod:
            return False
        return True

    def get_speed(self):
        return self.speed

    def get_sp_defence(self):
        return self.sp_defence

    def get_sp_attack(self):
        return self.sp_attack

    def get_defence(self):
        return self.defence

    def get_attack(self):
        return self.attack

    def get_hp(self):
        return self.hp
