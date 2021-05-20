from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

preq_bot = ChatBot(name='preq_bot')
trainer = ListTrainer(preq_bot)

with open('prequel_training.txt', 'r') as file:
    lines = file.readlines()
trainer.train(lines)

while True:
    text = input(': ')
    if 'exit' in text:
        break
    print(preq_bot.get_response(text))
