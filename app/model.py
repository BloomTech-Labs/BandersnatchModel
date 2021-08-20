from datetime import datetime
from zipfile import ZipFile

import pytz
from joblib import dump
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


class Model:

    def __init__(self, data_api):
        ...

    def __call__(self, feature_basis):
        ...

    @property
    def info(self):
        ...

    def score(self):
        ...
