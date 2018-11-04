import pickle
from sklearn.preprocessing import OneHotEncoder as OneHot, LabelEncoder, MinMaxScaler
import numpy as np

from core.actions import DISTINCT_ACTIONS

class Normalizer:
    def __init__(self, scaler=MinMaxScaler(feature_range=(0, 1))):
        self.scaler = scaler

    def normalize(self, column):
        # Get abs of each item in column and transfrom them to np array.
        column = np.array([abs(int(item)) for item in column], dtype=np.float64).reshape(len(column), 1)
        if len(column) == 1:
            return self.scaler.transform(column)
        return self.scaler.fit(column).transform(column)

    def decode(self, row):
        return self.scaler.inverse_transform(row)

    def save(self, path):
        pickle.dump(self.scaler, open(path, 'wb'))

def load_normalizer(path):
    return Normalizer(scaler=pickle.load(open(path, "rb")))