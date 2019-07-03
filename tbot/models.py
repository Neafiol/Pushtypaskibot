
import sqlite3
from datetime import date
from peewee import *

db = SqliteDatabase('../db.sqlite3')

class Subs(Model):
    tel_id=IntegerField()
    name = TextField()
    lessons = TextField()

    class Meta:
        database = db
        db_table='T_bot_subscriber'

class Calendar(Model):
    date=DateField()
    name = TextField()
    url = TextField()
    typeles = IntegerField()

    class Meta:
        database = db
        db_table='Calendar'

# Calendar.create_table()
# uncle_bob = Subs(name='Bob', tel_id=121212)
# uncle_bob.save()