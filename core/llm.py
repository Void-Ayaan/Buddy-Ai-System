import os
import json
import urllib.request
import urllib.parse
import re
import warnings
import threading

warnings.filterwarnings('ignore')

SYSTEM_PROMPT = """You are Buddy, a loyal, ultra-smart, fast, and helpful AI assistant for your boss (Ansh).
Always refer to yourself as Buddy. NEVER call yourself JARVIS, ChatGPT, or Claude.
Keep responses concise, polite, and helpful. Always address the user as Boss."""

LOCAL_GGUF_PATH = r"c:\buddy\models\Qwen3-1.7B-Q4_K_M.gguf"
_local_gguf_model = None
_gguf_load_attempted = False

def clean_ascii_text(text):
    """Clean HTML tags and unicode artifacts for crisp presentation."""
    if not text:
        return ""
    # Strip HTML tags
    clean = re.sub(r'<[^>]+>', '', text)
    # Convert HTML entities
    clean = clean.replace('&quot;', '"').replace('&#039;', "'").replace('&amp;', '&').replace('&nbsp;', ' ')
    # Filter non-ASCII unicode artifacts
    clean = re.sub(r'[^\x00-\x7F]+', ' ', clean)
    return " ".join(clean.split())

def query_gguf_local_model(prompt):
    """Query local GGUF model directly with non-blocking timeout."""
    global _local_gguf_model, _gguf_load_attempted
    res_container = [None]

    def _run():
        global _local_gguf_model, _gguf_load_attempted
        try:
            if _local_gguf_model is None and not _gguf_load_attempted:
                _gguf_load_attempted = True
                if os.path.exists(LOCAL_GGUF_PATH):
                    from ctransformers import AutoModelForCausalLM
                    _local_gguf_model = AutoModelForCausalLM.from_pretrained(
                        LOCAL_GGUF_PATH,
                        model_type="qwen2",
                        max_new_tokens=120,
                        gpu_layers=0
                    )

            if _local_gguf_model:
                formatted_prompt = f"System: {SYSTEM_PROMPT}\nUser: {prompt}\nBuddy:"
                res = _local_gguf_model(formatted_prompt)
                if res and res.strip():
                    res_container[0] = res.strip()
        except Exception:
            pass

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    t.join(timeout=0.6)
    return res_container[0]

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
        with urllib.request.urlopen(req, timeout=1.5) as response:
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
            with urllib.request.urlopen(req, timeout=1.5) as response:
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

def query_wikipedia_knowledge(prompt):
    """
    Query Wikipedia REST API with automatic typo auto-correction via OpenSearch.
    Handles typos like 'tonny stark' -> 'Tony Stark'!
    """
    try:
        clean_topic = re.sub(r"^(?:tell\s+me\s+about|who\s+is|who\s+was|what\s+is|what\s+are|define|explain|where\s+is|history\s+of|how\s+to)\s+", "", prompt, flags=re.IGNORECASE).strip()
        if not clean_topic:
            clean_topic = prompt

        target_title = clean_topic

        # Step 1: Direct summary query
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(target_title)}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=2.5) as response:
                data = json.loads(response.read().decode('utf-8'))
                extract = clean_ascii_text(data.get('extract', ''))
                if extract and len(extract) > 30:
                    return f"Here is what I found about {data.get('title', clean_topic)}, Boss:\n\n{extract}"
        except Exception:
            pass

        # Step 2: OpenSearch Typo Auto-Correction (e.g. 'tonny stark' -> 'Tony Stark')
        try:
            search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={urllib.parse.quote(clean_topic)}&limit=1&format=json"
            req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=2.5) as response:
                search_data = json.loads(response.read().decode('utf-8'))
                if len(search_data) > 1 and search_data[1]:
                    target_title = search_data[1][0]

                    summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(target_title)}"
                    req2 = urllib.request.Request(summary_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                    with urllib.request.urlopen(req2, timeout=2.5) as response2:
                        data2 = json.loads(response2.read().decode('utf-8'))
                        extract2 = clean_ascii_text(data2.get('extract', ''))
                        if extract2 and len(extract2) > 30:
                            return f"Here is what I found about {target_title}, Boss:\n\n{extract2}"
        except Exception:
            pass

        # Step 3: Wikipedia Query List Search Fallback
        try:
            wiki_search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(prompt)}&format=json"
            req3 = urllib.request.Request(wiki_search_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req3, timeout=2.5) as response3:
                data3 = json.loads(response3.read().decode('utf-8'))
                search_results = data3.get('query', {}).get('search', [])
                if search_results:
                    snippets = []
                    for item in search_results[:2]:
                        res_title = item.get('title', '')
                        res_snippet = clean_ascii_text(item.get('snippet', ''))
                        if res_snippet and len(res_snippet) > 20:
                            snippets.append(f"**{res_title}**: {res_snippet}")
                    if snippets:
                        return f"Here is what I retrieved for your query, Boss:\n\n" + "\n\n".join(snippets)
        except Exception:
            pass

    except Exception:
        pass
    return None

def web_search_knowledge_synthesis(prompt):
    """Retrieve real-time web knowledge via Wikipedia and DuckDuckGo."""
    # Try Wikipedia Knowledge API first
    wiki_res = query_wikipedia_knowledge(prompt)
    if wiki_res:
        return wiki_res

    # Try DuckDuckGo DDGS search dynamically
    try:
        import importlib
        DDGS = None
        for mod_name in ["duckduckgo_search", "ddgs"]:
            try:
                mod = importlib.import_module(mod_name)
                DDGS = getattr(mod, "DDGS", None)
                if DDGS:
                    break
            except Exception:
                pass

        if DDGS:
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

def ask_ai(prompt):
    """
    EXPLICIT MULTI-TIER REASONING HIERARCHY:

    1. Tier 1: Greetings & Identity (Hello, Who are you)
       │
       ▼
    2. Tier 2: Local LLM Engine & Local Knowledge Model (TRY FIRST!)
       ├── Queries Local GGUF Model (c:\\buddy\\models\\Qwen3-1.7B-Q4_K_M.gguf)
       ├── Queries Local Ollama Instance (localhost:11434)
       ├── Queries Local OpenAI-Compatible Server (LM Studio / Llamafile)
       ├── Queries Local Code Synthesizer
       └── IF Local Model generates an answer ➔ RETURNS IMMEDIATELY! (Zero Web Search)
       │
       ▼ (Only if Local Models are offline or return no answer)
    3. Tier 3: Web Search & Wikipedia (FALLBACK ONLY)
       └── Typo Auto-Correcting Wikipedia REST + Query List Search + DuckDuckGo
    """
    if not prompt or not prompt.strip():
        return "How can I assist you today, Boss?"

    prompt_clean = prompt.strip()
    prompt_lower = prompt_clean.lower()

    # -------------------------------------------------------------
    # TIER 1: Greetings & Identity (Hello, Who are you)
    # -------------------------------------------------------------
    if prompt_lower in ["who are you", "what is your name", "who made you"]:
        return f"I am Buddy, powered by your local Qwen3-1.7B GGUF model ({os.path.basename(LOCAL_GGUF_PATH)}), Boss!"
    elif prompt_lower in ["hello", "hi", "hey", "hello buddy", "hey buddy"]:
        return "Hello, Boss! I am online and ready to assist you."

    # -------------------------------------------------------------
    # TIER 2: Local LLM Engine & Local Knowledge Model (TRY FIRST!)
    # -------------------------------------------------------------
    # A. Try Local GGUF Model (c:\buddy\models\Qwen3-1.7B-Q4_K_M.gguf)
    gguf_res = query_gguf_local_model(prompt_clean)
    if gguf_res:
        return gguf_res

    # B. Try Local Ollama Instance (localhost:11434)
    ollama_res = query_ollama_local(prompt_clean)
    if ollama_res:
        return ollama_res

    # C. Try Local OpenAI-compatible server (LM Studio / Llamafile)
    openai_res = query_local_openai_compatible(prompt_clean)
    if openai_res:
        return openai_res

    # D. Try Local Code Generator
    code_res = generate_code_response(prompt_clean)
    if code_res:
        return code_res

    # -------------------------------------------------------------
    # TIER 3: Web Search & Wikipedia (FALLBACK ONLY)
    # -------------------------------------------------------------
    web_res = web_search_knowledge_synthesis(prompt_clean)
    if web_res:
        return web_res

    # Clean fallback response addressing Boss Ansh
    topic = re.sub(r"^(?:tell\s+me\s+about|who\s+is|what\s+is|explain|define|test|how\s+to)\s+", "", prompt_clean, flags=re.IGNORECASE).strip()
    return f"Boss, I searched for '{topic.title()}' across your Knowledge Engine. Feel free to ask me to make a master prompt, search YouTube/Google, or execute any system protocol!"
