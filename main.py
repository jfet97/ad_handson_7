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
from bloom_filter import BloomFilter


def question1(lc_size, stream):

    # exact number of users just to check if things are done well
    users = set()
    lc_users = LinearCounter(lc_size)

    morning_users_bf = BloomFilter(8 * lc_size, 8)
    happy_users_bf = BloomFilter(8 * lc_size, 8)

    happyness_to_lc = {
        True: LinearCounter(lc_size),
        False: LinearCounter(lc_size)
    }

    happyness_day_part_to_lc = {
        True: {
            dayPart.MORNING: LinearCounter(lc_size),
            dayPart.AFTERNOON: LinearCounter(lc_size),
            dayPart.EVENING: LinearCounter(lc_size),
            dayPart.NIGHT: LinearCounter(lc_size)
        },
        False: {
            dayPart.MORNING: LinearCounter(lc_size),
            dayPart.AFTERNOON: LinearCounter(lc_size),
            dayPart.EVENING: LinearCounter(lc_size),
            dayPart.NIGHT: LinearCounter(lc_size)
        }
    }

    happyness_exact = {
        True: set(),
        False: set()
    }
    happyness_day_part_exact = {
        True: {
            dayPart.MORNING: set(),
            dayPart.AFTERNOON: set(),
            dayPart.EVENING: set(),
            dayPart.NIGHT: set()
        },
        False: {
            dayPart.MORNING: set(),
            dayPart.AFTERNOON: set(),
            dayPart.EVENING: set(),
            dayPart.NIGHT: set()
        }

    }

    tweet = stream.nextRecord()
    while tweet is not None:
        username = stream.username()

        users.add(username)
        lc_users.add(username)

        happyness_to_lc[stream.ispositive()].add(username)
        happyness_day_part_to_lc[stream.ispositive(
        )][stream.timeBin()].add(username)

        happyness_exact[stream.ispositive()].add(username)
        happyness_day_part_exact[stream.ispositive(
        )][stream.timeBin()].add(username)

        if stream.timeBin() == dayPart.MORNING:
            morning_users_bf.add(username)
        if stream.ispositive():
            happy_users_bf.add(username)

        tweet = stream.nextRecord()

    print("yuri", morning_users_bf.count_estimation() +
          happy_users_bf.count_estimation() - (morning_users_bf.union(happy_users_bf).count_estimation()))

    print("exact_users", len(users))
    print("estimated_users", lc_users.count_estimation())
    print("happy_percentage",
          happyness_to_lc[True].count_estimation() / lc_users.count_estimation())
    print("unhappy_percentage",
          happyness_to_lc[False].count_estimation() / lc_users.count_estimation())

    print(
        "morning_happy_exact",
        len(happyness_day_part_exact[True][dayPart.MORNING]))
    print(
        "afternoon_happy_exact",
        len(happyness_day_part_exact[True][dayPart.AFTERNOON]))
    print(
        "evening_happy_exact",
        len(happyness_day_part_exact[True][dayPart.EVENING]))
    print(
        "night_happy_exact",
        len(happyness_day_part_exact[True][dayPart.NIGHT]))

    print(
        "morning_happy",
        happyness_day_part_to_lc[True][dayPart.MORNING].count_estimation())
    print(
        "afternoon_happy",
        happyness_day_part_to_lc[True][dayPart.AFTERNOON].count_estimation())
    print(
        "evening_happy",
        happyness_day_part_to_lc[True][dayPart.EVENING].count_estimation())
    print(
        "night_happy",
        happyness_day_part_to_lc[True][dayPart.NIGHT].count_estimation())

    print(
        "morning_happy_exact_percentage",
        len(happyness_day_part_exact[True][dayPart.MORNING]) / len(happyness_exact[True]))
    print(
        "afternoon_happy_exact_percentage",
        len(happyness_day_part_exact[True][dayPart.AFTERNOON]) / len(happyness_exact[True]))
    print(
        "evening_happy_exact_percentage",
        len(happyness_day_part_exact[True][dayPart.EVENING]) / len(happyness_exact[True]))
    print(
        "night_happy_exact_percentage",
        len(happyness_day_part_exact[True][dayPart.NIGHT]) / len(happyness_exact[True]))

    print(
        "morning_happy_percentage",
        happyness_day_part_to_lc[True][dayPart.MORNING].count_estimation() /
        happyness_to_lc[True].count_estimation())
    print(
        "afternoon_happy_percentage",
        happyness_day_part_to_lc[True][dayPart.AFTERNOON].count_estimation() /
        happyness_to_lc[True].count_estimation())
    print(
        "evening_happy_percentage",
        happyness_day_part_to_lc[True][dayPart.EVENING].count_estimation() /
        happyness_to_lc[True].count_estimation())
    print(
        "night_happy_percentage",
        happyness_day_part_to_lc[True][dayPart.NIGHT].count_estimation() /
        happyness_to_lc[True].count_estimation())

    print(
        "morning_unhappy_exact",
        len(happyness_day_part_exact[False][dayPart.MORNING]))
    print(
        "afternoon_unhappy_exact",
        len(happyness_day_part_exact[False][dayPart.AFTERNOON]))
    print(
        "evening_unhappy_exact",
        len(happyness_day_part_exact[False][dayPart.EVENING]))
    print(
        "night_unhappy_exact",
        len(happyness_day_part_exact[False][dayPart.NIGHT]))

    print(
        "morning_unhappy",
        happyness_day_part_to_lc[False][dayPart.MORNING].count_estimation())
    print(
        "afternoon_unhappy",
        happyness_day_part_to_lc[False][dayPart.AFTERNOON].count_estimation())
    print(
        "evening_unhappy",
        happyness_day_part_to_lc[False][dayPart.EVENING].count_estimation())
    print(
        "night_unhappy",
        happyness_day_part_to_lc[False][dayPart.NIGHT].count_estimation())

    print(
        "morning_unhappy_exact_percentage",
        len(happyness_day_part_exact[False][dayPart.MORNING]) / len(happyness_exact[False]))
    print(
        "afternoon_unhappy_exact_percentage",
        len(happyness_day_part_exact[False][dayPart.AFTERNOON]) / len(happyness_exact[False]))
    print(
        "evening_unhappy_exact_percentage",
        len(happyness_day_part_exact[False][dayPart.EVENING]) / len(happyness_exact[False]))
    print(
        "night_unhappy_exact_percentage",
        len(happyness_day_part_exact[False][dayPart.NIGHT]) / len(happyness_exact[False]))

    print(
        "morning_unhappy_percentage",
        happyness_day_part_to_lc[False][dayPart.MORNING].count_estimation() /
        happyness_to_lc[False].count_estimation())
    print(
        "afternoon_unhappy_percentage",
        happyness_day_part_to_lc[False][dayPart.AFTERNOON].count_estimation() /
        happyness_to_lc[False].count_estimation())
    print(
        "evening_unhappy_percentage",
        happyness_day_part_to_lc[False][dayPart.EVENING].count_estimation() /
        happyness_to_lc[False].count_estimation())
    print(
        "night_unhappy_percentage",
        happyness_day_part_to_lc[False][dayPart.NIGHT].count_estimation() /
        happyness_to_lc[False].count_estimation())


def question2(ss_size, n_of_favorite_words, stream):
    tweet = stream.nextRecord()

    words_counter = SpaceSaving(ss_size)
    dinstict_words = set()

    if tweet.ispositive():
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

    dataset = DS.HandsonDatasets.HUGE
    print("input: " + dataset.path)

    stream = mystream(dataset.path)
    question1(dataset.sizes[0], stream)

    # stream.reset()
    # question2(dataset.sizes[1], 30, stream)

    # stream.reset()
    # question3(dataset.sizes[2], 4, stream)

    # stream.reset()
    # question4(dataset.sizes[3], 30, stream)
