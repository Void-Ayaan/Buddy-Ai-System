import requests
import xml.etree.ElementTree as ET

def get_latest_news():
    """Fetch top live news headlines from Google News RSS feed."""
    url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        res = requests.get(url, headers=headers, timeout=6)
        if res.status_code == 200:
            root = ET.fromstring(res.content)
            items = root.findall(".//item")[:3]
            headlines = []
            for idx, item in enumerate(items):
                title = item.find("title").text
                clean_title = title.split(" - ")[0].strip()
                headlines.append(f"Headline {idx+1}: {clean_title}")

            news_str = ". ".join(headlines)
            return f"Here are the top news headlines, Boss: {news_str}"
    except Exception:
        pass

    return "Could not fetch latest news right now. Please check your internet connection."
