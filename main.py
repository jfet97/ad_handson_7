# 10k random lines from https://www.kaggle.com/kazanova/sentiment140 containing
# the polarity of the tweet ("+", "-")
# the date of the tweet
# the user that tweeted
# the text of the tweet

# define PY_SSIZE_T_CLEAN

# import hyperloglog
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

    day_part_happy_exact = {
        dayPart.MORNING: 0,
        dayPart.AFTERNOON: 0,
        dayPart.EVENING: 0,
        dayPart.NIGHT: 0
    }

    tweet = stream.nextRecord()
    while tweet is not None:
        username = stream.username()

        users.add(username)
        lc_users.add(username)

        hapyness_to_lc[stream.ispositive()].add(username)
        day_part_to_lc[stream.timeBin()].add(username)

        # debug
        if stream.ispositive():
            day_part_happy_exact[stream.timeBin()] += 1

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
        "morning_happy_exact",
        day_part_happy_exact[dayPart.MORNING])
    print(
        "afternoon_happy_exact",
        day_part_happy_exact[dayPart.AFTERNOON])
    print(
        "evening_happy_exact",
        day_part_happy_exact[dayPart.EVENING])
    print(
        "night_happy_exact",
        day_part_happy_exact[dayPart.NIGHT])

    print(
        "morning_happy",
        happy_morning_users.count_estimation())
    print(
        "afternoon_happy",
        happy_afternoon_users.count_estimation())
    print(
        "evening_happy",
        happy_evening_users.count_estimation())
    print(
        "night_happy",
        happy_night_users.count_estimation())

    print(
        "morning_happy_exact_percentage",
        day_part_happy_exact[dayPart.MORNING] / sum(day_part_happy_exact.values()))
    print(
        "afternoon_happy_exact_percentage",
        day_part_happy_exact[dayPart.AFTERNOON] / sum(day_part_happy_exact.values()))
    print(
        "evening_happy_exact_percentage",
        day_part_happy_exact[dayPart.EVENING] / sum(day_part_happy_exact.values()))
    print(
        "night_happy_exact_percentage",
        day_part_happy_exact[dayPart.NIGHT] / sum(day_part_happy_exact.values()))

    print(
        "morning_happy_percentage",
        happy_morning_users.count_estimation() /
        lc_happy_users.count_estimation())
    print(
        "afternoon_happy_percentage",
        happy_afternoon_users.count_estimation() /
        lc_happy_users.count_estimation())
    print(
        "evening_happy_percentage",
        happy_evening_users.count_estimation() /
        lc_happy_users.count_estimation())
    print(
        "night_happy_percentage",
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


def question3(lc_size, k, stream):

    tweet = stream.nextRecord()
    exact_happy_users_once = set()
    exact_happy_users_multiple = set()

    lcs_happy_users_once = [LinearCounter(lc_size, i) for i in range(k)]

    lc_happy_users_multiple = LinearCounter(lc_size)

    while tweet is not None:
        if stream.ispositive():
            words = stream.tokenizedTweet()

            for word in words:
                if all(map(lambda lc: lc.contains(word), lcs_happy_users_once)):
                    lc_happy_users_multiple.add(word)
                else:
                    lcs_happy_users_once[0].contains(word)
                    list(map(lambda lc: lc.add(word), lcs_happy_users_once))

                if word in exact_happy_users_once:
                    exact_happy_users_multiple.add(word)
                else:
                    exact_happy_users_once.add(word)

        tweet = stream.nextRecord()

    print("exact_happy_users_once",
          len(exact_happy_users_once))
    print("exact_happy_users_multiple",
          len(exact_happy_users_multiple))
    print("lcs_happy_users_once",
          int(sum(map(lambda lc: lc.count_estimation(), lcs_happy_users_once)) / len(lcs_happy_users_once)))
    print("lc_happy_users_multiple",
          lc_happy_users_multiple.count_estimation())


def question4(ss_size, how_many_counts, stream):
    tweet = stream.nextRecord()

    happy_len_counter = SpaceSaving(ss_size)
    unhappy_len_counter = SpaceSaving(ss_size)

    while tweet is not None:
        if stream.ispositive():
            happy_len_counter.add(stream.length())
        else:
            unhappy_len_counter.add(stream.length())
        tweet = stream.nextRecord()

    print("happy_len_counter", happy_len_counter.query(how_many_counts))
    print("unhappy_len_counter", unhappy_len_counter.query(how_many_counts))

    print("avg_happy_msg_len", int(sum(map(
        lambda c: c[0], happy_len_counter.query(how_many_counts))) / how_many_counts))
    print("avg_unhappy_msg_len", int(sum(map(
        lambda c: c[0], unhappy_len_counter.query(how_many_counts))) / how_many_counts))


if __name__ == "__main__":

    dataset = DS.HandsonDatasets.MEDIUM
    print("input: " + dataset.path)

    stream = mystream(dataset.path)
    question1(dataset.sizes[0], stream)

    # stream.reset()
    # question2(dataset.sizes[1], 30, stream)

    # stream.reset()
    # question3(dataset.sizes[2], 4, stream)

    # stream.reset()
    # question4(dataset.sizes[3], 30, stream)
