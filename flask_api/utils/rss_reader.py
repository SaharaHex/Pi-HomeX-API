import feedparser

def fetch_rss_items(feed_url, limit=10):
    feed = feedparser.parse(feed_url)
    items = []

    for entry in feed.entries[:limit]:
        items.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.get('published', 'N/A'),
            'summary': entry.get('summary', '')
        })

    return items
