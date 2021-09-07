import os
import json
#import matplotlib.pyplot as plt

# from decouple import config
# ENVIRONMENT = config('ENVIRONMENT')
ENVIRONMENT = 'local'
print(ENVIRONMENT)


def openAllJsons(lang='es', path=None):
    if ENVIRONMENT == 'local':
        return openFromLocal(lang=lang, path=path)
    return None


def openFromLocal(lang='es', path=None):

    intents = None
    json_files = [pos_json for pos_json in os.listdir(
        path) if pos_json.endswith('.json')]
    for filename in json_files:
        with open(path + filename) as json_data:
            if intents is None:
                intents = json.load(json_data)['intents']
            else:

                prev = json.load(json_data)['intents']
                for i in prev:
                    intents.append(i)
    # print intents
    return intents


""" def plot_history(history):
    print("Ploting history")
    print(history.history.keys())
    #  "Accuracy"
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()
    # "Loss"
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()
 """
