# File: cron.py
# Project Cron Job

from datetime import datetime
from time import time
from pyak import *
import models

# start the clock
start = time()

stanData = { 'latitude' : 37.427474, 'longitude' : -122.169719, 'name' : 'Stanford University' }
bamaData = { 'latitude' : 33.214023, 'longitude' : -87.539142, 'name' : 'University of Alabama' }
berkData = { 'latitude' : 37.871899, 'longitude' : -122.25854, 'name' : 'UC Berkeley' }
dartData = { 'latitude' : 43.704441, 'longitude' : -72.288693, 'name' : 'Dartmouth College' }
haveData = { 'latitude' : 40.006652, 'longitude' : -75.305318, 'name' : 'Haverford College' }
bldrData = { 'latitude' : 40.007581, 'longitude' : -105.265942, 'name' : 'CU Boulder' }
oxfdData = { 'latitude' : 51.756634, 'longitude' : -1.254704, 'name' : 'University of Oxford' }

stanford, created = models.School.get_or_create(name = stanData['name'], defaults = stanData)
alabama, created = models.School.get_or_create(name = bamaData['name'], defaults = bamaData)
berkeley, created = models.School.get_or_create(name = berkData['name'], defaults = berkData)
dartmouth, created = models.School.get_or_create(name = dartData['name'], defaults = dartData)
haverford, created = models.School.get_or_create(name = haveData['name'], defaults = haveData)
boulder, created = models.School.get_or_create(name = bldrData['name'], defaults = bldrData)
oxford, created = models.School.get_or_create(name = oxfdData['name'], defaults = oxfdData)
schools = [(stanford, stanData), (alabama, bamaData), (berkeley, berkData), (dartmouth, dartData),
  (haverford, haveData), (boulder, bldrData), (oxford, oxfdData)] # and maybe more later

# ideally do not change ID to keep this project on the DL
yakker = Yakker(userID = '93F6BC5EF48244882397787B92DDE98F')

# TODO: maybe make some schools
# not process on every cron run
for school in schools:
  schoolEntry = school[0]
  schoolData = school[1]
  
  schoolLocation = Location(schoolData['latitude'], schoolData['longitude'])
  yakker.updateLocation(schoolLocation)
  yaks = yakker.getYaks()

  yakCount = 0
  commentCount = 0

  for yak in yaks:
    yakDict = models.convertYakToDict(yak, schoolEntry)
    models.processYakDict(yakDict, datetime.now())
    yakCount += 1

    if (yak.comments > 0):
      comments = yak.getComments()
      for comment in comments:
        commentDict = models.convertCommentToDict(comment, yak.messageID)
        models.processCommentDict(commentDict, datetime.now())
        commentCount += 1

  print('School: ' + schoolData['name'])
  print('Processed ' + str(yakCount) + ' yaks.')
  print('Processed ' + str(commentCount) + ' comments.\n')

print('Finished processing all schools.')
print('Ran in about ' + str(round(time() - start, 2)) + ' seconds.')
