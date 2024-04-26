from move import Move
from stats import Stats
import json


class Pokemon:
    type_chart = None

    @classmethod
    def intializeTypes(cls):
        with open("typechart.json", "r") as file:
            cls.type_chart = json.load(file)

    def __init__(self, name: str, types: [str], moves: [Move], stats: Stats):
        self.name = name
        self.types = types
        self.moves = moves
        self.stats = stats
        self.hp = self.stats.get_hp()*20

    def undo_move(self, move: Move, opponent):
        move_type = move.get_move_type()

        if move_type[1] == "physical":
            attack_mod = self.stats.get_attack_mod()
            attack_stat = self.stats.get_attack() * attack_mod

            defence_mod = opponent.get_stats().get_defence_mod()
            defence_stat = opponent.get_stats().get_defence() * defence_mod
        else:
            attack_mod = self.stats.get_sp_attack_mod()
            attack_stat = self.stats.get_sp_attack() * attack_mod

            defence_mod = opponent.get_stats().get_sp_defence_mod()
            defence_stat = opponent.get_stats().get_sp_defence() * defence_mod

        stab = 1.5 if move_type[0] in self.types else 1
        type_boost = 1
        for type in opponent.get_types():
            type_boost *= self.type_chart[move_type[0]][type]

        base_damage = ((((2*100)/5)+2)*move.get_damage()*(attack_stat/defence_stat)+2)/50
        damage = base_damage * stab * type_boost

        opponent.restore_health(damage)
        if move.get_status() != "":
            opponent.take_status(move.get_status())

    def restore_health(self, damage):
        self.hp += damage

    def perform_move(self, move: Move, opponent):
        move_type = move.get_move_type()

        if move_type[1] == "physical":
            attack_mod = self.stats.get_attack_mod()
            attack_stat = self.stats.get_attack() * attack_mod

            defence_mod = opponent.get_stats().get_defence_mod()
            defence_stat = opponent.get_stats().get_defence() * defence_mod
        else:
            attack_mod = self.stats.get_sp_attack_mod()
            attack_stat = self.stats.get_sp_attack() * attack_mod

            defence_mod = opponent.get_stats().get_sp_defence_mod()
            defence_stat = opponent.get_stats().get_sp_defence() * defence_mod

        stab = 1.5 if move_type[0] in self.types else 1
        type_boost = 1
        for type in opponent.get_types():
            type_boost *= self.type_chart[move_type[0]][type]
#       if type_boost == 0.25:
#           print("It was not very effective")
#       elif type_boost == 0.5:
#           print("It was not effective")
#       elif type_boost == 2:
#           print("It was very effective")
#       elif type_boost == 4:
#           print("It was super effective")

        base_damage = ((((2*100)/5)+2)*move.get_damage()*(attack_stat/defence_stat)+2)/50
        damage = base_damage * stab * type_boost

        target = self if move.get_to_self() else opponent
        target.take_damage(damage)
        if move.get_status() != "":
            changed = target.take_status(move.get_status())
            return changed

        return False

    def take_damage(self, damage: int):
        self.hp -= damage

    def take_status(self, status: str):
        status, change = status.split(":")
        action = self.stats.stat_mod[status]
        changed = action(int(change))
        return changed

    def is_dead(self):
        return self.hp <= 0

    def is_alive(self):
        return self.hp > 0

    def get_hp(self):
        return self.hp

    def get_name(self):
        return self.name

    def get_types(self):
        return self.types

    def get_moves(self):
        return self.moves

    def get_stats(self):
        return self.stats
