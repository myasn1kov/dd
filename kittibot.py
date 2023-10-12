import requests  # Импортируем библиотеку для работы с запросами
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram import Bot, ReplyKeyboardMarkup
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

load_dotenv()

secret_token = os.getenv('TOKEN')

URL = 'https://api.thecatapi.com/v1/images/search'

# Укажите id своего аккаунта в Telegram
chat_id = 533401501
text = 'Я пока совсем глупый!'
# Отправка сообщения
#bot.send_message(chat_id, text) 

def get_new_image():
    try:
        response = requests.get(URL) # пробуем получить фото котика 
    except Exception as error: # обрабатываем исключение и заменяем url
        # Печатать информацию в консоль теперь не нужно:
        # всё необходимое будет в логах
        # print(error)      
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
    
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat 

def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())

def wake_up(update, context):
    # В ответ на команду /start 
    # будет отправлено сообщение 'Спасибо, что включили меня'
    chat = update.effective_chat
    name = update.message.chat.first_name
    # Вот она, наша кнопка.
    # Обратите внимание: в класс передаётся список, вложенный в список, 
    # даже если кнопка всего одна.
    # Каждый вложенный список определяет
    # новый ряд кнопок в интерфейсе бота.
    # Здесь описаны две кнопки в первом ряду и одна - во втором.
    buttons = ReplyKeyboardMarkup(
        [['Обедал ли Саша?', 'Статус Саши'],['Фото котика', '/newcat']], resize_keyboard=True)
    context.bot.send_message(chat_id=chat.id, 
                             text='Спасибо, что включили меня, {}!'.format(name), 
                             # Добавим кнопку в содержимое отправляемого сообщения
                             reply_markup=buttons)

def status(update, context):
    # В ответ на команду /status 
    # будет отправлено сообщение 'Саша вас очень любит!'
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id,
                             text='Саша вас очень любит!')

def dinner(update, context):
    # В ответ на команду /status 
    # будет отправлено сообщение 'Саша вас очень любит!'
    chat = update.effective_chat
    if datetime.now().time() < datetime.strptime('14:00', '%H:%M').time():
        context.bot.send_message(chat_id=chat.id, 
                                 text='Саша еще не обедал!')
    else:
        context.bot.send_message(chat_id=chat.id, 
                                 text='Саша уже пообедал!')


def say_hi(update, context):
    # Получаем информацию о чате, из которого пришло сообщение,
    # и сохраняем в переменную chat
    chat = update.effective_chat
    # В ответ на любое текстовое сообщение 
    # будет отправлено 'Привет, я KittyBot!'
    context.bot.send_message(chat_id=chat.id, text='Саша получил ваше сообщение!')

# Регистрируется обработчик CommandHandler;
# он будет отфильтровывать только сообщения с содержимым '/start'
# и передавать их в функцию wake_up()

def main():
    # Здесь укажите токен, 
    # который вы получили от @Botfather при создании бот-аккаунта
    bot = Bot(token=secret_token)
    updater = Updater(token=secret_token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    # Регистрируется обработчик MessageHandler;
    # из всех полученных сообщений он будет выбирать только текстовые сообщения
    # и передавать их в функцию say_hi() или status
    updater.dispatcher.add_handler(MessageHandler(Filters.text('Статус Саши'), status))
    updater.dispatcher.add_handler(MessageHandler(Filters.text('Обедал ли Саша?'), dinner))
    updater.dispatcher.add_handler(MessageHandler(Filters.text('Фото котика'), new_cat))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))


    # Метод start_polling() запускает процесс polling, 
    # приложение начнёт отправлять регулярные запросы для получения обновлений.
    updater.start_polling()
    # Бот будет работать до тех пор, пока не нажмете Ctrl-C
    updater.idle() 

if __name__ == '__main__':
    main() 