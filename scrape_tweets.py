import tweepy
import sys
import jsonpickle
import os
import json


def main():
    acc_token = '1281800232-Uxokuhb8FZRcvTZgjpZVS2R6jJWTdPI02OCfoyX'
    acc_token_secret = 'elnGW6azrePB62GGzrf4s6DDQu15f3Pgw9EwsIe9nE2wq'
    consumer_key = '7sqbLPQfLHsx5YfefeLdH9h4S'
    consumer_secret = 'tGZKAeJPZfgAbu7J2u5OyDyFIP2q3XXoimwTDEtQWUQuKxZwnQ'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(acc_token, acc_token_secret)

    searchQuery = 'racism -filter:retweets'  # this is what we're searching for
    maxTweets = 1000*1000  # Some arbitrary large number
    tweetsPerQry = 100  # this is the max the API permits
    fName = 'tweets.txt'  # We'll store the tweets in a text file.

    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    if (not api):
        print("Can't Authenticate")
        sys.exit(-1)

    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1

    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))
    with open(fName, 'a+', encoding='utf-8') as f:
        while tweetCount < maxTweets:
            try:
                if (max_id <= 0):
                    if (not sinceId):
                        new_tweets = api.search(
                            q=searchQuery, tweet_mode='extended', count=tweetsPerQry)
                    else:
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                                since_id=sinceId, tweet_mode='extended')
                else:
                    if (not sinceId):
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                                max_id=str(max_id - 1), tweet_mode='extended')
                    else:
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                                max_id=str(max_id - 1),
                                                since_id=sinceId, tweet_mode='extended')
                if not new_tweets:
                    print("No more tweets found")
                    break
                for tweet in new_tweets:
                    text = tweet._json['full_text'].replace('\n','')
                    f.write(text+'\n')
                tweetCount += len(new_tweets)
                print("Downloaded {0} tweets".format(tweetCount))
                max_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                break

    print("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))


if __name__ == "__main__":
    main()

print('hello')
