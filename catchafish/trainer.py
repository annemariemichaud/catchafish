import multiprocessing
import time
import warnings
import os
from termcolor import colored

from catchafish.data import get_all_training_data
from catchafish.data import NAMES_MAPPING

from tensorflow.keras import Sequential, layers
from tensorflow.keras.applications import VGG16
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

path_to_current_dir = os.path.dirname(os.path.join(os.path.abspath(__file__)))

class Trainer(object):
    """docstring for ClassName"""
    def __init__(self, **kwargs):
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
        self.model = None
        self.kwargs = kwargs
        self.target_size = self.kwargs.get('target_size', (128,128))
        self.n_data_augmentation = self.kwargs.get('n_data_augmentation', 10)
        self.zca_whitening = self.kwargs.get('zca_whitening', False)
        self.patience = self.kwargs.get('patience', 10)
        self.epochs = self.kwargs.get('epochs', 1000)
        self.batch_size = self.kwargs.get('batch_size', 32)

    def get_estimator(self):
        self.model = Sequential()
        self.model.add(VGG16(include_top = False, input_shape = (128, 128, 3)))

        for k, v in self.model._get_trainable_state().items():
            k.trainable = False

        self.model.add(layers.Flatten())

        self.model.add(layers.Dense(50, activation = 'relu'))
        self.model.add(layers.Dense(11, activation = 'softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        return self.model

    def train(self):
        self.X_train, self.y_train = get_all_training_data(zca_whitening=self.zca_whitening,
            target_size=self.target_size,
            n_data_augmentation=self.n_data_augmentation)

        if self.model == None:
            self.get_estimator()

        es = EarlyStopping(monitor='val_loss', patience=self.patience, verbose=1)

        history = self.model.fit(self.X_train, to_categorical(self.y_train),
                    validation_split = 0.3,
                    epochs = self.epochs,
                    batch_size = self.batch_size,
                    callbacks = [es],
                    verbose = 1)

        return self.model

    def cross_validate(self):
        #Patience = 5, get_data = get_data1, n_neurons = 50, n_data_augmentation = 10
        pass

    #def evaluate(self):

    def save_model(self):
        path = path_to_current_dir + '/model.h5'
        self.model.save(path)
        return f'model saved at:{path}'

    def predict(self):
        path = path_to_current_dir + '/model.h5'
        self.model = load_model(path)

        path_to_demo_image = path_to_current_dir + '/demo_image.jpg'
        demo_image = load_img(path_to_demo_image, target_size=self.target_size)
        demo_image = img_to_array(demo_image)
        demo_image = np.expand_dims(demo_image, axis=0)

        predict_probas = self.model.predict(demo_image)
        predict_class = np.argmax(predict_probas[0])

        return NAMES_MAPPING[predict_class]

if __name__ == "__main__":
    t = Trainer()
    t.get_estimator()
    print(colored("############  Training model ############", "blue"))
    t.train()
    print(colored("############   Saving model    ############", "green"))
    t.save_model()

