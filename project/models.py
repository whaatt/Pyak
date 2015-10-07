# File: models.py
# Project DB Models

from peewee import *
import datetime

# use threadlocals option just for added safety
DB = SqliteDatabase('yak.db', threadlocals = True)

# suggested by peewee
class BaseModel(Model):
  class Meta:
    database = DB

class School(BaseModel):
  name = CharField(max_length = 128)
  latitude = DoubleField()
  longitude = DoubleField()

class Yak(BaseModel):
  content = TextField()
  latitude = DoubleField()
  longitude = DoubleField()
  likesHistory = TextField() # really array
  commentsHistory = TextField() # really array
  time = DateTimeField() # takes datetime objects
  school = ForeignKeyField(School, related_name='yaks')
  originalID = CharField(max_length = 64)

class Comment(BaseModel):
  content = TextField()
  likesHistory = TextField() # really array
  time = DateTimeField() # takes datetime objects
  yak = ForeignKeyField(Yak, related_name='comments')
  originalID = CharField(max_length = 64)
