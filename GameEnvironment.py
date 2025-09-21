import random
import copy

class GameEnvironment:
     def __init__(game,amount_of_players):
          game.amount_of_players = amount_of_players
          game.deck = ["AD","2D","3D","4D","5D","6D","7D","8D","9D","10D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","10S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","10C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","10H","JH","QH","KH"]
          game.shuffled_deck = []
          game.player1_hand = []
          game.player2_hand = []
          game.player3_hand = []
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

     def is_game_over(game):
         return game.shuffled_deck == [] and game.player1_hand == [] and game.player2_hand == [] and game.player3_hand == []
     

     def player1_turn(game):
         pass
     
     def player2_turn(game):
         pass
     
     def player3_turn(game):
         pass

     def game_loop(game):
        while True:
           print("hello")
           game.player1_turn()
           game.player2_turn()
           game.player3_turn()
           if game.is_game_over ():
               break

GoFish = GameEnvironment(3)
GoFish.game_loop()
