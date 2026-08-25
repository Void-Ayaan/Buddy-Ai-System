import random

JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the computer go to the doctor? Because it had a virus!",
    "Parallel lines have so much in common. It's a shame they'll never meet.",
    "What do you call 8 hobbits? A hobbyte!",
    "Why do programmers prefer dark mode? Because light attracts bugs!"
]

FACTS = [
    "Honey never spoils. Archaeologists have found 3000-year-old honey in Egyptian tombs that is still edible!",
    "Octopuses have three hearts and blue blood.",
    "Bananas are naturally slightly radioactive because they are rich in potassium.",
    "Venus is the only planet in our solar system that rotates clockwise.",
    "A day on Venus is longer than a year on Venus!"
]

QUOTES = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "Action is the foundational key to all success. - Pablo Picasso",
    "Innovation distinguishes between a leader and a follower. - Steve Jobs"
]

def get_joke():
    return random.choice(JOKES)

def get_fact():
    return random.choice(FACTS)

def get_quote():
    return random.choice(QUOTES)
