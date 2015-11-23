# File: classifier.py
# Automated Sentiment Classifier

# subjectivity lexicon analysis
from textblob import TextBlob

# unpickle classifier
# import pickle
import models

# uncomment and use this for Naive Bayes work
# reviews = open('data/classifiers/reviews.pickle')
# classifier = pickle.load(reviews) # deserialize

# comfort
i = 0

# iterate through all yak rows
for yak in models.Yak.select():
  content = TextBlob(yak.content)
  yak.polarity = content.polarity
  yak.subjectivity = content.subjectivity

  # just for runtime comfort
  if i % 1000 == 0: print(i)
  i += 1

  # stripped = filter(unicode.isalpha, yak.content).lower()
  # words = stripped.split(' ') # array of stripped words
  # features = dict([(word, True) for word in words])

  # sentiment = classifier.classify(features)
  # if sentiment == 'neg': yak.sentiment = 1
  # elif sentiment == 'pos': yak.sentiment = 2
  yak.save() # update entry

# iterate through all comment rows
for comment in models.Comment.select():
  content = TextBlob(comment.content)
  comment.polarity = content.polarity
  comment.subjectivity = content.subjectivity

  # just for runtime comfort
  if i % 1000 == 0: print(i)
  i += 1

  # stripped = filter(unicode.isalpha, comment.content).lower()
  # words = stripped.split(' ') # array of stripped words
  # features = dict([(word, True) for word in words])

  # sentiment = classifier.classify(features)
  # if sentiment == 'neg': comment.sentiment = 1
  # elif sentiment == 'pos': comment.sentiment = 2
  comment.save() # update entry
