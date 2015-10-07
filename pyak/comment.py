# File: comment.py
# Yak Comment Model

from datetime import datetime
def parseTime(timeStr):
  format = '%Y-%m-%d %H:%M:%S'
  return datetime.strptime(timeStr, format)

class Comment:
  def __init__(self, raw, messageID, client):
    self.client = client
    self.messageID = messageID
    self.commentID = raw['commentID']
    self.comment = raw['comment']
    self.time = parseTime(raw['time'])
    self.likes = int(raw['numberOfLikes'])
    self.posterID = raw['posterID']
    self.liked = int(raw['liked'])

    # strip any backslashes that have popped up
    self.messageID = self.messageID.replace('\\', '')

  def upvote(self):
    if self.liked == 0:
      self.likes += 1
      self.liked += 1

      # only triggers if not already voted on
      return self.client.upvoteComment(self.commentID)

  def downvote(self):
    if self.liked == 0:
      self.likes -= 1
      self.liked += 1

      # only triggers if not already voted on
      return self.client.downvoteComment(self.commentID)

  def report(self):
    return self.client.reportComment(self.commentID, self.messageID)

  def delete(self):
    if self.posterID == self.client.ID:
      return self.client.deleteComment(self.commentID, self.messageID)

  def reply(self, comment):
    return self.client.postComment(self.messageID, comment)

  def printComment(self):
    myAction = ''
    if self.liked > 0:
      myAction = '+'
    elif self.liked < 0:
      myAction = '-'

    # looks like + (123) Comment goes here.
    print('%s (%s) %s' % (myAction, self.likes, self.comment))
