import random

class JavaTunnel:
    
    def predictStrongestBot(self, usX, usY, opponentX, opponentY):
        print("Predicting strongest bot with parameters usX: {}, usY: {}, opponentX: {}, opponentY: {}".format(usX, usY, opponentX, opponentY))
        strongest_bot_name = ["Thunder", "BCP"][random.randint(0, 1)] 

        return strongest_bot_name