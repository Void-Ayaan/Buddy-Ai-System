import re
import json
import logging
from core.tool_registry import TOOL_REGISTRY, execute_registered_tool, select_candidate_tools
from core.tool_calling import execute_model_tool_calling

class ReActEngine:
    """
    🧠 ReAct (Reason + Act) Multi-Agent Function Calling & Multi-Step Execution Loop.
    Uses native LLM function calling and multi-step reasoning.
    """
    def __init__(self):
        self.max_steps = 5

    def is_multi_step_request(self, prompt):
        """Detect if user request explicitly combines multiple distinct tool actions."""
        prompt_lower = prompt.lower()
        connectors = [" and ", " then ", ", and ", " after that ", " also "]
        if not any(c in prompt_lower for c in connectors):
            return False

        # Only trigger multi-step if at least two distinct action categories are present
        action_hits = 0
        if any(w in prompt_lower for w in ["open", "launch", "editor", "vscode", "chrome"]):
            action_hits += 1
        if any(w in prompt_lower for w in ["timer", "alarm", "remind"]):
            action_hits += 1
        if any(w in prompt_lower for w in ["project", "last python", "last saved", "pull up"]):
            action_hits += 1
        if any(w in prompt_lower for w in ["turbo boost", "boost pc", "clean ram", "optimize ram"]):
            action_hits += 1
        if any(w in prompt_lower for w in ["kill", "close all processes", "close all apps"]):
            action_hits += 1
        if any(w in prompt_lower for w in ["weather", "temperature", "forecast"]):
            action_hits += 1

        return action_hits >= 2

    def decompose_into_plan(self, prompt):
        """
        Decomposes complex prompt into sequential ReAct Tool Actions.
        Avoids false positives (e.g. 'boost my morale' will never trigger turbo_boost).
        """
        prompt_lower = prompt.lower()
        plan = []

        # 1. Open App / Code Editor
        if any(k in prompt_lower for k in ["code editor", "open vscode", "open editor", "open notepad", "open chrome"]):
            app_name = "vscode" if "vscode" in prompt_lower or "code editor" in prompt_lower else "notepad"
            plan.append({"tool": "open_app", "args": {"app_name": app_name}})

        # 2. Locate Last Python Project / Saved File
        if any(k in prompt_lower for k in ["last python project", "last project", "last saved file", "pull up my last"]):
            plan.append({"tool": "locate_last_saved_file", "args": {}})

        # 3. Code / Game / Website Generation
        if any(k in prompt_lower for k in ["write code", "generate code", "build game", "make game", "create game", "make website", "build website"]):
            plan.append({"tool": "code_agent", "args": {"request": prompt}})

        # 4. Timer / Alarm (e.g., "set a timer for 25 minutes")
        timer_match = re.search(r"\b(?:timer|alarm|remind\s+me)\b.*?(\d+\s*(?:minutes?|mins?|seconds?|hours?))", prompt_lower)
        if timer_match:
            plan.append({"tool": "set_timer", "args": {"prompt": timer_match.group(1)}})
        elif any(k in prompt_lower for k in ["timer", "remind me in", "set alarm"]):
            plan.append({"tool": "set_timer", "args": {"prompt": prompt}})

        # 5. System RAM / Turbo Boost (Only for system performance, NOT 'boost morale')
        if any(k in prompt_lower for k in ["turbo boost", "boost pc", "speed up pc", "boost system", "clean ram", "optimize ram"]):
            plan.append({"tool": "turbo_boost", "args": {}})

        # 6. Clean Temp Files
        if any(k in prompt_lower for k in ["clean temp", "clear temp", "temp cache", "junk files"]):
            plan.append({"tool": "clean_temp", "args": {}})

        # 7. Kill Processes
        if any(k in prompt_lower for k in ["kill all processes", "kill all apps", "close all processes", "close background apps"]):
            plan.append({"tool": "kill_all_processes", "args": {}})

        # 8. Speed Test
        if any(k in prompt_lower for k in ["speed test", "network speed", "internet speed"]):
            plan.append({"tool": "run_speed_test", "args": {}})

        # 9. Lock Workstation
        if any(k in prompt_lower for k in ["lock pc", "screen lock", "lock workstation"]) and "block" not in prompt_lower:
            plan.append({"tool": "lock_pc", "args": {}})

        # 10. Weather (Extract city dynamically or auto-detect, never hardcode London)
        if any(k in prompt_lower for k in ["weather", "temperature", "forecast"]):
            city_match = re.search(r"\b(?:weather|temperature)\s+(?:in|for|at)\s+([a-zA-Z\s]+)", prompt, flags=re.IGNORECASE)
            city = city_match.group(1).strip() if city_match else None
            plan.append({"tool": "get_weather", "args": {"city": city}})

        # 11. Notes
        if "add note" in prompt_lower or "take note" in prompt_lower:
            clean_note = re.sub(r"^(?:add\s+note|take\s+a\s+note|take\s+note)\s*(?:to|that|:)?\s*", "", prompt, flags=re.IGNORECASE).strip()
            plan.append({"tool": "add_note", "args": {"note": clean_note or prompt}})

        return plan

    def execute_react_loop(self, prompt):
        """
        Execute full ReAct Multi-Step Loop:
        1. Tries native LLM tool calling first.
        2. Falls back to decomposed deterministic plan if LLM is unavailable.
        """
        # First, attempt native LLM function calling
        try:
            llm_result = execute_model_tool_calling(prompt)
            if llm_result:
                return llm_result
        except Exception as e:
            logging.warning(f"[ReActEngine] Model tool calling failed: {e}")

        # Fallback to deterministic plan
        plan = self.decompose_into_plan(prompt)
        if not plan:
            return None

        results = []
        for idx, step in enumerate(plan, 1):
            tool_name = step["tool"]
            args = step["args"]

            if tool_name == "code_agent":
                from agents.coding_agent import CodingAgent
                agent = CodingAgent()
                obs = agent.process_code_request(args.get("request", prompt))
            else:
                obs = execute_registered_tool(tool_name, args)

            results.append(f"**Step {idx} ({tool_name.upper()})**: {obs}")

        return "\n\n".join(results)

react_engine = ReActEngine()
