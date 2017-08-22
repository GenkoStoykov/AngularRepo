from __future__ import print_function

import os
import random
import sys
import time
import datetime
from twitter import Twitter, OAuth, TwitterHTTPError


class Retweeter():
    """
            Bot that automates several actions on Twitter, such as following users
            and favoriting tweets.
        """

    def __init__(self, token, token_secret, consumer_key, consumer_secret,last_update_time ):
        # this variable contains the configuration for the bot
        self.token = token
        self.token_secret = token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.last_update_time = last_update_time
        # this variable contains the authorized connection to the Twitter API
        self.TWITTER_CONNECTION = Twitter(auth=OAuth(self.token, self.token_secret, self.consumer_key, self.consumer_secret))

        # Used for random timers
        random.seed()

    def retweets(self, keywords, count=20):
        """
        Add users to list slug that are tweeting phrase.
        """
        idlist = []
        result = self.TWITTER_CONNECTION.statuses.user_timeline(screen_name=keywords,count=count)
        for tweet in result:
            try:
                created_at = time.mktime(time.strptime(tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y'));
                if (created_at - self.last_update_time < 0):
                    continue
                print("%s tweeted : %s : %s" % (tweet["user"]["screen_name"] ,tweet["text"],tweet["created_at"]), file=sys.stdout)
                #Retweet
                result = self.TWITTER_CONNECTION.statuses.retweet(id=tweet["id"])
                print("Retweeted: %s" % (result["text"].encode("utf-8")), file=sys.stdout)
                idlist.append(tweet["id"])
                # when you have already retweeted a tweet, this error is thrown
            except TwitterHTTPError as api_error:
                # quit on rate limit errors
                if "rate limit" in str(api_error).lower():
                    print("You have been rate limited. "
                          "Wait a while before running the bot again.", file=sys.stderr)
                    return idlist
                print("Error: %s" % (str(api_error)), file=sys.stderr)
        return idlist

if __name__ == '__main__':

    OAUTH_TOKEN = "316545541 - KuAqgwnwoG2U0hteVVogQCOCozLkhIVIcChnZ19O";
    OAUTH_SECRET = "gtfBT1nhbsh4l1IoQ9FubV9Uz6t0LItiyRC2NywW10zV8";
    CONSUMER_KEY = "gbbO6thCfWxKjp99v7CWGxiU5";
    CONSUMER_SECRET = "tw3Qha7gV4a3xew2euXj6UWYO3hiMlpLWuudYR3w5AegLgp2bQ";

    last_time = time.mktime(time.strptime("Sun Jun 18 00:00:00 +0000 2017", '%a %b %d %H:%M:%S +0000 %Y'));
    bot = Retweeter(OAUTH_TOKEN,OAUTH_SECRET,CONSUMER_KEY,CONSUMER_SECRET,last_time);

    bot.retweets("nytimes");
