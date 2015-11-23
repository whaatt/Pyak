# File: sampling.py
# Sampling Random Content

from peewee import fn
from models import Yak

# sample school Yaks
for i in range(1, 8):
  yaks = Yak.select().where(Yak.school == i) \
    .order_by(fn.Random()).limit(100) # 100 random
  yakIDs = [yak.id for yak in yaks]

  # write sampled yak IDs to a sample text file
  filename = 'data/samples/schools/' + str(i) + '.txt'
  with open(filename, 'w') as file:
    for yakID in yakIDs: # per line
      file.write('%s\n' % str(yakID))

# top yaks are simply the top 100 yaks ordered by their final like count
topYaks = Yak.select().order_by(Yak.finalLikeCount.desc()).limit(100)
lowYaks = Yak.select().where(Yak.finalLikeCount == -4) \
  .order_by(fn.Random()).limit(100) # 100 random low yaks

# write top yak IDs to a sample file
filename = 'data/samples/topYaks.txt'
yakIDs = [yak.id for yak in topYaks]
with open(filename, 'w') as file:
  for yakID in yakIDs: # per line
    file.write('%s\n' % str(yakID))

# write low yak IDs to a sample file
filename = 'data/samples/lowYaks.txt'
yakIDs = [yak.id for yak in lowYaks]
with open(filename, 'w') as file:
  for yakID in yakIDs: # per line
    file.write('%s\n' % str(yakID))
