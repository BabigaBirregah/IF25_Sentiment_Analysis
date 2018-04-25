# https://pypi.org/project/twitter/
# http://socialmedia-class.org/twittertutorial.html

from twitter import *


def connect_method():
    # Variables that contains the user credentials to access Twitter API
    ACCESS_TOKEN = '2390902586-sCozuoFv7hkgXOiqVmBenFaAbLhbPH0WzrhfXVr'
    ACCESS_SECRET = 'MW1vksBifH9vvRXWzBy4WbPpzK51WnkjudbauymAsxl5H'
    CONSUMER_KEY = '5gtIlLJA1AbWzTHbPWOUiVD0V'
    CONSUMER_SECRET = 'eaYcylnb8q1cFvhgaAQm5dNYqd9CmVfnuUioiHktynLoau4Wuf'

    return OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)


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
        nb_tweets -= 1
        if msg['text']:
            only_text.append(msg['text'])

        if not nb_tweets:  # to stop the loop when reaching the desired amount of tweets
            break

    # deal with the text
    pass


collect_tweet()
