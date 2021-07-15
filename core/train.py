import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from utils.nltk_utils import bag_of_words, tokenize, stem
from core.model import NeuralNet
from utils.fileHandler import openAllJsons


class ChatDataset(Dataset):

    def __init__(self, X_train, y_train):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    # support indexing such that dataset[i] can be used to get i-th sample
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    # we can call len(dataset) to return the size
    def __len__(self):
        return self.n_samples


class Train:

    def __init__(self, lang='en'):
        self.lang = lang
        self.all_words = []
        self.tags = []
        self.X_train = []
        self.y_train = []
        self.xy = []

    ############
    #
    # main call to build the model
    #
    def build(self):
        intents = openAllJsons(lang='en')
        self.processIntents(intents)
        self.createTrainingData()
        model = self.startTraining()
        self.saveModel(model)

    ############
    #
    # Open all intents and process them
    #
    def processIntents(self, intents):
        for intent in intents:
            tag = intent['tag']
            # add to tag list
            self.tags.append(tag)
            for pattern in intent['patterns']:
                # tokenize each word in the sentence
                w = tokenize(pattern)
                # add to our words list
                self.all_words.extend(w)
                # add to xy pair
                self.xy.append((w, tag))

        # stem and lower each word
        ignore_words = ['?', '.', '!']
        self.all_words = [stem(w, self.lang)
                          for w in self.all_words if w not in ignore_words]
        # remove duplicates and sort
        self.all_words = sorted(set(self.all_words))
        self.tags = sorted(set(self.tags))

        print(len(self.xy), "patterns")
        print(len(self.tags), "tags:", self.tags)
        print(len(self.all_words), "unique stemmed words:", self.all_words)

    ############
    #
    # Create all the data needed for training
    # the model
    #
    def createTrainingData(self):
        X_train = []
        y_train = []
        # create training data
        for (pattern_sentence, tag) in self.xy:
            # X: bag of words for each pattern_sentence
            bag = bag_of_words(pattern_sentence, self.all_words)
            X_train.append(bag)
            # y: PyTorch CrossEntropyLoss needs only class labels, not one-hot
            label = self.tags.index(tag)
            y_train.append(label)

        self.X_train = np.array(X_train)
        self.y_train = np.array(y_train)

    ############
    #
    # Actually start the training
    #
    def startTraining(self):
        num_epochs = 1000
        batch_size = 8
        learning_rate = 0.001
        input_size = len(self.X_train[0])
        hidden_size = 8
        output_size = len(self.tags)
        print("input size: ", input_size, " - ", "output size: ", output_size)
        dataset = ChatDataset(self.X_train, self.y_train)
        train_loader = DataLoader(dataset=dataset,
                                  batch_size=batch_size,
                                  shuffle=True,
                                  num_workers=0)

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        model = NeuralNet(input_size, hidden_size, output_size).to(device)

        # Loss and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
        # Train the model
        for epoch in range(num_epochs):
            for (words, labels) in train_loader:
                words = words.to(device)
                labels = labels.to(dtype=torch.long).to(device)

                # Forward pass
                outputs = model(words)
                # if y would be one-hot, we must apply
                # labels = torch.max(labels, 1)[1]
                loss = criterion(outputs, labels)

                # Backward and optimize
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            if (epoch+1) % 100 == 0:
                print(
                    f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

        print(f'final loss: {loss.item():.4f}')

        data = {
            "model_state": model.state_dict(),
            "input_size": input_size,
            "hidden_size": hidden_size,
            "output_size": output_size,
            "all_words": self.all_words,
            "tags": self.tags
        }

        return data

    ############
    #
    # Save the training model
    #
    def saveModel(self, data):
        FILE = "trainedModels/data_"+self.lang+"_trained.pth"
        torch.save(data, FILE)

        print(f'training complete. file saved to {FILE}')
