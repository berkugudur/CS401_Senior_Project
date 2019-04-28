from py4j.java_gateway import get_field
from predictor import Predictor
from predictorHP import PredictorHP

class BotPredictor(object):
    def __init__(self, hp_model_path, action_model_path):
        self.predictorHP = PredictorHP(hp_model_path)
        self.predictor = Predictor(action_model_path)
        
    def get_predicted_hp(self, p1_action,p1_x, p1_y, p2_x, p2_y):
        return self.predictorHP.predict(p1_action, p1_x, p1_y, p2_x, p2_y)
        
    def get_predicted_action(self, p1_action, p1_hp, p1_x, p1_y, p2_hp, p2_x, p2_y):
        return self.predictor.predict(p1_action, p1_hp, p1_x, p1_y, p2_hp, p2_x, p2_y)