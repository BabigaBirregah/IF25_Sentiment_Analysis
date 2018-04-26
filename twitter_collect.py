# https://pypi.org/project/twitter/
# http://socialmedia-class.org/twittertutorial.html

from twitter import *

import credentials


def connect_method():
    ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET = credentials.credentials()
    return OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)  # you should create a credential function,
    #  in a separate file not included to git, returning a tuple
    # (ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)


def search_sample(query):
    connect_twitter = Twitter(auth=connect_method())
    result_query = connect_twitter.search.tweets(q=query)
    result_query = result_query['statuses']  # return a list of dictionaries containing tweets only

    # we just want the text from it
    only_text = list()
    for dic in result_query:
        only_text.append(dic['text'])

    # deal with the text
    pass


def collect_tweet(nb_tweets=1):
    twitter_userstream = TwitterStream(auth=connect_method())

    only_text = list()
    for msg in twitter_userstream.statuses.sample():  # infinite loop
        print(msg)  # TODO : just for debugging purpose ; remove after not needed anymore
        try:
            if msg['text']:
                only_text.append(msg['text'])
                nb_tweets -= 1

        except:
            pass

        if not nb_tweets:  # to stop the loop when reaching the desired amount of tweets
            break

    # deal with the text
    print(only_text)
    pass


collect_tweet()
