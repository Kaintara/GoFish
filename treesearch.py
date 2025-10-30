import random
from collections import Counter
import math
import copy

'''
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
'''

class GameEnvironment:
    def __init__(game, amount_of_players):
        game.amount_of_players = amount_of_players

    def auto_move(game,state): #If the Ai knows a player has a card they have they will automatically ask them for it.
        s = copy.deepcopy(state)
        for x in s["history"]:
            if x[2] == 'draw':
                s['history'].remove(x)
        history = s["history"][-(game.amount_of_players *2):]
        Ai = state["current_player"][1]
        known_hands = {k: [] for k, a in s["hands"].items() if k != Ai}
        auto_moves = []

        for i in history:
            if i[2] == 'took' and i[0] != Ai:
                known_hands[i[0]].append(i[1])
            elif i[2] == 'ask' and i[0] != Ai:
                known_hands[i[0]].append(i[1])

        for card in s["hands"][Ai]:
            rank = card[0]
            for player, known_cards in known_hands.items():
                if any(c[0] == rank for c in known_cards):
                    auto_moves.append((player, rank, 'ask'))

        for move in auto_moves:
            if move in history:
                auto_moves.remove(move)
        try:
            return random.choice(auto_moves)
        except:
            return None
        
    def determinization(game,state): #Function will calculate what cards players have and then assume the rest for the first part of the ISMCTS
        copied = copy.deepcopy(state)
        Ai = copied["current_player"][1]
        hands = {k: v for k, v in copied["hands"].items() if k != Ai}

        Determined_hands = {k: [] for k in copied["hands"].keys()}
        Determined_hands[f"{Ai}"] = copied["hands"][Ai]

        deck = copied["deck"][:]
        for x in [c for l,c in copied["hands"].items() if l != Ai]:
            deck.extend(x)
        random.shuffle(deck)
        history = copied["history"]
        if not history:
            for i in range(game.amount_of_players):
                if f'player{i+1}' != Ai:
                    for x in range(0,8):
                        Determined_hands[f'player{i+1}'].append(deck.pop())

        for i in history:
            if i[2] == 'took' and i[0] != Ai:
                try:
                    deck.remove(i[1])
                    Determined_hands[i[0]].append(i[1])
                except:
                    continue
                
        for i in history:
            if i[2] == 'ask' and i[0] != Ai:
                lst = [x for x in deck if x.startswith(i[1])]
                if lst:
                    card = lst[random.randint(0,len(lst)-1)]
                    Determined_hands[i[0]].append(card)
                    deck.remove(card)
        for i in history:
            if i[0] != Ai:
                if len(hands[i[0]]) != len(Determined_hands[i[0]]):
                    while len(Determined_hands[i[0]]) < len(hands[i[0]]) and len(deck) > 1:
                        card = deck[random.randint(0,len(deck)-1)]
                        Determined_hands[i[0]].append(card)
                        deck.remove(card)
        copied["hands"] = Determined_hands
        return copied

    def get_legal_moves(game,state):
        asks = []
        index, player_name = state["current_player"]
        hand = state["hands"][player_name]
        for x in hand:
            asks.append(x[0])
        asks = list(dict.fromkeys(asks))
        available = []
        for i in range(game.amount_of_players):
            if f"player{i+1}" != player_name and len(state["hands"][f'player{i+1}']) > 0:
                 available.append(i)
        moves = []
        for card in asks:
            for option in available:
                    moves.append((f'player{option+1}',card,'ask')) 
        return moves
    
    def remove_set(game, rank, hand):
        remove_cards = [f"{rank}D", f"{rank}S", f"{rank}H", f"{rank}C"]
        for card in remove_cards:
            if card in hand:
                hand.remove(card)
    
    def check_for_sets(game,state):
        for player, hand in state["hands"].items():
            ranks = [card[:-1] for card in hand]
            counts = Counter(ranks)
            sets = [rank for rank, count in counts.items() if count == 4]
            for set in sets:
                state["sets"][player].append(set)
                game.remove_set(set,hand)

    def apply_move(game,state,move):
        s = copy.deepcopy(state)
        current_index = s["current_player"][0]
        current_name = f"player{current_index + 1}"
        target_player, rank, action = move
        history = s["history"]
        history.append(move)
        asked_hand = s["hands"][target_player]
        Correct = False
        for card in asked_hand:
            if rank == card[0]:
                Correct = True
                history.append((s["current_player"][1],card,'took',target_player))
                s["hands"][current_name].append(card)
                asked_hand.remove(card)
        if Correct:
            s["current_player"] = (current_index, current_name)
        else:
            if s["deck"]:
                s["hands"][current_name].append(s["deck"][0])
                s["deck"].remove(s["deck"][0])
        next_index = (current_index + 1) % game.amount_of_players
        s["current_player"] = (next_index, f'player{next_index + 1}')
        s["history"] = history

        game.check_for_sets(s)
        return s

    def is_terminal(game,state):
        return (not state["deck"]) and all(len(hand) == 0 for hand in state["hands"].values())
    
    def get_reward(game,state,index):
        for hand in state["hands"][f'player{index+1}']:
            ranks = [card[:-1] for card in hand]
            counts = Counter(ranks)
            near_sets = [rank for rank, count in counts.items() if count == 3]
            if near_sets:
                return len(state["sets"][f'player{index+1}']) + int(len(near_sets)*0.5)
            else:
                return len(state["sets"][f'player{index+1}'])




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
    
    def best_child(self,c_param=1.41):
        choices = []
        for child in self.children:
            if not self.children:
                return None
            if child.visits == 0:
                UCT = float('inf')
            else:
                UCT = (child.value / child.visits) + (c_param * math.sqrt(2 * math.log(self.visits + 1)/child.visits))
            choices.append(UCT)
        if not choices:
            return None
        return self.children[choices.index(max(choices))]
    
    def simulations(self,state,game_env):
        s = copy.deepcopy(state)
        for x in range(5):
            moves = game_env.get_legal_moves(s)
            if not moves:
                break
            move = random.choice(moves)
            s = game_env.apply_move(s,move)
        return s



def one_level_mcts(root_state,root_player,game_env,iterations):
        det_root = game_env.determinization(root_state)
        root_node = Node(det_root, parent=None, move_from_parent=None)
        root_node.untried_moves = game_env.get_legal_moves(root_node.state)
        print(root_node.untried_moves)
        for move in root_node.untried_moves:
            child_state = game_env.apply_move(det_root, move)
            child_node = Node(child_state, root_node, move)
            root_node.children.append(child_node)
            child_node.untried_moves = []
        for _ in range(iterations):
                child = random.choice(root_node.children)
                if not child:
                    continue
                sim_state = copy.deepcopy(child.state)
                final_state = child.simulations(sim_state,game_env)
                reward = game_env.get_reward(final_state, root_player)
                if not reward:
                    child.value += 0
                else:
                    child.value += reward
                child.visits += 1
                
        best_child = max(root_node.children, key=lambda c: c.value / c.visits if c.visits > 0 else 0)
        return (root_node.best_child(1.4)).move_from_parent

def two_level_mcts(root_state,root_player,game_env,iterations):
        det_root = game_env.determinization(root_state)
        root_node = Node(det_root, parent=None, move_from_parent=None)
        root_node.untried_moves = game_env.get_legal_moves(root_node.state)
        for move in root_node.untried_moves:
            first_child_state = game_env.apply_move(det_root, move)
            first_child_node = Node(first_child_state, root_node, move)
            root_node.children.append(first_child_node)
            sec_moves = game_env.get_legal_moves(first_child_state)
            for sec_move in sec_moves:
                sec_child_state = game_env.apply_move(first_child_state, sec_move)
                sec_child_node = Node(sec_child_state, first_child_node, sec_move)
                first_child_node.children.append(sec_child_node)

        for _ in range(iterations):
            for first_child in root_node.children:
                if not first_child.children:
                        continue
                child = random.choice(first_child.children)
                sim_state = copy.deepcopy(child.state)
                final_state = child.simulations(sim_state,game_env)
                reward = game_env.get_reward(final_state, root_player)
                child.visits += 1
                if not reward:
                    child.value += 0
                else:
                    child.value += reward
        
        for first_child in root_node.children:
            if first_child.children:
                first_child.visits = sum(child.visits for child in first_child.children)
                first_child.value = sum(child.value for child in first_child.children)
        return (root_node.best_child(1.4)).move_from_parent
    
def three_level_mcts(root_state,root_player,game_env,iterations):
        det_root = game_env.determinization(root_state)
        root_node = Node(det_root, parent=None, move_from_parent=None)
        root_node.untried_moves = game_env.get_legal_moves(root_node.state)
        for move in root_node.untried_moves:
            first_child_state = game_env.apply_move(det_root, move)
            first_child_node = Node(first_child_state, root_node, move)
            root_node.children.append(first_child_node)
            first_child_node.untried_moves = game_env.get_legal_moves(first_child_state)
            for sec_move in first_child_node.untried_moves:
                sec_child_state = game_env.apply_move(first_child_state, sec_move)
                sec_child_node = Node(sec_child_state, first_child_node, sec_move)
                first_child_node.children.append(sec_child_node)
                third_moves = game_env.get_legal_moves(sec_child_state)
                for third_move in third_moves:
                    thi_child_state = game_env.apply_move(sec_child_state,third_move)
                    thi_child_node = Node(thi_child_state,sec_child_node,third_move)
                    sec_child_node.children.append(thi_child_node)

        for _ in range(iterations):
            for first_child in root_node.children:
                for sec_child in first_child.children:
                    if not sec_child.children:
                        continue
                    child = random.choice(sec_child.children)
                    sim_state = copy.deepcopy(child.state)
                    final_state = child.simulations(sim_state,game_env)
                    reward = game_env.get_reward(final_state, root_player)
                    child.visits += 1
                    if not reward:
                        child.value += 0
                    else:
                        child.value += reward

        for first_child in root_node.children:
            for sec_child in first_child.children:
                if sec_child.children:
                    sec_child.visits = sum(child.visits for child in sec_child.children)
                    sec_child.value = sum(child.value for child in sec_child.children)

                if first_child.children:
                    first_child.visits = sum(child.visits for child in first_child.children)
                    first_child.value = sum(child.value for child in first_child.children)
        return (root_node.best_child(1.4)).move_from_parent
