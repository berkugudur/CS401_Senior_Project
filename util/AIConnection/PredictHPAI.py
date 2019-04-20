from py4j.java_gateway import get_field
from predictor import Predictor
from BotPredictor import BotPredictor

class PredictHPAI(object):
    def __init__(self, gateway):
        self.BCPvsThunderBot = BotPredictor("example_data/bcpvsthunder/hpmodel/", "example_data/bcpvsthunder/actionmodel/")
        self.BCPvsUtalBot = BotPredictor("example_data/bcpvsutal/hpmodel/", "example_data/bcpvsutal/actionmodel/")
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

        bcpvsthunder_predicted_hp = self.BCPvsThunderBot.get_predicted_hp(action, opponent_x, opponent_y, us_x, us_y)
        bcpvsutal_predicted_hp = self.BCPvsUtalBot.get_predicted_hp(action, opponent_x, opponent_y, us_x, us_y)
        print ( "thunder: " + str(int(bcpvsthunder_predicted_hp)))
        print ( "utal: " + str(int(bcpvsutal_predicted_hp)))
        print ( "----------------")
        
        if bcpvsthunder_predicted_hp >= bcpvsutal_predicted_hp:
            predicted_action = self.BCPvsThunderBot.get_predicted_action(action, opponent_hp, opponent_x, opponent_y, us_hp, us_x, us_y)
        else:
            predicted_action = self.BCPvsUtalBot.get_predicted_action(action, opponent_hp, opponent_x, opponent_y, us_hp, us_x, us_y)

        self.cc.commandCall(predicted_action)
                        
    class Java:
        implements = ["aiinterface.AIInterface"]
        