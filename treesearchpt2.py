import random
from collections import Counter
import copy
import math

#########################
# Game Environment Class
#########################
class GameEnvironment:
    def __init__(self, amount_of_players):
        self.amount_of_players = amount_of_players

    def determinization(self, state):
        """
        Create a fully determinized state for ISMCTS from partial observation.
        This guesses unknown cards for other players based on history.
        """
        s = copy.deepcopy(state)
        ai_name = s["current_player"][1]
        known_hands = {k: v for k, v in s["hands"].items() if k != ai_name}
        det_hands = {k: [] for k in known_hands}
        det_hands[ai_name] = s["hands"][ai_name][:]

        deck = s["deck"][:]
        for cards in known_hands.values():
            deck.extend(cards)

        # Apply history to refine determinization
        for move in s["history"]:
            player, rank, action = move[:3]
            if action == "took" and player != ai_name:
                det_hands[player].append(move[1])
                if move[1] in deck:
                    deck.remove(move[1])
            elif action == "ask" and player != ai_name:
                candidates = [c for c in deck if c.startswith(rank)]
                if candidates:
                    card = random.choice(candidates)
                    det_hands[player].append(card)
                    deck.remove(card)

        # Fill remaining unknown cards randomly
        for player in det_hands:
            if player != ai_name and len(det_hands[player]) < len(s["hands"][player]):
                while len(det_hands[player]) < len(s["hands"][player]):
                    card = deck.pop(random.randrange(len(deck)))
                    det_hands[player].append(card)

        s["hands"] = det_hands
        return s

    def get_legal_moves(self, state):
        """
        Returns list of valid moves for current player: ('ask', 'target_player', 'rank')
        """
        moves = []
        current_index, current_name = state["current_player"]
        hand = state["hands"][current_name]
        ranks_in_hand = list(dict.fromkeys([c[0] for c in hand]))
        for target_index in range(self.amount_of_players):
            target_name = f"player{target_index+1}"
            if target_name != current_name and state["hands"][target_name]:
                for rank in ranks_in_hand:
                    moves.append(("ask", target_name, rank))
        return moves

    def remove_set(self, rank, hand):
        """
        Removes a completed set (4 cards of same rank) from a hand
        """
        for suit in "DSHC":
            card = f"{rank}{suit}"
            if card in hand:
                hand.remove(card)

    def check_for_sets(self, state):
        """
        Moves completed sets from hands to sets dict
        """
        for player, hand in state["hands"].items():
            counts = Counter([c[0] for c in hand])
            for rank, count in counts.items():
                if count == 4:
                    state["sets"][player].append(rank)
                    self.remove_set(rank, hand)

    def apply_move(self, state, move):
        """
        Apply a move to a state and return the resulting state
        """
        s = copy.deepcopy(state)
        current_index, current_name = s["current_player"]
        action, target_player, rank = move
        history = s["history"]
        history.append(move)

        # Ask target player's hand
        target_hand = s["hands"][target_player]
        successful = False
        for card in target_hand[:]:
            if card[0] == rank:
                successful = True
                s["hands"][current_name].append(card)
                target_hand.remove(card)
                history.append((current_name, card, "took", target_player))

        # If failed, draw a card
        if not successful and s["deck"]:
            s["hands"][current_name].append(s["deck"].pop(0))
            # Move turn to next player
            next_index = (current_index + 1) % self.amount_of_players
            s["current_player"] = (next_index, f"player{next_index+1}")
        elif successful:
            # Stay on current player if successful
            s["current_player"] = (current_index, current_name)

        s["history"] = history
        self.check_for_sets(s)
        return s

    def is_terminal(self, state):
        """
        Returns True if the game is over (deck empty and all hands empty)
        """
        return not state["deck"] and all(len(h) == 0 for h in state["hands"].values())

    def get_reward(self, state, player_index):
        """
        Returns reward (number of sets) for player_index
        """
        player_name = f"player{player_index+1}"
        return len(state["sets"][player_name])

#########################
# Node Class for MCTS
#########################
class Node:
    def __init__(self, state, parent=None, move_from_parent=None):
        self.state = state
        self.parent = parent
        self.move_from_parent = move_from_parent
        self.children = []
        self.untried_moves = None
        self.visits = 0
        self.value = 0.0

    def tried_all_moves(self):
        return self.untried_moves is not None and len(self.untried_moves) == 0

    def best_child(self, c_param=1.41):
        """
        UCT calculation to select best child node
        """
        choices = []
        for child in self.children:
            if child.visits == 0:
                uct = float('inf')
            else:
                uct = (child.value / child.visits) + c_param * math.sqrt(2 * math.log(self.visits + 1) / child.visits)
            choices.append(uct)
        return self.children[choices.index(max(choices))]

    def simulate(self, game_env):
        """
        Perform a random rollout from current node until terminal state
        """
        s = copy.deepcopy(self.state)
        while not game_env.is_terminal(s):
            moves = game_env.get_legal_moves(s)
            if not moves:
                break
            move = random.choice(moves)
            s = game_env.apply_move(s, move)
        return s

#########################
# ISMCTS Function
#########################
def ismcts(root_state, root_player, game_env, iterations=3, c_param=1.41, num_determinizations=5):
    """
    Runs ISMCTS to find best move for root_player
    """

    # Precompute a set of determinized states for faster computation
    determinized_states = [game_env.determinization(root_state) for _ in range(num_determinizations)]

    root_node = Node(random.choice(determinized_states))
    root_node.untried_moves = game_env.get_legal_moves(root_node.state)

    for _ in range(iterations):
        # Pick a determinized state randomly
        det_state = random.choice(determinized_states)
        node = root_node

        # 1) Selection
        while node.tried_all_moves() and not game_env.is_terminal(node.state):
            node = node.best_child(c_param=c_param)

        # 2) Expansion
        if not game_env.is_terminal(node.state):
            if node.untried_moves is None:
                node.untried_moves = game_env.get_legal_moves(node.state)
            if node.untried_moves:
                move = node.untried_moves.pop(random.randrange(len(node.untried_moves)))
                new_state = game_env.apply_move(det_state, move)
                child = Node(new_state, parent=node, move_from_parent=move)
                child.untried_moves = game_env.get_legal_moves(new_state)
                node.children.append(child)
                node = child

        # 3) Simulation
        terminal_state = node.simulate(game_env)

        # 4) Backpropagation
        reward = game_env.get_reward(terminal_state, root_player)
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent

    # Return best move by visit count
    best_child = max(root_node.children, key=lambda c: c.visits)
    return best_child.move_from_parent

#########################
# Example usage
#########################

test_state = {'hands': 
         {'player1': 
          ['JS', '7S', '2H', '3C', '8S', '4S', 'JD', 'AC'], 
          'player2': ['9S', '6S', '2D', 'QH', '5C', '4D', 'JC'], 
          'player3': ['AS', '3H', '9C', '8C', '9D', 'AH', '1D', '1S', '5H'], 
          'player4': ['KH', '1C', 'KD', '8D', '6C', '5S', '7C', '4C', '3D', '7D', '6D', '5D']}, 
          'sets': {'player1': [], 'player2': [], 'player3': [], 'player4': []}, 
          'deck': ['QD', 'KC', '2S', 'AD', '2C', '7H', '6H', 'QS', '4H', '1H', 'KS', '9H', '8H', '3S', 'QC', 'JH'], 
          'current_player': (3,'player4'), 
          'history': [('player2', 'K', 'ask'), 
                      ('player4', '3D', 'draw'), 
                      ('player3', '7', 'ask'), 
                      ('player1', 'AC', 'draw'), 
                      ('player1', 'Q', 'ask'), 
                      ('player2', '1S', 'draw'), 
                      ('player2', '1', 'ask'), 
                      ('player3', '1S', 'took', 'player2'), 
                      ('player4', 'A', 'ask'), 
                      ('player3', '5H', 'draw'), 
                      ('player2', '7', 'ask'), 
                      ('player4', '7D', 'took', 'player2'), 
                      ('player3', '6', 'ask'), 
                      ('player4', '6D', 'took', 'player3'), 
                      ('player1', '5', 'ask'), 
                      ('player4', '5D', 'took', 'player1')]}


env = GameEnvironment(amount_of_players=4)
root_player = 3  # player4 (0-indexed)
best_move = ismcts(root_state=test_state, root_player=root_player, game_env=env,
                       iterations=3, num_determinizations=5)
print("Best move for player4:", best_move)