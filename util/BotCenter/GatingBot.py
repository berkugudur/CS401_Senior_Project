from py4j.java_gateway import get_field
# from predictor import Predictor

class GatingBot(object):
    def __init__(self, gateway, bot_center):
        self.gateway = gateway
        self.bot_center = bot_center
        
    def close(self):
        # Propogate to bot center
        self.bot_center.close()
        
    def getInformation(self, frameData):
        self.frameData = frameData

        # Propogate to bot center
        self.bot_center.getInformation(frameData)
        
    def roundEnd(self, x, y, z):
        # Propogate to bot center
        self.bot_center.roundEnd(x, y, z)

    def getScreenData(self, sd):
        # Propogate to bot center
        self.bot_center.getScreenData(sd)
        
    def initialize(self, gameData, player):
        self.inputKey = self.gateway.jvm.struct.Key()
        self.frameData = self.gateway.jvm.struct.FrameData()
        self.cc = self.gateway.jvm.aiinterface.CommandCenter()

        self.player = player
        self.gameData = gameData
        
        # Propogate to bot center
        self.bot_center.initialize(gameData, player)

        return 0
        
    # Here we are providing the input to FightingICE platform.
    def input(self):
        # Inputs variable is an array that contatins actions for every ai in bot center.
        # For example;
        #   If bot center includes Thunder and BCP, 
        #   inputs variable looks like this: ['input key of Thunder', 'input key of BCP]
        inputs = self.bot_center.input()

        # BotCenter's id method returns the index of given bot in the inputs array.
        thunder_id = self.bot_center.id("Thunder")

        # With this return value, only Thunder's inputs applied to the game environment.
        return inputs[thunder_id]
    
    def processing(self):
        # Propogate to bot center
        self.bot_center.processing()

        #
        
    class Java:
        implements = ["aiinterface.AIInterface"]
        