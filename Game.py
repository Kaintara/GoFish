import random
from collections import Counter
from treesearch import * 

class Game:
    def __init__(game,amount_of_players):
        game.amount_of_players = amount_of_players
        game.deck = ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"]
        game.shuffled_deck = []
        game.rank_order = {
            'A': 14,
            'K': 13,
            'Q': 12,
            'J': 11,
            '1': 10,
            '9': 9,
            '8': 8,
            '7': 7,
            '6': 6,
            '5': 5,
            '4': 4,
            '3': 3,
            '2': 2
        }
        game.hands = [[] for _ in range(amount_of_players)]
        game.sets = [[] for _ in range(amount_of_players)]
        game.turn = ''
        game.history = []
        game.state = {
            "hands": {},
            "sets": {},
            "deck" : game.shuffled_deck,
            "current_player": game.turn,
            "history": [],
        }
        game.env = GameEnvironment(amount_of_players)

        
    def Update_GameState(game):
        for i in range (0,game.amount_of_players):
            game.state["hands"][f'player{i+1}'] = list(game.hands[i])
            game.state["sets"][f'player{i+1}'] = list(game.sets[i])
            game.state["deck"] = list(game.shuffled_deck)
            game.state["current_player"] = (game.turn,f'player{game.turn+1}')
            game.state["history"] = list(game.history)

    def shuffle_cards(game):
        shuffled_deck = game.deck[:]
        random.shuffle(shuffled_deck)
        game.shuffled_deck = shuffled_deck #replace this with random.shuffle()
            
    def distribute_cards(game):
        players = game.hands
        for i in range(0,8):
            for player in players:
                player.append(game.shuffled_deck.pop())

    def draw_card(game,playernum):
        players = game.hands
        if game.shuffled_deck != []:
            players[playernum].append(game.shuffled_deck.pop())
            game.history.append((f'player{playernum + 1}',players[playernum][-1],'draw'))
            game.Update_GameState()

    def remove_set(game,card,hand):
        print(card)
        remove = [card+'D',card+'S',card+'H',card+'C']
        print(remove)
        for card in remove:
            hand.remove(card)

    def sort_cards(game):
        players = game.hands
        for x in players:
            x.sort(key=(lambda a : game.rank_order[a[0]]))
            print(x)


    def check_for_sets(game):
        players = game.hands
        for x in players:
            counter = []
            for card in x:
                counter.append(card[:-1])
            counts = Counter(counter)
            sets = [card for card, count in counts.items() if count == 4]
            if sets != []:
                for set in sets:
                    index = game.hands.index(x)
                    game.sets[index].append(set)
                    game.remove_set(set,x)
                    
    def next_vaild_player(game,playernum):
        for i in range(1, game.amount_of_players + 1):
            nvp = (playernum + i) % game.amount_of_players
            if game.hands[nvp] or game.shuffled_deck:
                return nvp
        return None

    def get_valid_moves(game,playernum):
        players = game.hands
        asks = []
        for x in players[playernum]:
            asks.append(x[0])
        asks = list(dict.fromkeys(asks))
        available = []
        for i in range(game.amount_of_players):
            if i != (playernum) and len(players[i]) > 0:
                available.append(i)
        moves = []
        for card in asks:
            for player in available:
                    moves.append((f'player{player+1}',card,'ask')) 
        return moves
                

    def is_game_over(game):
        return game.shuffled_deck == [] and all(len(hand) == 0 for hand in game.hands)


    def player_turn(game,playernum):
        moves = game.get_valid_moves(playernum)
        if not moves:
            if game.shuffled_deck:
                game.draw_card(playernum)
            nvp = game.next_vaild_player(playernum)
            if nvp is not None:
                game.turn = nvp
            return
        i = random.randint(0,len(moves)-1)
        game.history.append(moves[i])
        game.Update_GameState()
        if playernum == 1:
            move = game.expert_call()
            print("BOT")
        else:
            move = moves[i]
        target_player = int(move[0][6:]) - 1
        card = move[1]
        Correct = False

        for x in game.hands[target_player][:]:
            if card == x[0]:
                Correct = True
                game.history.append((f'player{(playernum+1)}',x,'took',f'player{(target_player+1)}'))
                game.Update_GameState()
                game.hands[playernum].append(x)
                game.hands[target_player].remove(x)
        if not Correct:
            nvp = None
            if game.shuffled_deck:
                game.draw_card(playernum)
                nvp = game.next_vaild_player(playernum)
            if any(len(hand) == 0 for hand in game.hands):
                nvp = game.next_vaild_player(playernum)
            if nvp is not None:
                game.turn = nvp
            else:
                game.turn = None

    def game_loop(game):
        game.shuffle_cards()
        game.distribute_cards()
        print(game.state)
        game.turn = random.randint(0,game.amount_of_players - 1)
        while not game.is_game_over() and game.turn is not None:
            game.Update_GameState()
            print(game.state)
            game.check_for_sets()
            game.player_turn(game.turn)
            input()
        for x in game.sets:
            print(x)

    def beginner_call(game):
        return one_level_mcts(game.state,game.turn,game.env,2)

    def easy_call(game):
        if random.randint(0,3) == 4:
            move = game.env.auto_move(game.state)
            if move:
                return move
            else:
                return one_level_mcts(game.state,game.turn,game.env,4)
        else:
            return one_level_mcts(game.state,game.turn,game.env,4)

    def medium_call(game):
        if random.randint(0,1) == 1:
            move = game.env.auto_move(game.state)
            if move:
                return move
            else:
                return two_level_mcts(game.state,game.turn,game.env,5)
        else:
            return two_level_mcts(game.state,game.turn,game.env,5)

    def hard_call(game):
        move = game.env.auto_move(game.state)
        if move:
            return move
        else:
            return two_level_mcts(game.state,game.turn,game.env,5)

    def expert_call(game):
        move = game.env.auto_move(game.state)
        if move:
            return move
        else:
            return three_level_mcts(game.state,game.turn,game.env,1)

GoFish = Game(4)
GoFish.game_loop()