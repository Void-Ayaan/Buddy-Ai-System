import re
import difflib

# Dictionary of Common Command Keyword Typo Corrections
KEYWORD_TYPO_MAP = {
    # Unlock & Lock typos
    "unlok": "unlock",
    "unlokc": "unlock",
    "anlock": "unlock",
    "unloc": "unlock",
    "lok": "lock",
    "lokc": "lock",
    "pasword": "password",
    "pasworde": "password",
    "passwrd": "password",
    
    # System & Hardware typos
    "sysytem": "system",
    "systm": "system",
    "computr": "computer",
    "compter": "computer",
    "laptp": "laptop",
    "diaganostic": "diagnostic",
    "diag": "diagnostic",
    "scane": "scan",
    
    # Prompt & AI typos
    "promt": "prompt",
    "propmt": "prompt",
    "promting": "prompting",
    "masterpromt": "master prompt",
    "eerthing": "everything",
    "eerything": "everything",
    "evrything": "everything",
    
    # Performance & Diagnostics typos
    "cheack": "check",
    "chek": "check",
    "chack": "check",
    "spead": "speed",
    "sped": "speed",
    "wether": "weather",
    "weathr": "weather",
    "cln": "clean",
    "optimise": "optimize",
    "optmize": "optimize",
    "recyle": "recycle",
    "recycel": "recycle",

    # Search & Media typos
    "serch": "search",
    "seach": "search",
    "wikipidia": "wikipedia",
    "ytube": "youtube",
    "volum": "volume",
    "volme": "volume",
}

# Known Core Command Targets for Fuzzy Matching
KNOWN_TARGETS = [
    "unlock pc", "lock pc", "system scan", "speed test", "clean temp",
    "make master prompt", "weather", "battery status", "check wifi",
    "empty recycle bin", "what can you do", "connect to mobile for audio",
    "who is tony stark", "tell me about blackhole", "what is python"
]

def normalize_fuzzy_input(text):
    """
    Fuzzy Spelling & Phrase Auto-Correction Engine:
    Auto-corrects misspelled words and misspelled sentences before routing to Agents.
    """
    if not text:
        return ""

    tokens = text.split()
    corrected_tokens = []

    for token in tokens:
        clean_tok = token.lower().strip(",.!?")
        # Direct dictionary substitution
        if clean_tok in KEYWORD_TYPO_MAP:
            corrected_tokens.append(KEYWORD_TYPO_MAP[clean_tok])
        else:
            corrected_tokens.append(token)

    corrected_text = " ".join(corrected_tokens)

    # Fuzzy match whole sentence against known command targets if similarity > 75%
    close_matches = difflib.get_close_matches(corrected_text.lower(), KNOWN_TARGETS, n=1, cutoff=0.75)
    if close_matches:
        return close_matches[0]

    return corrected_text
