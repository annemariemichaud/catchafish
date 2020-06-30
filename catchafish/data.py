'''Ce module rassemble toutes les fonctions utiles à l'extraction des données
de notre projet et aux étapes préliminaires de preprocessing.'''

import os
from google.cloud import storage

import numpy as np
import pandas as pd

from tensorflow.keras.preprocessing.image import DirectoryIterator, ImageDataGenerator
from sklearn.model_selection import train_test_split

from catchafish.gcp import BUCKET_NAME

NAMES_MAPPING = {
    0 : ("fish_01", "Dascyllus reticulatus"),
    1 : ("fish_02", "Plectroglyphidodon dickii"),
    2 : ("fish_03", "Chromis chrysura"),
    3 : ("fish_04", "Amphiprion clarkii"),
    4 : ("fish_05", "Chaetodon lunulatus"),
    5 : ("fish_07", "Myripristis kuntee"),
    6 : ("fish_08", "Acanthurus nigrofuscus"),
    7 : ("fish_09", "Hemigymnus fasciatus"),
    8 : ("fish_10", "Neoniphon sammara"),
    9 : ("fish_16", "Lutjanus fulvus"),
    10: ("fish_17", "Carassius auratus")
    }

def data_augmentation(X, y, zca_whitening = False, n_data_augmentation = 10, target_size = (128, 128)):
    '''Cette fonction prend comme argument des images (dataset partiel ou complet) sous
    la forme de nd-arrays NumPy X (features) et y (target) et renvoie une version
    "augmentée" de ces images.'''

    batch_size = 1500
    image_data_generator = ImageDataGenerator(
        zca_whitening = zca_whitening,
        rotation_range = 5,
        width_shift_range = 0.3,
        height_shift_range = 0.3,
        shear_range = 0.3,
        zoom_range = 0.3,
        horizontal_flip = True,
        fill_mode = 'nearest'
        )

    if zca_whitening:
        image_data_generator.fit(X)

    extended_output = []
    for images in image_data_generator.flow(X, y, batch_size = batch_size):
        extended_output.append(images)
        if len(extended_output) == n_data_augmentation:
            break

    X = extended_output[0][0]
    y = extended_output[0][1]

    for data_tuple in extended_output[1:]:
        X = np.concatenate((X, data_tuple[0]), axis = 0)
        y = np.concatenate((y, data_tuple[1]), axis = 0)

    return X, y

def get_data(val_split = False, val_size = 0.3, zca_whitening = False, target_size = (128, 128), n_data_augmentation = 10, local = False):
    '''Cette fonction parcourt le dossier contenant les images de départ et les renvoie,
    en uniformisant les tailles, sous forme de nd-arrays NumPy. La fonction exécute
    aussi un train_test_split qui distingue un dataset d'entraînement (70% des images)
    et un dataset de test (30% des images).'''

    client = storage.Client()
    if local:
        path_to_current_dir = os.path.dirname(os.path.join(os.path.abspath(__file__)))
        path = path_to_current_dir + '/data'
    else:
        path = "gs://{}/data".format(BUCKET_NAME)
        os.system('mkdir /tmp/data_tmp')
        os.system('gsutil cp -R {} /tmp/data_tmp'.format(path))

    batch_size = 1500
    dir_iterator = DirectoryIterator(
        directory = '/tmp/data_tmp/data',
        image_data_generator = None,
        target_size = target_size,
        batch_size = batch_size,
        shuffle = False,
        dtype = int
        )

    X = dir_iterator[0][0] / 255
    y = dir_iterator.labels

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

    X_train, y_train = data_augmentation(
        X_train, y_train,
        zca_whitening = zca_whitening,
        n_data_augmentation = n_data_augmentation,
        target_size = target_size
        )

    if val_split:

        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size = val_size)
        return X_train, X_val, X_test, y_train, y_val, y_test

    else:
        return X_train, X_test, y_train, y_test

def get_all_training_data(zca_whitening = False, target_size = (128, 128), n_data_augmentation = 10, local = False):
    '''Cette fonction renvoie l'ensemble du dataset sous la forme d'un X (tenseur
    NumPy de 4 dimensions rassemblant les différentes images) et d'un y (targets)
    afin d'entraîner le modèle sur le plus de données possibles.'''

    client = storage.Client()
    if local:
        path_to_current_dir = os.path.dirname(os.path.join(os.path.abspath(__file__)))
        path = path_to_current_dir + '/data'
    else:
        path = "gs://{}/data".format(BUCKET_NAME)
        os.system('mkdir /tmp/data_tmp')
        os.system('gsutil cp -R {} /tmp/data_tmp'.format(path))

    batch_size = 1500
    dir_iterator = DirectoryIterator(
        directory = '/tmp/data_tmp/data',
        image_data_generator = None,
        target_size = target_size,
        batch_size = batch_size,
        shuffle = True,
        dtype = int
        )

    X = dir_iterator[0][0] / 255
    y = np.argmax(dir_iterator[0][1], axis = 1)

    X, y = data_augmentation(
        X, y,
        zca_whitening = zca_whitening,
        n_data_augmentation = n_data_augmentation,
        target_size = target_size
        )

    return X, y

def names_mapping(y):
    '''Cette fonction prend pour argument un vecteur NumPy, constitué de targets
    entre 0 et 10, et renvoie un vecteur NumPy dans lequel les chiffres ont été
    remplacés par le nom latin de l'espèce.'''

    y = map(lambda x : NAMES_MAPPING[x][1], y)
    return np.array(list(y))

if __name__ == "__main__":

    X_train, X_val, X_test, y_train, y_val, y_test = get_data(val_split = True, local = False)

    print(f"X_train.shape : {X_train.shape}")
    print(f"X_val.shape : {X_val.shape}")
    print(f"X_test.shape : {X_test.shape}")

    print("_______________________________________")

    X, y = get_all_training_data(local = False)

    print(f"X.shape : {X.shape}")
    print(y[:10])
    print(names_mapping(y[:10]))
