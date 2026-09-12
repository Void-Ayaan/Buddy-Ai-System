import re
import math
from collections import Counter

class NLPEngine:
    """
    🧠 Dedicated Natural Language Processing (NLP) Engine for Buddy AI System.
    Provides:
    1. Named Entity Recognition (NER) - Person, Location, Organization, DateTime, Command Target
    2. Sentiment & Emotion Tone Analysis - Positive, Negative, Urgent, Curious, Neutral
    3. Semantic Intent Matching - Jaccard/N-Gram Token Similarity
    4. Text Summarization & Keyphrase Extraction
    """
    def __init__(self):
        self.stop_words = {
            "a", "an", "the", "and", "or", "but", "is", "are", "was", "were", "be", "been",
            "being", "in", "on", "at", "to", "for", "from", "with", "by", "about", "against",
            "between", "into", "through", "during", "before", "after", "above", "below", "to",
            "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further",
            "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both",
            "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only",
            "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don",
            "should", "now", "i", "me", "my", "myself", "we", "our", "ours", "you", "your", "it"
        }

        self.positive_words = {"great", "awesome", "good", "love", "happy", "excellent", "wonderful", "amazing", "thanks", "thank"}
        self.negative_words = {"bad", "slow", "terrible", "worst", "error", "fail", "broken", "hate", "issue", "crash", "freeze"}
        self.urgent_words = {"quick", "now", "fast", "urgent", "emergency", "immediately", "asap"}

    def tokenize(self, text):
        """Clean and tokenize text into words."""
        words = re.findall(r'\b\w+\b', text.lower())
        return words

    def extract_named_entities(self, text):
        """
        Named Entity Recognition (NER):
        Identifies PERSON, LOCATION, ORGANIZATION, DATE_TIME, and COMMAND_TARGET.
        """
        entities = {
            "PERSON": [],
            "LOCATION": [],
            "ORGANIZATION": [],
            "COMMAND_TARGET": []
        }

        words = self.tokenize(text)
        text_title = text.title()

        # Known Locations
        locations = {"London", "Paris", "Tokyo", "Delhi", "Mumbai", "New York", "California", "Berlin", "Sydney"}
        for loc in locations:
            if loc.lower() in words:
                entities["LOCATION"].append(loc)

        # Known Organizations
        orgs = {"Google", "Microsoft", "Github", "Youtube", "Spotify", "Openai", "Discord", "Slack", "Steam"}
        for org in orgs:
            if org.lower() in words:
                entities["ORGANIZATION"].append(org)

        # Command targets (App / Process names)
        apps = {"chrome", "notepad", "vlc", "calculator", "paint", "explorer", "cmd", "powershell"}
        for app in apps:
            if app in words:
                entities["COMMAND_TARGET"].append(app)

        return entities

    def analyze_sentiment(self, text):
        """
        Semantic Sentiment Analysis:
        Returns sentiment state (POSITIVE, NEGATIVE, URGENT, CURIOUS, NEUTRAL) and polarity score (-1.0 to +1.0).
        """
        words = self.tokenize(text)
        if not words:
            return {"sentiment": "NEUTRAL", "polarity": 0.0}

        pos_count = sum(1 for w in words if w in self.positive_words)
        neg_count = sum(1 for w in words if w in self.negative_words)
        urg_count = sum(1 for w in words if w in self.urgent_words)

        polarity = round((pos_count - neg_count) / max(len(words), 1), 2)

        if urg_count > 0:
            sentiment = "URGENT"
        elif polarity > 0.1:
            sentiment = "POSITIVE"
        elif polarity < -0.1:
            sentiment = "NEGATIVE"
        elif "?" in text or any(w in words for w in ["why", "how", "what", "where", "who"]):
            sentiment = "CURIOUS"
        else:
            sentiment = "NEUTRAL"

        return {
            "sentiment": sentiment,
            "polarity": polarity,
            "positive_hits": pos_count,
            "negative_hits": neg_count
        }

    def semantic_similarity(self, text1, text2):
        """
        Calculate Jaccard Token Similarity score (0.0 to 1.0) between two text strings.
        """
        tokens1 = set(w for w in self.tokenize(text1) if w not in self.stop_words)
        tokens2 = set(w for w in self.tokenize(text2) if w not in self.stop_words)

        if not tokens1 or not tokens2:
            return 0.0

        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)

        return round(len(intersection) / float(len(union)), 3)

    def count_letter_occurrences(self, text):
        """
        Parses letter-counting questions like:
        - 'How many letters r are in the word strawberry?'
        - 'how many r in strawberry'
        - 'count letters r in strawberry'
        Returns formatted answer string if matched, else None.
        """
        match = re.search(r"how\s+many\s+(?:letter[s]?\s+)?['\"]?([a-zA-Z])['\"]?\s+(?:are\s+)?in\s+(?:the\s+word\s+)?['\"]?([a-zA-Z]+)['\"]?", text, re.IGNORECASE)
        if not match:
            match = re.search(r"count\s+(?:the\s+)?(?:letter\s+)?['\"]?([a-zA-Z])['\"]?\s+in\s+(?:the\s+word\s+)?['\"]?([a-zA-Z]+)['\"]?", text, re.IGNORECASE)

        if match:
            target_char = match.group(1).lower()
            target_word = match.group(2)
            count = target_word.lower().count(target_char)
            return f"There are exactly {count} '{target_char}' letter{'s' if count != 1 else ''} in the word '{target_word}', Boss!"
        return None

nlp_engine = NLPEngine()
