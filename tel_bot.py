import telebot
from confing import TOKEN1
from bot_logic import gen_pass


bot = telebot.TeleBot(TOKEN1)


generate_password_t_r = False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}!')
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши что-нибудь!")

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['generate_password'])
def ask_password_length(message):
    global generate_password_t_r
    generate_password_t_r = True
    bot.reply_to(message, 'Введите количество символов для пароля:')

@bot.message_handler(func=lambda message: generate_password_t_r)
def generate_password(message):
    global generate_password_t_r
    try:
        length = int(message.text)
        if length <= 0:
            raise ValueError("Длина пароля должна быть положительным числом.")
        password = gen_pass(length)
        bot.reply_to(message, f'Ваш сгенерированный пароль: {password}')
    except ValueError:
        bot.reply_to(message, 'Неправильный ввод. Пожалуйста, введите положительное целое число.')
    finally:
        generate_password_t_r = False  


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == 'rick_rolls':
        bot.reply_to(message, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')

bot.polling()
