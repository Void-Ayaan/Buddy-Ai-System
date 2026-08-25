from tools.speed_test_tools import run_quick_speed_test
from tools.weather_tools import get_weather
from tools.news_tools import get_latest_news
from tools.speed_tools import check_website_status
from tools.translator_tools import translate_phrase

class NetworkAgent:
    """AGENT-05: Network Services, Live APIs, Weather, RSS News, and Speed Test."""
    def __init__(self):
        self.agent_id = "AGENT-05"
        self.name = "NETWORK-PILOT"

    def speed_test(self):
        return run_quick_speed_test()

    def weather(self, location=None):
        return get_weather(location)

    def news(self):
        return get_latest_news()

    def check_site(self, domain):
        return check_website_status(domain)

    def translate(self, text):
        return translate_phrase(text)
