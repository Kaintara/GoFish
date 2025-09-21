import random
from collections import Counter
import copy

class GameEnvironment:
     def __init__(game,amount_of_players):
          game.amount_of_players = amount_of_players
          game.deck = ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"]
          game.shuffled_deck = []
          game.hands = [[] for _ in range(amount_of_players)]
          game.sets = [[] for _ in range(amount_of_players)]
          game.turn = ''
          game.moves = ['ask','draw']
          game.history = []
          '''
          game.state = {
              "hands": {
                  "player1": game.player1_hand,
                  "player2": game.player2_hand,
                  "player3": game.player3_hand,
              },
              "sets": {
                  "player1": game.player1_sets,
                  "player2": game.player2_sets,
                  "player3": game.player3_sets,
              },
              "deck" : game.shuffled_deck,
              "current_player": game.turn,
              "history": game.moves,
          }
        '''

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
            players[playernum - 1].append(game.shuffled_deck.pop())

     def remove_set(game,card,hand):
         remove = [card+'D',card+'S',card+'H',card+'C']
         for card in remove:
             hand.remove(card)


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
         for x in players[playernum - 1]:
             asks.append(x[0])
         asks = list(dict.fromkeys(asks))
         print(asks)
         available = []
         for i in range(game.amount_of_players):
             if i != (playernum) and len(players[i]) > 0:
                 available.append(i)
         moves = []
         for card in asks:
             for player in available:
                    moves.append((f'player{player+1}',card)) 
         print(moves)
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

         move = moves[i]
         target_player = int(move[0][6:]) - 1
         card = move[1]
         Correct = False

         for x in game.hands[target_player][:]:
            if card == x[0]:
                Correct = True
                game.hands[playernum].append(x)
                game.hands[target_player].remove(x)
         if not Correct:
            if game.shuffled_deck:
               game.draw_card(playernum)
            nvp = game.next_vaild_player(playernum)
            if nvp is not None:
                game.turn = nvp
            else:
                game.turn = None

     def game_loop(game):
        game.shuffle_cards()
        game.distribute_cards()
        game.turn = random.randint(0,game.amount_of_players - 1)
        while not game.is_game_over() and game.turn is not None:
            game.check_for_sets()
            game.player_turn(game.turn)
        for x in game.sets:
            print(x)

GoFish = GameEnvironment(3)
print(GoFish)
GoFish.game_loop()