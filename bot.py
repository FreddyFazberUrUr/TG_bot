import random
import info
import telebot
from telebot import types
bot = telebot.TeleBot('token')

# Надеюсь, вы оцените по достоинству мои старания


@bot.message_handler(commands=['go', 'start'])
def say_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item3 = types.KeyboardButton("Еще немного фишек")
    item2 = types.KeyboardButton("Виды пельменей")
    item1 = types.KeyboardButton('Психология Патрика Бейтмена')

    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\n\nЯ - <b>{1.first_name}</b>, "
                     "создан <i>Тимофеем Евенко</i>\nВведи /help если "
                     "нужна помощь в управлении ботом".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup
                     )


@bot.message_handler(commands=['help'])
def go_help(message):
    bot.send_message(message.chat.id, 'Комманды:\n'
                                      '/start и /go - начать работу с ботом.\n'
                                      '/help - список комманд и их назначения.\n'
                                      '<b>Для остальных функций есть кнопки внизу ↓ (под строкой ввода)</b>',
                     parse_mode='html')


@bot.message_handler(content_types=["text"])
def go_send_messages(message):
    if message.chat.type == 'private':
        if message.text == 'Еще немного фишек':

            keyboard = types.InlineKeyboardMarkup(row_width=1)
            itemboo = types.InlineKeyboardButton("Ссылка на Google", url="https://google.com")
            itemboo1 = types.InlineKeyboardButton('Рандомное число', callback_data='one')
            itemboo2 = types.InlineKeyboardButton("Калькулятор", callback_data='two')
            itemboo3 = types.InlineKeyboardButton("Ссылочка", url='https://youtu.be/dQw4w9WgXcQ')
            itemboo4 = types.InlineKeyboardButton("Как твои дела?", callback_data='three')

            keyboard.add(itemboo, itemboo1, itemboo2, itemboo3, itemboo4)

            bot.send_message(message.chat.id,
                             "{0.first_name}, окей, смотри, что у нас есть тут:\n".format(message.from_user),
                             reply_markup=keyboard)
        elif message.text == 'Виды пельменей':
            bot.send_message(message.chat.id, info.dumplings, parse_mode='html')

        elif message.text == 'Психология Патрика Бейтмена':
            bot.send_message(message.chat.id, info.text_bateman, parse_mode='html')


@bot.message_handler(content_types=info.CONTENT_TYPES)
def no_text(message):
    bot.send_message(message.chat.id, "Это не текст и не команда. Забирайте обратно")
    if message.content_type == 'photo':
        bot.send_photo(message.chat.id, message.photo[0].file_id, message.caption)
    elif message.content_type == 'audio':
        bot.send_audio(message.chat.id, message.audio.file_id, message.caption)
    elif message.content_type == 'sticker':
        bot.send_sticker(message.chat.id, message.sticker.file_id, message.caption)
    elif message.content_type == 'document':
        bot.send_document(message.chat.id, message.document.file_id, message.caption)
    elif message.content_type == 'video':
        bot.send_video(message.chat.id, message.video.file_id, message.caption)
    else:
        bot.send_message(message.chat.id, 'Файл пока не поддерживается :(')


@bot.callback_query_handler(func=lambda call: call.data in ['one', 'two', 'three', 'fourth'])
def callback_inline_one(call):
    if call.message:
        if call.data == 'one':
            bot.send_message(call.message.chat.id, str(random.randint(0, 100000)), parse_mode="html")

        elif call.data == 'two':
            bot.send_message(call.message.chat.id, "Еще в разработке.")

        elif call.data == 'three':
            bot.send_message(call.message.chat.id, "С тобой всегда хорошо!", parse_mode="html")


if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except ConnectionError as e:
        print('Ошибка соединения: ', e)
    except Exception as r:
        print("Непридвиденная ошибка: ", r)
    finally:
        print("До встречи!")
