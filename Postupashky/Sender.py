import sqlite3
from itertools import groupby
import warnings
from time import sleep

warnings.filterwarnings("ignore")
from bs4 import BeautifulSoup
import re
import urllib3
import datetime
from Postupashky import  config
import telebot
from telebot import types
import sys
sys.path.append('../')

from Postupashky.models import Subs, Calendar

bot = telebot.TeleBot('724383512:AAFlLv7rbwC-DC_Bcr_abdkWCK1SZA4vkmU')


# datas = datetime.date.today().strftime("%Y-%m-%d")
def pars():
    d = datetime.datetime.today() + datetime.timedelta(days=1)

    events=Calendar.select().where(Calendar.date == d)

    try:
        print(events[0].name)
        for ev in events :
            etypes=str(ev.typeles).split(';');
            for s in Subs.select():
                for t in etypes:
                    sless=str(s.lessons).split(';')
                    if(t in sless):
                        sent_to_tg(ev.name, ev.url, s.tel_id)
                        break
    except:
        print("Завтра нет олимпиады")



def sent_to_tg(text, url,tel_id):
    print(text,url,tel_id)
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text=text, url=url)
    keyboard.add(url_button)
    bot.send_message(tel_id, "Привет, завтра олимпиада: \n"+text, reply_markup=keyboard)

if __name__ == '__main__':
    while (True):
        pars()
        sleep(60*60*24)