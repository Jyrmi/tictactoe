from peewee import *

db = SqliteDatabase("tictactoe.db")


class User(Model):
    email = CharField()
    password = CharField()
    salt = CharField()

    class Meta:
        database = db
