import random
import torch
from core.model import NeuralNet
from utils.nltk_utils import bag_of_words, tokenize
from utils.fileHandler import openAllJsons

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


THRESHOLD = 0.75


class Chat:
    def __init__(self, lang='en'):
        self.lang = lang
        self.intents = None
        self.all_words = []
        self.tags = []
        self.model = None

    ############
    #
    # start the chatting process
    #
    def startChat(self):
        self.intents = openAllJsons(self.lang)
        self.rebuildModel()
        self.chatting()

    ############
    #
    # rebuild the models from file by language
    #
    def rebuildModel(self):
        FILE = "trainedModels/data_"+self.lang+"_trained.pth"
        data = torch.load(FILE)
        input_size = data["input_size"]
        hidden_size = data["hidden_size"]
        output_size = data["output_size"]
        self.all_words = data['all_words']
        self.tags = data['tags']
        model_state = data["model_state"]

        self.model = NeuralNet(input_size, hidden_size, output_size).to(device)
        self.model.load_state_dict(model_state)
        self.model.eval()

    ############
    #
    # proccess the user's sentence in order to be used
    #
    def processSentence(self, sentence):
        sentence = tokenize(sentence)
        X = bag_of_words(sentence, self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)
        return X

    ############
    #
    # Search for a response from model
    #
    def searchForResponse(self, X):
        output = self.model(X)
        _, predicted = torch.max(output, dim=1)

        tag = self.tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > THRESHOLD:
            for intent in self.intents:
                if tag == intent["tag"]:
                    return random.choice(intent['responses'])
        return None

    ############
    #
    # Chatting on cmd
    #
    def chatting(self):
        bot_name = "Sam"
        print("Let's chat! (type 'quit' to exit)")
        while True:
            # sentence = "do you use credit cards?"
            sentence = input("You: ")
            if sentence == "quit":
                break

            X = self.processSentence(sentence)
            response = self.searchForResponse(X)
            if response:
                print(
                    f"{bot_name}: {response}")
            else:
                print(f"{bot_name}: I do not understand...")
