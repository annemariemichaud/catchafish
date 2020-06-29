import multiprocessing
import time
import warnings

from tensorflow.keras import Sequential, layers
from tensorflow.keras.applications import VGG16
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping

class Trainer(object):
    """docstring for ClassName"""
    def __init__(self, X, y, **kwargs):
        """
        FYI:
        __init__ is called every time you instatiate Trainer
        Consider kwargs as a dict containig all possible parameters given to your constructor
        Example:
            TT = Trainer(nrows=1000, estimator="Linear")
               ==> kwargs = {"nrows": 1000,
                            "estimator": "Linear"}
        :param X:
        :param y:
        :param kwargs:
        """
        self.X_train = X
        self.y_train = y
        #self.kwargs = kwargs
        #self.kwargs = ....

    def get_estimator(self):
        self.model = Sequential()
        self.model.add(VGG16(include_top = False, input_shape = (128, 128, 3)))

        for k, v in self.model._get_trainable_state().items():
            k.trainable = False

        self.model.add(layers.Flatten())

        self.model.add(layers.Dense(50, activation = 'relu'))
        self.model.add(layers.Dense(11, activation = 'softmax'))
        return self.model

    def train(self):
        self.model.fit(self.X_train, self.y_train)
        pass

    def cross_validate(self):
        #Patience = 5, get_data = get_data1, n_neurons = 50, n_data_augmentation = 10
        pass

    def evaluate(self):
        pass

    def predict(self):
        pass

    def save_model(self):
        pass

if __name__ == "__main__":
    g = get_estimator()
    #t = Trainer(X=X_train, y=y_train, **params)
    #del X_train, y_train
    print(colored("############  Training model   ############", "red"))
    t.train()
    print(colored("############  Evaluating model ############", "blue"))
    t.evaluate()
    print(colored("############   Saving model    ############", "green"))
    t.save_model()

