from peewee import *
from playhouse.db_url import connect
from .settings import get_settings

connstring = get_settings()["db"]

db = connect(connstring)

class FacebookThread(Model):
    pageid=CharField()
    postid = CharField()
    active = BooleanField()

    def get_combined(self):
        return "%s_%s" % (self.pageid, self.postid)

class FacebookComment(Model):
    postid = CharField(index=True)
    added = DateTimeField()
    fromname = CharField()
    fromid = CharField()
    message = CharField()
    threadid = ForeignKeyField(FacebookThread)

    class Meta:
        database = db # This model uses the "people.db" database.

class FacebookReply(Model):
    postid = CharField()
    message = CharField()
    responded = DateTimeField(null=True, index=True)

db.connect()
try:
    db.create_tables([FacebookComment])
except:
    pass