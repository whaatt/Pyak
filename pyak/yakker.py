# File: yakker.py
# Yak User Model

import base64
import hmac
import json
import os
import requests
import time

from decimal import Decimal
from hashlib import sha1, md5
from random import randrange

# import the Pyak helper classes
from pyak.peekLocation import PeekLocation
from pyak.location import Location
from pyak.comment import Comment
from pyak.yak import Yak

class Yakker:
  baseURL = 'https://us-east-api.yikyakapi.net/api/' # until they change it...
  userAgent = 'Dalvik/1.6.0 (Linux; U; AndroID 4.4.4; XT1060 Build/KXA21.12-L1.26)'

  # ideally specify a userID most of the time so we do not spam Yik Yak
  def __init__(self, userID = None, location = None, forceRegister = False):
    if location is None:
      location = Location('0', '0')
    self.updateLocation(location)

    if userID is None:
      userID = self.generateID()
      self.registerNewID(userID)
    elif forceRegister:
      self.registerNewID(userID)

    self.ID = userID
    self.handle = None

  def generateID(self):
    return md5(os.urandom(128)).hexdigest().upper()

  def registerNewID(self, ID):
    params = {
      'userID': ID,
      'lat': self.location.latitude,
      'long': self.location.longitude,
    }

    result = self.get('registerUser', params)
    return result

  def signRequest(self, page, params):
    key = 'EF64523D2BD1FA21F18F5BC654DFC41B'

    # just current time in seconds since epoch
    salt = str(int(time.time()))

    # the message is essentially the
    # request with parameters sorted
    msg = '/api/' + page
    sortedParams = params.keys()
    sortedParams.sort()

    if len(params) > 0:
      msg += '?'

    for param in sortedParams:
      msg += '%s=%s&' % (param, params[param])

    # chop off last ampersand
    if len(params) > 0:
      msg = msg[:-1]

    # append salt directly
    msg += salt

    # Calculate the signature
    h = hmac.new(key, msg, sha1)
    hash = base64.b64encode(h.digest())
    return hash, salt, msg

  def get(self, page, params):
    url = self.baseURL + page
    params['version'] = '2.1.001'

    hash, salt, msg = self.signRequest(page, params)
    params['salt'] = salt
    params['hash'] = hash

    headers = {
      'User-Agent': self.userAgent,
      'Accept-Encoding': 'gzip',
    }

    ret = requests.get(url, params = params, headers = headers)
    return ret # TODO: do we need a cookie here?

  def post(self, page, params):
    url = self.baseURL + page

    getParams = { 'userID': self.ID, 'version': '2.1.001' }
    hash, salt, msg = self.signRequest(page, getParams)
    getParams['salt'] = salt
    getParams['hash'] = hash

    headers = {
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'User-Agent': self.userAgent,
      'Accept-Encoding': 'gzip'
      # 'Cookie': self.cookie
    }

    data = ''
    sortedParams = params.keys()
    sortedParams.sort()

    for param in sortedParams:
      data += '%s=%s&' % (param, params[param])
      ret = requests.post(url, data = data, params = getParams, headers = headers)

    # does not work
    return ret

  def calcAccuracy(self): # needed in 2.6.3
    return format(Decimal(randrange(10000))/1000 % 30 + 20, '.3f')

  def getYakList(self, page, params):
    return self.parseYaks(self.get(page, params).text)

  def parseYaks(self, text):
    try: rawYaks = json.loads(text)['messages']
    except: rawYaks = []

    yaks = []
    for rawYak in rawYaks:
      yaks.append(Yak(rawYak, self))
    return yaks

  def parseComments(self, text, messageID):
    try: rawComments = json.loads(text)['comments']
    except: rawComments = []

    comments = []
    for rawComment in rawComments:
      comments.append(Comment(rawComment, messageID, self))
    return comments

  def contact(self, message):
    params = {
      'userID': self.ID,
      'message': message
    }

    # just for completeness
    return self.get('contactUs', params)

  def upvoteYak(self, messageID):
    params = {
      'userID': self.ID,
      'messageID': messageID,
      'lat': self.location.latitude,
      'long': self.location.longitude,
    }

    # like = upvote on Yak
    return self.get('likeMessage', params)

  def downvoteYak(self, messageID):
    params = {
        'userID': self.ID,
        'messageID': messageID,
        'lat': self.location.latitude,
        'long': self.location.longitude,
    }

    # opposite of a downvote is a ... like?
    return self.get('downvoteMessage', params)

  def upvoteComment(self, commentID):
    params = {
      'userID': self.ID,
      'commentID': commentID,
      'lat': self.location.latitude,
      'long': self.location.longitude,
    }

    # like = upvote on comment
    return self.get('likeComment', params)

  def downvoteComment(self, commentID):
    params = {
      'userID': self.ID,
      'commentID': commentID,
      'lat': self.location.latitude,
      'long': self.location.longitude,
    }

    # opposite of a downvote is a ... like?
    return self.get('downvoteComment', params)

  def reportYak(self, messageID):
    params = {
      'userID': self.ID,
      'messageID': messageID,
      'lat': self.location.latitude,
      'long': self.location.longitude,
    }

    # report Yak endpoint
    return self.get('reportMessage', params)

  def deleteYak(self, messageID):
    params = {
      'userID': self.ID,
      'messageID': messageID,
      'lat': self.location.latitude,
      'long': self.location.longitude,
    }

    # delete Yak endpoint
    return self.get('deleteMessage2', params)

  def reportComment(self, commentID, messageID):
    params = {
      'userID': self.ID,
      'commentID': commentID,
      'messageID': messageID,
      'lat': self.location.latitude,
      'long': self.location.longitude,
    }

    # report comment endpoint
    return self.get('reportMessage', params)

  def deleteComment(self, commentID, messageID):
    params = {
      'userID': self.ID,
      'commentID': commentID,
      'messageID': messageID,
      'lat': self.location.latitude,
      'long': self.location.longitude,
    }

    # delete comment endpoint
    return self.get('deleteComment', params)

  def getGreatest(self):
    params = {
      'userID': self.ID,
      'lat': self.location.latitude,
      'long': self.location.longitude,
    }

    # all time tops endpoint
    return self.getYakList('getGreatest', params)

  def getMyTops(self):
    params = {
        'userID': self.ID,
        'lat': self.location.latitude,
        'long': self.location.longitude,
    }

    # get my tops endpoint
    return self.getYakList('getMyTops', params)

  def getRecentReplied(self):
    params = {
        'userID': self.ID,
        'lat': self.location.latitude,
        'long': self.location.longitude,
    }

    # get recent replies endpoint
    return self.getYakList('getMyRecentReplies', params)

  # make sure location is Location object
  def updateLocation(self, location):
    self.location = location

  def getMyRecentYaks(self):
    params = {
      'userID': self.ID,
      'lat': self.location.latitude,
      'long': self.location.longitude,
    }

    # get recent yaks endpoint
    return self.getYakList('getMyRecentYaks', params)

  def getAreaTops(self):
    params = {
      'userID': self.ID,
      'lat': self.location.latitude,
      'long': self.location.longitude,
    }

    # best in area endpoint
    return self.getYakList('getAreaTops', params)

  def getYaks(self):
    params = {
      'userID': self.ID,
      'lat': self.location.latitude,
      'long': self.location.longitude,
    }

    # get list of yaks by location
    return self.getYakList('getMessages', params)

  # probably does not work because of cookie issues
  def postYak(self, message, showloc = False, handle = False):
    params = {
      'userID': self.ID,
      'lat': self.location.latitude,
      'long': self.location.longitude,
      'message': message.replace(' ', '+')
    }

    if not showloc: params['hidePin'] = '1'
    if handle and (self.handle is not None):
      params['hndl'] = self.handle
    return self.post('sendMessage', params)

  def getComments(self, messageID):
    params = {
      'userID': self.ID,
      'messageID': messageID,
      'lat': self.location.latitude,
      'long': self.location.longitude,
    }

    # get post comments endpoint [we also parse here]
    return self.parseComments(self.get('getComments', params).text, messageID)

  def postComment(self, messageID, comment):
    params = {
      'userID': self.ID,
      'messageID': messageID,
      'comment': comment,
      'lat': self.location.latitude,
      'long': self.location.longitude,
    }

    # post comment endpoint
    return self.post('postComment', params)

  def getPeekLocations(self):
    params = {
      'userID': self.ID,
      'lat': self.location.latitude,
      'long': self.location.longitude,
    }

    # get peek locations [list of places]
    # TODO: why is this getMessages?
    data = self.get('getMessages', params).json()

    peeks = []
    for peekJSON in data['otherLocations']:
      peeks.append(PeekLocation(peekJSON))
    return peeks

  def getFeaturedLocations(self):
    params = {
      'userID': self.ID,
      'lat': self.location.latitude,
      'long': self.location.longitude,
    }

    # get promoted locations [list of places]
    # TODO: why is this getMessages?
    data = self.get('getMessages', params).json()

    peeks = []
    for peekJSON in data['featuredLocations']:
      peeks.append(PeekLocation(peekJSON))
    return peeks

  def getYakarma(self):
    params = {
      'userID': self.ID,
      'lat': self.location.latitude,
      'long': self.location.longitude,
    }

    # TODO: why is this getMessages?
    data = self.get('getMessages', params).json()
    return int(data['yakarma'])

  def peek(self, peekID):
    if isinstance(peekID, PeekLocation):
      peekID = peekID.ID

      params = {
        'userID': self.ID,
        'lat': self.location.latitude,
        'long': self.location.longitude,
        'peekID': peekID,
      }

    # peek locations endpoint
    return self.getYakList('getPeekMessages', params)
