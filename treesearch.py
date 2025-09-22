import random
import copy
from collections import Counter

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


def determinization(state): #Function will calculate what cards players have and then assume the rest for the first part of the ISMCTS
    Ai = state["current_player"][1]
    hands = {k: v for k, v in state["hands"].items() if k != Ai}

    Determined_hands = {k: [] for k, a in state["hands"].items() if k != Ai}
    Determined_hands["Ai_hand"] = state["hands"][Ai]

    deck = state["deck"]
    for x in [c for l,c in state["hands"].items() if l != Ai]:
        deck.extend(x)

    history = state["history"]

    for i in history:
        if i[2] == 'took' and i[0] != Ai:
            Determined_hands[i[0]].append(i[1])
            deck.remove(i[1])
    for i in history:
        if i[2] == 'ask' and i[0] != Ai:
            lst = [x for x in deck if x.startswith(i[1])]
            card = lst[random.randint(0,len(lst)-1)]
            Determined_hands[i[0]].append(card)
            deck.remove(card)
    for i in history:
        if i[0] != Ai:
            if len(hands[i[0]]) != len(Determined_hands[i[0]]):
                while len(Determined_hands[i[0]]) < len(hands[i[0]]):
                    card = deck[random.randint(0,len(deck)-1)]
                    Determined_hands[i[0]].append(card)
                    deck.remove(card)

    return Determined_hands

print(determinization(test_state))
print(all(len(hand) == 0 for hand in test_state["hands"]))

class GameEnvironment:
    def __init__(game, amount_of_players):
        super().__init__(amount_of_players)

    def get_legal_moves(state):
        player = state["current_player"][0]
        hand = state["hands"]
        #for x in players[playernum]:
       #     asks.append(x[0])
        asks = list(dict.fromkeys(asks))
        available = []
      #  for i in range(game.amount_of_players):
      #      if i != (playernum) and len(players[i]) > 0:
      #           available.append(i)
        moves = []
        for card in asks:
            for player in available:
                    moves.append((f'player{player+1}',card,'ask')) 
        return moves

    def clone_state(self, state):
        return copy.deepcopy(state)
    
    def is_terminal(state):
        return (not state["deck"]) and all(len(hand) == 0 for hand in state["hands"].values())
    





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
        return self.untried_moves is None and len(self.untried_moves) == 0