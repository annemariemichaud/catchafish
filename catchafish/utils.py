'''This module gathers general methods useful for our project.'''

import matplotlib.pyplot as plt

def plot_history(history, title = '', axs = None, exp_name = ""):
    '''When provided with a tensorflow.keras "history" object, this function plots
    the train and test losses through epochs on an axis and the train and test
    accuracies through epochs on another axis.'''
    if axs is not None:
        ax1, ax2 = axs
    else:
        f, (ax1, ax2) = plt.subplots(1, 2, figsize = (12, 4))

    if len(exp_name) > 0 and exp_name[0] != '_':
        exp_name = '_' + exp_name

    ax1.plot(history.history['loss'], label = 'train' + exp_name)
    ax1.plot(history.history['val_loss'], label = 'val' + exp_name)
    ax1.set_ylim(0, 2)
    ax1.set_title('BCE loss')
    ax1.legend()

    ax2.plot(history.history['accuracy'], label = 'train accuracy'  + exp_name)
    ax2.plot(history.history['val_accuracy'], label = 'val accuracy'  + exp_name)
    ax2.set_ylim(0.25, 1)
    ax2.set_title('Accuracy')
    ax2.legend()

    return (ax1, ax2)
