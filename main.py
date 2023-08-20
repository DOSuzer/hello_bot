import os
import telebot

from dotenv import load_dotenv, find_dotenv
from telebot import types
from telegram_bot_pagination import InlineKeyboardPaginator

from db import Database


if not find_dotenv():
    print('Переменные окружения не загружены т.к отсутствует файл .env')
    exit()
else:
    load_dotenv()

token = os.getenv('TOKEN_API')


class User:
    def __init__(self, name):
        self.name = name
        self.family_name = None
        self.sex = None
        self.photo = None
        self.user_id = None


user_dict = {}

bot = telebot.TeleBot(token)

db = Database()
db.create_db()
print('БД подключена и бот запущен!')


@bot.message_handler(commands=['users'])
def get_users(message):
    """Просмотр пользователей для зарегистрированных пользователей."""
    if not db.user_exists(message.from_user.id):
        start_message(message)
    else:
        send_user_page(message)


@bot.callback_query_handler(func=lambda call:
                            call.data.split('#')[0] == 'user')
def user_page_callback(call):
    """Удаление профиля для отображения нового."""
    page = int(call.data.split('#')[1])
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    send_user_page(call.message, page)


def send_user_page(message, page=1):
    """Отправка профиля пользователя."""
    user_pages = db.get_users()
    paginator = InlineKeyboardPaginator(
        len(user_pages),
        current_page=page,
        data_pattern='user#{page}'
    )
    text = (f'Имя: {user_pages[page-1][1]},\n'
            f'Фамилия: {user_pages[page-1][2]},\n'
            f'Пол: {user_pages[page-1][3]}')
    bot.send_photo(chat_id=message.chat.id,
                   photo=user_pages[page-1][4],
                   caption=text,
                   reply_markup=paginator.markup,
                   parse_mode='Markdown')


@bot.message_handler(commands=['start'])
def start_message(message):
    """Точка старта. Знакомство либо список доступных команд."""
    bot.send_message(message.chat.id, 'Здравствуй путник ✌️ ')
    if not db.user_exists(message.from_user.id):
        msg = bot.send_message(message.chat.id,
                               'Давай знакомиться. Введи своё имя:')
        bot.register_next_step_handler(msg, process_name_step)
    else:
        bot.send_message(message.chat.id,
                         'Для просмотра пользователей отправь /users')


def process_name_step(message):
    """Фиксируем имя, фото, id и создаем экземпляр класса пользователя."""
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        user.user_id = message.from_user.id
        user.photo = bot.get_user_profile_photos(
            message.from_user.id).photos[0][0].file_id
        msg = bot.reply_to(message, 'Введи свою фамилию:')
        bot.register_next_step_handler(msg, process_family_name_step)
    except Exception as e:
        bot.reply_to(message, e)


def process_family_name_step(message):
    """Фиксируем фамилию."""
    try:
        chat_id = message.chat.id
        family_name = message.text
        user = user_dict[chat_id]
        user.family_name = family_name
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                           resize_keyboard=True)
        markup.add('Мужской', 'Женский')
        msg = bot.reply_to(message, 'Укажи свой пол:', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, e)


def process_sex_step(message):
    """Фиксируем пол и отправляем данные в БД."""
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == u'Мужской') or (sex == u'Женский'):
            user.sex = sex
        else:
            raise Exception('Хей, мы вообще-то в России!')
        bot.send_message(chat_id, 'Рад знакомству '
                         + user.name + ' ' + user.family_name
                         + '\nПол: ' + user.sex)
        bot.send_message(chat_id, '\n Теперь тебе доступен просмотр'
                         + ' других профлей по команде /users.')
        db.add_user(user)
    except Exception as e:
        bot.reply_to(message, e)


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.infinity_polling()
