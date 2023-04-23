# 10k random lines from https://www.kaggle.com/kazanova/sentiment140 containing
# the polarity of the tweet ("+", "-")
# the date of the tweet
# the user that tweeted
# the text of the tweet

#define PY_SSIZE_T_CLEAN

#import hyperloglog
from stream import *
from lc import LinearCounter
from space_saving import SpaceSaving
import dataset as DS

def question1(lc_size, stream):

  # exact number of users just to check if things are done well
  users = set()

  lc_users = LinearCounter(lc_size)
  lc_happy_users = LinearCounter(lc_size)
  lc_unhappy_users = LinearCounter(lc_size)
  lc_morning_tweets = LinearCounter(lc_size)
  lc_afternoon_tweets = LinearCounter(lc_size)
  lc_evening_tweets = LinearCounter(lc_size)
  lc_night_tweets = LinearCounter(lc_size)

  hapyness_to_lc = {True: lc_happy_users, False: lc_unhappy_users}

  day_part_to_lc = {
      dayPart.MORNING: lc_morning_tweets,
      dayPart.AFTERNOON: lc_afternoon_tweets,
      dayPart.EVENING: lc_evening_tweets,
      dayPart.NIGHT: lc_night_tweets
  }

  tweet = stream.nextRecord()
  while tweet is not None:
      username = stream.username()

      users.add(username)
      lc_users.add(username)

      hapyness_to_lc[stream.ispositive()].add(username)
      day_part_to_lc[stream.timeBin()].add(username)

      tweet = stream.nextRecord()

  happy_morning_users = lc_happy_users.intersect(lc_morning_tweets)
  happy_afternoon_users = lc_happy_users.intersect(lc_afternoon_tweets)
  happy_evening_users = lc_happy_users.intersect(lc_evening_tweets)
  happy_night_users = lc_happy_users.intersect(lc_night_tweets)

  print("exact_users", len(users))
  print("estimated_users", lc_users.count_estimation())
  print("happy",
        lc_happy_users.count_estimation() / lc_users.count_estimation())
  print("unhappy",
        lc_unhappy_users.count_estimation() / lc_users.count_estimation())

  print(
      "morning_happy",
      happy_morning_users.count_estimation() /
      lc_happy_users.count_estimation())
  print(
      "afternoon_happy",
      happy_afternoon_users.count_estimation() /
      lc_happy_users.count_estimation())
  print(
      "evening_happy",
      happy_evening_users.count_estimation() /
      lc_happy_users.count_estimation())
  print(
      "night_happy",
      happy_night_users.count_estimation() /
      lc_happy_users.count_estimation())  


def question2(ss_size, n_of_favorite_words, stream): 
  tweet = stream.nextRecord()

  words_counter = SpaceSaving(ss_size)
  dinstict_words = set()
  while tweet is not None:
      words = stream.tokenizedTweet()
      for word in words:
          words_counter.add(word)
          dinstict_words.add(word)
      tweet = stream.nextRecord()

  print("exact_words", len(dinstict_words))
  print("favorite_words", words_counter.query(n_of_favorite_words))

def question3(lc_size, stream):

  tweet = stream.nextRecord()
  happy_users_words_counter = LinearCounter(lc_size)
  exact_words = set()

  while tweet is not None:
    if stream.ispositive():
      words = stream.tokenizedTweet()
      for word in words:
          happy_users_words_counter.add(word)
          exact_words.add(word)
    tweet = stream.nextRecord()

  print("happy_users_words",  happy_users_words_counter.count_estimation())
  print("happy_users_exact_words",  len(exact_words))
  

if __name__ == "__main__":

  dataset = DS.HandsonDatasets.HUGE
  print("input: " + dataset.path)

  stream = mystream(dataset.path)
  
  # question1(dataset.sizes[0], stream)
  # stream.reset()

  # question2(dataset.sizes[1], 30, stream)
  # stream.reset()

  question3(dataset.sizes[2], stream)
  stream.reset()
  

  
