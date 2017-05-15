#! /usr/bin/env python3
import getpass
import os
import re
import subprocess
import sys

import praw
import requests
from bs4 import BeautifulSoup

import credentials as c


def main():

    file_path = '/home/' + getpass.getuser() + '/Pictures/reddit_wp/'

    if not os.path.exists(file_path):
        os.mkdir(file_path)

    # Replace any of these characters
    regex = re.compile(r'(\s|/|\(|\))')

    # Create reddit instance
    reddit = praw.Reddit(client_id=c.id, client_secret=c.secret,
                         password=c.password, username=c.username,
                         user_agent='dailybackground 0.1')

    subreddit = reddit.subreddit('wallpapers')
    # print(dir(subreddit.hot(limit=1).next()))
    url = subreddit.hot(limit=1).next().url

    for submission in subreddit.hot(limit=1):
        url = submission.url
        title = regex.sub('_', submission.title).lower()

    image, title = get_img(url, title)

    # Used for logging file
    print('Image title: ', title)

    with open(file_path + title, 'wb') as f:
        f.write(image)

    set_envir()
    os.system("gsettings set org.gnome.desktop.background picture-uri "
              "file:///home/" + getpass.getuser() + "/Pictures/reddit_wp/" + title)


def get_img(url, img_title='test'):
    try:
        r = requests.get(url)
        ct = r.content
    except requests.RequestException as e:
        print(e)
        sys.exit(1)
    else:
        # print(r.headers)
        if 'html' in r.headers['Content-Type']:
            # use bs4 to extract image
            bs = BeautifulSoup(ct, 'lxml')
            html_images = bs.find_all('img', class_='post-image-placeholder')
            print(html_images[0].get('src'))
            try:
                image = requests.get('https:' + html_images[0].get('src')).content
                file_title = img_title
            except requests.RequestException as e:
                print(e)
                sys.exit(1)
        else:
            image_format = r.headers['Content-Type'].replace('image/jpeg', 'jpg').replace('image/png', 'png')
            image = r.content
            file_title = img_title + '.' + image_format

        return image, file_title


# https://askubuntu.com/questions/483687/editing-gsettings-unsuccesful-when-initiated-from-cron
def set_envir():
    pid = subprocess.check_output(["pgrep", "gnome-session"]).decode("utf-8").strip()
    cmd = "grep -z DBUS_SESSION_BUS_ADDRESS /proc/"+pid+"/environ|cut -d= -f2-"
    os.environ["DBUS_SESSION_BUS_ADDRESS"] = subprocess.check_output(['/bin/bash', '-c', cmd])\
        .decode("utf-8").strip().replace("\0", "")

if __name__ == '__main__':
    main()
