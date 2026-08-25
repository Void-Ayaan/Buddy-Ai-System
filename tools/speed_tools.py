import requests
import time

def check_website_status(domain):
    """Check if a website is up, down, or slow."""
    clean_domain = domain.lower().replace("check website", "").replace("is", "").replace("down", "").replace("working", "").strip()
    if not clean_domain:
        clean_domain = "google.com"

    if not clean_domain.startswith("http"):
        url = f"https://{clean_domain}"
    else:
        url = clean_domain

    try:
        start_time = time.time()
        res = requests.get(url, timeout=5)
        latency = int((time.time() - start_time) * 1000)

        if res.status_code < 400:
            return f"Website {clean_domain} is online and responding normally with {latency} ms latency, Boss!"
        else:
            return f"Website {clean_domain} returned HTTP status code {res.status_code}."
    except Exception:
        return f"Website {clean_domain} appears to be unreachable or offline right now."
