#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser

def parse_podcast(url):
    """Main parsing function for podcast"""

    feed = feedparser.parse(url)
    print(feed['feed']['title'])

if __name__ == "__main__":
	parse_podcast('http://feeds.serialpodcast.org/serialpodcast')
	parse_podcast('http://radiofrance-podcast.net/podcast09/rss_15644.xml')