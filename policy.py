from node import Node
import random
import math
import copy


class Policy:
    def __init__(self):
        pass


class DefaultPolicy(Policy):
    def __init__(self):
        pass

    def select_action(self, actions):
        return random.choice(actions)

    def simulate(self, node: Node):
        initial_node = copy.deepcopy(node)
        total_util = 0
        num_sims = 0
        for i in range(100):
            node = copy.deepcopy(initial_node)
            player = node.get_player()
            opponent = node.get_opponent()
            turn = node.get_turn()
            while player.is_alive() and opponent.is_alive():
                move = self.select_action(player.get_moves())
                player.perform_move(move, opponent)
                turn = not turn
                temp = player
                player = opponent
                opponent = temp

            if turn:
                total_util += player.get_hp() - opponent.get_hp()
            else:
                total_util += opponent.get_hp() - player.get_hp()
            num_sims += 1
        return total_util/num_sims


class TreePolicy(Policy):
    def __init__(self):
        pass

    def select_action(self, node: Node, c: int):
        # turn = True -> max player, turn = False -> min player
        # c -> exploration constant
        max_value = -math.inf
        min_value = math.inf
        max_move = None
        min_move = None

        for move in node.get_player().get_moves():
            visited = node.get_visited()
            chosen = node.get_chosen(move)
            if chosen == 0:
                # print("not chosen:", move.get_name())
                return move
            exploration_term = c*(math.sqrt(math.log10(visited)/chosen))
            utility = node.get_util(move)

            if node.get_turn():
                value = utility + exploration_term
                if value > max_value:
                    max_value = value
                    max_move = move
            else:
                value = utility - exploration_term
                if value < min_value:
                    min_value = value
                    min_move = move

        if node.get_turn():
            return max_move
        return min_move


class EpsilonGreedyPolicy(Policy):
    def __init__(self, epsilon):
        self.epsilon = epsilon

    def select_action(self, node: Node):
        greedy = random.random() > self.epsilon
        if greedy:
            max = -math.inf
            min = math.inf
            max_action = None
            min_action = None
            for move in node.get_player().get_moves():
                chosen = node.get_chosen(move)
                if chosen == 0:
                    return move
                if node.get_turn():
                    if node.get_util(move) > max:
                        max = node.get_util(move)
                        max_action = move
                else:
                    if node.get_util(move) < min:
                        min = node.get_util(move)
                        min_action = move

            if node.get_turn():
                return max_action
            return min_action
        else:
            return random.choice(node.get_player().get_moves())
