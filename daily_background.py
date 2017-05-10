#! /usr/bin/env python3
import getpass
import os
import re
import subprocess
import sys

import praw
import requests

import credentials as c


def main():

    file_path = '/home/' + getpass.getuser() + '/Pictures/reddit_wp/'

    if not os.path.exists(file_path):
        os.mkdir(file_path)

    regex = re.compile(r'(\s|/)')

    # Create reddit instance
    reddit = praw.Reddit(client_id=c.id, client_secret=c.secret,
                         password=c.password, username=c.username,
                         user_agent='dailybackground 0.1')

    subreddit = reddit.subreddit('wallpapers')
    # print(dir(subreddit.hot(limit=1).next()))
    url = subreddit.hot(limit=1).next().url

    for submission in subreddit.hot(limit=10):
        if 'redd' in submission.domain:
            url = submission.url
            title = regex.sub('_', submission.title).lower()
            break
    print(title.replace('<\s>', '_'))

    try:
        r = requests.get(url)
    except requests.RequestException as e:
        print(e)
        sys.exit(1)
    else:
        image_format = r.headers['Content-Type'].replace('image/jpeg', 'jpg').replace('image/png', 'png')
        image = r.content
        title = title + '.' + image_format

    print('Image title: ', title)

    with open(file_path + title, 'wb') as f:
        f.write(image)

    set_envir()
    os.system("gsettings set org.gnome.desktop.background picture-uri "
              "file:///home/" + getpass.getuser() + "/Pictures/reddit_wp/" + title)


# https://askubuntu.com/questions/483687/editing-gsettings-unsuccesful-when-initiated-from-cron
def set_envir():
    pid = subprocess.check_output(["pgrep", "gnome-session"]).decode("utf-8").strip()
    cmd = "grep -z DBUS_SESSION_BUS_ADDRESS /proc/"+pid+"/environ|cut -d= -f2-"
    os.environ["DBUS_SESSION_BUS_ADDRESS"] = subprocess.check_output(
        ['/bin/bash', '-c', cmd]).decode("utf-8").strip().replace("\0", "")

if __name__ == '__main__':
    main()
