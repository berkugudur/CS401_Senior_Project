from keras.models import load_model
import numpy as np

import sys
# For using core package that located in the one upper folder.
sys.path.append('../../')

from core.json_importer import parse_json_file
from core.preproccessing import load_normalizer
from core.actions import one_hot_encode, decode

class PredictorHP:

    def __init__(self, model_path):
        self.model_path = model_path
        self.model = load_model(self.model_path + "/model.h5")
        self.xp1_normalizer = load_normalizer(self.model_path + "/xp1_norm.save")
        self.xp2_normalizer = load_normalizer(self.model_path + "/xp2_norm.save")
        self.yp1_normalizer = load_normalizer(self.model_path + "/yp1_norm.save")
        self.yp2_normalizer = load_normalizer(self.model_path + "/yp2_norm.save")
        self.model._make_predict_function()

    def predict(self, p1_action,p1_x, p1_y, p2_x, p2_y):
        data = []
        data.extend(one_hot_encode([p1_action]))
        data.extend(self.xp1_normalizer.normalize([p1_x]))
        data.extend(self.xp2_normalizer.normalize([p2_x]))
        data.extend(self.yp1_normalizer.normalize([p1_y]))
        data.extend(self.yp2_normalizer.normalize([p2_y]))

        data = np.array([[item for sublist in data for item in sublist]])
        predicted_hp = self.model.predict(data)
        return np.argmax(predicted_hp)
