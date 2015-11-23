# File: tagging.py
# Manual Content Coding

# not cross platform LOL
from msvcrt import getch
from os import system
from models import Yak

# used below for school ID to location conversion
location = ['Stanford', 'Alabama', 'Berkeley',
  'Dartmouth', 'Haverford', 'Boulder', 'Oxford']

# iterate and try to tag these things
files = ['data/samples/schools/1.txt',
    		 'data/samples/schools/2.txt',
    		 'data/samples/schools/3.txt',
    		 'data/samples/schools/4.txt',
    		 'data/samples/schools/5.txt',
    		 'data/samples/schools/6.txt',
    		 'data/samples/schools/7.txt',
    		 'data/samples/topYaks.txt',
    		 'data/samples/lowYaks.txt']

# iterate files and IDs
yakIDs = [] # read in
for filename in files:
  with open(filename, 'r') as file:
    yakIDs += [int(line.rstrip('\n')) for line in file]

# start the coding
pos = 0 # allow seek?
while pos < len(yakIDs):
  yak = Yak.get(Yak.id == yakIDs[pos])

  # quick skip
  if yak.isCoded:
    pos += 1
    continue

  system('clear')
  print('Progress: ' + str(pos) + '/' + str(len(yakIDs)))
  print('#' + str(yak.id) + ': ' + yak.content.encode('utf-8'))
  print('\nPost Upvotes: ' + str(yak.finalLikeCount))
  print('Posting Time: ' + str(yak.time))
  print('Posting Location: ' + location[yak.school.id - 1])

  # code voice
  print('\n\tVoice:')
  print('\t[Q] Internal')
  print('\t[W] External')
  print('\t[E] Unknown')
  key = getch()

  if key == 'q': yak.voice = 1
  elif key == 'w': yak.voice = 2
  elif key == 'e': yak.voice = 0
  else: break

  system('clear')
  print('Progress: ' + str(pos) + '/' + str(len(yakIDs)))
  print('#' + str(yak.id) + ': ' + yak.content.encode('utf-8'))
  print('\nPost Upvotes: ' + str(yak.finalLikeCount))
  print('Posting Time: ' + str(yak.time))
  print('Posting Location: ' + location[yak.school.id - 1])

  # code relevance
  print('\n\tRelevance:')
  print('\t[Q] Circumstantial')
  print('\t[W] General')
  print('\t[E] Irrelevant')
  print('\t[R] Unknown')
  key = getch()

  if key == 'q': yak.relevance = 1
  elif key == 'w': yak.relevance = 2
  elif key == 'e': yak.relevance = 3
  elif key == 'r': yak.relevance = 0
  else: break

  system('clear')
  print('Progress: ' + str(pos) + '/' + str(len(yakIDs)))
  print('#' + str(yak.id) + ': ' + yak.content.encode('utf-8'))
  print('\nPost Upvotes: ' + str(yak.finalLikeCount))
  print('Posting Time: ' + str(yak.time))
  print('Posting Location: ' + location[yak.school.id - 1])

  # code theme
  print('\n\tTheme:')
  print('\t[Q] Academic')
  print('\t[W] Social')
  print('\t[E] Collective')
  print('\t[R] Extracurricular')
  print('\t[T] External')
  print('\t[Y] Unknown')
  key = getch()

  if key == 'q': yak.theme = 1
  elif key == 'w': yak.theme = 2
  elif key == 'e': yak.theme = 3
  elif key == 'r': yak.theme = 4
  elif key == 't': yak.theme = 5
  elif key == 'y': yak.theme = 0
  else: break

  # confirm or redo the tagging on this
  print('\nPress [QWERT] to confirm.')
  if getch() in 'qwert':
    # see if done coding
    if yak.voice != 0 and \
      yak.theme != 0 and \
      yak.relevance != 0:
      yak.isCoded = True
    yak.save()
    pos += 1
