# this program interfaces with the twitter api to fetch user bookmarks

import json
import glob
import functools

all_bookmarks = []
md_file = open("bookmarks.md", "w+")  # save in markdown file, if no file exists  using '+' creates one

files = [file for file in glob.glob("Bookmarks/*")]  # use glob to read all files from the folder
for file_name in files:
    print(file_name)
    with open(file_name) as bk:
        data = json.load(bk)
    all_bookmarks.append(data)


# construct bookmarked tweet url
def constructUrl(tweet_id, username):
    return "https://twitter.com/" + username + "/status/" + tweet_id


# format the text to write in file
def formatText(text):
    text = text.replace("\n-", " ")
    text = text.replace("\n", " ")
    text = text[:100] + "..."
    return text


# get value of nested dictionary
def deep_get(dictionary, keys, default=None):
    return functools.reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."),
                            dictionary)


# loop through all_bookmarks
for data in all_bookmarks:
    instructions_list = deep_get(data, "data.bookmark_timeline.timeline.instructions")
    if instructions_list == None: continue
    tweet_entries_list = deep_get(instructions_list[0], "entries")
    for tweet_entry in tweet_entries_list:
        result = deep_get(tweet_entry, "content.itemContent.tweet_results.result")
        username = deep_get(result, "core.user_results.result.legacy.screen_name")
        text = deep_get(result, "legacy.full_text")
        tweet_id = deep_get(result, "rest_id")
        if tweet_id == None or username == None or text == None: continue
        text = formatText(text)
        url = constructUrl(tweet_id, username)
        bookmarked_tweet = "\n- " + text + "\n" + "\t - " + url
        md_file.write(bookmarked_tweet)
