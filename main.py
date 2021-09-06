#!/usr/bin/env python
import getopt
import sys
import os
from core.Chat import Chat
from utils.cmd import bcolors

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# question = ''
# if lang == 'es':
#     greeting = 'BOT: Hola!, como te puedo ayudar?'
# else:
#     greeting = 'BOT: Hi, how can I help you?'

# print(greeting)
# while question is not 'exit':
#     question = input('')
#     answer = chatbot.response(question)
#     print('BOT:', answer)


def main(argv):
    lang = 'es'
    question = 'hi'
    user_id = ''
    try:
        opts, args = getopt.getopt(
            argv, "hl:q:u", ["language=", "question=", "userid="])
    except getopt.GetoptError:
        print('index.py -l <language> -q <question> -u <user-id>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('index.py -l <language> -q <question> -u <user-id>')
            sys.exit()
        elif opt in ("-l", "--language"):
            lang = arg
        elif opt in ("-q", "--question"):
            question = arg
        elif opt in ("-u", "--userid"):
            user_id = arg
    print('Input language is: ', lang)
    print('Input question is: ', question)
    print('Input user_id is: ', user_id)
    my_chat = Chat(lang)
    answer = my_chat.cmdChat(question)
    print(bcolors.OKBLUE +
          f"{answer}" + bcolors.ENDC)
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
