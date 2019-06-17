# DISCLAIMER: YOU MUST GIVE BOT MOD ON YOUR SUBREDDIT

# SETTINGS

CLIENT_ID = ""                          # Type the gibberish under the app's name between the quotes.

CLIENT_SECRET = ""                      # Type the gibberish labeled "secret" on the app between the quotes.

BOT_NAME = "Repost Reporter"            # Feel free to change this, it won't affect anything.

USERNAME = ""                           # The username of the bot account.

PASSWORD = ""                           # The password of the bot account.

SUBREDDIT = ""                          # Your subreddit you want the bot to comment in.

RMS_THRESHOLD_PERCENT = 8               # This number represents the maximum amount an image can differ from another while still being considered a repost

TIME_LIMIT = 180                        # This number represents the amount of time (in days) before an image can be reposted

# CODE

import praw, time, math
from urllib.request import urlopen
from PIL import Image, ImageChops
import numpy as np

posts = []

# Code to calculate RMS
def compare (image1, image2):           
    errors = np.asarray(ImageChops.difference(image1, image2)) / 255
    return math.sqrt(np.mean(np.square(errors))) * 100

 # Creates Reddit instance
reddit = praw.Reddit(client_id=CLIENT_ID,                              
                    client_secret=CLIENT_SECRET,
                    user_agent=BOT_NAME,
                    username=USERNAME,
                    password=PASSWORD)

while True:
    for submission in reddit.subreddit(SUBREDDIT).stream.submissions():

        # Clears posts every TIME_LIMIT
        posts = list(filter(lambda x: (time.time() - x["time"])/3600/24 <= TIME_LIMIT, posts))  

        # Tries to fetch image from post, if the post is a text post, nothing will happen
        try:                                            
            h = Image.open(urlopen(submission.url))
        except:
            continue
        
        # Removes post if image is in RMS_THRESHOLD_PERCENT of the saved posts, otherwise it will save the post
        if len(list(filter(lambda x: compare(h, x["histogram"]) < RMS_THRESHOLD_PERCENT, posts))) >= 1:
            submission.mod.remove()
        else:
            posts.append({"histogram": h, "time": time.time()})
            