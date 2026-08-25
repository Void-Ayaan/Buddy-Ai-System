import os
import json
import urllib.request
import urllib.parse
from duckduckgo_search import DDGS

LEARNED_MEMORY_FILE = "memory/learned_knowledge.json"

def check_internet_connection():
    """Verify if laptop is currently connected to active internet."""
    try:
        urllib.request.urlopen("https://www.google.com", timeout=3)
        return True
    except Exception:
        return False

def load_learned_knowledge():
    """Load persistent learned knowledge memory."""
    if not os.path.exists(LEARNED_MEMORY_FILE):
        return {}
    try:
        with open(LEARNED_MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_learned_topic(topic, summary, details):
    """Save newly learned topic into persistent memory."""
    os.makedirs(os.path.dirname(LEARNED_MEMORY_FILE), exist_ok=True)
    memory = load_learned_knowledge()
    topic_key = topic.lower().strip()

    memory[topic_key] = {
        "topic": topic,
        "summary": summary,
        "details": details
    }

    try:
        with open(LEARNED_MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=4)
        return True
    except Exception:
        return False

def fetch_wikipedia_summary(topic):
    """Fetch structured encyclopedic summary from Wikipedia API."""
    try:
        encoded = urllib.parse.quote(topic)
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"
        req = urllib.request.Request(url, headers={"User-Agent": "BuddyAI/2.5"})
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode('utf-8'))
            extract = data.get("extract", "")
            if extract:
                ascii_extract = "".join([c for c in extract if ord(c) < 128]).strip()
                return ascii_extract
    except Exception:
        pass
    return None

def learn_topic_from_internet(topic):
    """Autonomous Learning Protocol: Crawls web & Wikipedia, synthesizes facts & saves to memory."""
    if not check_internet_connection():
        return "I am currently offline, Boss! Please connect to the internet so I can learn this topic for you."

    if not topic or len(topic.strip()) == 0:
        return "Please specify what topic you would like me to learn, Boss!"

    topic_clean = topic.strip()
    print(f"\n[ AGENT-11 LEARNER: Initializing deep learning process for '{topic_clean}'... ]")

    snippets = []

    # Source 1: Wikipedia REST API
    wiki_summary = fetch_wikipedia_summary(topic_clean)
    if wiki_summary:
        snippets.append(wiki_summary)

    # Source 2: DuckDuckGo Search API
    try:
        ddgs = DDGS()
        results = list(ddgs.text(topic_clean, max_results=5))
        if results:
            for r in results:
                body = r.get('body', '')
                if body:
                    ascii_body = "".join([c for c in body if ord(c) < 128]).strip()
                    if len(ascii_body) > 30 and ascii_body not in snippets:
                        snippets.append(ascii_body)
    except Exception:
        pass

    if not snippets:
        return f"I connected to the internet and searched for '{topic_clean}', but could not find clear learning materials, Boss."

    summary = " ".join(snippets[:2])
    if len(summary) > 400:
        summary = summary[:400] + "..."

    full_details = "\n".join([f"- {s}" for s in snippets])

    save_learned_topic(topic_clean, summary, full_details)

    return (
        f"Knowledge acquisition complete, Boss! I have learned about '{topic_clean}'.\n\n"
        f"**Summary**: {summary}\n\n"
        f"This topic is now permanently stored in my brain!"
    )

def recall_learned_topic(topic):
    """Query persistent learned knowledge."""
    memory = load_learned_knowledge()
    topic_key = topic.lower().strip()

    if topic_key in memory:
        data = memory[topic_key]
        return f"Here is what I learned about {data['topic']}, Boss:\n{data['summary']}"

    # Fuzzy match
    for k, v in memory.items():
        if topic_key in k or k in topic_key:
            return f"Here is what I learned about {v['topic']}, Boss:\n{v['summary']}"

    return None
