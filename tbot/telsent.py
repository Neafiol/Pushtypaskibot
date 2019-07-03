# -*- coding: utf-8 -*-
import config
import telebot
from telebot import types
import sqlite3
import sys
import os


# from T_bot.models import Subscriber
def log(txt):
    file = open("../log.txt", "a")
    file.write(txt + '\n')
    file.close()


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def repeat_all_messages(message):  # Название функции не играет никакой роли, в принципе

    conn = sqlite3.connect("../db.sqlite3")  # или :memory: чтобы сохранить в RAM
    db = conn.cursor()
    # добавим в базу
    now = db.execute("""
       SELECT * FROM T_bot_subscriber WHERE tel_id={}
    """.format(message.chat.id)).fetchall()

    if (len(now) == 0):
        name = str(message.from_user.first_name) + '_' + str(message.from_user.last_name)
        db.execute("""
            INSERT INTO T_bot_subscriber  (tel_id, `name`) VALUES({},'{}')
        """.format(str(message.chat.id), name))
        bot.send_message(message.chat.id, config.start_text)
    else:
        bot.send_message(message.chat.id, config.restart_text)
    conn.commit()
    conn.close()
    print("enter: ", message.chat.id)

    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Математика', callback_data='meth')
    button.OneTimeKeyboard = True
    button1 = types.InlineKeyboardButton(text='Информатика', callback_data='inform')
    button1.OneTimeKeyboard = True
    markup.add(button, button1)

    bot.send_message(message.chat.id, "Выбери интересующие тебя предметы", reply_markup=markup)

    log("Присоеденился:" + str(message.from_user.last_name))


@bot.callback_query_handler(func=lambda call: True)
def repeat_all_messages(call):
    conn = sqlite3.connect("../db.sqlite3")  # или :memory: чтобы сохранить в RAM
    db = conn.cursor()
    if call.from_user:
        if call.data == "/done":
            db.execute("""
                               UPDATE T_bot_subscriber SET  status_message=0 WHERE `tel_id`={}
                            """.format(call.from_user.id))

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Вопрос закрыт")
            bot.send_message(chat_id=call.message.chat.id, text="Предмет выбран")
            log("Закрыл вопрос:" + call.from_user.last_name)
    conn.commit()
    conn.close()


@bot.message_handler(content_types=["text"])
# обработка ответа от участника
def repeat_all_messages(message):
    bot.send_message(message.chat.id, "Я не отвечаю на сообщения.")
    log(str(message.from_user.last_name) + ' : ' + message.text)


if __name__ == '__main__':
    # bot.send_message(445330281, "123")
    try:
        bot.polling(none_stop=True)
    except:
        print("Error")
        bot.polling(none_stop=True)
