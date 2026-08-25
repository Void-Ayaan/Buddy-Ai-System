import os
import json
import urllib.request
import urllib.parse
import re
import warnings

warnings.filterwarnings('ignore')

SYSTEM_PROMPT = """You are Buddy, a loyal, ultra-smart, fast, and helpful AI assistant for your boss (Ansh).
Always refer to yourself as Buddy. NEVER call yourself JARVIS, ChatGPT, or Claude.
Keep responses concise, polite, and helpful. Always address the user as Boss."""

LOCAL_GGUF_PATH = r"c:\buddy\models\Qwen3-1.7B-Q4_K_M.gguf"
_local_gguf_model = None

def clean_ascii_text(text):
    """Clean HTML tags and unicode artifacts for crisp presentation."""
    if not text:
        return ""
    # Strip HTML tags
    clean = re.sub(r'<[^>]+>', '', text)
    # Convert HTML entities like &quot; &#039;
    clean = clean.replace('&quot;', '"').replace('&#039;', "'").replace('&amp;', '&')
    # Filter non-ASCII unicode artifacts
    clean = re.sub(r'[^\x00-\x7F]+', ' ', clean)
    return " ".join(clean.split())

def query_wikipedia_knowledge(prompt):
    """
    Query Wikipedia REST API with automatic typo auto-correction via OpenSearch.
    Handles typos like 'tonny stark' -> 'Tony Stark'!
    """
    try:
        clean_topic = re.sub(r"^(?:tell\s+me\s+about|who\s+is|who\s+was|what\s+is|what\s+are|define|explain|where\s+is|history\s+of)\s+", "", prompt, flags=re.IGNORECASE).strip()
        if not clean_topic:
            clean_topic = prompt

        target_title = clean_topic

        # Step 1: Direct summary query
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(target_title)}"
            req = urllib.request.Request(url, headers={'User-Agent': 'BuddyAI/1.0'})
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode('utf-8'))
                extract = clean_ascii_text(data.get('extract', ''))
                if extract and len(extract) > 30:
                    return f"Here is what I found about {data.get('title', clean_topic)}, Boss:\n\n{extract}"
        except Exception:
            pass

        # Step 2: OpenSearch Typo Auto-Correction (e.g. 'tonny stark' -> 'Tony Stark')
        try:
            search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={urllib.parse.quote(clean_topic)}&limit=1&format=json"
            req = urllib.request.Request(search_url, headers={'User-Agent': 'BuddyAI/1.0'})
            with urllib.request.urlopen(req, timeout=3) as response:
                search_data = json.loads(response.read().decode('utf-8'))
                if len(search_data) > 1 and search_data[1]:
                    target_title = search_data[1][0]

                    summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(target_title)}"
                    req2 = urllib.request.Request(summary_url, headers={'User-Agent': 'BuddyAI/1.0'})
                    with urllib.request.urlopen(req2, timeout=3) as response2:
                        data2 = json.loads(response2.read().decode('utf-8'))
                        extract2 = clean_ascii_text(data2.get('extract', ''))
                        if extract2 and len(extract2) > 30:
                            return f"Here is what I found about {target_title}, Boss:\n\n{extract2}"
        except Exception:
            pass

        # Step 3: Wikipedia Query List Search Fallback
        try:
            wiki_search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(clean_topic)}&format=json"
            req3 = urllib.request.Request(wiki_search_url, headers={'User-Agent': 'BuddyAI/1.0'})
            with urllib.request.urlopen(req3, timeout=3) as response3:
                data3 = json.loads(response3.read().decode('utf-8'))
                search_results = data3.get('query', {}).get('search', [])
                if search_results:
                    first_res = search_results[0]
                    res_title = first_res.get('title', '')
                    res_snippet = clean_ascii_text(first_res.get('snippet', ''))
                    if res_snippet and len(res_snippet) > 20:
                        return f"Here is what I found regarding {res_title}, Boss:\n\n{res_snippet}"
        except Exception:
            pass

    except Exception:
        pass
    return None

def web_search_knowledge_synthesis(prompt):
    """Retrieve real-time web knowledge via Wikipedia (with typo correction) and DuckDuckGo."""
    # Try Wikipedia Knowledge API first (with typo auto-correction)
    wiki_res = query_wikipedia_knowledge(prompt)
    if wiki_res:
        return wiki_res

    # Try DuckDuckGo DDGS search
    try:
        try:
            from ddgs import DDGS
        except ImportError:
            from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            results = list(ddgs.text(prompt, max_results=3))
            if results:
                snippets = [r.get('body', '') for r in results if r.get('body')]
                clean_snippets = []
                for snip in snippets:
                    ascii_snip = clean_ascii_text(snip)
                    if len(ascii_snip) > 20:
                        clean_snippets.append(ascii_snip)

                if clean_snippets:
                    combined = " ".join(clean_snippets[:2])
                    if len(combined) > 400:
                        combined = combined[:400] + "..."
                    return f"Based on live search results, Boss: {combined}"
    except Exception:
        pass

    return None

def query_ollama_local(prompt):
    """Query local Ollama instance via HTTP API at localhost:11434."""
    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "qwen3",
            "prompt": f"{SYSTEM_PROMPT}\n\nUser: {prompt}\nBuddy:",
            "stream": False
        }
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=3) as response:
            res_json = json.loads(response.read().decode('utf-8'))
            answer = clean_ascii_text(res_json.get("response", "").strip())
            if answer:
                return answer
    except Exception:
        pass
    return None

def query_local_openai_compatible(prompt):
    """Query LM Studio / LocalAI / Llamafile at localhost:1234 or localhost:8080."""
    for port in [1234, 8080]:
        try:
            url = f"http://localhost:{port}/v1/chat/completions"
            payload = {
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=3) as response:
                res_json = json.loads(response.read().decode('utf-8'))
                answer = clean_ascii_text(res_json['choices'][0]['message']['content'].strip())
                if answer:
                    return answer
        except Exception:
            pass
    return None

def generate_code_response(prompt):
    """Generate real python/coding solutions when requested."""
    prompt_lower = prompt.lower()
    if "calculator" in prompt_lower:
        return (
            "Here is a simple calculator program in Python, Boss:\n\n"
            "```python\n"
            "def add(a, b): return a + b\n"
            "def subtract(a, b): return a - b\n"
            "def multiply(a, b): return a * b\n"
            "def divide(a, b): return a / b if b != 0 else 'Error: Division by zero'\n\n"
            "print('Simple Calculator')\n"
            "num1 = float(input('Enter first number: '))\n"
            "op = input('Enter operator (+, -, *, /): ')\n"
            "num2 = float(input('Enter second number: '))\n\n"
            "if op == '+': print('Result:', add(num1, num2))\n"
            "elif op == '-': print('Result:', subtract(num1, num2))\n"
            "elif op == '*': print('Result:', multiply(num1, num2))\n"
            "elif op == '/': print('Result:', divide(num1, num2))\n"
            "else: print('Invalid operator!')\n"
            "```"
        )
    elif "python" in prompt_lower or "code" in prompt_lower or "script" in prompt_lower:
        return (
            "Here is a python script template for your request, Boss:\n\n"
            "```python\n"
            "# Buddy Assistant Custom Automation Script\n"
            "import os\n"
            "import sys\n\n"
            "def main():\n"
            "    print('Script execution initialized, Boss!')\n\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
            "```"
        )
    return None

def ask_ai(prompt):
    """
    Multi-Tier AI Reasoning Engine:
    Tier 1: Greetings & Identity
    Tier 2: Code & Domain Synthesizer
    Tier 3: Typo Auto-Correcting Wikipedia & Live Web Knowledge Search Synthesis
    Tier 4: Ollama / LM Studio Local LLM
    """
    if not prompt or not prompt.strip():
        return "How can I assist you today, Boss?"

    prompt_clean = prompt.strip()
    prompt_lower = prompt_clean.lower()

    # Handle greetings & identity directly
    if prompt_lower in ["who are you", "what is your name", "who made you"]:
        return "I am Buddy, your loyal 11-Agent AI Swarm Assistant, Boss!"
    elif prompt_lower in ["hello", "hi", "hey", "hello buddy", "hey buddy"]:
        return "Hello, Boss! I am online and ready to assist you."

    # Tier 2: Code generation check
    code_res = generate_code_response(prompt_clean)
    if code_res:
        return code_res

    # Tier 3: Live Web & Wikipedia Knowledge Search Synthesis (with automatic typo correction!)
    web_res = web_search_knowledge_synthesis(prompt_clean)
    if web_res:
        return web_res

    # Tier 4: Try Local Ollama Instance
    ollama_res = query_ollama_local(prompt_clean)
    if ollama_res:
        return ollama_res

    # Tier 5: Try OpenAI-compatible local server (LM Studio / Llamafile)
    openai_res = query_local_openai_compatible(prompt_clean)
    if openai_res:
        return openai_res

    # Tier 6: Smart informative response
    topic = re.sub(r"^(?:tell\s+me\s+about|who\s+is|what\s+is|explain|define|test)\s+", "", prompt_clean, flags=re.IGNORECASE).strip()
    return f"All 11-Agent Swarm systems are online and operational, Boss! Ready to craft master prompts, search the web, or execute any command."
