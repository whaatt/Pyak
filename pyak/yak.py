# File: yak.py
# Yak Message Model

from datetime import datetime
def parseTime(timeStr):
  format = '%Y-%m-%d %H:%M:%S'
  return datetime.strptime(timeStr, format)

class Yak:
  def __init__(self, raw, client):
    self.client = client
    self.posterID = raw['posterID']
    self.hidePin = bool(int(raw['hidePin']))
    self.messageID = raw['messageID']
    self.deliveryID = raw['deliveryID']
    self.longitude = raw['longitude']
    self.comments = int(raw['comments'])
    self.time = parseTime(raw['time'])
    self.latitude = raw['latitude']
    self.likes = int(raw['numberOfLikes'])
    self.message = raw['message']
    self.type = raw['type']
    self.liked = int(raw['liked'])
    self.reyaked = raw['reyaked']

    # yaks do not always have a handle
    try: self.handle = raw['handle']
    except KeyError: self.handle = None

    # for some reason this seems necessary
    self.messageID = self.messageID.replace('\\', '')

  def upvote(self):
    if self.liked == 0:
      self.liked += 1
      self.likes += 1

      # only triggers if not already voted on
      return self.client.upvoteYak(self.messageID)

  def downvote(self):
    if self.liked == 0:
      self.liked -= 1
      self.likes -= 1

      # only triggers if not already voted on
      return self.client.downvoteYak(self.messageID)

  def report(self):
    return self.client.reportYak(self.messageID)

  def delete(self):
    if self.posterID == self.client.ID:
      return self.client.deleteYak(self.messageID)

  def addComment(self, comment):
    return self.client.postComment(self.messageID, comment)

  def getComments(self):
    return self.client.getComments(self.messageID)
