import os
import json
import urllib.request
import urllib.parse
import re
import warnings
import logging
from core.llamafile_manager import ensure_llamafile_server_running, is_llamafile_server_running

warnings.filterwarnings('ignore')

SYSTEM_PROMPT = """You are Buddy, a loyal, ultra-smart, fast, and helpful AI assistant for your boss (Ansh).
Always refer to yourself as Buddy. NEVER call yourself JARVIS, ChatGPT, or Claude.
Keep responses concise, polite, and helpful. Always address the user as Boss."""

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

def query_local_openai_compatible(messages, tools=None, tool_choice=None, max_tokens=512, temperature=0.2, timeout=90, auto_spawn=True, chat_template_kwargs=None):
    """
    Query local OpenAI-compatible server (llamafile on 8080, LM Studio on 1234).
    Supports multi-turn messages array, streaming/non-streaming, and native tool calling.
    Exceptions are properly logged instead of silently swallowed.
    """
    if auto_spawn:
        ensure_llamafile_server_running()

    payload = {
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    if tools:
        payload["tools"] = tools
    if tool_choice:
        payload["tool_choice"] = tool_choice
    if chat_template_kwargs is not None:
        payload["chat_template_kwargs"] = chat_template_kwargs

    data = json.dumps(payload).encode('utf-8')

    for port in [8080, 1234]:
        url = f"http://127.0.0.1:{port}/v1/chat/completions"
        try:
            req = urllib.request.Request(
                url,
                data=data,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                res_json = json.loads(response.read().decode('utf-8'))
                choices = res_json.get("choices", [])
                if choices:
                    return choices[0].get("message", {})
        except Exception as e:
            logging.warning(f"[Local LLM] Request to {url} failed: {e}")

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
            with urllib.request.urlopen(req, timeout=3.0) as response:
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
            with urllib.request.urlopen(req, timeout=3.0) as response:
                search_data = json.loads(response.read().decode('utf-8'))
                if len(search_data) > 1 and search_data[1]:
                    target_title = search_data[1][0]

                    summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(target_title)}"
                    req2 = urllib.request.Request(summary_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                    with urllib.request.urlopen(req2, timeout=3.0) as response2:
                        data2 = json.loads(response2.read().decode('utf-8'))
                        extract2 = clean_ascii_text(data2.get('extract', ''))
                        if extract2 and len(extract2) > 30:
                            return f"Here is what I found about {target_title}, Boss:\n\n{extract2}"
        except Exception:
            pass
    except Exception as e:
        logging.warning(f"[Wikipedia] Query error: {e}")

    return None

def web_search_knowledge_synthesis(prompt):
    """Retrieve real-time web knowledge via Wikipedia and DuckDuckGo."""
    wiki_res = query_wikipedia_knowledge(prompt)
    if wiki_res:
        return wiki_res

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
                    clean_snippets = [clean_ascii_text(s) for s in snippets if len(clean_ascii_text(s)) > 20]
                    if clean_snippets:
                        combined = " ".join(clean_snippets[:2])
                        if len(combined) > 400:
                            combined = combined[:400] + "..."
                        return f"Based on live search results, Boss: {combined}"
    except Exception as e:
        logging.warning(f"[WebSearch] Search error: {e}")

    return None

SYSTEM_PROMPT = (
    "You are Buddy, a fast, responsive, and intelligent AI desktop assistant. "
    "If tools are provided that fulfill the user's action or task, call the appropriate tool function directly. "
    "Keep answers direct, natural, and helpful without verbose internal monologue or unnecessary preamble."
)

def build_chat_messages(user_prompt, system_prompt=SYSTEM_PROMPT):
    """Assemble conversation history into standard OpenAI messages array."""
    messages = [{"role": "system", "content": system_prompt}]
    try:
        from memory.memory_manager import _load_session_history
        history = _load_session_history()
        for turn in history[-6:]:
            u = turn.get("user")
            b = turn.get("buddy")
            if u:
                messages.append({"role": "user", "content": u})
            if b:
                messages.append({"role": "assistant", "content": b})
    except Exception as e:
        logging.warning(f"[LLM] Could not load chat history: {e}")

    messages.append({"role": "user", "content": user_prompt})
    return messages

def ask_ai(prompt, tools=None, auto_spawn=True):
    """
    Main conversational AI entry point:
    1. Feeds prompt with multi-turn conversation history to Qwen3 local model.
    2. Falls back to explicit web search only if user explicitly asks for web/wikipedia.
    3. Returns honest transparent diagnostic status if local model server is unreachable.
    """
    if not prompt or not prompt.strip():
        return "How can I assist you today, Boss?"

    prompt_clean = prompt.strip()
    prompt_lower = prompt_clean.lower()

    # Explicit Web/Wiki Search (only if explicitly requested by keyword)
    search_keywords = ["search wikipedia for", "search google for", "search web for", "lookup on wikipedia"]
    if any(sk in prompt_lower for sk in search_keywords):
        web_res = web_search_knowledge_synthesis(prompt_clean)
        if web_res:
            return web_res

    # Build messages array with real multi-turn conversation history
    messages = build_chat_messages(prompt_clean)

    # Intelligently select candidate tools if not explicitly supplied
    if tools is None:
        try:
            from core.tool_registry import select_candidate_tools
            candidate_tools = select_candidate_tools(prompt_clean)
            if candidate_tools:
                tools = candidate_tools
        except Exception:
            tools = None

    # For tool calls, allow 512 tokens; for conversational, 150 tokens. Always disable thinking mode for fast sub-30s CPU response.
    token_budget = 512 if tools else 150
    chat_kwargs = {"enable_thinking": False}
    message_obj = query_local_openai_compatible(
        messages,
        tools=tools,
        max_tokens=token_budget,
        temperature=0.2,
        timeout=90,
        auto_spawn=auto_spawn,
        chat_template_kwargs=chat_kwargs
    )
    if message_obj:
        tool_calls = message_obj.get("tool_calls")
        if tool_calls:
            try:
                from core.tool_registry import execute_registered_tool
                results = []
                for call in tool_calls:
                    fn = call.get("function", {})
                    fn_name = fn.get("name", "")
                    raw_args = fn.get("arguments", "{}")
                    try:
                        args = json.loads(raw_args) if isinstance(raw_args, str) and raw_args.strip() else (raw_args or {})
                    except Exception:
                        args = {}
                    logging.info(f"[ask_ai] Executing tool '{fn_name}' with args {args}")
                    obs = execute_registered_tool(fn_name, args)
                    results.append((fn_name, obs))

                if len(results) == 1:
                    return str(results[0][1])
                elif len(results) > 1:
                    return "\n\n".join([f"**Step {i} ({n.upper()})**: {o}" for i, (n, o) in enumerate(results, 1)])
            except Exception as e:
                logging.warning(f"[ask_ai] Tool execution failed: {e}")

        content = message_obj.get("content", "")
        if content and content.strip():
            return clean_ascii_text(content.strip())

    # Fallback to web search ONLY if the user explicitly asked for factual lookup/search
    search_intent = any(k in prompt_lower for k in ["who is", "who was", "what is", "search", "lookup", "tell me about", "wikipedia"])
    if search_intent and not any(k in prompt_lower for k in ["based on", "told you", "shopping", "list", "dinner", "cake", "eggs"]):
        fallback_search = web_search_knowledge_synthesis(prompt_clean)
        if fallback_search:
            return fallback_search

    # Transparent, non-template fallback when model is unreachable
    return "[Offline Mode] Local model engine (llamafile) is not reachable on port 8080. Start the model server via launch_hud.bat or run 'python main.py' to enable conversational reasoning."

