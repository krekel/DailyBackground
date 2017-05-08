#! /usr/bin/env python3
import requests
import praw
import credentials as c
import os
import re
import getpass


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
    image = requests.get(url).content

    # TODO add image extension to title
    # if image.startswith(b'FF\D8')

    with open(file_path + title, 'wb') as f:
        f.write(image)

    os.system("gsettings set org.gnome.desktop.background picture-uri "
              "file:///home/" + getpass.getuser() + "/Pictures/reddit_wp/" + title)

if __name__ == '__main__':
    main()
