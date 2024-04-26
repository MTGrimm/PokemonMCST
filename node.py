from move import Move
from pokemon import Pokemon
import copy


class Node:
    def __init__(self, pl0: Pokemon, pl1: Pokemon, turn: bool):
        self.player = pl0 if turn else pl1
        self.opponent = pl1 if turn else pl0
        self.turn = turn
        self.children = [None, None, None, None]
        self.move_names = [move.get_name() for move in self.player.get_moves()]
        self.action_utilities = dict.fromkeys(self.move_names, 0)
        self.action_chosen = dict.fromkeys(self.move_names, 0)
        self.visited = 0

    def create_child(self, move):
        pl0 = self.player if self.turn else self.opponent
        pl1 = self.opponent if self.turn else self.player
        child = Node(copy.deepcopy(pl0), copy.deepcopy(pl1), not self.turn)
        index = self.move_names.index(move.get_name())
        self.children[index] = child
        return child

    def select_child(self, move: Move):
        index = self.move_names.index(move.get_name())
        return self.children[index]

    def increment_visit(self):
        self.visited += 1

    def increment_action(self, move: Move):
        self.action_chosen[move.get_name()] += 1

    def adjust_utility(self, move: Move, utility: int):
        old_util = self.action_utilities[move.get_name()]
        new_util = old_util + (utility - old_util)/self.get_chosen(move)
        self.action_utilities[move.get_name()] = new_util

    def get_player(self):
        return self.player

    def get_opponent(self):
        return self.opponent

    def get_turn(self):
        return self.turn

    def get_util(self, move: Move):
        return self.action_utilities[move.get_name()]

    def get_visited(self):
        return self.visited

    def get_chosen(self, move: Move):
        return self.action_chosen[move.get_name()]

    def has_children(self):
        for child in self.children:
            if child is not None:
                return True
        return False

    def __str__(self):
        moves = ""
        current_node = self
        while current_node.has_children():
            print(current_node.get_player().get_name())
            if self.get_turn():
                max_action = max(current_node.action_utilities, key=current_node.action_utilities.get)
                for move in current_node.get_player().get_moves():
                    if move.get_name() == max_action:
                        moves += max_action + " -> "
                        current_node = current_node.select_child(move)
                        continue
            else:
                min_action = min(current_node.action_utilities, key=current_node.action_utilities.get)
                for move in current_node.get_player().get_moves():
                    if move.get_name() == min_action:
                        moves += min_action + " -> "
                        current_node = current_node.select_child(move)
                        continue
        return moves
