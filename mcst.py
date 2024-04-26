from node import Node
from pokemon import Pokemon
from stats import Stats
from move import Move
from policy import DefaultPolicy, TreePolicy, EpsilonGreedyPolicy
import copy
import time
import math


class MCST:
    def __init__(self, e: float):
        self.dp = DefaultPolicy()
        self.tp = TreePolicy()
        self.egp = EpsilonGreedyPolicy(e)
        self.c = 3

    def run2(self, start_node: Node, duration: int):
        start_time = time.time()
        node = start_node
        while time.time() - start_time < duration:
            node = self.search(node)

        return node

    def run(self, start_node: Node, duration: int):
        node = start_node
        while node.get_player().is_alive() and node.get_opponent().is_alive():
            start_time = time.time()
            while time.time() - start_time < duration:
                node = self.search(node)
            player = node.get_player()
            if node.get_turn():
                max_util = -math.inf
                max_move = None
                for move in player.get_moves():
                    if node.get_util(move) > max_util:
                        max_util = node.get_util(move)
                        max_move = move
                print(max_move.get_name())
                node = node.select_child(max_move)
            else:
                min_util = math.inf
                min_move = None
                for move in player.get_moves():
                    if node.get_util(move) < min_util:
                        min_util = node.get_util(move)
                        min_move = move
                print(min_move.get_name())
                node = node.select_child(min_move)

        return start_node

    def search(self, node: Node):
        search_path = self.select_path(node)
        utility = self.dp.simulate(copy.deepcopy(search_path[-1][0]))
        self.backpropagate(search_path, utility)
        return search_path[0][0]

    def select_path(self, node: Node):
        path = []
        player = node.get_player()
        opponent = node.get_opponent()
        move = None
        current_node = node
        while player.is_alive() and opponent.is_alive():
            # move = self.tp.select_action(current_node, self.c)
            move = self.egp.select_action(current_node)
            path.append((current_node, move))
            new_node = current_node.select_child(move)
            if new_node is None:
                new_node = current_node.create_child(move)
                player = new_node.get_player()
                opponent = new_node.get_opponent()
                opponent.perform_move(move, player)  # since we switched
                return path
            current_node = new_node
            player = current_node.get_player()
            opponent = current_node.get_opponent()

        return path

    def backpropagate(self, path: (Node, int), utility: int):
        for node, move in path:
            node.increment_visit()
            node.increment_action(move)
            node.adjust_utility(move, utility)


def print_tree(node: Node, value="root", level=0):
    if node is not None:
        print("  " * level + str(value))
        for i, child in enumerate(node.children):
            print_tree(child, node.get_util(node.get_player().get_moves()[i]), level + 1)


if __name__ == "__main__":
    Pokemon.intializeTypes()
    charizard_moves = []
    charizard_stats = Stats(78, 84, 78, 109, 85, 100)
    flamethrower = Move("flamethrower", ["fire", "sp"], 70, "", 10, False)
    self_flame = Move("self flame", ["fire", "sp"], 10, "sp attack:2", 10, True)
    sunthrower = Move("sunthrower", ["fire", "sp"], 90, "", 10, False)
    self_sun = Move("self sun", ["fire", "sp"], 5, "sp attack:4", 10, True)
    charizard_moves.append(flamethrower)
    charizard_moves.append(self_flame)
    charizard_moves.append(sunthrower)
    charizard_moves.append(self_sun)
    charizard = Pokemon("charizard", ["fire"], charizard_moves, charizard_stats)

    blastoise_moves = []
    blastoise_stats = Stats(78, 84, 78, 109, 85, 100)
    water_gun = Move("water gun", ["water", "sp"], 18, "", 10, False)
    sp_soak = Move("sp soak", ["water", "sp"], 0, "sp defence:-1", 10, False)
    hydro_jet = Move("hydro jet", ["water", "sp"], 30, "", 10, False)
    sp_hoze = Move("sp hoze", ["water", "sp"], 0, "sp defence:-2", 10, False)
    blastoise_moves.append(water_gun)
    blastoise_moves.append(sp_soak)
    blastoise_moves.append(hydro_jet)
    blastoise_moves.append(sp_hoze)
    blastoise = Pokemon("blastoise", ["water"], blastoise_moves, blastoise_stats)

    mcst1 = MCST(0.05)
    start1 = Node(copy.deepcopy(charizard), copy.deepcopy(blastoise), True)
    print("Moves chosen for epsilon of 0.05: ")
    finish1 = mcst1.run(start1, 1)

    mcst2 = MCST(0.10)
    start2 = Node(copy.deepcopy(charizard), copy.deepcopy(blastoise), True)
    print("Moves chosen for epsilon of 0.10: ")
    finish2 = mcst2.run(start2, 1)

    mcst3 = MCST(0.20)
    start3 = Node(charizard, blastoise, True)
    print("Moves chosen for epsilon of 0.20: ")
    finish3 = mcst3.run(start3, 1)

    mcst4 = MCST(0.40)
    start4 = Node(charizard, blastoise, True)
    print("Moves chosen for epsilon of 0.40: ")
    finish4 = mcst4.run(start4, 1)
