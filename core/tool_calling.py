import json
import logging
from core.llm import build_chat_messages, query_local_openai_compatible, clean_ascii_text
from core.tool_registry import select_candidate_tools, execute_registered_tool

def execute_model_tool_calling(user_input, max_tokens=256, temperature=0.1, timeout=60):
    """
    Native LLM Function Calling & ReAct Tool Loop:
    1. Sends conversation history + user query + candidate tool JSON schemas to Qwen3.
    2. If Qwen3 returns tool_calls, executes each tool and returns the observation(s).
    3. If Qwen3 answers conversationally, returns the generated text directly.
    4. If the model fails or is offline, returns None for fallback handling.
    """
    if not user_input or not user_input.strip():
        return None

    messages = build_chat_messages(user_input.strip())
    tools = select_candidate_tools(user_input.strip())
    if not tools:
        tools = None

    try:
        response_msg = query_local_openai_compatible(
            messages=messages,
            tools=tools,
            max_tokens=max_tokens,
            temperature=temperature,
            timeout=timeout
        )
    except Exception as e:
        logging.warning(f"[ToolCalling] Model request failed: {e}")
        return None

    if not response_msg:
        return None

    tool_calls = response_msg.get("tool_calls")
    if tool_calls:
        results = []
        for call in tool_calls:
            fn = call.get("function", {})
            fn_name = fn.get("name", "")
            raw_args = fn.get("arguments", "{}")

            try:
                if isinstance(raw_args, str):
                    args = json.loads(raw_args) if raw_args.strip() else {}
                else:
                    args = raw_args or {}
            except Exception as e:
                logging.warning(f"[ToolCalling] Failed to parse args '{raw_args}': {e}")
                args = {}

            logging.info(f"[ToolCalling] Executing tool '{fn_name}' with args {args}")
            obs = execute_registered_tool(fn_name, args)
            results.append((fn_name, obs))

        if len(results) == 1:
            return results[0][1]
        elif len(results) > 1:
            formatted = []
            for idx, (tname, tobs) in enumerate(results, 1):
                formatted.append(f"**Step {idx} ({tname.upper()})**: {tobs}")
            return "\n\n".join(formatted)

    content = response_msg.get("content", "")
    if content and content.strip():
        return clean_ascii_text(content.strip())

    return None
