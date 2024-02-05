from peewee import *
import datetime

db = SqliteDatabase("tictactoe.db")

class BaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

class User(BaseModel):
    email = CharField()
    password = CharField()
    salt = CharField()

class Game(BaseModel):
    """
    moves: a list of moves in order that they were made as JSON 
    """
    moves = CharField(default="")
    started_at = DateTimeField(null=True)
    ended_at = DateTimeField(null=True)

class GamePlayer(BaseModel):
    user_id = CharField()
    game_id = CharField()
    is_creator = BooleanField(default=False)
    is_winner = BooleanField(default=False)