
from core.Chat import Chat


lang = 'es'
my_chat = Chat(lang, path='intents/' + lang + '/')
my_chat.startChat()
