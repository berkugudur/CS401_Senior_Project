import random

class JavaTunnel:
    def __init__(self, predictors, predictor_names):
        self.predictors = predictors
        self.predictor_names = predictor_names

    def predictStrongestBot(self, action, usX, usY, opponentX, opponentY):
        print("asda")
        predicted_hps = []
        for index, predictor in enumerate(self.predictors):
            action_ = str(action.rstrip("\r"))
            opponentX_ = int(opponentX.rstrip("\r"))
            opponentY_ = int(opponentY.rstrip("\r"))
            usX_ = int(usX.rstrip("\r"))
            usY_ = int(usY.rstrip("\r"))
            predicted_hp = predictor.get_predicted_hp(action_, opponentX_, opponentY_, usX_, usY_)
            predicted_hps.append(predicted_hp)
            print(self.predictor_names[index] + ": " + str(predicted_hp))

        # Find maximum valued predictor 
        maximum_hp = max(predicted_hps)
        index_of_predictor = predicted_hps.index(maximum_hp)

        print("\n\t" + self.predictor_names[index_of_predictor] + " has the biggest hp value.\n")    
        #print("Predicting strongest bot with parameters usX: {}, usY: {}, opponentX: {}, opponentY: {}".format(usX, usY, opponentX, opponentY))
    
        #strongest_bot_name = ["Thunder", "BCP"][random.randint(0, 1)] 

        return self.predictor_names[index_of_predictor]