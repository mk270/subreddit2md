#!/usr/bin/env python3

"""Generate a list of markdown links from a subreddit, specified in
   $SUBREDDIT"""

import requests
import time
import random
import os

subreddit = os.environ.get('SUBREDDIT', 'mk270')

def api(url, args):
    delay = 0.3

    while delay < 10:
        resp = requests.get(url, params=args).json()
        if "error" not in resp:
            return resp
        delay += 0.1 + random.random()
        time.sleep(delay)
    assert False, "timeout"

def get_posts():
    args = {
        "sort": "new",
        "limit": 100
    }
    template = """http://www.reddit.com/r/{0}/new.json"""
    url = template.format(subreddit)
    while True:
        results = api(url, args)
        args["after"] = results['data']['after']
        for child in results['data']['children']:
            yield child['data']
        if args["after"] is None:
            break

def run():
    fmt = "* [{0}]({1})"
    for post in get_posts():
        print(fmt.format(post['title'], post['url']))

if __name__ == '__main__':
    run()
