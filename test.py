from ChatBot import load_bot
from chatterbot import conversation
my_bot = load_bot('')
response_text = ''
while True:
    if response_text == '':
        input_statement = conversation.Statement(text=input(':'))
    else:
        input_statement = conversation.Statement(text=input(':'), in_response_to=response_text)
    if 'exit' in input_statement.text:
        break
    print('Previous statement: ', response_text)
    response = my_bot.generate_response(input_statement)
    response_text = response.text
    print('Your statement: ', input_statement.text)
    print('Bots response: ', response.text)