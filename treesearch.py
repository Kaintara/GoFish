from GameEnvironment import Game

Go_Fish = Game(3)

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0.0

state = {'Hand':[],
        'P1_Sets':[],
        'P2_Sets':[],
        'P3_Sets':[],
        'P4_Sets':[]}