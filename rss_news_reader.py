import sys
sys.path.append("./database")
from database.connect_db import get_rss_media_all, add_rss_feed, RssFeed, delete_rss_feed
import feedparser

def get_rss():
    current_record_no = 1
    max_repeat_count = 10
    rss_media_list = get_rss_media_all()
    for media in rss_media_list:
        print(f"=== Getting From [ {media.name} ] ===")
        print(f"From: {media.rss_url}")

        repeat_count = 0
        rss_feed_list = []
        feeds = feedparser.parse(media.rss_url)
        print(feeds)
        for i in range(0, len(feeds["entries"])):

            rss_feed = RssFeed()
            rss_feed.no = current_record_no
            rss_feed.title = feeds["entries"][i]["title"]
            rss_feed.link = feeds["entries"][i]["link"]
            rss_feed.updated_at = feeds["entries"][i]["published"]
            rss_feed.media_idx = media.idx

            print(f"[ {media.name} ] {rss_feed.title}")
            print(f"   Link: {rss_feed.link}")
            rss_feed_list.append(rss_feed)

            current_record_no = current_record_no + 1
            repeat_count = repeat_count + 1
            if repeat_count == max_repeat_count:
                break

        if len(rss_feed_list) == 0: continue
        delete_rss_feed(media.idx)
        for rss_feed in rss_feed_list:
            add_rss_feed(rss_feed)

        print(f"=== End From {media.name}")

import schedule, time
schedule.every().day.at("22:36:30").do(get_rss)

while True:
    schedule.run_pending()
    time.sleep(1)