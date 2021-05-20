from ChatBot import load_bot

my_bot = load_bot('')

while True:
    text = input(': ')
    if 'exit' in text:
        break
    print(my_bot.get_response(text))