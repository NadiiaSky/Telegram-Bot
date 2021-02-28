import telebot
from telebot import types

bot = telebot.TeleBot("1611700876:AAHimV4W1CEvMrwlL95bJr_qpiW3XkXYXvI")  # You can set parse_mode by
# default. HTML or MARKDOWN

user_dict = {}

CHANGE_NAME_TEXT = "Змінити ім'я"
CHANGE_AGE_TEXT = "Змінити вік"
CHANGE_GENDER_TEXT = "Змінити стать"
BACK_TEXT = "Назад"

INFO_TEXT = "Інформація про мене"
SETTINGS_TEXT = "Налаштування"

MALE = "Чоловік"
FEMALE = "Жінка"


class User:
    def __init__(self):
        self.name = None
        self.age = None
        self.gender = None

    def set_name(self, name):
        if 2 <= len(name) <= 20:
            self.name = name
        else:
            raise Exception("Ім'я повинно бути від 2 до 20 символів")

    def set_age(self, age):
        if age.isdigit():
            self.age = age
        else:
            raise Exception("Вік повинен бути вказаний цифрою. \nСкільки тобі років?")

    def set_gender(self, gender):
        if (gender == MALE) or (gender == FEMALE):
            self.gender = gender
        else:
            raise Exception("Стать повинна бути вибрана з меню. \nЯка ваша стать?")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
    Привіт! Давай знайомитись:) \nНапиши своє ім'я
    """)
    bot.register_next_step_handler(msg, send_name)


def send_name(message):
    chat_id = message.chat.id
    name = message.text
    user = User()
    user_dict[chat_id] = user

    try:
        user.set_name(name)
    except Exception as e:
        msg = bot.reply_to(message, "Ім'я повинно бути від 2 до 20 символів")
        bot.register_next_step_handler(msg, send_name)
        return

    msg = bot.reply_to(message, 'Чудово, а тепер свій вік')
    bot.register_next_step_handler(msg, send_age)


def send_age(message):
    chat_id = message.chat.id
    age = message.text
    user = user_dict[chat_id]

    try:
        user.set_age(age)
    except Exception as e:
        msg = bot.reply_to(message, "Вік повинен бути вказаний цифрою. \nСкільки тобі років?")
        bot.register_next_step_handler(msg, send_age)
        return

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(MALE, FEMALE)
    msg = bot.send_message(message.chat.id, 'Вкажи свою стать', reply_markup=markup)
    bot.register_next_step_handler(msg, send_gender)


def send_gender(message):
    chat_id = message.chat.id
    gender = message.text
    user = user_dict[chat_id]

    try:
        user.set_gender(gender)
    except Exception as e:
        msg = bot.reply_to(message, "Стать повинна бути вибрана з меню. \nЯка ваша стать?")
        bot.register_next_step_handler(msg, send_gender)
        return

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(INFO_TEXT, SETTINGS_TEXT)
    msg = bot.send_message(message.chat.id, 'Ось ми і познайомились, ' + user.name + ':)', reply_markup=markup)
    bot.send_message(message.chat.id, 'Обери пункт меню')
    bot.register_next_step_handler(msg, choose_action)


def choose_action(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    chat_id = message.chat.id
    user = user_dict[chat_id]
    menu = message.text
    if menu == INFO_TEXT:
        print(user.name, user.age, user.gender)
        msg = bot.reply_to(message, "Ім'я " + user.name + '\nВік: ' + str(user.age) + '\nСтать: ' + user.gender)
        bot.register_next_step_handler(msg, choose_action)
    elif menu == SETTINGS_TEXT:
        markup.add(CHANGE_NAME_TEXT, CHANGE_AGE_TEXT, CHANGE_GENDER_TEXT, BACK_TEXT)
        msg = bot.send_message(message.chat.id, 'Обери функцію', reply_markup=markup)
        bot.register_next_step_handler(msg, edit_action)


def edit_action(message):
    menu = message.text
    if menu == CHANGE_NAME_TEXT:
        msg = bot.send_message(message.chat.id, "Введіть нове ім'я")
        bot.register_next_step_handler(msg, edit_name)
    elif menu == CHANGE_AGE_TEXT:
        msg = bot.send_message(message.chat.id, "Введіть нове значення віку")
        bot.register_next_step_handler(msg, edit_age)
    elif menu == CHANGE_GENDER_TEXT:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(MALE, FEMALE)
        msg = bot.send_message(message.chat.id, "Оберіть свою стать", reply_markup=markup)
        bot.register_next_step_handler(msg, edit_gender)
    elif menu == BACK_TEXT:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(INFO_TEXT, SETTINGS_TEXT)
        msg = bot.reply_to(message, 'Обери пункт меню', reply_markup=markup)
        bot.register_next_step_handler(msg, choose_action)


def edit_name(message):
    chat_id = message.chat.id
    name = message.text
    user = user_dict[chat_id]
    try:
        user.set_name(name)
    except Exception as e:
        msg = bot.reply_to(message, str(e))
        bot.register_next_step_handler(msg, edit_name)
        return

    msg = bot.reply_to(message, "Чудово, ваше нове ім'я: " + user.name)
    bot.register_next_step_handler(msg, edit_action)


def edit_age(message):
    chat_id = message.chat.id
    age = message.text
    user = user_dict[chat_id]

    try:
        user.set_age(age)
    except Exception as e:
        msg = bot.reply_to(message, str(e))
        bot.register_next_step_handler(msg, edit_age)
        return

    msg = bot.reply_to(message, "Чудово, ваш новий вік: " + user.age)
    bot.register_next_step_handler(msg, edit_action)


def edit_gender(message):
    chat_id = message.chat.id
    gender = message.text
    user = user_dict[chat_id]

    try:
        user.set_gender(gender)
    except Exception as e:
        msg = bot.reply_to(message, str(e))
        bot.register_next_step_handler(msg, edit_gender)
        return

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(CHANGE_NAME_TEXT, CHANGE_AGE_TEXT, CHANGE_GENDER_TEXT, BACK_TEXT)
    msg = bot.reply_to(message, "Чудово, ваша стать: " + user.gender, reply_markup=markup)
    bot.register_next_step_handler(msg, edit_action)


bot.polling()
