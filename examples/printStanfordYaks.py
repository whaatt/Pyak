# File: printStanfordYaks.py
# Testing Pyak on Stanford Yaks

from pyak import *

yakker = Yakker(userID = '93F6BC5EF48244882397787B92DDE98F')
stanford = Location('37.42636', '-122.171869')
yakker.updateLocation(stanford)
yaks = yakker.getYaks()

# print out the yaks in ascending order of likes
for yak in sorted(yaks, key = lambda x: x.likes):
  print yak.message.encode('utf-8'), yak.messageID
  if yak.comments > 0: print yak.getComments()