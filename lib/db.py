from peewee import *
from .settings import get_settings

connstring = get_settings()["db"]

db = MySQLDatabase(connstring)

class FacebookComment(Model):
    postid = CharField(index=True)
    added = DateTimeField()
    fromname = CharField()
    fromid = CharField()
    message = CharField()
    threadid = CharField(index=True)

    class Meta:
        database = db # This model uses the "people.db" database.

class FacebookReply(Model):
    postid = CharField()
    message = CharField()
    responded = DateTimeField(null=True, index=True)
    threadid = CharField(index=True)

db.connect()
try:
    db.create_tables([FacebookComment])
except:
    pass