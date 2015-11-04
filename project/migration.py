# File: migration.py
# DB Migration For Analysis

# contains all migration tools
from playhouse.migrate import *

# use threadlocals option just for added safety
DB = SqliteDatabase('data/scrape.db', threadlocals = True)
migrator = SqliteMigrator(DB)

# create Peewee objects for each of the new fields
# refer to the study codebook for a detailed key
voice = IntegerField(default = 0) # 0 is unknown
relevance = IntegerField(default = 0) # 0 is unknown
theme = IntegerField(default = 0) # 0 is unknown
codedYak = BooleanField(default = False)

# fields specific to coding comments for certain Yaks
# refer to the study codebook for a detailed key
disposition = IntegerField(default = 0)
codedComment = BooleanField(default = False)

# playing around with automated sentiment analysis
# field = 1 is negative and field = 2 is positive
sentimentYak = IntegerField(default = 0) # 0 is unknown
sentimentComment = IntegerField(default = 0) # 0 is unknown

with DB.transaction(): # transaction just for safety
  migrate(migrator.add_column('yak', 'voice', voice),
          migrator.add_column('yak', 'theme', theme),
          migrator.add_column('yak', 'relevance', relevance),
          migrator.add_column('yak', 'isCoded', codedYak),
          migrator.add_column('yak', 'sentiment', sentimentYak),
          migrator.add_column('comment', 'disposition', disposition),
          migrator.add_column('comment', 'isCoded', codedComment),
          migrator.add_column('comment', 'sentiment', sentimentComment))
