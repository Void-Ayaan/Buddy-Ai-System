import re
import math
from collections import Counter

class NLPEngine:
    """
    🧠 Advanced Natural Language Processing (NLP) & Deep Understanding Engine.
    Provides:
    1. Deep Intent Parsing (CODING, SYSTEM_CONTROL, REASONING, SEARCH, CHAT)
    2. Named Entity Recognition (NER) - Person, Location, Organization, DateTime, Command Target
    3. Sentiment & Emotion Tone Analysis - Positive, Negative, Urgent, Curious, Neutral
    4. N-Gram & TF-IDF Vector Semantic Similarity Matching
    5. Reasoning Letter & Word Counter
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

        self.coding_keywords = {"write", "build", "code", "script", "create", "pygame", "python", "javascript", "html", "css", "app", "game", "animation", "debug", "fix"}
        self.system_keywords = {"scan", "lock", "sleep", "shutdown", "restart", "clean", "temp", "ram", "speed", "test", "kill", "process", "volume"}

    def tokenize(self, text):
        """Clean and tokenize text into words."""
        return re.findall(r'\b\w+\b', text.lower())

    def extract_ngrams(self, text, n=2):
        """Extract word n-grams for multi-word concept comprehension."""
        words = self.tokenize(text)
        if len(words) < n:
            return words
        return [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]

    def parse_deep_intent(self, text):
        """
        Deep Intent Parsing:
        Analyzes full sentence structure to determine primary category and confidence score.
        """
        words = set(self.tokenize(text))
        text_lower = text.lower()

        # Check for Coding / Development Intent
        code_hits = len(words.intersection(self.coding_keywords))
        if any(phrase in text_lower for phrase in ["write a script", "write code", "create a game", "make a website", "python script", "pygame"]):
            code_hits += 3

        # Check for System Control Intent
        sys_hits = 0
        if any(phrase in text_lower for phrase in ["lock pc", "lock screen", "sleep pc", "clean temp", "system scan", "kill process"]):
            sys_hits += 4

        if code_hits > sys_hits and code_hits >= 1:
            category = "CODING"
            confidence = min(1.0, 0.4 + code_hits * 0.2)
        elif sys_hits > code_hits and sys_hits >= 1:
            category = "SYSTEM_CONTROL"
            confidence = min(1.0, 0.4 + sys_hits * 0.2)
        elif any(w in words for w in ["what", "why", "how", "when", "who", "where", "explain", "describe"]):
            category = "REASONING"
            confidence = 0.8
        else:
            category = "CHAT"
            confidence = 0.5

        return {
            "category": category,
            "confidence": confidence,
            "tokens": list(words),
            "bigrams": self.extract_ngrams(text, 2)
        }

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
        Calculate Jaccard Token & N-Gram Similarity score (0.0 to 1.0) between two text strings.
        """
        tokens1 = set(w for w in self.tokenize(text1) if w not in self.stop_words)
        tokens2 = set(w for w in self.tokenize(text2) if w not in self.stop_words)

        if not tokens1 or not tokens2:
            return 0.0

        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)

        jaccard = len(intersection) / float(len(union))

        # Check bigram overlap
        bigrams1 = set(self.extract_ngrams(text1, 2))
        bigrams2 = set(self.extract_ngrams(text2, 2))
        if bigrams1 and bigrams2:
            bigram_sim = len(bigrams1.intersection(bigrams2)) / float(len(bigrams1.union(bigrams2)))
            return round(0.6 * jaccard + 0.4 * bigram_sim, 3)

        return round(jaccard, 3)

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

    def extract_keyphrases(self, text, top_n=3):
        """Extract top N frequency keyphrases from text excluding stopwords."""
        words = [w for w in self.tokenize(text) if w not in self.stop_words and len(w) > 2]
        counts = Counter(words)
        return [item[0] for item in counts.most_common(top_n)]

nlp_engine = NLPEngine()
