from py4j.java_gateway import get_field
from predictor import Predictor
from BotPredictor import BotPredictor

class PredictHPAI(object):
    def __init__(self, gateway):
        print("hp ai created")
        self.predictors = [
            BotPredictor("example_data/bcpvsthunder/hpmodel/", "example_data/bcpvsthunder/actionmodel/"),
            BotPredictor("example_data/bcpvsutal/hpmodel/", "example_data/bcpvsutal/actionmodel/")
        ]
        # For help logging
        self.predictor_names = [
            "Thunder",
            "Utal"
        ]
        self.gateway = gateway
        
    def close(self):
        pass
        
    def getInformation(self, frameData):
        self.frameData = frameData
        
    def roundEnd(self, x, y, z):
        pass

    def getScreenData(self, sd):
    	pass
        
    def initialize(self, gameData, player):
        self.inputKey = self.gateway.jvm.struct.Key()
        self.frameData = self.gateway.jvm.struct.FrameData()
        self.cc = self.gateway.jvm.aiinterface.CommandCenter()

        self.player = player
        self.gameData = gameData
        return 0
        
    def input(self):
        return self.inputKey
    
    # Return true if given points are close to do attack actions.
    def are_they_close(self, us_x, us_y, opponent_x, opponent_y):
        return True    

    def processing(self):
        if self.frameData.getEmptyFlag() or self.frameData.getRemainingTime() <= 0:
            self.isGameJustStarted = True
            return
            
        self.cc.setFrameData(self.frameData, self.player)

        us = self.frameData.getCharacter(self.player)
        opponent = self.frameData.getCharacter(not self.player)

        action = opponent.getAction().toString()
        opponent_hp = opponent.getHp()
        opponent_x = opponent.getX()
        opponent_y = opponent.getY()

        us_hp = us.getHp()
        us_x = us.getX()
        us_y = us.getY()

        # If there is running command do it, else clear and add predicted action
        if self.cc.getSkillFlag():
            self.inputKey = self.cc.getSkillKey()
            return
        self.inputKey.empty()
        self.cc.skillCancel()
        
        # If they are not close hp prediction mechanism will fail therefore use just action prediction.
        if self.are_they_close(us_x, us_y, opponent_x, opponent_y):
            predicted_hps = []

            # Evaluate all predictions for each predictor
            for index, predictor in enumerate(self.predictors):
                predicted_hp = predictor.get_predicted_hp(action, opponent_x, opponent_y, us_x, us_y)
                predicted_hps.append(predicted_hp)

                print(self.predictor_names[index] + ": " + str(predicted_hp))

            # Find maximum valued predictor 
            maximum_hp = max(predicted_hps)
            index_of_predictor = predicted_hps.index(maximum_hp)
            maximum_predictor = self.predictors[index_of_predictor]

            print("\n\t" + self.predictor_names[index_of_predictor] + " has the biggest hp value.\n")
            print("---------------------------------------")

            predicted_action = maximum_predictor.get_predicted_action(action, opponent_hp, opponent_x, opponent_y, us_hp, us_x, us_y)

            self.cc.commandCall(predicted_action)
        else: # They are not close, just apply the first bot's predicted action.
            print("They are not close to predict hp action.")
            predicted_action = self.predictors[0].get_predicted_action(action, opponent_hp, opponent_x, opponent_y, us_hp, us_x, us_y)
            self.cc.commandCall(predicted_action)


                        
    class Java:
        implements = ["aiinterface.AIInterface"]
        