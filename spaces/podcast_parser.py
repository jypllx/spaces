#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
import psycopg2
import datetime

def parse_podcast(url):
    """Parses an XML feed and stores it to the db"""

    feed = feedparser.parse(url)
    # print("======")
    # for key, value in feed.entries[0].iteritems() :
    #     print("%s:   %s" % (key, value))
    # print("======")

    # print(feed.feed.tags[0].term)

    conn = psycopg2.connect("dbname=spaces user=spaces")

    channelId = getChannelId(conn, url, feed)

    for item in feed.entries:
        # print(item.title)
        # print(item.id)
        # print(item.duration)
        if existsItem(conn, channelId, item):
            pass
        else:
            saveItem(conn, channelId, item)

    conn.close()

def getChannelId(conn, url, feed):
    cur = conn.cursor()

    query = "SELECT id FROM channels WHERE name = '%s' AND url = '%s';" % (
      feed.feed.title, 
      url)

    cur.execute(query)
    res = cur.fetchall()

    if (len(res) > 1):
        print('More than one')
        #raise Exception('Found multiple instance of (%s, %s)' % (feed.feed['title'], url))
    elif (len(res) == 0):
       print('None')
       sql = "INSERT INTO channels (url, name, genre, language, link) VALUES (%s, %s, %s, %s, %s);"
       print(feed.feed.link)
       cur.execute(sql, (url, 
           feed.feed.title, 
           feed.feed.tags[0].term, 
           feed.feed.language, 
           feed.feed.link))
       conn.commit()
       cur.execute(query)
       res = cur.fetchall()
       conn.commit()

    channelId = res[0]
    print("Channel id : %s" % (channelId))

    cur.close()
    return channelId

def existsItem(conn, channelId, item):
    cur = conn.cursor()

    query = "SELECT id FROM items WHERE channel_id=%s AND name=%s"
    cur.execute(query, (channelId, item.title))
    res = cur.fetchall()
    conn.commit()
    cur.close
    if (len(res) > 1):
        print('More than one podcast for %s, %s' % (channelId, item.title))
        raise Exception('Merde!!')
    elif (len(res) == 1):
        return True
    else:
        return False

def saveItem(conn, channelId, item):
    cur = conn.cursor()
    sql="INSERT INTO items (channel_id, item_id, name, duration) VALUES (%s, %s, %s, %s);"
    cur.execute(sql, (channelId, item.title, item.id, item.itunes_duration))
    conn.commit()
    cur.close()


if __name__ == "__main__":
    parse_podcast('http://feeds.serialpodcast.org/serialpodcast')
	#parse_podcast('http://radiofrance-podcast.net/podcast09/rss_15644.xml')