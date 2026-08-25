import urllib.parse
import webbrowser

def search_google(query):
    query_clean = query.strip()
    encoded = urllib.parse.quote(query_clean)
    url = f"https://www.google.com/search?q={encoded}"
    webbrowser.open(url)
    return f"Searching Google for {query_clean}"

def search_youtube(query):
    query_clean = query.strip()
    encoded = urllib.parse.quote(query_clean)
    url = f"https://www.youtube.com/results?search_query={encoded}"
    webbrowser.open(url)
    return f"Searching YouTube for {query_clean}"

def search_wikipedia(query):
    query_clean = query.strip()
    encoded = urllib.parse.quote(query_clean)
    url = f"https://en.wikipedia.org/wiki/Special:Search?search={encoded}"
    webbrowser.open(url)
    return f"Searching Wikipedia for {query_clean}"
