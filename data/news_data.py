import feedparser

def get_coindesk_news(limit=20):
    rss_url = "https://www.coindesk.com/arc/outboundfeeds/rss/"
    feed = feedparser.parse(rss_url)

    news = []

    for article in feed.entries[:limit]:
        news.append({
            "title": article.title,
            "summary": article.get("summary", ""),
            "published": article.get("published", ""),
            "link": article.link,
            "source": "CoinDesk"
        })

    return news

