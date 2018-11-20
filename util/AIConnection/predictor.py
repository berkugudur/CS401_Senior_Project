from keras.models import load_model
import numpy as np

import sys
# For using core package that located in the one upper folder.
sys.path.append('../../')

from core.json_importer import parse_json_file
from core.preproccessing import load_normalizer
from core.actions import one_hot_encode, decode

class Predictor:

    def __init__(self, model_path):
        self.model_path = model_path
        self.model = load_model(self.model_path + "/model.h5")
        self.p1_hp_normalizer = load_normalizer(self.model_path + "/p1_hp_norm.save")
        self.p2_hp_normalizer = load_normalizer(self.model_path + "/p2_hp_norm.save")
        self.x_normalizer = load_normalizer(self.model_path + "/x_norm.save")
        self.y_normalizer = load_normalizer(self.model_path + "/y_norm.save")
        self.model._make_predict_function()

    def predict(self, p1_action, p1_hp, p1_x, p1_y, p2_hp, p2_x, p2_y):
        data = []
        data.extend(one_hot_encode([p1_action]))
        data.extend(self.p1_hp_normalizer.normalize([p1_hp]))
        data.extend(self.p2_hp_normalizer.normalize([p2_hp]))
        data.extend(self.x_normalizer.normalize([p1_x - p2_x]))
        data.extend(self.y_normalizer.normalize([p1_y - p2_y]))

        data = np.array([[item for sublist in data for item in sublist]])

        predicted_action = self.model.predict(data)
        return decode(predicted_action)
