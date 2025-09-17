import random

class Game:
     def __init__(game,amount_of_players):
          game.amount_of_players = amount_of_players
          game.deck = ["AD","2D","3D","4D","5D","6D","7D","8D","9D","10D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","10S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","10C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","10H","JH","QH","KH"]
          game.player1_state = []
          game.player1_hand = []
          game.player2_hand = []
          game.player3_hand = [] 
          game.player4_hand = []
          game.player5_hand = [] #max number of player is five. ONLY one AI.
          game.shuffled_deck = []


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
            elif game.amount_of_players == 4:
                game.player1_hand.append(game.shuffled_deck.pop())
                game.player2_hand.append(game.shuffled_deck.pop())
                game.player3_hand.append(game.shuffled_deck.pop())
                game.player4_hand.append(game.shuffled_deck.pop())
            else:
                game.player1_hand.append(game.shuffled_deck.pop())
                game.player2_hand.append(game.shuffled_deck.pop())
                game.player3_hand.append(game.shuffled_deck.pop())
                game.player4_hand.append(game.shuffled_deck.pop())
                game.player5_hand.append(game.shuffled_deck.pop())

     def player1_turn(game):
          text = "Your Hand: "
          for x in game.player1_hand:
            text += (x+' ')
          print(text)
          
               
     

     def game_loop(game):
        while True:
            if game.amount_of_players == 3:
                    game.player1_turn()
                    #game.player2_turn()
                    #game.player3_turn()
            elif game.amount_of_players == 4:
                    game.player1_turn()
                    game.player2_turn()
                    game.player3_turn()
                    game.player4_turn()
            else:
                    game.player1_turn()
                    game.player2_turn()
                    game.player3_turn()
                    game.player4_turn()
                    game.player5_turn()

Go_Fish = Game(3)
Go_Fish.shuffle_cards()
Go_Fish.distribute_cards()
Go_Fish.game_loop()
print(Go_Fish.player1_hand,Go_Fish.player2_hand,Go_Fish.player3_hand)
print(Go_Fish.deck,len(Go_Fish.deck))
print(Go_Fish.shuffled_deck)