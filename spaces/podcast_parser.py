#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
import psycopg2

def parse_podcast(url):
    """Parses an XML feed and stores it to the db"""

    feed = feedparser.parse(url)
    print("======")
    # for key, value in feed.iteritems() :
    # 	print("%s:   %s" % (key, value))
    # print("======")

    print(feed['feed']['tags'][0]['term'])

    conn = psycopg2.connect("dbname=spaces user=spaces")

    feedId = getFeedId(conn, url, feed)

    conn.close()

def getFeedId(conn, url, feed):
    cur = conn.cursor()

    query = "SELECT id FROM feeds WHERE name = '%s' AND url = '%s';" % (
      feed['feed']['title'], 
      url)

    cur.execute(query)
    res = cur.fetchall()

    if (len(res) > 1):
        print('More than one')
        #raise Exception('Found multiple instance of (%s, %s)' % (feed['feed']['title'], url))
    elif (len(res) == 0):
       print('None')
       sql = "INSERT INTO feeds (url, name, genre, language, link) VALUES (%s, %s, %s, %s, %s);"

       print(url)
       print(feed['feed']['title'])
       print(feed['feed']['tags'][0]['term'])
       print(feed['feed']['language'])
       print(feed['feed']['link'])
       cur.execute(sql, (url, 
           feed['feed']['title'], 
           feed['feed']['tags'][0]['term'], 
           feed['feed']['language'], 
           feed['feed']['link']))
       conn.commit()
       cur.execute(query)
       res = cur.fetchall()

    feedId = res[0]
    print("feed id : %s" % (feedId))

    cur.close()
    return feedId

if __name__ == "__main__":
    parse_podcast('http://feeds.serialpodcast.org/serialpodcast')
	#parse_podcast('http://radiofrance-podcast.net/podcast09/rss_15644.xml')