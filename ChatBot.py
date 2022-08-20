from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot import conversation
import pickle
import os
import time

from config import create_twitter_api, readConfig
from twitter import checkForDMs


def train_bot(my_bot):
    corpus_trainer = ChatterBotCorpusTrainer(my_bot)
    corpus_trainer.train('chatterbot.corpus.english')

    # with open(save_path, 'w') as file:
    #     pickle.dump(my_bot, file)
    return my_bot


def load_bot(file_name):
    my_bot = ChatBot(name='fake_laura', read_only=False,
                     logic_adapters=['chatterbot.logic.MathematicalEvaluation',
                                     'chatterbot.logic.BestMatch',
                                     'chatterbot.logic.TimeLogicAdapter'])
    if os.path.exists('db.sqlite3'):
        return my_bot
    else:
        return train_bot(my_bot)


def main():
    # Creating/loading the chatbot
    my_bot = load_bot('chatterbot.pkl')

    # Setting up twitter functionality
    api = create_twitter_api()
    since_id = readConfig()

    while True:
        new_messages, since_id = checkForDMs(api, since_id)
        if new_messages:
            for message in reversed(new_messages):
                senderID = message[0]
                text = message[1]
                sender = message[2]
                response = my_bot.get_response(text)
                print('Sender: ', sender)
                print('Text: ', text)
                print('Response: ', response)
                api.send_direct_message(senderID, response.text)
        time.sleep(60)


if __name__ == '__main__':
    main()
