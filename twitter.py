import json
import os
from config import setConfig


def checkForDMs(api, maxTime):
    messages = api.list_direct_messages(100)
    times = []
    messages_list = []
    print('Checking for new messages')
    newMessages = False
    for dm in messages:
        message_data = dm.message_create['message_data']
        text = message_data['text']
        senderID = dm.message_create['sender_id']
        sender = api.get_user(senderID).screen_name
        # new_since_id = max()
        latest_time = dm.created_timestamp
        times.append(latest_time)
        recipient = api.get_user(dm.message_create['target']['recipient_id']).screen_name
        same = (recipient == sender)
        if int(dm.created_timestamp) > int(maxTime) and (sender != 'fake_laurarawra'):
            print('Responding to message from: ', sender)
            # names = [x for x in text.split(' ') if '@' in x]
            messages_list.append([senderID, text, sender])
            newMessages = True
    if not newMessages:
        print('No new messages')
        return [], maxTime
    maxTime = max(times)
    setConfig(maxTime)
    return messages_list, maxTime

def parseTweets(api, userID):
    # https://fairyonice.github.io/extract-someones-tweet-using-tweepy.html
    all_tweets = queryUserTweets(api, userID, 50)
    filename = str(userID) + '.json'
    dictionary = readJson(filename)
    for info in all_tweets:
        dictionary = parseString(info.full_text, dictionary)

    saveJson(filename, dictionary)
    return filename


def saveJson(path, dictionary):
    with open(path, 'w+') as f:
        json.dump(dictionary, f)


def parseString(text, dictionary):
    words = text.replace('.', '').replace(',', '').replace(':', '').replace(';', '').split(' ')
    for i in range(len(words)-2):
        key = words[i] + ' ' + words[i+1]
        value = words[i+2]
        try:
            if value not in dictionary[key]:
                dictionary[key].append(value)
        except:
            dictionary[key] = []
            dictionary[key].append(value)
    return dictionary


def readJson(path):
    try:
        if os.path.exists(path):
            with open(path, 'r') as file:
                dictionary = json.load(file)
                return dictionary
        else:
            saveJson(path, {})
            return {}
    except Exception as e:
        print(e)
        return {}


def get_max_id(api, userID):
    tweet = api.user_timeline(screen_name=userID,
                               # 200 is the maximum allowed count
                               count=1,
                               include_rts=False,
                               # Necessary to keep full_text
                               # otherwise only the first 140 words are extracted
                               tweet_mode='extended'
                               )
    return tweet[-1].id


def queryUserTweets(api, userID, num_tweets=None, oldest_id=None):
    """ Query for tweets from specified user
    Args:
        - api: tweepy api object
        - userID: string specified user
        - num_tweets: int number of tweets to get, default is None
                    for all tweets
        - since_id: int optional time id to grab tweets since_id
    Returns:
        - tweets: list of tweepy tweet objects"""
    loop = True
    if not num_tweets:
        count = 200
        num_tweets = 10000
    elif num_tweets < 200:
        count = num_tweets
        loop = False
    else:
        count = 200

    if oldest_id is not None:
        max_id = oldest_id - 1
    else:
        max_id = get_max_id(api, userID)
    all_tweets = []
    while True:
        # https://fairyonice.github.io/extract-someones-tweet-using-tweepy.html
        tweets = api.user_timeline(screen_name=userID,
                                # 200 is the maximum allowed count
                                count=count,
                                include_rts = False,
                                max_id=max_id,
                                # Necessary to keep full_text
                                # otherwise only the first 140 words are extracted
                                tweet_mode = 'extended'
                                )
        print('Tweets read: ', len(all_tweets))
        if len(tweets) == 0 or not loop or len(all_tweets) > num_tweets:
            all_tweets.extend(tweets)
            break
        all_tweets.extend(tweets)
        oldest_id = tweets[-1].id
        max_id = oldest_id
    return all_tweets


def get_tweet_text(api, userID, num_tweets=50):
    tweets_text = []
    tweets = queryUserTweets(api, userID, num_tweets)
    for info in tweets:
        tweets_text.append(info.full_text)
    return tweets_text