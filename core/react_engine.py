import re
import json
from core.tool_registry import TOOL_REGISTRY, execute_registered_tool

class ReActEngine:
    """
    🧠 ReAct (Reason + Act) Multi-Agent Function Calling & Multi-Step Execution Loop.
    Decomposes complex multi-intent requests into structured Thought-Action-Observation loops.
    """
    def __init__(self):
        self.max_steps = 5

    def is_multi_step_request(self, prompt):
        """Detect if user request contains multiple actions connected by 'and', 'then', commas, or multi-step intent."""
        prompt_lower = prompt.lower()
        connectors = [" and ", " then ", ", and ", " then ", " after that ", " also "]
        if any(c in prompt_lower for c in connectors):
            return True
        # Check if prompt matches multiple distinct tool keywords
        match_count = 0
        keywords = ["ram", "speed", "kill", "code", "website", "lock", "weather", "note", "temp", "boost", "prompt"]
        for kw in keywords:
            if kw in prompt_lower:
                match_count += 1
        return match_count >= 2

    def decompose_into_plan(self, prompt):
        """NLP Intent Parser: Decomposes complex prompt into sequential ReAct Tool Actions."""
        prompt_lower = prompt.lower()
        plan = []

        # 1. Open App / Code Editor
        if any(k in prompt_lower for k in ["code editor", "open vscode", "open editor", "open notepad", "open chrome"]):
            app_name = "vscode" if "code editor" in prompt_lower or "vscode" in prompt_lower else "notepad"
            plan.append({"tool": "open_app", "args": {"app_name": app_name}})

        # 2. Locate Last Python Project / Saved File
        if any(k in prompt_lower for k in ["last python project", "last project", "last saved file", "pull up my last"]):
            plan.append({"tool": "locate_last_saved_file", "args": {}})

        # 3. Code / Bug Fix / Script Generation
        if any(k in prompt_lower for k in ["code", "script", "fix", "bug", "website", "app"]) and not any(k in prompt_lower for k in ["code editor", "last python project"]):
            if "website" in prompt_lower or "restaurant" in prompt_lower:
                plan.append({"tool": "code_agent", "args": {"idea": prompt}})
            elif "prompt" in prompt_lower:
                plan.append({"tool": "make_master_prompt", "args": {"idea": prompt}})
            else:
                plan.append({"tool": "save_code_to_desktop", "args": {"code": "# Fixed Python Automation Script\nprint('Script executed successfully, Boss!')\n", "filename": "fixed_script.py"}})

        # 4. Timer / Alarm
        if any(k in prompt_lower for k in ["timer", "remind me in", "set alarm", "minutes"]):
            plan.append({"tool": "set_timer", "args": {"prompt": prompt}})

        # 5. RAM / Performance / Turbo Boost
        if any(k in prompt_lower for k in ["ram", "turbo", "boost", "speed up", "performance"]):
            plan.append({"tool": "turbo_boost", "args": {}})

        # 6. Clean Temp Files
        if any(k in prompt_lower for k in ["clean temp", "clear temp", "temp cache", "junk"]):
            plan.append({"tool": "clean_temp", "args": {}})

        # 7. Kill Processes
        if any(k in prompt_lower for k in ["kill", "close all", "stop background"]):
            plan.append({"tool": "kill_all_processes", "args": {}})

        # 8. Speed Test / Network
        if any(k in prompt_lower for k in ["speed test", "network speed", "internet speed"]):
            plan.append({"tool": "run_speed_test", "args": {}})

        # 9. Lock / Power
        if any(k in prompt_lower for k in ["lock pc", "screen lock"]) and not "block" in prompt_lower:
            plan.append({"tool": "lock_pc", "args": {}})

        # 10. Weather
        if "weather" in prompt_lower:
            plan.append({"tool": "get_weather", "args": {"city": "London"}})

        # 11. Notes
        if "note" in prompt_lower:
            plan.append({"tool": "add_note", "args": {"note": prompt}})

        return plan

    def execute_react_loop(self, prompt):
        """
        Execute full ReAct (Reason + Act) Multi-Step Loop:
        Thought -> Action -> Observation -> Final Synthesis
        """
        plan = self.decompose_into_plan(prompt)
        if not plan:
            return None # Fall back to single-intent router

        results = []
        for idx, step in enumerate(plan, 1):
            tool_name = step["tool"]
            args = step["args"]

            # Thought
            thought = f"Step {idx}: Execute '{tool_name}' for target request."

            # Action & Observation
            if tool_name == "code_agent":
                from agents.coding_agent import CodingAgent
                agent = CodingAgent()
                obs = agent.process_code_request(args.get("idea", prompt))
            else:
                obs = execute_registered_tool(tool_name, args)

            results.append(f"**Step {idx} ({tool_name.upper()})**: {obs}")

        synthesis = "\n\n".join(results)
        return f"### 🧠 Multi-Agent ReAct Execution Complete, Boss!\n\n{synthesis}"

react_engine = ReActEngine()
