import requests
import re

LANG_MAP = {
    "hindi": "hi",
    "spanish": "es",
    "french": "fr",
    "german": "de",
    "japanese": "ja",
    "italian": "it",
    "chinese": "zh",
    "russian": "ru",
}

def translate_phrase(text):
    """Translate English phrase to target language with console safe formatting."""
    text_lower = text.lower().strip()

    match = re.search(r"translate\s+(.+?)\s+to\s+([a-zA-Z]+)", text_lower)
    if not match:
        return "Please specify translation like 'translate hello to Hindi'."

    phrase = match.group(1).strip()
    lang_name = match.group(2).strip().lower()

    lang_code = LANG_MAP.get(lang_name, "hi")

    url = f"https://api.mymemory.translated.net/get?q={phrase}&langpair=en|{lang_code}"

    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            translated = data["responseData"]["translatedText"]
            
            # Clean non-ASCII for Windows cp1252 console safety
            safe_translated = translated.encode("ascii", "replace").decode("ascii")
            if "?" in safe_translated and len(safe_translated.replace("?", "")) < 2:
                return f"Translated '{phrase}' to {lang_name.capitalize()} successfully, Boss!"
            
            return f"Translation of '{phrase}' in {lang_name.capitalize()} is: {translated}, Boss!"
    except Exception:
        pass

    return f"Could not translate '{phrase}' right now."
