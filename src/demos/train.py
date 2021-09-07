from pytorch_chatbot.train import Train

lang = 'es'
train = Train(lang, intentsPath='src/demos/intents/es/')
train.build()
