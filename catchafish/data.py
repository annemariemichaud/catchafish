import numpy as np
from tensorflow.keras.preprocessing.image import DirectoryIterator
from sklearn.model_selection import train_test_split

def get_data(val_split = False, test_size = 0.3):
    '''This function returns the '''
    path = '../catchafish/data'
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
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size = 0.3)
        return X_train, X_val, X_test, y_train, y_val, y_test
    else:
        return X_train, X_test, y_train, y_test

if __name__ == "__main__":
	X_train, X_val, X_test, y_train, y_val, y_test = get_data(val_split = True)
	print(f"X_train.shape : {X_train.shape}")
	print(f"X_val.shape : {X_val.shape}")
	print(f"X_test.shape : {X_test.shape}")