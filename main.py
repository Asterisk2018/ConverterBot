import telebot
from config import TOKEN, keys
from extensions import ConvertionException, CriptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Я твой бот-конвертер валют и вот что умею: \n\
- Показывать списки доступных для конвертации валют -/values \n\
- Конвертировать валюты.\n\
Чтобы начать конвертацию, введите команду в следующем формате: \n\
    <имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n\
    Чтобы увидеть список всех доступных валют, введите команду-/values\n\
Если нужно напомнить, как начать конвертацию, введите команду - /help'
    bot.reply_to(message, f'Привет, {message.chat.id}!\n' + text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные для ковертации валюты'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, f'{text} \n Если нужно напомнить, как начать конвертацию, введите команду - /help')

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
   try:
       values = message.text.split(' ')
       if len(values) != 3:
           raise ConvertionException('Слишком много параметров')
       quote, base, amount = values
       total_base = CriptoConverter.convert(quote, base, amount)
   except ConvertionException as e:
       bot.reply_to(message, f'Ошибка пользователя.\n{e}')
   except Exception as e:
       bot.reply_to(message, f'Хм, что-то пошло не так с {e}')
   else:
       text = f'Стоимость {amount} {quote} в {base} = {total_base}'
       bot.send_message(message.chat.id, text)

bot.polling()