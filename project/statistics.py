# File: statistics.py
# DB Data Analysis

from numpy import std, mean, median
from models import Yak, YakLikeCount
import csv, datetime

# study duration in hours
duration = float(24 * 14)

# get a cursor of 100 school yaks
def getCursorForBreakdown(school):
  schoolYakIDs = [] # read in
  with open('data/samples/schools/' + str(school) + '.txt', 'r') as file:
    schoolYakIDs = [int(line.rstrip('\n')) for line in file]
  return Yak.select().where(Yak.id << schoolYakIDs)

# statistical summary of vector
def summaryString(numbers):
  summary = '[' + str(min(numbers))
  summary += ', ' + str(max(numbers)) + ']'
  summary += ' (Mean = ' + str(mean(numbers))
  summary += ', SD = ' + str(std(numbers, ddof = 1))
  summary += ', Median = ' + str(median(numbers)) + ')'

  #like [1, 3] (Mean = 2, STD = 0.3, Median = 1)
  return summary # used for yak sets

# run summaries on a set of yaks
def summarizeYaks(yakCursor, label):
  return
  print(label + ' (' + str(yakCursor.count()) + ')')
  print('Posts/Hour: ' + str(yakCursor.count() / duration))
  upvoteCounts = [yak.finalLikeCount for yak in yakCursor]

  commentLists = [yak.comments for yak in yakCursor] # lists of comments
  comments = [item for subList in commentLists for item in subList]
  commentUpvotes = [comment.finalLikeCount for comment in comments]

  print('Total Comment Count: ' + str(len(comments)))
  print('Upvote Count: ' + summaryString(upvoteCounts))
  print('Comment Upvotes: ' + summaryString(commentUpvotes))
  print('') # end with an extra newline character

# create distribution breakdowns by tags
def createBreakdown(yakCursor, label):
  return
  print(label) # just the label since breakdown
  relevances = ['Circumstantial', 'General', 'Irrelevant']
  themes = ['Academic', 'Social', 'Collective', 'Extracurricular', 'External']

  # print count of each
  # to create a breakdown
  for i in range(len(relevances)):
    rowCells = '' # CSV string
    for j in range(len(themes)):
      subset = yakCursor.where(Yak.theme == j + 1, Yak.relevance == i + 1)
      rowCells += str(subset.count()) + ', '
    print(rowCells[:-2])
  print('') # end with NL

# gets voice breakdown for a cursor
def printVoiceCounts(yakCursor, label):
  print(label) # just label since count
  voices = ['Internal', 'External']

  voiceStr = ''
  # print voice breakdown
  for i in range(len(voices)):
    subset = yakCursor.where(Yak.voice == i + 1)
    voiceStr += str(subset.count()) + ', '
  print(voiceStr[:-2] + '\n')

# summaries of how long yaks lasted
def summarizeDurations(yakCursor, label):
  return
  print(label + ': Yak Lasting Duration')
  creationTimes = [yak.time for yak in yakCursor]
  finalLikeTimes = [(YakLikeCount.select().where(YakLikeCount.yak == yak.id)
    .order_by(YakLikeCount.time.desc()).get().time) for yak in yakCursor]

  durations = [] # fill up
  for i in range(len(creationTimes)):
    timeDelta = finalLikeTimes[i] - creationTimes[i]
    minutes = timeDelta.total_seconds() / 60.0
    durations.append(minutes)

  print(summaryString(durations))
  print('') # end with new line

# write percentage + time for upvotes to CSV
def writeUpvoteCSV(yakCursor, filename):
  return
  with open(filename, 'wb') as output:
    writer = csv.writer(output) # wraps stream
    writer.writerow(['Elapsed Minutes', 'Upvote Fraction'])

    # add points to scatterplot
    for yak in yakCursor:
      startTime = yak.time
      finalCount = yak.finalLikeCount
      if finalCount <= 0: continue
      for like in YakLikeCount.select().where(YakLikeCount.yak == yak.id):
        timeDelta = like.time - startTime # return type TimeDelta
        minutes = timeDelta.total_seconds() / 60.0
        if like.count <= 0: continue # avoid negative counts
        if like.count > finalCount: continue # avoid high fractions
        writer.writerow([minutes, float(like.count) / finalCount])

# summarize the number of posts by time posted or votes
def summarizeYaksByTime(yakCursor, label, offset, votes):
  return
  print(label) # just for identification
  dayHours = [x[:] for x in [[0] * 24] * 7]
  dayCounts = [x[:] for x in [[0] * 24] * 7]

  # bucket each yak
  # Sunday is day zero
  skips = 0 # see below
  for yak in yakCursor.order_by(Yak.finalLikeCount.desc()):
    # skip the first 5 yaks to avoid wild outliers
    if skips < 5 and votes:
      skips += 1
      continue

    # adjust yak time based on the passed timezone offset
    adjTime = yak.time + datetime.timedelta(hours = offset)
    votesAvg = yak.finalLikeCount if votes else 1 # 1 for raw counts
    dayHours[adjTime.isoweekday() % 7][adjTime.hour] += votesAvg
    dayCounts[adjTime.isoweekday() % 7][adjTime.hour] += 1

  # normalize score by post counts
  for i in range(len(dayHours)):
    for j in range(len(dayHours[i])):
      if dayHours[i][j] == 0 or not votes: continue
      dayHours[i][j] /= float(dayCounts[i][j])

  # output CSV style data
  for day in dayHours:
    dayStr = '' # build up
    for hourValue in day:
      dayStr += str(hourValue) + ', '
    print(dayStr[:-2])
  print('') # add new line

# get a general statistical summary
allYaks = Yak.select() # no where() specified
summarizeYaks(allYaks, 'All Collected Yaks')

# get statistical summaries by school
stanford = Yak.select().where(Yak.school == 1)
alabama = Yak.select().where(Yak.school == 2)
berkeley = Yak.select().where(Yak.school == 3)
dartmouth = Yak.select().where(Yak.school == 4)
haverford = Yak.select().where(Yak.school == 5)
boulder = Yak.select().where(Yak.school == 6)
oxford = Yak.select().where(Yak.school == 7)

summarizeYaks(stanford, 'Stanford University')
summarizeYaks(alabama, 'University of Alabama')
summarizeYaks(berkeley, 'UC Berkeley')
summarizeYaks(dartmouth, 'Dartmouth College')
summarizeYaks(haverford, 'Haverford College')
summarizeYaks(boulder, 'CU Boulder')
summarizeYaks(oxford, 'Oxford University')

# get statistical summaries by voice tag
internal = Yak.select().where(Yak.voice == 1)
external = Yak.select().where(Yak.voice == 2)

summarizeYaks(internal, 'Internal Voice')
summarizeYaks(external, 'External Voice')

# get statistical summaries by relevance tag
circumstantial = Yak.select().where(Yak.relevance == 1)
general = Yak.select().where(Yak.relevance == 2)
irrelevant = Yak.select().where(Yak.relevance == 3)

summarizeYaks(circumstantial, 'Circumstantial Relevance')
summarizeYaks(general, 'General Relevance')
summarizeYaks(irrelevant, 'No Relevance')

# get statistical summaries by theme tag
academic = Yak.select().where(Yak.theme == 1)
social = Yak.select().where(Yak.theme == 2)
collective = Yak.select().where(Yak.theme == 3)
extracurricular = Yak.select().where(Yak.theme == 4)
external = Yak.select().where(Yak.theme == 5)

summarizeYaks(academic, 'Academic Theme')
summarizeYaks(social, 'Social Theme')
summarizeYaks(collective, 'Collective Theme')
summarizeYaks(extracurricular, 'Extracurricular Theme')
summarizeYaks(external, 'External Theme')

# get statistical summaries by polarity
positive = Yak.select().where(Yak.polarity > 0)
negative = Yak.select().where(Yak.polarity < 0)

summarizeYaks(positive, 'Positive Polarity')
summarizeYaks(negative, 'Negative Polarity')

# iterate bottom yak file
bottomYakIDs = [] # read in
with open('data/samples/lowYaks.txt', 'r') as file:
  bottomYakIDs = [int(line.rstrip('\n')) for line in file]

# iterate top yak file
topYakIDs = [] # read in
with open('data/samples/topYaks.txt', 'r') as file:
  topYakIDs = [int(line.rstrip('\n')) for line in file]

# create cursors for top and bottom yaks [<< means in]
bottomYaks = Yak.select().where(Yak.id << bottomYakIDs)
topYaks = Yak.select().where(Yak.id << topYakIDs)
stanfordB = getCursorForBreakdown(1)
alabamaB = getCursorForBreakdown(2)
berkeleyB = getCursorForBreakdown(3)
dartmouthB = getCursorForBreakdown(4)
haverfordB = getCursorForBreakdown(5)
boulderB = getCursorForBreakdown(6)
oxfordB = getCursorForBreakdown(7)

# create a bunch of breakdowns by cursors
createBreakdown(stanfordB, 'Stanford University')
createBreakdown(alabamaB, 'University of Alabama')
createBreakdown(berkeleyB, 'UC Berkeley')
createBreakdown(dartmouthB, 'Dartmouth College')
createBreakdown(haverfordB, 'Haverford College')
createBreakdown(boulderB, 'CU Boulder')
createBreakdown(oxfordB, 'Oxford University')
createBreakdown(topYaks, 'Top 100 Yaks')
createBreakdown(bottomYaks, '100 Bottom Yaks')

# get a bunch of voice breakdowns by cursor
printVoiceCounts(stanfordB, 'Stanford University')
printVoiceCounts(alabamaB, 'University of Alabama')
printVoiceCounts(berkeleyB, 'UC Berkeley')
printVoiceCounts(dartmouthB, 'Dartmouth College')
printVoiceCounts(haverfordB, 'Haverford College')
printVoiceCounts(boulderB, 'CU Boulder')
printVoiceCounts(oxfordB, 'Oxford University')
printVoiceCounts(topYaks, 'Top 100 Yaks')
printVoiceCounts(bottomYaks, '100 Bottom Yaks')

# get low Yak cursors for each of the schools
allYaksLow = allYaks.where(Yak.finalLikeCount == -4)
stanfordLow = stanford.where(Yak.finalLikeCount == -4)
alabamaLow = alabama.where(Yak.finalLikeCount == -4)
berkeleyLow = berkeley.where(Yak.finalLikeCount == -4)
dartmouthLow = dartmouth.where(Yak.finalLikeCount == -4)
haverfordLow = haverford.where(Yak.finalLikeCount == -4)
boulderLow = boulder.where(Yak.finalLikeCount == -4)
oxfordLow = oxford.where(Yak.finalLikeCount == -4)

# create a bunch of duration summaries by cursor
summarizeDurations(allYaksLow, 'All Collected Yaks Low')
summarizeDurations(stanfordLow, 'Stanford University Low')
summarizeDurations(alabamaLow, 'University of Alabama Low')
summarizeDurations(berkeleyLow, 'UC Berkeley Low')
summarizeDurations(dartmouthLow, 'Dartmouth College Low')
summarizeDurations(haverfordLow, 'Haverford College Low')
summarizeDurations(boulderLow, 'CU Boulder Low')
summarizeDurations(oxfordLow, 'Oxford University Low')

# get high Yak cursors for each of the schools
allYaksTop = allYaks.order_by(Yak.finalLikeCount.desc()).limit(100)
stanfordTop = stanford.order_by(Yak.finalLikeCount.desc()).limit(100)
alabamaTop = alabama.order_by(Yak.finalLikeCount.desc()).limit(100)
berkeleyTop = berkeley.order_by(Yak.finalLikeCount.desc()).limit(100)
dartmouthTop = dartmouth.order_by(Yak.finalLikeCount.desc()).limit(100)
haverfordTop = haverford.order_by(Yak.finalLikeCount.desc()).limit(100)
boulderTop = boulder.order_by(Yak.finalLikeCount.desc()).limit(100)
oxfordTop = oxford.order_by(Yak.finalLikeCount.desc()).limit(100)

# create a bunch of upvote CSVs by cursor
writeUpvoteCSV(allYaks, 'data/analysis/CSV/all/full.csv')
writeUpvoteCSV(stanford, 'data/analysis/CSV/all/stanford.csv')
writeUpvoteCSV(alabama, 'data/analysis/CSV/all/alabama.csv')
writeUpvoteCSV(berkeley, 'data/analysis/CSV/all/berkeley.csv')
writeUpvoteCSV(dartmouth, 'data/analysis/CSV/all/dartmouth.csv')
writeUpvoteCSV(haverford, 'data/analysis/CSV/all/haverford.csv')
writeUpvoteCSV(boulder, 'data/analysis/CSV/all/boulder.csv')
writeUpvoteCSV(oxford, 'data/analysis/CSV/all/oxford.csv')
writeUpvoteCSV(allYaksTop, 'data/analysis/CSV/top/full.csv')
writeUpvoteCSV(stanfordTop, 'data/analysis/CSV/top/stanford.csv')
writeUpvoteCSV(alabamaTop, 'data/analysis/CSV/top/alabama.csv')
writeUpvoteCSV(berkeleyTop, 'data/analysis/CSV/top/berkeley.csv')
writeUpvoteCSV(dartmouthTop, 'data/analysis/CSV/top/dartmouth.csv')
writeUpvoteCSV(haverfordTop, 'data/analysis/CSV/top/haverford.csv')
writeUpvoteCSV(boulderTop, 'data/analysis/CSV/top/boulder.csv')
writeUpvoteCSV(oxfordTop, 'data/analysis/CSV/top/oxford.csv')

# create a bunch of temporal post count breakdowns
summarizeYaksByTime(stanford, 'Stanford University', -3, False)
summarizeYaksByTime(alabama, 'University of Alabama', -1, False)
summarizeYaksByTime(berkeley, 'UC Berkeley', -3, False)
summarizeYaksByTime(dartmouth, 'Dartmouth College', 0, False)
summarizeYaksByTime(haverford, 'Haverford College', 0, False)
summarizeYaksByTime(boulder, 'CU Boulder',-2, False)
summarizeYaksByTime(oxford, 'Oxford University', 4, False)

# create a bunch of temporal upvote count breakdowns
summarizeYaksByTime(stanford, 'Stanford University', -3, True)
summarizeYaksByTime(alabama, 'University of Alabama', -1, True)
summarizeYaksByTime(berkeley, 'UC Berkeley', -3, True)
summarizeYaksByTime(dartmouth, 'Dartmouth College', 0, True)
summarizeYaksByTime(haverford, 'Haverford College', 0, True)
summarizeYaksByTime(boulder, 'CU Boulder',-2, True)
summarizeYaksByTime(oxford, 'Oxford University', 4, True)
