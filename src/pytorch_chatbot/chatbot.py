import random
import torch
from pytorch_chatbot.model import NeuralNet
from pytorch_chatbot.utils.nltk_utils import bag_of_words, tokenize
from pytorch_chatbot.utils.fileHandler import openAllJsons
from pytorch_chatbot.utils.cmd import bcolors

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


THRESHOLD = 0.75
user_id = 123


class Chat:
    def __init__(self, lang='es', intentsPath='intents/es/', modelPath='trainedModels/data_es_trained.pth'):
        self.lang = lang
        self.intents = None
        self.all_words = []
        self.tags = []
        self.model = None
        self.intentsPath = intentsPath
        self.modelPath = modelPath
        self.context = {}

    ############
    #
    # start the chatting process
    #
    def startChat(self):
        self.setup()
        self.chatting()

    def setup(self):
        self.intents = openAllJsons(self.lang, path=self.intentsPath)
        self.rebuildModel()

    def simpleChat(self, sentence):
        X = self.processSentence(sentence)
        response, action = self.searchForResponse(X)
        if response:
            return response, action
        else:
            return "I do not understand..."

    ############
    #
    # rebuild the models from file by language
    #
    def rebuildModel(self):
        # FILE = "trainedModels/data_"+self.lang+"_trained.pth"
        FILE = self.modelPath
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
        X = bag_of_words(sentence, self.all_words, self.lang)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)
        return X

    def setContext(self, user_id, context_to_set):
        if user_id not in self.context:
            self.context[user_id] = []
        print('context to be setted:', context_to_set)
        self.context[user_id].append(context_to_set)

    def removeContext(self, user_id, context_to_set):
        if user_id in self.context and context_to_set in self.context[user_id]:
            print('context to be removed:', context_to_set)
            self.context[user_id].remove(context_to_set)

        ############
        #
        # Search for a response from model
        #

    def searchForResponse(self, X):
        answer = None
        action = None
        output = self.model(X)
        _, predicted = torch.max(output, dim=1)

        tag = self.tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > THRESHOLD:
            for i in self.intents:
                if tag == i["tag"]:

                    # check if has action and perform the action
                    if 'action' in i:
                        action = i['action']

                    # check if this intent is contextual and applies to this user's conversation
                    if not 'context_filter' in i or \
                            (user_id in self.context and 'context_filter' in i and i['context_filter'] in self.context[user_id]):
                        print('tag:', i['tag'])
                        if 'context_filter' in i:
                            print('context used on conversation:',
                                  i['context_filter'])
                        # a random response from the intent
                        answer = random.choice(i['responses'])

                    # set context for this intent if necessary
                    if 'context_set' in i:
                        self.setContext(user_id, i['context_set'])
                    # remove context for this intent if necessary
                    if 'context_remove' in i:
                        self.removeContext(user_id, i['context_remove'])
        print(self.context)
        return answer, action

    ############
    #
    # Chatting on cmd
    #

    def chatting(self):
        bot_name = "Bebop"
        print(bcolors.OKBLUE + "Let's chat! (type 'quit' to exit)" + bcolors.ENDC)
        while True:
            # sentence = "do you use credit cards?"
            sentence = input("You: ")
            if sentence == "quit":
                break

            X = self.processSentence(sentence)
            response = self.searchForResponse(X)
            if response:
                print(bcolors.OKBLUE +
                      f"{bot_name}: {response}" + bcolors.ENDC)
            else:
                print(
                    f"{bcolors.OKBLUE} {bot_name}: I do not understand...{bcolors.ENDC}")
