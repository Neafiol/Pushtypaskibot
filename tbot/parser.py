import sqlite3
from itertools import groupby
import warnings
from time import sleep

warnings.filterwarnings("ignore")
from bs4 import BeautifulSoup
import re
import urllib3
import datetime
import config
import telebot
from telebot import types
import sys
sys.path.append('../')

from models import Subs, Calendar

bot = telebot.TeleBot(config.token)


# datas = datetime.date.today().strftime("%Y-%m-%d")
def pars():
    d = datetime.datetime.today() + datetime.timedelta(days=6)

    events=Calendar.select().where(Calendar.date == d)
    print(events[0].name)

    subs=Subs.select()
    for s in subs:
        tps = str(s.lessons).split(';')
        for e in events:
            if str(e.typeles) in tps:
                sent_to_tg(e.name, e.url,s.tel_id)



def sent_to_tg(text, url,tel_id):
    print(tel_id)
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text=text, url=url)
    keyboard.add(url_button)
    bot.send_message(tel_id, "Привет, завтра олимпиада: \n"+text, reply_markup=keyboard)

if __name__ == '__main__':
    while (True):
        pars()
        sleep(60*60*24)