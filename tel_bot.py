import telebot
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo
)
from confing import TOKEN1  # Убедитесь, что TOKEN1 содержит ваш токен бота
from bot_logic import gen_pass, flip_coin

bot = telebot.TeleBot(TOKEN1)

# Параметры Mini App (замените на свои значения)
WEB_APP_URL = "https://pytelegrambotminiapp.vercel.app"  # URL вашего Mini App

generate_password_t_r = False

# *** Обработчики команд ***

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Обработчик команды /start."""
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}!')
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши что-нибудь!")
    bot.reply_to(message, 'Советую написать /help')

    # Добавляем кнопки для Mini App при старте
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("Открыть Mini App", web_app=WebAppInfo(WEB_APP_URL))) # Добавляем кнопку на клавиатуру
    bot.send_message(message.chat.id, "Нажмите кнопку ниже, чтобы открыть Mini App:", reply_markup=markup)

@bot.message_handler(commands=['hello'])
def send_hello(message):
    """Обработчик команды /hello."""
    bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    """Обработчик команды /bye."""
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['generate_password'])
def ask_password_length(message):
    """Обработчик команды /generate_password."""
    global generate_password_t_r
    generate_password_t_r = True
    bot.reply_to(message, 'Введите количество символов для пароля:')

@bot.message_handler(func=lambda message: generate_password_t_r)
def generate_password(message):
    """Обработчик ввода длины пароля."""
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

@bot.message_handler(commands=['coin'])
def send_coin(message):
    """Обработчик команды /coin."""
    coin = flip_coin()
    bot.reply_to(message, f"Монетка выпала так: {coin}")

@bot.message_handler(commands=['help'])
def send_command(message):
    """Обработчик команды /help."""
    bot.reply_to(message, 'Доступные команды: /start, /hello, /bye, /generate_password, /coin, /yesno, /miniapp, rick_rolls')  # Added miniapp command

@bot.message_handler(commands=['yesno'])
def ask_yesno(message):
    """Обработчик команды /yesno.  Отправляет inline-клавиатуру с Yes/No."""
    bot.send_message(message.chat.id, "Вы согласны?", reply_markup=gen_markup())

@bot.message_handler(commands=['miniapp'])
def send_miniapp_button(message):
    """Обработчик команды /miniapp.  Отправляет сообщение с кнопкой для запуска Mini App."""
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Открыть Mini App", web_app=WebAppInfo(WEB_APP_URL))) # Добавляем кнопку в inline keyboard
    bot.send_message(message.chat.id, "Нажмите кнопку ниже, чтобы открыть Mini App:", reply_markup=markup)

# *** Обработчики Inline Keyboard ***

def gen_markup():
    """Создает inline-клавиатуру с кнопками Yes и No."""
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
                InlineKeyboardButton("No", callback_data="cb_no"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """Обработчик callback-запросов для кнопок Yes/No."""
    if call.data == "cb_yes":
        bot.answer_callback_query(call.id, "Вы выбрали 'Да'!")
        bot.send_message(call.message.chat.id, "Вы выбрали: Да")
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Вы выбрали 'Нет'!")
        bot.send_message(call.message.chat.id, "Вы выбрали: Нет")
    else:
        bot.answer_callback_query(call.id, "Неизвестный вариант ответа")
        bot.send_message(call.message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте еще раз.")

# *** Обработчик данных, полученных из Mini App ***

@bot.message_handler(content_types=['web_app_data'])
def web_app_data_handler(message):
    """Обработчик данных, отправленных из Mini App."""
    try:
        bot.reply_to(message, f"Вы отправили из Mini App: {message.web_app_data.data}")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка при обработке данных из Mini App: {e}")

# *** Обработчик всех остальных сообщений ***
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """Обработчик всех текстовых сообщений, не являющихся командами."""
    if message.text == 'rick_rolls':
        bot.reply_to(message, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    else:
        bot.reply_to(message, 'я не понимаю')


# *** Запуск бота ***

bot.infinity_polling()
