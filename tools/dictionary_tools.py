import requests

def get_word_definition(text):
    """Fetch dictionary definition of a word."""
    clean_word = text.lower().replace("define", "").replace("meaning of", "").replace("what does", "").replace("mean", "").strip()
    clean_word = clean_word.split()[0] if clean_word else "algorithm"

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{clean_word}"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
            pos = data[0]["meanings"][0]["partOfSpeech"]
            return f"Definition of {clean_word.capitalize()} ({pos}): {meaning}"
    except Exception:
        pass

    return f"Could not find definition for '{clean_word}'."
