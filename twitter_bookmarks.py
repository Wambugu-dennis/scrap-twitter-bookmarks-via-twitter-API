import json
import glob
import functools
# import os
import tweepy

consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret"
access_token = "your_access_token"
access_token_secret = "your_access_token_secret"

# authenticating with Twitter API
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret)

api = tweepy.API(auth)
bookmarks = []
md_file = open("bookmarks.md", "w+")  

files = [file for file in glob.glob("Bookmarks/*")]  # use glob to read all files from the folder
for file_name in files:
    print(file_name)
    with open(file_name) as bk:
        data = json.load(bk)
        bookmarks.append(data)

def constructUrl(tweet_id, username):
    return "https://twitter.com/" + username + "/status/" + tweet_id

def formatText(text):
    text = text.replace("\n-", " ")
    text = text.replace("\n", " ")
    text = text[:100] + "..."
    return text


def deep_get(dictionary, keys, default=None):
    return functools.reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."),
                            dictionary)



username = input("Enter username: ")
tweet_id = input("Enter tweet ID: ")


for data in all_bookmarks:
    instructions_list = deep_get(data, "data.bookmark_timeline.timeline.instructions")
    if instructions_list == None: continue
    tweet_entries_list = deep_get(instructions_list[0], "entries")
    for tweet_entry in tweet_entries_list:
        result = deep_get(tweet_entry, "content.itemContent.tweet_results.result")
        tweet_username = deep_get(result, "core.user_results.result.legacy.screen_name")
        text = deep_get(result, "legacy.full_text")
        tweet_id_result = deep_get(result, "rest_id")
        if tweet_id_result == None or tweet_username == None or text == None: continue
        if tweet_id_result == tweet_id and tweet_username == username:
            text = formatText(text)
            url = constructUrl(tweet_id, username)
            bookmarked_tweet = "\n- " + text + "\n" + "\t - " + url
            md_file.write(bookmarked_tweet)
            break
    else:
        continue
    break
