import random
from collections import Counter

class GameEnvironment:
     def __init__(game,amount_of_players):
          game.amount_of_players = amount_of_players
          game.deck = ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"]
          game.shuffled_deck = []
          game.player1_hand = []
          game.player2_hand = []
          game.player3_hand = []
          game.player1_sets = []
          game.player2_sets = []
          game.player3_sets = []
          game.turn = ''
          game.moves = ['ask','draw']
          game.history = []
          game.state = {
              "hands": {
                  "player1": game.player1_hand,
                  "player2": game.player2_hand,
                  "player3": game.player3_hand,
              },
              "sets": {
                  "player1": [],
                  "player2": [],
                  "player3": [],
              },
              "deck" : game.shuffled_deck,
              "current_player": game.turn,
              "history": game.moves,
          }


     def shuffle_cards(game):
         shuffled_deck = game.deck[:]
         random.shuffle(shuffled_deck)
         game.shuffled_deck = shuffled_deck #replace this with random.shuffle()
            
     def distribute_cards(game):
        for i in range(0,8):
            if game.amount_of_players == 3:
                game.player1_hand.append(game.shuffled_deck.pop())
                game.player2_hand.append(game.shuffled_deck.pop())
                game.player3_hand.append(game.shuffled_deck.pop())

     def draw_card(game,playernum):
         players = [game.player1_hand,game.player2_hand,game.player3_hand]
         players[playernum - 1].append(game.shuffled_deck.pop())

     def remove_set(game,card,hand):
         remove = [card+'D',card+'S',card+'H',card+'C']
         for card in remove:
             hand.remove(card)


     def check_for_sets(game):
        players = [game.player1_hand,game.player2_hand,game.player3_hand]
        for x in players:
            counter = []
            for card in x:
                counter.append(card[:-1])
            counts = Counter(counter)
            sets = [card for card, count in counts.items() if count == 4]
            if sets != []:
                for set in sets:
                    if x == game.player1_hand:
                        game.player1_sets.append(set)
                    elif x == game.player2_hand:
                        game.player2_sets.append(set)
                    else:
                        game.player3_sets.append(set)
                    game.remove_set(set,x)
                    



     def get_valid_moves(game,playernum):
         players = [game.player1_hand,game.player2_hand,game.player3_hand]
         asks = []
         for x in players[playernum - 1]:
             asks.append(x[0])
         asks = list(dict.fromkeys(asks))
         print(asks)
         available = []
         for i in range(game.amount_of_players):
             if i != (playernum - 1) and len(players[i]) > 0:
                 available.append(i)
         moves = []
         for card in asks:
             for player in available:
                    moves.append((f'player{player+1}',card)) 
         print(moves)
         return moves
                 

     def is_game_over(game):
         return game.shuffled_deck == [] and game.player1_hand == [] and game.player2_hand == [] and game.player3_hand == []
     

     def player1_turn(game):
         moves = game.get_valid_moves(1)
         i = int(input("Enter Move Number."))
         global Correct
         Correct = False
         if moves[i][0] == 'player2':
            for x in game.player2_hand:
                if moves[i][1] == x[0]:
                    Correct = True
                    game.player1_hand.append(x)
                    game.player2_hand.remove(x)
            if Correct == False:
                game.draw_card(1)
                game.turn = 'player2'
            else:
                game.turn = 'player1'

     
     def player2_turn(game):

         game.turn = 'player3'
     
     def player3_turn(game):

         game.turn = 'player1'

     def game_loop(game):
        game.shuffle_cards()
        game.distribute_cards()
        game.turn = 'player' + str(random.randint(1,3))
        while True:
            if game.is_game_over ():
               break
            elif game.turn == 'player1':
                game.player1_turn()
            elif game.turn == 'player2':
                game.player2_turn()
            elif game.turn == 'player3':
                game.player3_turn()

GoFish = GameEnvironment(3)
GoFish.shuffle_cards()
GoFish.distribute_cards()

print(GoFish.player1_hand.sort())
print(GoFish.player1_hand)
GoFish.player1_hand = ['5C','5D','5H','5S']
GoFish.check_for_sets()
print(GoFish.player1_sets)
print(GoFish.player1_hand)