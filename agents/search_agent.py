from tools.web_search_tools import search_google, search_youtube, search_wikipedia

class SearchAgent:
    """AGENT-09: Google, YouTube, and Wikipedia Web Search Protocol."""
    def __init__(self):
        self.agent_id = "AGENT-09"
        self.name = "WEB-SEARCH"

    def google(self, query):
        return search_google(query)

    def youtube(self, query):
        return search_youtube(query)

    def wiki(self, query):
        return search_wikipedia(query)
