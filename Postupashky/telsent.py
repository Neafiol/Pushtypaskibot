# -*- coding: utf-8 -*-

import telebot
from telebot import types
import sys
import os
import urllib3
sys.path.append('../')
from models import Subs

token = '724383512:AAFlLv7rbwC-DC_Bcr_abdkWCK1SZA4vkmU'

start_text="""
    Привет, я буду напоминать тебе о всех олипиадах, дедлайнах регистрауии, подачи заявок на проектные конкурсы и тд.
    Уведомления приходят за день до мероприятия, так что не отключай уведомления, буть расторопным и удачи тебе.
"""
restart_text="""
    Ты уже с нами.
"""

bot = telebot.TeleBot(token)

# from T_bot.models import Subscriber
def log(txt):
    print(txt)
    file = open("../log.txt", "a")
    file.write(txt + '\n')
    file.close()



@bot.message_handler(commands=['start'])
def repeat_all_messages(message):  # Название функции не играет никакой роли, в принципе

    if len(Subs.select().where(Subs.tel_id == message.chat.id))==0:
        user=Subs(lessons='-1', name=str(message.from_user.first_name) + '_' + str(message.from_user.last_name), tel_id=int(message.chat.id))
        user.save()
        bot.send_message(message.chat.id, start_text)

        http = urllib3.PoolManager()
        http.request('GET', "https://alarmerbot.ru/?key=754bbe-fe8dcd-e68fa9&message="+'Вступил: '+str(message.from_user.first_name))

    else:
        bot.send_message(message.chat.id, restart_text)


    markup = types.InlineKeyboardMarkup()
    less_text = ['Математика', 'Информатика', 'Физика', 'Экономика', 'Биология', 'Химия']

    for i in range(6):
        button = types.InlineKeyboardButton(text=less_text[i], callback_data=str(i))
        markup.add(button)


    bot.send_message(message.chat.id, "Выбери интересующие тебя предметы", reply_markup=markup)




@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    less_text=['Математика','Информатика','Физика','Экономика','Биология','Химия']
    print(type(call.data))


    if call.from_user:
        if int(call.data) in range(6):

            s=Subs.select().where(Subs.tel_id == call.message.chat.id).get()
            s.lessons+=';'+str(call.data)
            s.save()

            bot.send_message(chat_id=call.message.chat.id, text="Предмет выбран "+less_text[int(call.data)])

            markup = types.InlineKeyboardMarkup()
            les=str(s.lessons).split(';')
            for i in range(len(less_text)):
                b=True
                for k in les:
                    if i==int(k):
                        b=False
                        break
                if(b):
                    button = types.InlineKeyboardButton(text=less_text[int(i)], callback_data=str(i))
                    markup.add(button)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Можешь еще выбрать" ,reply_markup=markup)

            
            log(str(call.from_user.last_name)+"Выбрал: "+call.data)


@bot.message_handler(content_types=["text"])
# обработка ответа от участника
def repeat_all_messages(message):
    bot.send_message(message.chat.id, "Я не отвечаю на сообщения.")
    try:
        log(str(message.from_user.last_name) + ' : ' +str(message.text))
    except:
        1


if __name__ == '__main__':
    #bot.send_message(445330281, "123")
    while (True):
        try:
            bot.polling(none_stop=True)
        except:
            print("Error")
            bot.polling(none_stop=True)
