'''Ce module rassemble toutes les fonctions utiles à l'extraction des données
de notre projet et aux étapes préliminaires de preprocessing.'''

import os
import numpy as np
from tensorflow.keras.preprocessing.image import DirectoryIterator, ImageDataGenerator
from sklearn.model_selection import train_test_split


def get_data(val_split = False, val_size = 0.3):
    '''Cette fonction parcourt le dossier contenant les images de départ et les renvoie,
    en uniformisant les tailles, sous forme de nd-arrays NumPy. La fonction exécute
    aussi un train_test_split qui distingue un dataset d'entraînement (70% des images)
    et un dataset de test (30% des images). '''
    path_to_current_dir = os.path.dirname(os.path.join(os.path.abspath(__file__)))
    path = path_to_current_dir + '/data'
    batch_size = 100000

    dir_iterator = DirectoryIterator(directory = path,
                                     image_data_generator = None,
                                     target_size = (32, 32),
                                     batch_size = batch_size,
                                     shuffle = False,
                                     dtype = int)

    X = dir_iterator[0][0]
    y = dir_iterator.labels

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 1)

    if val_split:
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size = val_size)
        return X_train, X_val, X_test, y_train, y_val, y_test
    else:
        return X_train, X_test, y_train, y_test


def get_data_test(val_split = False, val_size = 0.3, zca_whitening = False):
    '''Cette fonction parcourt le dossier contenant les images de départ et les renvoie,
    en uniformisant les tailles, sous forme de nd-arrays NumPy. La fonction exécute
    aussi un train_test_split qui distingue un dataset d'entraînement (70% des images)
    et un dataset de test (30% des images) '''
    path_to_current_dir = os.path.dirname(os.path.join(os.path.abspath(__file__)))
    path = path_to_current_dir + '/data_test'
    batch_size = 1500
    dir_iterator = DirectoryIterator(directory = path,
                                     image_data_generator = None,
                                     target_size = (128, 128),
                                     batch_size = batch_size,
                                     shuffle = False,
                                     dtype = int)
    X = dir_iterator[0][0] / 255
    y = dir_iterator.labels
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 1)
    image_data_generator = ImageDataGenerator(zca_whitening = zca_whitening,
                                              rotation_range = 5,
                                              width_shift_range = 0.3,
                                              height_shift_range = 0.3,
                                              shear_range = 0.3,
                                              zoom_range = 0.3,
                                              horizontal_flip = True,
                                              fill_mode = 'nearest')
    if zca_whitening:
        image_data_generator.fit(X_train)

    extended_output = []
    for images in image_data_generator.flow(X_train, y_train, batch_size = batch_size):
        extended_output.append(images)
        if len(extended_output) == 5:
            break

    X_train = extended_output[0][0]
    y_train = extended_output[0][1]

    for data_tuple in extended_output[1:]:
        X_train = np.concatenate((X_train, data_tuple[0]), axis = 0)
        y_train = np.concatenate((y_train, data_tuple[1]), axis = 0)

    if val_split:
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size = val_size)
        return X_train, X_val, X_test, y_train, y_val, y_test
    else:
        return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    #X_train, X_val, X_test, y_train, y_val, y_test = get_data(val_split = True)
    #print(f"X_train.shape : {X_train.shape}")
    #print(f"X_val.shape : {X_val.shape}")
    #print(f"X_test.shape : {X_test.shape}")
    #print("---")
    X_train, X_val, X_test, y_train, y_val, y_test = get_data_test(val_split = True)
    print(f"X_train.shape : {X_train.shape}")
    print(f"X_val.shape : {X_val.shape}")
    print(f"X_test.shape : {X_test.shape}")


