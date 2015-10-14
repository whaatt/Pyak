# File: models.py
# Project DB Models

from peewee import *
import datetime

# use threadlocals option just for added safety
DB = SqliteDatabase('yak.db', threadlocals = True)
DB.connect() # explicit to show any errors

# suggested by peewee
class BaseModel(Model):
  class Meta:
    database = DB

class School(BaseModel):
  name = CharField(max_length = 127)
  latitude = DoubleField()
  longitude = DoubleField()

class Yak(BaseModel):
  content = TextField()
  latitude = DoubleField()
  longitude = DoubleField()
  finalLikeCount = IntegerField()
  finalCommentCount = IntegerField()
  time = DateTimeField() # takes datetime objects
  school = ForeignKeyField(School, related_name = 'yaks')
  originalID = CharField(max_length = 63, unique = True)
  isSpecial = BooleanField() # true if official message

class YakLikeCount(BaseModel):
  count = IntegerField()
  time = DateTimeField()
  # access like count history using yak.likeCounts
  yak = ForeignKeyField(Yak, related_name = 'likeCounts')

class YakCommentCount(BaseModel):
  count = IntegerField()
  time = DateTimeField()
  # access like count history using yak.commentCounts
  yak = ForeignKeyField(Yak, related_name = 'commentCounts')

class Comment(BaseModel):
  content = TextField()
  finalLikeCount = IntegerField()
  time = DateTimeField() # takes datetime objects
  yak = ForeignKeyField(Yak, related_name = 'comments')
  originalID = CharField(max_length = 63, unique = True)

class CommentLikeCount(BaseModel):
  count = IntegerField()
  time = DateTimeField()
  # access like count history using comment.likeCounts
  comment = ForeignKeyField(Comment, related_name = 'likeCounts')

# yak is a Pyak Yak object
# school is a valid fkey in schools
def convertYakToDict(yak, school):
  yakDict = {} # just a dictionary
  yakDict['content'] = yak.message
  yakDict['latitude'] = yak.latitude
  yakDict['longitude'] = yak.longitude
  yakDict['finalLikeCount'] = yak.likes
  yakDict['finalCommentCount'] = yak.comments
  yakDict['time'] = yak.time # datetime object
  yakDict['school'] = school # should be valid
  yakDict['originalID'] = yak.messageID # unique
  yakDict['isSpecial'] = yak.messageID[0] != 'R'

  # for processing
  return yakDict

# yakDict is an output of conversion
# now is the retrieval time as datetime
def processYakDict(yakDict, now):
  try: # searches for original yak ID in Yak table
    yak = Yak.get(originalID = yakDict['originalID'])
    oldLikeCount = yak.finalLikeCount # save old values
    oldCommentCount = yak.finalCommentCount # used below

    # update like and comments counts to new
    for key, value in yakDict.iteritems():
      setattr(yak, key, value)
    yak.save() # updates entry
    newYak = False

  # make yak if nonexistent
  except Yak.DoesNotExist:
    yak = Yak.create(**yakDict)
    newYak = True

  # see if we need to add an entry to the like counts table  
  likesChanged = newYak or (oldLikeCount != yakDict['finalLikeCount']) # was it updated
  if likesChanged: YakLikeCount.create(count = yakDict['finalLikeCount'], time = now, yak = yak)

  # see if we need to add an entry to the comment counts table  
  commentsChanged = newYak or (oldCommentCount != yakDict['finalCommentCount']) # was it updated
  if commentsChanged: YakCommentCount.create(count = yakDict['finalCommentCount'], time = now, yak = yak)

# comment is a Pyak comment object
# yakID is a Yik Yak API yak ID stored in DB
def convertCommentToDict(comment, yakID):
  commentDict = {} # just a dictionary
  commentDict['content'] = comment.comment
  commentDict['finalLikeCount'] = comment.likes
  commentDict['time'] = comment.time # datetime
  commentDict['originalID'] = comment.commentID

  yak = Yak.get(originalID = yakID)
  commentDict['yak'] = yak

  # for processing
  return commentDict

# commentDict is an output of conversion
# now is the retrieval time as datetime
def processCommentDict(commentDict, now):
  try: # searches for original comment ID in comment table
    comment = Comment.get(originalID = commentDict['originalID'])
    oldLikeCount = comment.finalLikeCount # save old value for below

    # update comment like count to new value
    for key, value in commentDict.iteritems():
      setattr(comment, key, value)
    comment.save() # updates entry
    newComment = False

  # make comment if nonexistent
  except Comment.DoesNotExist:
    comment = Comment.create(**commentDict)
    newComment = True

  # see if we need to add an entry to the like counts table  
  likesChanged = newComment or (oldLikeCount != commentDict['finalLikeCount']) # was it updated
  if likesChanged: CommentLikeCount.create(count = commentDict['finalLikeCount'], time = now, comment = comment)

# any additional tables have to be explicitly added here to get created and recognized on startup
DB.create_tables([School, Yak, YakLikeCount, YakCommentCount, Comment, CommentLikeCount], safe = True)
