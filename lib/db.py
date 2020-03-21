from peewee import *
from .settings import get_settings

connstring = get_settings()["db"]

db = MySQLDatabase(connstring)

class Post(Model):
    postid = CharField()
    added = DateField()

    class Meta:
        database = db # This model uses the "people.db" database.