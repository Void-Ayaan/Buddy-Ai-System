from tools.learner_tools import learn_topic_from_internet, recall_learned_topic, check_internet_connection

class LearnerAgent:
    """AGENT-11: Autonomous Knowledge Acquisition, Web Scraping, and Neural Memory Engine."""
    def __init__(self):
        self.agent_id = "AGENT-11"
        self.name = "KNOWLEDGE-LEARNER"

    def learn(self, topic):
        return learn_topic_from_internet(topic)

    def recall(self, topic):
        return recall_learned_topic(topic)

    def is_online(self):
        return check_internet_connection()
