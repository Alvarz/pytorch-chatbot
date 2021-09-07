
from pytorch_chatbot.chatbot import Chat

lang = 'es'
my_chat = Chat(lang, intentsPath='src/demos/intents/' + lang + '/')
my_chat.startChat()

# my_chat.setup()
#answer, action = my_chat.simpleChat("hola")
#print(answer, action)
